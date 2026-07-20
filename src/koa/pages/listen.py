import base64
import json

import numpy as np
from nicegui import ui

from koa.data.chords import CHORDS, get_chord
from koa.pages import fx
from koa.fretboard import render_fretboard
from koa.ml.recognition import get_recognizer
from koa.pages.common import page_header

_CHORD_IDS = [c["id"] for c in CHORDS]

# Records ~1.6s of mic audio, decodes it to PCM in the browser, decimates to
# ~16 kHz, and returns the Float32 samples as base64 so Python can run chroma.
_RECORD_JS = """
return (async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({audio: true});
    const rec = new MediaRecorder(stream);
    const chunks = [];
    rec.ondataavailable = e => chunks.push(e.data);
    rec.start();
    await new Promise(r => setTimeout(r, 1600));
    await new Promise(r => { rec.onstop = r; rec.stop(); });
    stream.getTracks().forEach(t => t.stop());
    const buf = await (new Blob(chunks)).arrayBuffer();
    const ctx = new (window.AudioContext || window.webkitAudioContext)();
    const audio = await ctx.decodeAudioData(buf);
    const data = audio.getChannelData(0);
    const ratio = Math.max(1, Math.floor(audio.sampleRate / 16000));
    const out = new Float32Array(Math.floor(data.length / ratio));
    for (let i = 0; i < out.length; i++) out[i] = data[i * ratio];
    const bytes = new Uint8Array(out.buffer);
    let bin = '';
    for (let i = 0; i < bytes.length; i++) bin += String.fromCharCode(bytes[i]);
    return JSON.stringify({sr: Math.floor(audio.sampleRate / ratio), b64: btoa(bin)});
  } catch (e) {
    return JSON.stringify({error: String(e)});
  }
})();
"""


def build_listen() -> None:
    page_header("/listen")
    state = {"target": "C"}

    with ui.column().classes("w-full max-w-3xl mx-auto items-center gap-4 p-6"):
        ui.label("Ear Trainer").classes("text-3xl font-bold")
        ui.label(
            "Play a chord on your ukulele and the app listens and tells you what it heard. "
            "Pick a target, hear it, then strum and check."
        ).classes("text-gray-500 text-center max-w-2xl")
        ui.label(
            "Needs microphone access — allow it when prompted (works on localhost)."
        ).classes("text-xs text-gray-400")

        with ui.row().classes("items-center gap-8"):
            with ui.column().classes("items-center gap-2"):
                ui.label("Target chord").classes("text-sm text-gray-400")
                target_select = ui.select(_CHORD_IDS, value="C").props("dense")
                diagram = ui.html(render_fretboard(get_chord("C")))
                ref_audio = ui.audio("/audio/chord/C").props("preload=none").classes("hidden")
                ui.button("Hear it", icon="volume_up", on_click=ref_audio.play).props("flat size=sm")

            with ui.column().classes("items-center gap-2 w-64"):
                record_btn = ui.button(
                    "Record & check", icon="mic", on_click=lambda: record_and_check()
                ).props("size=lg")
                status = ui.label("").classes("text-sm text-gray-500 h-5")
                heard = ui.label("").classes("text-4xl font-bold")
                verdict = ui.label("").classes("text-lg font-semibold h-7")

    def on_target(e) -> None:
        state["target"] = e.value
        diagram.set_content(render_fretboard(get_chord(e.value)))
        ref_audio.set_source(f"/audio/chord/{e.value}")
        heard.text = ""
        verdict.text = ""

    target_select.on_value_change(on_target)

    async def record_and_check() -> None:
        record_btn.disable()
        status.text = "Listening… strum the chord now"
        heard.text = ""
        verdict.text = ""
        try:
            raw = await ui.run_javascript(_RECORD_JS, timeout=12.0)
        except Exception:
            status.text = "Couldn't reach the microphone. Try again."
            record_btn.enable()
            return
        record_btn.enable()
        status.text = ""

        data = json.loads(raw) if raw else {}
        if not raw or data.get("error"):
            status.text = "Microphone blocked or unavailable — check browser permissions."
            return
        samples = np.frombuffer(base64.b64decode(data["b64"]), dtype=np.float32)
        if samples.size < 512:
            status.text = "That was too quiet — play a bit louder and try again."
            return

        pred, conf = get_recognizer().predict_samples(samples, int(data["sr"]))
        heard.text = pred
        if pred == state["target"]:
            verdict.text = f"Correct! ({conf * 100:0.0f}% sure)"
            verdict.style("color: #16a34a")
            fx.award("ear_practice")
        else:
            verdict.text = f"Sounded like {pred} — aim for {state['target']}"
            verdict.style("color: #dc2626")
