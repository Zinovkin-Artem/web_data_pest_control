import streamlit as st


def shapka(predpr, nazva, kilkist_obl, z_po:str, vidpovid):

    
   
        # z, po = z_po.split("-")
    if z_po:     
        _str = z_po
    else:
        _str = "бар'єр відсутній"

    st.markdown(
        """
        <h1 style="
            text-align: center;
            color: #0057b7; 
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        ">
            ВАС ВІТАЄ ДЕЗ-ЕЛЬТОР
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
    f"""
    <h2 style="
        text-align: center;
        color: #008000; 
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
    ">
         {predpr} 
        \n {nazva}
    </h2>
    """,
    unsafe_allow_html=True
)
    
    col1, col2 = st.columns(2)
    with col1:
        
        st.markdown(f"""
        <div style="background-color: #f0f8ff; padding: 10px; border-radius: 5px; margin-bottom: 20px; text-align: center;">
            <strong>Відповідальний:</strong><br>
            {vidpovid}
        </div>
    """, unsafe_allow_html=True)
        
    with col2:
        
        st.markdown(f"""
    <div style="background-color: #f0f8ff; padding: 10px; border-radius: 5px; margin-bottom: 20px; text-align: center;">
        <strong>Кількість обладнання {kilkist_obl}:</strong><br>
        {_str}
    </div>
""", unsafe_allow_html=True)
        
    if _str == "бар'єр відсутній":
        st.markdown(
            "<h1 style='text-align: center; font-size: 120px;'>🤷‍♂️</h1>", 
            unsafe_allow_html=True
        )
        return False
    else:
        return True
