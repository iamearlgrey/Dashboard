"""
Run this on a schedule (cron / GitHub Actions / Task Scheduler) to
regenerate dashboard.png. The ESP32 just fetches that file.

Usage:
    python3 main.py                 # real data, needs CALENDAR_FEEDS set in config.py
    python3 main.py --demo          # placeholder data, no network needed
    python3 main.py --out foo.png   # custom output path
"""

from __future__ import annotations

import argparse

from config import CALENDAR_FEEDS
from render import render_dashboard
from localtime import today_local


def build(use_demo: bool, out_path: str):
    if use_demo or not CALENDAR_FEEDS:
        from demo_data import get_demo_days
        days = get_demo_days()
        if not use_demo:
            print("[info] CALENDAR_FEEDS is empty in config.py — using demo data. "
                  "Add your feed URLs to config.py to pull real data.")
    else:
        from fetch_calendar import get_calendar_days
        from fetch_weather import get_weather_by_date
        days = get_calendar_days()
        weather = get_weather_by_date()
        for d in days:
            if d.the_date in weather:
                d.weather = weather[d.the_date]

    path = render_dashboard(days, out_path, today=today_local())
    print(f"[ok] wrote {path}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--demo", action="store_true", help="use placeholder data instead of live feeds")
    p.add_argument("--out", default="dashboard.png", help="output image path")
    args = p.parse_args()
    build(use_demo=args.demo, out_path=args.out)
