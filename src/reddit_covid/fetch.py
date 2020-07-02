import pandas as pd
import matplotlib.pyplot as plt
import io

state = "nc"


def graph(df):
    """
    Builds the graph of two 2 week periods of positive COVID-19 cases.
    """
    ax = plt.gca()
    ax.set_axis_off()
    df[:28].plot(
        x='date', y='positiveIncrease', linewidth=2.0, color='blue', ax=ax)
    plt.legend('', frameon=False)
    f = io.BytesIO()
    plt.savefig(f)
    return f.getvalue()


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

    print(daily.info())
    print(daily.head())
    return daily
