import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import sql
from datetime import datetime



def diagramma(_pred):    

    data = sql.diagr_tretiy_how_mishi(_pred)
    
    
    months = sorted([i[0] for  i in data],  key=lambda date: datetime.strptime(date, "%m.%Y"))
    
    # Заголовок выбора диапазона
    st.markdown("<h3 style='text-align: center;'>Виберіть діапазон дат:</h3>", unsafe_allow_html=True)

    # Выбор диапазона
    selected_range = st.select_slider(
        "Виберіть необхідний діапазон", 
        options=months, 
        value=(months[0], months[-1]), 
        label_visibility="collapsed"
    )

    # Фильтруем данные
    start_idx = months.index(selected_range[0])
    end_idx = months.index(selected_range[1]) + 1  # +1, чтобы включить последний месяц
    filtered_data = [entry for entry in data if entry[0] in months[start_idx:end_idx]]

    # # Переключатель ВКЛ/ВЫКЛ
    # toggle_state = st.toggle("Додати інший барьер", value=False)

    # Извлекаем данные для диаграммы
    labels = [entry[0] for entry in filtered_data]
    values1 = [entry[1] for entry in filtered_data]  # Первое значение
    values2 = [entry[2] for entry in filtered_data]  # Второе значение
    
    # Построение графика
    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(labels))  # Позиции по оси X
    width = 0.4  # Ширина столбцов

  
 

    # Подписи значений сверху
   
    # Первый столбец
    bars1 = ax.bar(x - width/2, values1, width=width, label="Загальна кількість поїдання принади за місяць %", color='blue', alpha=0.7)
    ax.bar_label(bars1, padding=3, fontsize=10, color='black')

   
    bars2 = ax.bar(x + width/2, values2, width=width, label="Загальна кількість гризунів за місяць шт", color='orange', alpha=0.7)
    ax.bar_label(bars2, padding=3, fontsize=10, color='black')



   


    # Настройки осей
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45)
    ax.set_ylabel("Значення")
    ax.set_title("ПОРІВНЯЛЬНА ДІАГРАММА АКТИВНОСТІ ГРИЗУНІВ")
    ax.legend()

    # Отображение графика
    st.pyplot(fig)

if __name__ == "__main__":

   
    diagramma("ТОВ 'АДМ'")