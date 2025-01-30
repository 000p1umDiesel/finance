import streamlit as st
from functions import fetch_candles
from datetime import datetime

st.subheader("Загрузка данных и график скользящих средних")

ticket = st.text_input("Введите тикер", "")

fetch_button = st.button("Получить данные")

with st.expander("Расширенный фильтр"):
    start_date = st.date_input("Дата начала", datetime(2020, 1, 1))
    end_date = st.date_input("Дата окончания", datetime.today())
    advanced_filter_button = st.button("Получить данные с фильтром")


def load_data():
    """Загружает данные на основе тикера и фильтров."""
    if fetch_button and ticket:
        return fetch_candles(ticket, start=None, end=None, interval=24)
    elif advanced_filter_button and ticket:
        return fetch_candles(ticket, start=start_date, end=end_date, interval=24)
    return None


df = load_data()

if df is not None:
    st.session_state.df = df
    st.success("Данные успешно загружены и сохранены в сессию.")
    st.session_state.ticket = ticket
else:
    st.error("Введите тикер и нажмите кнопку для получения данных.")
