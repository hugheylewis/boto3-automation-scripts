from datetime import datetime, timedelta, timezone

def format_date(date_str):
    """Formats the date with the day of the week and suffix (st, nd, rd, and th)"""
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    day_of_week = date_obj.strftime('%A')
    day = date_obj.day

    if 10 <= day <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')

    formatted_date = date_obj.strftime(f'{day_of_week}, %B {day}{suffix}, %Y')
    return formatted_date


end_date = datetime.now(timezone.utc).date()
start_date = (datetime.now(timezone.utc) - timedelta(days=14)).date()