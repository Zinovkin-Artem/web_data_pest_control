import streamlit as st
import pandas as pd
import numpy as np


def show_page_2():
    # Функция для сохранения значения в session_state
    def store_value(key):
        st.session_state[key] = st.session_state["_" + key]

    # Функция для загрузки значения из session_state, если оно еще не сохранено
    def load_value(key, default_value, value_list):
        if key not in st.session_state:
            st.session_state[key] = default_value  # Значение по умолчанию
        # Проверяем, что значение в session_state находится в списке
        if st.session_state[key] not in value_list:
            st.session_state[key] = default_value  # Если нет, возвращаем значение по умолчанию

    #################################################################################

    st.write("Here's our first attempt at using data to create a table:")

    # Инициализация значений для выбора
    month = ["январь", "февраль", "март"]
    _value = ["месяц", "квартал", "год"]

    # Загрузка значений из session_state, с установкой значений по умолчанию
    load_value("selectbox_value", "январь", month)  # Месяц по умолчанию
    load_value("selectbox_value_1", "месяц", _value)  # Период по умолчанию

    # Выбор периода (месяц, квартал, год)
    selected_value_2 = st.sidebar.selectbox("Выберите период", _value, 
                                            index=_value.index(st.session_state["selectbox_value_1"]),
                                            key="_selectbox_value_1", on_change=store_value, args=["selectbox_value_1"])

    # Если выбран месяц, выбираем конкретный месяц
    if selected_value_2 == "месяц":
        selected_value_1 = st.sidebar.selectbox("Выберите месяц", month, 
                                                index=month.index(st.session_state["selectbox_value"]),
                                                key="_selectbox_value", on_change=store_value, args=["selectbox_value"])

        # Показать таблицу для "февраля"
        if selected_value_1 == "февраль":
            st.write(pd.DataFrame({
                '1 column': [1, 2, 3, 4],
                'second column': [10, 20, 30, 40],
                '3 column': [1, 2, 3, 4],
                '4 column': [10, 20, 30, 40]
            }))

    ###########################################################

    # Простой selectbox для выбора месяца (повторно)
    dyce_1 = st.selectbox("Выберите месяц", ["январь", "февраль", "март"])

    ###########################################################

    # Разметка с колонками
    row1 = st.columns(3)
    row2 = st.columns(3)

    for col in row1 + row2:
        with col:
            col.title(":logotipo ukr.png:")

    ###########################################################

    # Вкладки для выбора изображений
    tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])

    with tab1:
        st.header("A cat")
        st.image("https://static.streamlit.io/examples/cat.jpg", width=200)
    with tab2:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
    with tab3:
        st.header("An owl")
        st.write(2 + 2)

