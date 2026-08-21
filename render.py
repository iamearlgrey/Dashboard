"""
Turns a list[Day] into a PNG by filling template.html with data and
screenshotting it. All visual formatting lives in template.html — this
file only prepares plain data for it (strings, not styling decisions).
"""

from __future__ import annotations

import os
from datetime import date, time as dtime

from jinja2 import Environment, FileSystemLoader
from PIL import Image

from config import DISPLAY_WIDTH, DISPLAY_HEIGHT, DITHER_TO_1BIT
from models import Day
from weather_icons import get_icon_svg
from localtime import today_local

_HERE = os.path.dirname(os.path.abspath(__file__))


def _fmt_time(t: dtime | None) -> str:
    if t is None:
        return ""
    h = t.hour % 12 or 12
    ampm = "a" if t.hour < 12 else "p"
    return f"{h}:{t.minute:02d}{ampm}" if t.minute else f"{h}{ampm}"


def _fmt_temp(v) -> str:
    return str(round(v)) if v is not None else "--"


def _build_today_context(day: Day) -> dict:
    grouped = []
    for person_name, events in day.events_grouped_by_person():
        grouped.append((
            person_name,
            [{"time_str": _fmt_time(e.start_time), "title": e.title} for e in events],
        ))
    return {
        "dayname_full": day.the_date.strftime("%A").upper(),
        "datestr": day.the_date.strftime("%B %-d").upper(),
        "hi": _fmt_temp(day.weather.high),
        "lo": _fmt_temp(day.weather.low),
        "meal": day.meal,
        "grouped_events": grouped,
        "icon_svg": get_icon_svg(day.weather.condition, size=54),
    }


def _build_week_day_context(day: Day) -> dict:
    person_lines = []
    for person_name, events in day.events_grouped_by_person():
        parts = []
        for e in events:
            t = _fmt_time(e.start_time)
            parts.append(f"{t} {e.title}" if t else e.title)
        person_lines.append({"who": person_name.upper(), "text": ", ".join(parts)})

    return {
        "dayname": day.the_date.strftime("%a").upper(),
        "daynum": day.the_date.strftime("%-d"),
        "hi": _fmt_temp(day.weather.high),
        "lo": _fmt_temp(day.weather.low),
        "meal": day.meal,
        "person_lines": person_lines,
        "icon_svg": get_icon_svg(day.weather.condition, size=33),
    }


def render_dashboard(days: list[Day], out_path: str, today: date | None = None) -> str:
    today = today or today_local()
    today_day = next((d for d in days if d.the_date == today), days[0])
    week_days = [d for d in days if d.the_date != today_day.the_date]

    env = Environment(loader=FileSystemLoader(_HERE))
    template = env.get_template("template.html")
    html = template.render(
        width=DISPLAY_WIDTH,
        height=DISPLAY_HEIGHT,
        today=_build_today_context(today_day),
        week_days=[_build_week_day_context(d) for d in week_days],
    )

    html_path = os.path.join(_HERE, "_rendered_dashboard.html")
    with open(html_path, "w") as f:
        f.write(html)

    raw_png_path = out_path + ".raw.png"
    _screenshot(html_path, raw_png_path)

    # Kept as real 8-bit grayscale (not 1-bit) specifically because some
    # e-ink display tools — Kindle's own "eips", for one — refuse to paint
    # a 1-bit image at all ("8bit only" error) even though the content is
    # visually black/white either way. main.py's Kindle-rotation step reads
    # from this file rather than the thresholded dashboard.png below.
    grayscale_path = out_path + ".grayscale.png"
    Image.open(raw_png_path).convert("L").save(grayscale_path)

    if DITHER_TO_1BIT:
        img = Image.open(raw_png_path).convert("L")
        # Hard black/white threshold (not dithered) — crisper text on e-ink
        # than PIL's default Floyd-Steinberg dither.
        img = img.point(lambda p: 255 if p > 140 else 0).convert("1")
        img.save(out_path)
    else:
        Image.open(raw_png_path).save(out_path)

    os.remove(raw_png_path)
    os.remove(html_path)
    return out_path


def _screenshot(html_path: str, out_path: str):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": DISPLAY_WIDTH, "height": DISPLAY_HEIGHT})
        page.goto(f"file://{html_path}")
        page.screenshot(path=out_path)
        browser.close()
