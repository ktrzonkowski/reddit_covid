import pandas as pd
from datetime import datetime

state = "nc"


def fetch():
    """
    Fetches data from covidtracking.com. A data API run by The Atlantic.
    Returns a dataframe indexed by date.
    """
    daily = pd.read_csv(
        f'https://covidtracking.com/api/v1/states/{state}/daily.csv')

    daily["date"] = daily["date"].apply(str)
    daily["date"] = pd.to_datetime(daily["date"], format="%Y%m%d")
    daily = daily.set_index(pd.DatetimeIndex(daily['date']))
    daily = daily.truncate(after=datetime(2020, 4, 6))
    return daily
