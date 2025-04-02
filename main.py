import streamlit as st
from datetime import datetime

import requests



st.markdown(
    """
    <style>
    .main {
        max-width: 85%;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)




import sql  # предполагаем, что это ваш модуль для работы с базой данных
from page_0 import show_page_0
from page_1 import show_page_1
from page_2 import show_page_2
from page_3 import show_page_3
from page_4 import show_page_4
from page_5 import show_page_5
from page_6 import show_page_6

# Используем session_state вместо глобальной переменной
if "predpr" not in st.session_state:
    st.session_state["predpr"] = []  # Список предприятий

#определяем ip входящего
def get_real_ip():
    try:
        response = requests.get("https://api64.ipify.org?format=json")
        return response.json().get("ip", "Не удалось получить IP")
    except Exception as e:
        return f"Ошибка: {e}"



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
        username = st.session_state["username"]
        password = st.session_state["password"]
        
        # Проверяем логин и пароль
        user_data = sql.show_login(username)  # Получаем данные из БД по имени пользователя
        if user_data and user_data[0].lower() == username.lower() and user_data[1] == password:
            st.session_state["password_correct"] = True

            predpr_session_state = user_data[2]
          
            if st.session_state["username"].lower() == "admin":
               
                predpr_session_state = sql.show_login_admin()
            if st.session_state["username"].lower() != "admin":
                sql.vxod_v_streamlit(st.session_state["password"], st.session_state["username"], datetime.now(), get_real_ip())
           
                
                
            del st.session_state["password"]
            del st.session_state["username"]


            
           
            # Добавляем предприятие в session_state
            st.session_state["predpr"].append(predpr_session_state)
            
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True
    
    st.markdown(
    "<h2 style='text-align: center; color: #2E86C1;'>💼 СИСТЕМА ВЗАЄМОДІЇ З КЛІЄНТАМИ</h2>",
    unsafe_allow_html=True
)

    login_form()
    if "password_correct" in st.session_state and not st.session_state["password_correct"]:
        st.error("😕 User not known or password incorrect")
    return False

# Проверка пароля
if not check_password():
    st.stop()


# Теперь используем session_state для хранения predpr
if st.session_state["predpr"]:
    _predp = st.session_state["predpr"]

    if "," in _predp[0]:
        _predp = _predp[0].split(",")


    # если предприятий для показа в списке больше 8 система поймет что вошел админ
    if len(st.session_state["predpr"][0].split(","))>8:
        is_admin = True 
    else:
        is_admin = False
    



    # Устанавливаем значение по умолчанию, если его нет в session_state
    if "selected_predp" not in st.session_state:
        st.session_state["selected_predp"] = _predp[0]  # Берём первое предприятие

    if len(_predp) > 1:
        selected_predp = st.sidebar.radio(
            "Оберіть підприємство:", _predp, key="selected_predp"
        )
    else:
        selected_predp = _predp[0]  # Если одно предприятие, выбираем его автоматически
        
   
    # Если предприятий несколько, выбираем раздел для текущего предприятия
    selected_page = st.sidebar.radio(
        f"ВИБЕРІТЬ РОЗДІЛ",
        ["Загальні відомості","Перший бар'єр", "Другий бар'єр", "Третій бар'єр", "📄 ДОКУМЕНТИ", "🔔ПОВІДОМЛЕННЯ", "📊Генерація exel файлів"],
        key="selected_page"
)

    # Обработка страниц
    if selected_page == "Загальні відомості":
        show_page_0(selected_predp, "IIII",  "Загальні відомості")
    elif selected_page == "Перший бар'єр":
        show_page_1(selected_predp, "I", "Перший бар'єр")
    elif selected_page == "Другий бар'єр":
        show_page_2(selected_predp, "II", "Другий бар'єр")
    elif selected_page == "Третій бар'єр":
        show_page_3(selected_predp, "III", "Третій бар'єр")
    elif selected_page == "📄 ДОКУМЕНТИ":
        show_page_4(selected_predp)
    elif selected_page == "🔔ПОВІДОМЛЕННЯ":
        show_page_5(selected_predp, is_admin)
    elif selected_page == "📊Генерація exel файлів":
        show_page_6(selected_predp)
    
