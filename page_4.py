import requests
import pandas as pd
import apimoex
import vectorbt as vbt
import numpy as np
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
import streamlit as st
from functions import (
    fetch_candles,
    MA_with_fix_window,
    MA_generate_optimal_portfolio,
    make_prediciton,
)

st.subheader("Прогнозирование временных рядов")

days = st.number_input(
    "Количество дней для прогнозирования", step=1, value=None, min_value=1
)

if st.session_state.df is not None:
    check_button = st.button("Прогнозировать")
else:
    st.warning("Необходимо загрузить данные")

if check_button:
    fig1, fig2, forecast = make_prediciton(st.session_state.df, days)
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)
    # st.session_state.forecast = forecast
    forecast.rename(columns={"ds": "date", "yhat": "close"}, inplace=True)
    forecast = forecast[["date", "close"]]
    forecast = forecast.set_index("date")
    st.session_state.forecast = forecast

if st.session_state.forecast is not None:
    check_optimal_button = st.button(
        "Сгенерировать оптимальные параметры MA с учетом прогнозирования"
    )
    if check_optimal_button:
        stats, optimal_short_MA, optimal_long_MA, plot_MA_with_optimal_portfolio = (
            MA_generate_optimal_portfolio(
                df=st.session_state.forecast,
                start_window_of_MA=1,
                end_window_of_MA=250,
                init_cash=100000,
                fees=0.00003,
                frequence="1D",
            )
        )
        optimum_df = pd.DataFrame(
            {
                "Короткая скользящая средняя в прогнозировании": [optimal_short_MA],
                "Длинная скользящая средняя в прогнозировании": [optimal_long_MA],
            }
        )
        st.write(stats, optimum_df)
        st.plotly_chart(plot_MA_with_optimal_portfolio)
