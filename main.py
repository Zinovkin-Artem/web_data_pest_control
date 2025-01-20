import streamlit as st
import sql  # предполагаем, что это ваш модуль для работы с базой данных
from page_1 import show_page_1
from page_2 import show_page_2

# Функция для проверки пароля
def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form to collect username & password"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            submit_button = st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        # Предполагаем, что sql.show_login() возвращает кортеж с данными пользователя
        username = st.session_state["username"]
        password = st.session_state["password"]
        
        # Проверяем логин и пароль
        user_data = sql.show_login(username)  # Получаем данные из БД по имени пользователя
        if user_data and user_data[0].lower() == username.lower() and user_data[1] == password:
            st.session_state["password_correct"] = True
            # Удаляем пароль и логин из session_state, чтобы не хранить их
            del st.session_state["password"]
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Проверяем, прошел ли пользователь проверку пароля
    if st.session_state.get("password_correct", False):
        return True

    # Показать форму для ввода логина и пароля
    login_form()
    if "password_correct" in st.session_state and not st.session_state["password_correct"]:
        st.error("😕 User not known or password incorrect")
    return False

# Проверка пароля, если неправильно, остановим выполнение
if not check_password():
    st.stop()


# Навигация с использованием selectbox
page = st.sidebar.radio("Выберите страницу", ["page_1", "page_2"])

# Логика для перехода между страницами
if page == "page_1":
    show_page_1()
elif page == "page_2":
    show_page_2()
