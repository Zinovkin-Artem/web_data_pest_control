from zvit import Zvit
import streamlit as st
from chek_list_in_exel_copy import Chek_list_in_exel
import pandas as pd
import plotly.express as px

def show_page_5(predpriyatie, bar):
    col1, col2, col3 = st.columns(3)
    with col1:
        report = Chek_list_in_exel(predpriyatie, bar, "01", "2024")
        report.main()

    with col2:
        report = Zvit(predpriyatie).main()



    # Генерируем тестовые данные (замени на свои)
    data = {
        "Дата": pd.date_range(start="2024-01-01", periods=10, freq="W"),
        "Крысы": [5, 3, 4, 6, 2, 8, 9, 4, 3, 7],
        "Тараканы": [10, 15, 13, 17, 12, 19, 25, 22, 18, 20],
    }

    df = pd.DataFrame(data)

    # Выбор вредителей для анализа
    options = st.multiselect("Выберите вредителей", df.columns[1:], default=df.columns[1:])

    # Фильтруем данные
    df_filtered = df[["Дата"] + options]

    # Строим график
    fig = px.line(df_filtered, x="Дата", y=options, markers=True, title="Тенденция появления вредителей")
    st.plotly_chart(fig)





#     #ВЫБОР МЕСЯЦ ГОД
#     import streamlit as st
#     from datetime import datetime

#     # Украинские названия месяцев
#     months_ua = [
#         "Січень", "Лютий", "Березень", "Квітень", "Травень", "Червень",
#         "Липень", "Серпень", "Вересень", "Жовтень", "Листопад", "Грудень"
#     ]

#     current_month = datetime.today().month
#     current_year = datetime.today().year

#     # Выбор месяца
#     selected_month = st.selectbox("Оберіть місяць", months_ua, index=current_month - 1)

#     # Выбор года
#     selected_year = st.number_input("Оберіть рік", min_value=2000, max_value=2100, value=current_year, step=1)

#     st.write(f"📅 Ви обрали: {selected_month} {selected_year}")

# #############################################################################################

   
    
    

#     # st.write("selected_predp:", predpriyatie)
#     # st.write("barrier:", bar)

#     # report = Chek_list_in_exel(predpriyatie, bar, "01", "2024")
#     # report.main()
