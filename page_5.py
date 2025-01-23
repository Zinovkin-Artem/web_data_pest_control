from PestControl.chek_list_in_exel_copy import Chek_list_in_exel
import streamlit as st


def show_page_5(predpriyatie, bar):
    #ВЫБОР МЕСЯЦ ГОД
    # import streamlit as st
    # from datetime import datetime

    # # Украинские названия месяцев
    # months_ua = [
    #     "Січень", "Лютий", "Березень", "Квітень", "Травень", "Червень",
    #     "Липень", "Серпень", "Вересень", "Жовтень", "Листопад", "Грудень"
    # ]

    # current_month = datetime.today().month
    # current_year = datetime.today().year

    # # Выбор месяца
    # selected_month = st.selectbox("Оберіть місяць", months_ua, index=current_month - 1)

    # # Выбор года
    # selected_year = st.number_input("Оберіть рік", min_value=2000, max_value=2100, value=current_year, step=1)

    # st.write(f"📅 Ви обрали: {selected_month} {selected_year}")

#############################################################################################

   
    
    

    st.write("selected_predp:", predpriyatie)
    st.write("barrier:", bar)

    report = Chek_list_in_exel(predpriyatie, bar, "01", "2024")
    report.main()
