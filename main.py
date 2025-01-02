import requests
import pandas as pd
import apimoex
import vectorbt as vbt
import numpy as np
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
import streamlit as st
from functions import fetch_candles, MA_with_fix_window, MA_generate_optimal_portfolio


def main():
    download_data_and_MA = st.Page("page_1.py", title="Загрузка данных")
    fix_MA = st.Page(
        "page_2.py",
        title="Построение графика скользящих средних с оптимальными значениями",
    )
    find_optimal_MA = st.Page(
        "page_3.py", title="Генерация оптимальных значений скользящих средних"
    )
    time_series_prediction = st.Page(
        "page_4.py", title="Прогнозирование временного ряда"
    )
    pg = st.navigation(
        [download_data_and_MA, fix_MA, find_optimal_MA, time_series_prediction]
    )
    st.set_page_config(page_title="MA cross", page_icon=":material/edit:")
    pg.run()


if __name__ == "__main__":
    main()
