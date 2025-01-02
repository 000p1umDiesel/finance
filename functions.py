import requests
import pandas as pd
import apimoex
import vectorbt as vbt
import numpy as np
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
import streamlit as st


@st.cache_data
def fetch_candles(ticket, interval=24, start=None, end=None):
    """
    Получение свечей для указанного тикера.

    :param ticker: Тикер (например, 'SBER')
    :param interval: Интервал свечей (например, 60)
    :param start: Начальная дата (в формате 'YYYY-MM-DD')
    :param end: Конечная дата (в формате 'YYYY-MM-DD')
    :return: DataFrame с обработанными данными
    """
    session = requests.Session()
    try:
        data = apimoex.get_market_candles(
            session, ticket, interval=interval, start=start, end=end
        )
        df = pd.DataFrame(data)

        df.set_index(pd.to_datetime(df["begin"]), inplace=True)
        df = df["close"]
        return df
    finally:
        session.close()


def MA_with_fix_window(df, fast_ma_window, slow_ma_window, init_cash, fees):
    pf_buy_hold = vbt.Portfolio.from_holding(close=df, init_cash=init_cash)
    pf_buy_hold.total_profit()

    fast_ma = vbt.MA.run(df, window=fast_ma_window)
    slow_ma = vbt.MA.run(df, window=slow_ma_window)

    entries = fast_ma.ma_crossed_above(slow_ma)
    exits = fast_ma.ma_crossed_below(slow_ma)

    pf_ma_strat = vbt.Portfolio.from_signals(
        close=df,
        entries=entries,
        exits=exits,
        init_cash=init_cash,
        fees=fees,
    )

    pf_ma_strat.total_profit()

    stats_of_fix_strategy = pf_ma_strat.stats()

    plot_of_fix_strategy = pf_ma_strat.plot(width=1600, height=1000)

    return stats_of_fix_strategy, plot_of_fix_strategy


def MA_generate_optimal_portfolio(
    df,
    start_window_of_MA,
    end_window_of_MA,
    fees=0.00003,
    init_cash=100000,
    frequence="1D",
):
    windows = np.arange(start_window_of_MA, end_window_of_MA)
    fast_ma, slow_ma = vbt.MA.run_combs(
        close=df, window=windows, r=2, short_names=["fast", "slow"]
    )
    entries = fast_ma.ma_crossed_above(slow_ma)
    exits = fast_ma.ma_crossed_below(slow_ma)

    pf_100_ma_strats = vbt.Portfolio.from_signals(
        close=df,
        entries=entries,
        exits=exits,
        size=np.inf,
        fees=fees,
        freq=frequence,
        init_cash=init_cash,
    )

    pf_100_ma_strats.total_profit().max()

    best_MAs = pf_100_ma_strats.total_profit().idxmax()

    optimal_short_MA = best_MAs[0]
    optimal_long_MA = best_MAs[1]

    stats = pf_100_ma_strats[best_MAs].stats()

    plot_MA_with_optimal_portfolio = pf_100_ma_strats[best_MAs].plot(
        width=1600, height=1000
    )

    return stats, optimal_short_MA, optimal_long_MA, plot_MA_with_optimal_portfolio


def make_prediciton(df, days_for_prediction):
    df_forecast = df.reset_index()
    df_forecast = df_forecast[["begin", "close"]].rename(
        columns={"begin": "ds", "close": "y"}
    )
    model = Prophet(
        daily_seasonality=False, weekly_seasonality=False, yearly_seasonality=True
    )
    model.fit(df_forecast)
    future = model.make_future_dataframe(periods=days_for_prediction)
    forecast = model.predict(future)
    fig_1 = plot_plotly(model, forecast)
    fig_2 = plot_components_plotly(model, forecast)
    return fig_1, fig_2, forecast
