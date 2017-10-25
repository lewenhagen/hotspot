"""
Functions for create date and time objects
"""
import datetime
import math



def create_time(hour):
    """
    Create time object.
    """
    hour = int(hour)
    minute = 0
    second = 0
    return datetime.time(hour=hour, minute=minute, second=second)



def create_date(date):
    """
    Create date object from string
    """
    day = int(date[8:])
    month = int(date[5:7])
    year = int(date[:4])
    return datetime.date(day=day, month=month, year=year)



def create_dates(start, end):
    """
    Creates two date objects, start and end
    """
    date_start = create_date(start)
    date_end = create_date(end)
    return date_start, date_end



def create_times(start=0, end=0):
    """
    Create two time objects, start and end
    """
    time_start = create_time(start)
    time_end = create_time(end)

    return time_start, time_end



def create_hours_event(event):
    """
    create time and date for unit Hours
    """
    date_start, date_end = create_dates(event["datestart"], event["dateend"])

    time_start, time_end = create_times(event["timestart"][:2], event["timeend"][:2])

    event_end = create_datetime(date_end, time_end) + datetime.timedelta(hours=1)

    return create_event_dict(date_start, time_start, event_end)



def create_days_event(event):
    """
    create time and date for unit Days
    """
    date_start, date_end = create_dates(event["datestart"], event["dateend"])

    time_start, time_end = create_times()

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



def create_datetime_tupl(date_tupl):
    """
    Create datetime object from string
    """
    return datetime.datetime.strptime(date_tupl[1] + " " + date_tupl[0] + " " + date_tupl[2] + " " + date_tupl[3],"%b %d %Y %H:%M:%S")



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
