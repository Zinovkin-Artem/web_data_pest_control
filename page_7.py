from sql import dezinseksiy, dezinseksiy_zapis
import streamlit as st
import pandas as pd
import datetime

def show_page_7(predpriyatie, is_admin):
    date = dezinseksiy(predpriyatie)

    if not date:
        st.markdown(f"""
        <div style="background-color: #f0f8ff; padding: 10px; border-radius: 5px; margin-bottom: 20px; text-align: center;">
            <strong>"ІНФОРМАЦІЯ ВІДСУТНЯ"</strong><br>
            <h1 style='text-align: center; font-size: 120px;'>🤷‍♂️</h1>
        </div>
    """, unsafe_allow_html=True)
        
    else:
        if is_admin:
            # Календарь для даты
            date_input = st.date_input("Виберіть дату:", datetime.date.today())

            

            # Используем text_area для ширины
            roboti_input = st.text_area("Роботи що проводились:", height=100)

            preparat_input = st.text_input("Препарат:")

            # Кнопка с проверкой
            if st.button("Записать в БД"):
                if not roboti_input.strip():  # Проверяем, что поле не пустое
                    st.error("Заповніть поле роботи що проводились!")
                else:
                    dezinseksiy_zapis(predpriyatie, date_input, roboti_input, preparat_input)
                    st.success("Записано")

        df = pd.DataFrame(date, columns=['Дата', 'Опис робіт', 'Препарат'])
        df['Дата'] = df['Дата'].dt.strftime('%d.%m.%Y')
        # Перенумеровываем индекс с 1
        df.index = df.index + 1

        # Выводим с помощью st.table(), который точно не показывает индекс
        st.subheader('Таблиця робіт проведених за одноразовим замовленням')
        st.table(df)
                


       


