import sql as sql_bd_copy
import sql
from collections import defaultdict
import re
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


def krugovaya_diagr(predpr, monse, year,):

    st.header(f"Активність гризунів по приміщеннях")
    st.write(f"Дата {monse}.{year}")

    _dates, _month, _data_dict = sql_bd_copy.value_from_db_for_cheklist(monse, year, "III", predpr)

    grouped_data = defaultdict(list)

    for entry in _data_dict:
        for container, (value, _) in entry.items():
        
            if "-" in  value:
                try:
                    grouped_data[container].append(int(value.split("-")[1]))
                except:
                    pass
        
    # Преобразуем в обычный словарь
    grouped_data_dict = {key: tuple(values) for key, values in grouped_data.items()}


        
    podpis_danix = sql.podpis_danix_1(predpr)
   

    grouped_data = defaultdict(int)

    for container_list, label in podpis_danix:
        for container in container_list:
            str_container = str(container)  # Переводим номер контейнера в строку для сопоставления
            if str_container in grouped_data_dict:
                grouped_data[label] += sum(grouped_data_dict[str_container])  # Суммируем значения контейнера

    # Преобразуем в обычный словарь
    grouped_data = dict(grouped_data)
    if not grouped_data:
        st.write("У цьому місяці гризуни відсунні")
        return
    
  
    

        
    try:
        final_data = [(re.findall(r'\n(.*?)\n', label, re.DOTALL)[0].capitalize(), total ) for label, total in  grouped_data.items() if total > 0]
    except:
        try:
            final_data = [(f"{label.split(",")[1]} {label.split(",")[2]}", total ) for label, total in  grouped_data.items() if total > 0]
        except:
            final_data = [(f"{label.split(",")[1]}", total ) for label, total in  grouped_data.items() if total > 0]

  
    
    def plot_pie_chart(data):
        # Суммируем повторяющиеся категории
        unique_data = {}
        for label, value in data:
            if label in unique_data:
                unique_data[label] += value  # Суммируем значения для повторяющихся категорий
            else:
                unique_data[label] = value

        labels, values = zip(*unique_data.items())

        # Создаем диаграмму без встроенных подписей
        fig, ax = plt.subplots()
        wedges, _, _ = ax.pie(
            values, autopct='', startangle=140, wedgeprops={'edgecolor': 'black'}
        )

        # Добавляем подписи вручную
        total = sum(values)
        for i, wedge in enumerate(wedges):
            angle = (wedge.theta2 + wedge.theta1) / 2  # Средний угол сектора
            x = np.cos(np.radians(angle)) * 1.3  # Выносим подпись наружу
            y = np.sin(np.radians(angle)) * 1.3
            percent = (values[i] / total) * 100
            ax.text(x, y, f"{labels[i]}: {values[i]} ({percent:.1f}%)", ha='center', fontsize=10, weight='bold')

        ax.axis('equal')  # Сделать круг ровным

        st.pyplot(fig)

        
    
    plot_pie_chart(final_data)
