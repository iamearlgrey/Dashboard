"""
Small set of hand-drawn line icons for weather conditions. Deliberately
simple/monochrome (stroke-only, no fills) so they stay crisp after the
1-bit e-ink threshold — colored weather emoji turn into noisy blobs
once thresholded, plain line icons don't.
"""

_SUN = """<svg viewBox="0 0 40 40" width="{size}" height="{size}">
<circle cx="20" cy="20" r="8" fill="none" stroke="#000" stroke-width="2.2"/>
<g stroke="#000" stroke-width="2.2" stroke-linecap="round">
<line x1="20" y1="2" x2="20" y2="7"/><line x1="20" y1="33" x2="20" y2="38"/>
<line x1="2" y1="20" x2="7" y2="20"/><line x1="33" y1="20" x2="38" y2="20"/>
<line x1="7" y1="7" x2="10.5" y2="10.5"/><line x1="29.5" y1="29.5" x2="33" y2="33"/>
<line x1="33" y1="7" x2="29.5" y2="10.5"/><line x1="10.5" y1="29.5" x2="7" y2="33"/>
</g></svg>"""

_PARTLY_CLOUDY = """<svg viewBox="0 0 40 40" width="{size}" height="{size}">
<circle cx="16" cy="15" r="7" fill="none" stroke="#000" stroke-width="2.2"/>
<g stroke="#000" stroke-width="2" stroke-linecap="round">
<line x1="16" y1="1" x2="16" y2="4"/><line x1="4" y1="15" x2="7" y2="15"/>
<line x1="5.5" y1="4.5" x2="7.6" y2="6.6"/><line x1="26.4" y1="4.5" x2="24.3" y2="6.6"/>
</g>
<path d="M13 24 h16 a6 6 0 0 0 0-12 a8 8 0 0 0-15.3-2.4 A6.5 6.5 0 0 0 13 24 Z" fill="#fff" stroke="#000" stroke-width="2.2" stroke-linejoin="round"/>
</svg>"""

_CLOUDY = """<svg viewBox="0 0 40 40" width="{size}" height="{size}">
<path d="M8 28 h22 a7 7 0 0 0 0-14 a9 9 0 0 0-17.3-2.7 A7.5 7.5 0 0 0 8 28 Z" fill="none" stroke="#000" stroke-width="2.2" stroke-linejoin="round"/>
</svg>"""

_RAIN = """<svg viewBox="0 0 40 40" width="{size}" height="{size}">
<path d="M8 20 h22 a7 7 0 0 0 0-14 a9 9 0 0 0-17.3-2.7 A7.5 7.5 0 0 0 8 20 Z" fill="none" stroke="#000" stroke-width="2.2" stroke-linejoin="round"/>
<g stroke="#000" stroke-width="2.2" stroke-linecap="round">
<line x1="14" y1="26" x2="11" y2="35"/><line x1="21" y1="26" x2="18" y2="35"/><line x1="28" y1="26" x2="25" y2="35"/>
</g></svg>"""

_SNOW = """<svg viewBox="0 0 40 40" width="{size}" height="{size}">
<path d="M8 18 h22 a7 7 0 0 0 0-14 a9 9 0 0 0-17.3-2.7 A7.5 7.5 0 0 0 8 18 Z" fill="none" stroke="#000" stroke-width="2.2" stroke-linejoin="round"/>
<g stroke="#000" stroke-width="2" stroke-linecap="round">
<line x1="14" y1="24" x2="14" y2="34"/><line x1="9.5" y1="26.5" x2="18.5" y2="31.5"/><line x1="18.5" y1="26.5" x2="9.5" y2="31.5"/>
<line x1="26" y1="24" x2="26" y2="34"/><line x1="21.5" y1="26.5" x2="30.5" y2="31.5"/><line x1="30.5" y1="26.5" x2="21.5" y2="31.5"/>
</g></svg>"""

_STORM = """<svg viewBox="0 0 40 40" width="{size}" height="{size}">
<path d="M8 18 h22 a7 7 0 0 0 0-14 a9 9 0 0 0-17.3-2.7 A7.5 7.5 0 0 0 8 18 Z" fill="none" stroke="#000" stroke-width="2.2" stroke-linejoin="round"/>
<path d="M21 22 l-6 10 h5 l-3 7 l9-11 h-5 z" fill="#000" stroke="#000" stroke-width="1.5" stroke-linejoin="round"/>
</svg>"""

_FOG = """<svg viewBox="0 0 40 40" width="{size}" height="{size}">
<g stroke="#000" stroke-width="2.2" stroke-linecap="round">
<line x1="6" y1="13" x2="30" y2="13"/><line x1="4" y1="20" x2="36" y2="20"/>
<line x1="8" y1="27" x2="32" y2="27"/>
</g></svg>"""

_ICONS = {
    "clear": _SUN,
    "mostly clear": _SUN,
    "sunny": _SUN,
    "partly cloudy": _PARTLY_CLOUDY,
    "cloudy": _CLOUDY,
    "fog": _FOG,
    "drizzle": _RAIN,
    "rain": _RAIN,
    "heavy rain": _RAIN,
    "showers": _RAIN,
    "snow": _SNOW,
    "heavy snow": _SNOW,
    "storms": _STORM,
}


def get_icon_svg(condition: str, size: int = 28) -> str:
    key = (condition or "").strip().lower()
    template = _ICONS.get(key, _SUN)
    return template.format(size=size)
