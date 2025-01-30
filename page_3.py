import pandas as pd
import streamlit as st
from functions import MA_generate_optimal_portfolio

st.subheader("Подбор оптимальных значений скользящих средних")

start_window_of_MA = st.number_input("Генерация окон от", value=None, step=1)
end_window_of_MA = st.number_input("Генерация окон до", value=None, step=1)

init_cash = st.number_input(
    "Введите начальный капитал (необязательно)", step=1, value=100000
)

fees = st.number_input("Введите комиссию (необязательно)", value=0.00003)

if start_window_of_MA is not None and end_window_of_MA is not None:
    if start_window_of_MA <= end_window_of_MA:
        check_find = st.button("Поиск оптимальных значений для скольщих средних")
        if check_find:
            (
                optimal_stats,
                optimal_short_MA,
                optimal_long_MA,
                plot_MA_with_optimal_portfolio,
            ) = MA_generate_optimal_portfolio(
                df=st.session_state.df,
                start_window_of_MA=start_window_of_MA,
                end_window_of_MA=end_window_of_MA,
                init_cash=init_cash,
                fees=fees,
                frequence="1D",
            )

            st.write(optimal_stats)
            optimum_df = pd.DataFrame(
                {
                    "Короткая скользящая средняя": [optimal_short_MA],
                    "Длинная скользящая средняя": [optimal_long_MA],
                }
            )
            st.write(optimum_df)
            st.plotly_chart(plot_MA_with_optimal_portfolio)

            first_date = st.session_state.df.reset_index()["begin"][0].strftime(
                "%Y-%m-%d"
            )

            last_date_index = st.session_state.df.reset_index()["begin"].shape[0] - 1

            last_date = st.session_state.df.reset_index()["begin"][last_date_index - 1]

            # excel_file = optimum_df.to_excel(excel_writer="xlsxwriter", index=False)

            # st.download_button(
            #     label="Скачать оптимальные значения для MA excel файл",
            #     data=excel_file,
            #     file_name=f"optimum_values_for_{st.session_state.ticket}_for_date_{first_date}_{last_date}.xlsx",
            # )

            file_path = "temp_file.xlsx"
            optimum_df.to_excel(
                file_path, index=False, sheet_name="Sheet1", engine="xlsxwriter"
            )

            # Чтение файла для скачивания
            with open(file_path, "rb") as file:
                st.download_button(
                    label="Скачать оптимальные значения для MA excel файл",
                    data=file.read(),
                    file_name=f"optimum_values_for_{st.session_state.get('ticket', 'default_ticket')}_for_date_{first_date}_{last_date}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
