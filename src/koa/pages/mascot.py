"""A cozy koala-with-ukulele mascot, drawn as inline SVG."""

_FUR = "#9BA6AC"
_FUR_DARK = "#7E8990"
_EAR_IN = "#E7C3B7"
_NOSE = "#565A5D"
_CHEEK = "#E39A93"
_UKE = "#D8A24A"
_UKE_DARK = "#C68E3F"


def koala_svg(width: int = 180) -> str:
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" viewBox="0 0 220 210"
     role="img" aria-label="Ukoala mascot">
  <!-- ears -->
  <circle cx="60" cy="50" r="30" fill="{_FUR}" stroke="{_FUR_DARK}" stroke-width="2"/>
  <circle cx="160" cy="50" r="30" fill="{_FUR}" stroke="{_FUR_DARK}" stroke-width="2"/>
  <circle cx="60" cy="52" r="16" fill="{_EAR_IN}"/>
  <circle cx="160" cy="52" r="16" fill="{_EAR_IN}"/>
  <!-- head -->
  <ellipse cx="110" cy="88" rx="60" ry="54" fill="{_FUR}" stroke="{_FUR_DARK}" stroke-width="2"/>
  <!-- cheeks -->
  <circle cx="74" cy="104" r="10" fill="{_CHEEK}" opacity="0.55"/>
  <circle cx="146" cy="104" r="10" fill="{_CHEEK}" opacity="0.55"/>
  <!-- eyes -->
  <circle cx="88" cy="80" r="6" fill="#3A3A3A"/>
  <circle cx="132" cy="80" r="6" fill="#3A3A3A"/>
  <circle cx="90" cy="78" r="2" fill="#fff"/>
  <circle cx="134" cy="78" r="2" fill="#fff"/>
  <!-- nose -->
  <ellipse cx="110" cy="104" rx="20" ry="15" fill="{_NOSE}"/>
  <ellipse cx="103" cy="99" rx="5" ry="3" fill="#7c7f81"/>
  <!-- body -->
  <ellipse cx="110" cy="178" rx="52" ry="34" fill="{_FUR}" stroke="{_FUR_DARK}" stroke-width="2"/>
  <!-- ukulele held across the belly -->
  <g transform="rotate(-14 110 168)">
    <rect x="52" y="163" width="70" height="9" rx="4" fill="{_UKE_DARK}"/>
    <ellipse cx="140" cy="167" rx="26" ry="21" fill="{_UKE}" stroke="{_UKE_DARK}" stroke-width="2"/>
    <circle cx="140" cy="167" r="6.5" fill="#4A3B22"/>
    <rect x="48" y="160" width="7" height="15" rx="2" fill="#6b5a3a"/>
    <line x1="55" y1="165" x2="150" y2="165" stroke="#F2E3C6" stroke-width="1"/>
    <line x1="55" y1="167.5" x2="150" y2="167.5" stroke="#F2E3C6" stroke-width="1"/>
    <line x1="55" y1="170" x2="150" y2="170" stroke="#F2E3C6" stroke-width="1"/>
  </g>
  <!-- paws -->
  <ellipse cx="70" cy="176" rx="13" ry="10" fill="{_FUR}" stroke="{_FUR_DARK}" stroke-width="2"/>
  <ellipse cx="150" cy="184" rx="13" ry="10" fill="{_FUR}" stroke="{_FUR_DARK}" stroke-width="2"/>
</svg>
"""
