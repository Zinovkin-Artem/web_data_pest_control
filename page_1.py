import streamlit as st
import pandas as pd
import numpy as np
from PestControl.chek_list_in_exel_copy import Chek_list_in_exel




def show_page_1(predpriyatie, bar):
    col1, col2, col3 = st.columns(3)
    with col1:
        report = Chek_list_in_exel(predpriyatie, bar, "01", "2024")
        report.main()
#############################################
    chart_data = pd.DataFrame(
        {
            "col1": list(range(20)),
            "col2": np.random.randn(20),
            "col3": np.random.randn(20),
        }
    )

    st.bar_chart(
        chart_data,
        x="col1",
        y=["col2", "col3"],
        color=["#FF0000", "#0000FF"],  # Optional
    )
    #################################################

    # st.metric(label="Temperature", value="70 °F", delta="1.2 °F")

    chart_data = pd.DataFrame(
        {
            "col1": np.random.randn(20),
            "col2": np.random.randn(20),
            "col3": np.random.choice(["A", "B", "C"], 20),
        }
    )

    st.line_chart(chart_data, x="col1", y="col2", color="col3")

    ##############################################################




    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature", "70 °F", "1.2 °F")
    col2.metric("Wind", "9 mph", "-8%")
    col3.metric("Humidity", "86%", "4%")
    ###################################################

    a, b = st.columns(2)
    c, d = st.columns(2)

    a.metric("Temperature", "30°F", "-9°F", border=True)
    b.metric("Wind", "4 mph", "2 mph", border=True)

    c.metric("Humidity", "77%", "5%", border=True)
    d.metric("Pressure", "30.34 inHg", "-2 inHg", border=True)
    ##################################################

   

    
