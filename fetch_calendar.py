"""
Pulls events from one or more ICS feed URLs (Google Calendar's "secret
address in iCal format", iCloud public calendar links, Outlook, etc.)
and normalizes them into Day/Event objects for the renderer.

Handles recurring events (weekly soccer practice, etc.) via
recurring_ical_events, which expands recurrences into concrete
instances for the date range we ask for.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, time as dtime

import requests
import recurring_ical_events
from icalendar import Calendar

from models import Day, Event, DayWeather
from config import CALENDAR_FEEDS
from localtime import today_local


def _fetch_ics_text(url: str) -> str:
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    return resp.text


def get_calendar_days(start: date | None = None) -> list[Day]:
    """
    Returns 7 Day objects (start .. start+6) populated with events and
    meals pulled from CALENDAR_FEEDS. Weather is left empty here —
    fetch_weather.py fills that in separately.
    """
    start = start or today_local()
    end = start + timedelta(days=7)

    days = {start + timedelta(days=i): Day(the_date=start + timedelta(days=i))
            for i in range(7)}

    for feed in CALENDAR_FEEDS:
        try:
            ics_text = _fetch_ics_text(feed["url"])
        except Exception as e:
            print(f"[warn] could not fetch feed '{feed['name']}': {e}")
            continue

        cal = Calendar.from_ical(ics_text)
        occurrences = recurring_ical_events.of(cal).between(start, end)

        for comp in occurrences:
            summary = str(comp.get("summary", "(untitled)"))
            dtstart = comp.get("dtstart").dt

            if isinstance(dtstart, datetime):
                ev_date = dtstart.date()
                start_time = dtstart.time()
                dtend = comp.get("dtend")
                end_time = dtend.dt.time() if dtend and isinstance(dtend.dt, datetime) else None
            else:
                # all-day event (icalendar gives a plain date)
                ev_date = dtstart
                start_time = None
                end_time = None

            if ev_date not in days:
                continue

            if feed.get("kind") == "meal":
                days[ev_date].meal = summary
            else:
                days[ev_date].events.append(Event(
                    title=summary,
                    source=feed["name"],
                    color=feed.get("color", "#000000"),
                    start_time=start_time,
                    end_time=end_time,
                ))

    ordered = [days[start + timedelta(days=i)] for i in range(7)]
    for d in ordered:
        d.events.sort(key=lambda e: (e.start_time is None, e.start_time or dtime(0, 0)))
    return ordered
