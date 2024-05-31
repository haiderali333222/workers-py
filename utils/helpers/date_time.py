from datetime import datetime, date
from dateutil.parser import parse


# get dates and time
def get_date_time():
    today = date.today()
    now = datetime.now()
    d2 = today.strftime("%B %d, %Y")
    current_time = now.strftime("%H:%M:%S")
    date_time = f"{d2} {current_time}"
    date_time = parse(date_time)
    return date_time
