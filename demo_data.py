"""
Fake but realistic data, used to build and tune the layout without
needing real calendar feeds hooked up yet. Once fetch_calendar.py and
fetch_weather.py are wired to your real feeds, main.py just swaps
this out.
"""

from __future__ import annotations

from datetime import date, time, timedelta
from models import Day, Event, DayWeather
from localtime import today_local

MEALS = [
    "Tacos", "Leftovers", "Spaghetti & Meatballs", "Sheet-Pan Chicken",
    "Breakfast for Dinner", "Pizza Night", "Grilled Salmon + Veggies",
]

CONDITIONS = ["Clear", "Partly Cloudy", "Cloudy", "Rain", "Storms", "Snow", "Fog"]

SAMPLE_EVENTS = [
    [("Dentist - Kai", "Mom", "#000000", time(9, 0), time(9, 45))],
    [("Soccer practice", "Dad", "#000000", time(17, 30), time(18, 30))],
    [("Dr appt", "Mom", "#000000", time(9, 0), time(9, 45)),
     ("Haircut", "Mom", "#000000", time(13, 0), time(13, 30)),
     ("Book club", "Mom", "#000000", time(19, 0), time(20, 30)),
     ("Soccer practice", "Dad", "#000000", time(17, 30), time(18, 30))],
    [("Parent-teacher conf.", "Mom", "#000000", time(16, 0), time(16, 30)),
     ("Trash day", "Family", "#000000", None, None)],
    [("Piano lesson", "Kai", "#000000", time(15, 0), time(15, 30))],
    [("Birthday party - Ana", "Family", "#000000", time(13, 0), time(15, 0))],
    [],
]


def get_demo_days(start: date | None = None) -> list[Day]:
    start = start or today_local()
    days = []
    for i in range(7):
        d = start + timedelta(days=i)
        events = [
            Event(title=t, source=s, color=c, start_time=st, end_time=et)
            for (t, s, c, st, et) in SAMPLE_EVENTS[i % len(SAMPLE_EVENTS)]
        ]
        days.append(Day(
            the_date=d,
            meal=MEALS[i % len(MEALS)],
            events=events,
            weather=DayWeather(high=78 - i, low=58 + i % 3, condition=CONDITIONS[i % len(CONDITIONS)]),
        ))
    return days
