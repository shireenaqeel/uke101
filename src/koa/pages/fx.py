"""Whimsical feedback effects: floating XP, level-ups, badge unlocks, confetti."""

from nicegui import ui

from koa import gamification

_CONFETTI_JS = """
(() => {
  const colors = ['#E07856','#F2B705','#6FB3A0','#F27B9D','#7C9EE0','#EC9A6A'];
  for (let i = 0; i < 70; i++) {
    const d = document.createElement('div');
    const size = 6 + Math.random() * 8;
    d.style.cssText = `position:fixed;top:-12px;left:${Math.random()*100}vw;width:${size}px;`
      + `height:${size}px;background:${colors[i % colors.length]};border-radius:2px;`
      + `z-index:9999;pointer-events:none;`;
    document.body.appendChild(d);
    const dur = 2200 + Math.random() * 1600;
    d.animate(
      [{transform: `translateY(0) rotate(0deg)`, opacity: 1},
       {transform: `translateY(105vh) rotate(${Math.random()*900-450}deg)`, opacity: .9}],
      {duration: dur, easing: 'cubic-bezier(.2,.6,.4,1)'}
    );
    setTimeout(() => d.remove(), dur);
  }
})();
"""


def confetti() -> None:
    ui.run_javascript(_CONFETTI_JS)


def celebrate(result: dict) -> None:
    """Show playful feedback for the outcome of ``gamification.award``."""
    if result.get("xp"):
        ui.notify(f"+{result['xp']} XP ✨", position="top", color="amber-8", timeout=1500)
    if result.get("leveled_up"):
        ui.notify(
            f"Level up! You're level {result['level']} 🎉",
            position="top", type="positive", timeout=3500,
        )
        confetti()
    for badge in result.get("new_badges", []):
        ui.notify(
            f"Badge unlocked — {badge['icon']} {badge['name']}!",
            position="top", color="deep-orange-6", timeout=3500,
        )
        confetti()


def award(source: str) -> None:
    """Convenience: award XP for an action and celebrate it in one call."""
    celebrate(gamification.award(source))
