"""
Functions for create date and time objects
"""
import datetime
import math



def create_time(hour=0):
    """
    Create time object.
    """
    hour = int(hour)
    minute = 0
    second = 0
    return datetime.time(hour=hour, minute=minute, second=second)



def create_date(date):
    """
    Create date object from date string
    """
    # Skapa från sträng direkt??!?!
    day = int(date[8:])
    month = int(date[5:7])
    year = int(date[:4])
    return datetime.date(day=day, month=month, year=year)



def create_hours(event):
    """
    create time and date for unit Hours
    """
    date_start = create_date(event["datestart"])
    date_end = create_date(event["dateend"])

    time_start = create_time(event["timestart"][:2])
    time_end = create_time(event["timeend"][:2])

    event_end = create_datetime(date_end, time_end) + datetime.timedelta(hours=1)

    return create_event_dict(date_start, time_start, event_end)



def create_days(event):
    """
    create time and date for unit Days
    """
    date_start = create_date(event["datestart"])
    date_end = create_date(event["dateend"])

    time_start = create_time()
    time_end = create_time()

    event_end = create_datetime(date_end, time_end) + datetime.timedelta(days=1)

    return create_event_dict(date_start, time_start, event_end)



def create_event_dict(ds, ts, event_end):
    """
    Create event dict with start and end datetime and duration
    """
    event_start = create_datetime(ds, ts)
    duration = event_end - event_start

    return {"start": event_start, "end": event_end, "duration": duration}



def create_datetime(date, time):
    """
    Create a datetime object from a date and time
    """
    return datetime.datetime.combine(date, time)



def create_timedelta(unit, value=1):
    """
    Increase datetime for 1 unit. ex. with 1 hour or 1 day
    """
    if unit == "Hours":
        return datetime.timedelta(hours=value)
    elif unit == "Days":
        return datetime.timedelta(days=value)



def get_nr_hours(duration):
    """
    Return duration as hours, rounded up.
    """
    return int(math.ceil((duration.total_seconds()/3600)))



def get_nr_days(start, end, duration):
    """
    Return duration as days
    """
    return duration.days



def get_nr_months(start, end):
    """
    Return number of months event span
    """
    months = (end.year - start.year) * 12
    months += end.month - start.month + 1
    return months



# def compare_date_time(start, end, unit):
#     """
#     Compare data <= date or time < time
#     """
#     if unit == "Days":
#         return start.date() < end.date()
#     elif unit == "Hours":
#         return start < end
