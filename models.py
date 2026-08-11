"""
Normalized data shapes. Both the real fetchers (fetch_calendar.py,
fetch_weather.py) and demo_data.py produce these same objects, so
render.py never has to know or care whether it's looking at real
Google Calendar data or made-up placeholder data.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, time
from typing import Optional


@dataclass
class Event:
    title: str
    source: str          # which calendar/person this came from, e.g. "Mom"
    color: str            # hex color tag for that source
    start_time: Optional[time] = None   # None = all-day event
    end_time: Optional[time] = None


@dataclass
class DayWeather:
    high: Optional[float] = None
    low: Optional[float] = None
    condition: str = ""   # short text: "Sunny", "Rain", etc.


@dataclass
class Day:
    the_date: date
    meal: Optional[str] = None
    events: list[Event] = field(default_factory=list)
    weather: DayWeather = field(default_factory=DayWeather)

    def events_grouped_by_person(self) -> list[tuple[str, list[Event]]]:
        """
        Groups this day's events by who they belong to (Event.source),
        each person's events sorted chronologically (all-day events last).
        Groups themselves are ordered by their earliest event's time, so
        whoever has the first appointment of the day appears first.
        Used for the detailed "today" panel.
        """
        by_person: dict[str, list[Event]] = {}
        for ev in self.events:
            by_person.setdefault(ev.source, []).append(ev)

        def sort_key(ev: Event):
            return (ev.start_time is None, ev.start_time or time(0, 0))

        for person_events in by_person.values():
            person_events.sort(key=sort_key)

        def group_key(item: tuple[str, list[Event]]):
            first = item[1][0]
            return sort_key(first)

        return sorted(by_person.items(), key=group_key)
