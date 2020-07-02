import pandas as pd
import matplotlib.pyplot as plt

state = "nc"


def graph(df):
    ax = plt.gca()
    ax.set_axis_off()
    df[:28].plot(
        x='date', y='positiveIncrease', linewidth=2.0, color='blue', ax=ax)
    plt.legend('', frameon=False)
    plt.show()


def fetch():
    daily = pd.read_csv(
        f'https://covidtracking.com/api/v1/states/{state}/daily.csv')

    daily["date"] = daily["date"].apply(str)
    daily["date"] = pd.to_datetime(daily["date"], format="%Y%m%d")
    daily = daily.set_index(pd.DatetimeIndex(daily['date']))

    print(daily.info())
    print(daily.head())
    graph(daily)
