import requests
import pandas as pd
import apimoex
import vectorbt as vbt
import numpy as np
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
import streamlit as st
from functions import fetch_candles, MA_with_fix_window, MA_generate_optimal_portfolio
from functions import MA_with_fix_window

st.subheader("График скользящих средних с фиксированным значениями скользящих средних")

fast_ma_window = st.number_input(
    "Введите число для короткой скользящей средней", value=None, step=1
)
slow_ma_window = st.number_input(
    "Введите число для длинной скользящей средней", value=None, step=1
)

init_cash = st.number_input(
    "Введите начальный капитал (необязательно)", step=1, value=100000
)

fees = st.number_input("Введите комиссию (необязательно)", value=0.00003)

st.write("Короткая скользящая средняя:", fast_ma_window)
st.write("Длинная скользящая средняя:", slow_ma_window)
st.write("Значение начального капитала:", init_cash)
st.write("Значение комиссии:", fees)

if fast_ma_window is not None and slow_ma_window is not None:
    if fast_ma_window is None or slow_ma_window is None:
        st.error("Введите значения для короткой и длинной скользящей средней.")
    elif fast_ma_window <= 0 or slow_ma_window <= 0:
        st.error("Окно скользящей средней должно быть больше нуля.")
    elif fast_ma_window >= len(st.session_state.df) or slow_ma_window >= len(
        st.session_state.df
    ):
        st.error("Окно скользящей средней не может превышать длину данных.")
    else:
        check_button = st.button("Получить график и статистику")
        if check_button:

            stats_of_fix_strategy, plot_of_fix_strategy = MA_with_fix_window(
                df=st.session_state.df,
                fast_ma_window=fast_ma_window,
                slow_ma_window=slow_ma_window,
                init_cash=init_cash,
                fees=fees,
            )
            st.write(stats_of_fix_strategy)
            st.plotly_chart(plot_of_fix_strategy)
