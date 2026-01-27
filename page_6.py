import streamlit as st
from datetime import datetime
from zvit_new import Zvit
from chek_list_in_exel_copy import Chek_list_in_exel
from chek_list_in_exel_lampi import Chek_list_in_exel_lamp
from akt_utiliz_create import Akti_utiliz_create


def show_page_6(predpriyatie):
    current_year = datetime.now().year
    if "show_form_zvit" not in st.session_state:
        st.session_state["show_form_zvit"] = False

    if st.session_state["show_form_zvit"]:
            current_year = datetime.today().year

    st.header("🧾 СТВОРЕННЯ ЗВІТУ")

    monse = st.selectbox("Місяць", ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"], index=int(datetime.today().month)-1, key="zvit_selekt")
    year = st.number_input("Оберіть рік", min_value=2000, max_value=2100, value=current_year, step=1, key="number_input_zvit")

    Zvit(predpriyatie, str(monse), str(year)).main()

    st.header("📋 СТВОРЕННЯ ЧЕК ЛИСТА")

    monse_chec = st.selectbox("Оберіть місяць", ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"], index=int(datetime.today().month)-1, key="barier_selekt")
    year_chec = st.number_input("Оберіть рік", min_value=2000, max_value=2100, value=current_year, step=1, key="number_input_cheklist")
    barier = st.selectbox("Оберіть барьер", ["I - II","III","Інсектицидні лампи"])
    if barier == "Інсектицидні лампи":
        barier = "ІЛ"
        Chek_list_in_exel_lamp(predpriyatie,barier, monse_chec, year_chec).main()
    else:
        Chek_list_in_exel(predpriyatie,barier, monse_chec, year_chec).main()


   
    st.header("🧾 СТВОРЕННЯ АКТУ УТИЛІЗАЦІЇ")

    monse_akt = st.selectbox("Місяць", ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"], index=int(datetime.today().month)-1, key="akt_selekt")
    year_akt = st.number_input("Оберіть рік", min_value=2000, max_value=2100, value=current_year, step=1, key="number_input_akt")
    Akti_utiliz_create(predpriyatie, str(monse_akt), str(year_akt)).main()