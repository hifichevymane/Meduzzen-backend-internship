import calendar
from datetime import datetime

import pytz
from django.utils import timezone


def set_start_end_date(months_count):
    now = timezone.now()
    end_date_month = now.month
    if months_count:
        end_date_month += int(months_count)

    end_date_year = now.year

    # If number of month is bigger than 12
    if end_date_month > 12:
        end_date_month -= 12
        end_date_month += 1
        
    if not months_count:
        last_day_of_current_month = calendar.monthrange(now.year, now.month)[1]
    else:
        last_day_of_current_month = calendar.monthrange(now.year, int(months_count))[1]

    start_date = datetime(
        year=now.year, month=now.month, 
        day=1, hour=0, minute=0, second=0, tzinfo=pytz.UTC)
        
    if not months_count:
        end_date = datetime(
            year=now.year, month=now.month, 
            day=last_day_of_current_month, 
            hour=23, minute=59, second=59,
            tzinfo=pytz.UTC)
    else:
        end_date = datetime(
            year=end_date_year, month=end_date_month, 
            day=last_day_of_current_month, 
            hour=23, minute=59, second=59,
            tzinfo=pytz.UTC)
    
    return start_date, end_date
