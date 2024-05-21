import pandas as pd
import datetime as dt
import pytz

session_times = {
    "Tokyo": ("00:00", "09:00"),
    "London": ("08:00", "17:00"),
    "New York": ("13:00", "22:00")
}

def convert_to_timezone(time, timezone):
    tz = pytz.timezone(timezone)
    return dt.datetime.combine(dt.date.today(), time).astimezone(tz).time()

session_times = {session: (convert_to_timezone(dt.time.fromisoformat(start), "UTC"),
                           convert_to_timezone(dt.time.fromisoformat(end), "UTC"))
                 for session, (start, end) in session_times.items()}

def get_current_time(timezone):
    tz = pytz.timezone(timezone)
    return dt.datetime.now(tz).time()

current_time = get_current_time("UTC")

def get_active_session(time):
    for session, (start, end) in session_times.items():
        if start <= time <= end:
            return session
    return "None"

active_session = get_active_session(current_time)

print("Active Forex session:", active_session)
