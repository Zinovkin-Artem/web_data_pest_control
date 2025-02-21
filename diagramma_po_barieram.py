import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import sql
from datetime import datetime
from danie_krugovaya_III import krugovaya_diagr


def get_cached_data(_pred, z_po, bar):
    """Загружаем данные и кэшируем их в session_state"""
    if st.session_state.get("cached_pred") != _pred:
        st.session_state["diagram_data"] = sql.dannie_iz_diagramma_1_2(_pred)
        st.session_state["grizuni_territory"] = sql.dannie_iz_grizuni_na_territorii(_pred)
        st.session_state["grizuni_v_givolovkax"] = sql.grizuni_v_givolovkax(_pred, z_po=z_po, barier=bar)
        st.session_state["cached_pred"] = _pred  # Запоминаем, для какого предприятия данные
    return st.session_state["diagram_data"], st.session_state["grizuni_territory"], st.session_state["grizuni_v_givolovkax"]


def diagramma(_pred, bar, z_po, flag = True): 
    data, data_2, data_3 = get_cached_data(_pred, z_po, bar)


    if flag:   
        # Получаем данные для первой диаграммы
        # data = sql.dannie_iz_diagramma_1_2(_pred)
    
        # Извлекаем месяцы, отсортированные по дате
        months = sorted([i[0] for i in data], key=lambda date: datetime.strptime(date, "%m.%Y"))
        
        # Заголовок выбора диапазона
        st.markdown("<h3 style='text-align: center;'>Виберіть діапазон дат:</h3>", unsafe_allow_html=True)

        # Выбор диапазона
        selected_range = st.select_slider(
            "Виберіть необхідний діапазон", 
            options=months, 
            value=("07.2023", months[-1]), 
            label_visibility="collapsed"
        )

        # Фильтруем данные
        start_idx = months.index(selected_range[0])
        end_idx = months.index(selected_range[1]) + 1  # +1, чтобы включить последний месяц
        filtered_data = [entry for entry in data if entry[0] in months[start_idx:end_idx]]

        # Переключатель для первой диаграммы
        toggle_state_1 = st.toggle("Додати інший бар'єр", value=False)

        # Извлекаем данные для диаграммы
        labels = [entry[0] for entry in filtered_data]
        values1 = [entry[1] for entry in filtered_data]  # поедание первый барьер
        values2 = [entry[2] for entry in filtered_data]  # поедание второй барьер

        # Построение первой диаграммы
        fig, ax = plt.subplots(figsize=(12, 6))
        x = np.arange(len(labels))  # Позиции по оси X
        width = 0.4  # Ширина столбцов

        if bar == "I":
            bars1 = ax.bar(x - width/2, values1, width=width, label="Загальне поїдання принади за місяць % перший бар'єр", color='blue', alpha=0.7)
            ax.bar_label(bars1, padding=3, fontsize=10, color='black')

            if toggle_state_1:
                bars2 = ax.bar(x + width/2, values2, width=width, label="Загальне поїдання принади за місяць % другий бар'єр", color='orange', alpha=0.7)
                ax.bar_label(bars2, padding=3, fontsize=10, color='black')

        elif bar == "II":
            bars2 = ax.bar(x, values2, width=width, label="Загальне поїдання принади за місяць % другий бар'єр", color='orange', alpha=0.7)
            ax.bar_label(bars2, padding=3, fontsize=10, color='black')

            if toggle_state_1:
                bars1 = ax.bar(x - width, values1, width=width, label="Загальне поїдання принади за місяць % перший бар'єр", color='blue', alpha=0.7)
                ax.bar_label(bars1, padding=3, fontsize=10, color='black')

        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=45)
        ax.set_ylabel("Значення")
        ax.set_title("ПОРІВНЯЛЬНА ДІАГРАММА АКТИВНОСТІ ГРИЗУНІВ")
        ax.legend()
        st.pyplot(fig)

        # Вторая диаграмма (грызуны на территории)
        # data_2 = sql.dannie_iz_grizuni_na_territorii(_pred)
        filtered_data_2 = [entry for entry in data_2 if entry[0] in months[start_idx:end_idx]]
        
        labels_2 = [entry[0] for entry in filtered_data_2]
        values1_2 = [entry[1] for entry in filtered_data_2]  # Мыши
        values2_2 = [entry[2] for entry in filtered_data_2]  # Крысы

        toggle_state_2 = st.toggle("Показати гризунів по видах", value=False)

        fig2, ax2 = plt.subplots(figsize=(12, 6))
        x_2 = np.arange(len(labels_2))

        if toggle_state_2:
            bars1_2 = ax2.bar(x_2 - width/2, values1_2, width=width, label="Миші", color='blue', alpha=0.7)
            ax2.bar_label(bars1_2, padding=3, fontsize=10, color='black')

            bars2_2 = ax2.bar(x_2 + width/2, values2_2, width=width, label="Криси", color='orange', alpha=0.7)
            ax2.bar_label(bars2_2, padding=3, fontsize=10, color='black')
        else:
            total_values_2 = [entry[1] + entry[2] for entry in filtered_data_2]
            bars_2 = ax2.bar(x_2, total_values_2, width=width, label="Загальна кількість гризунів", color='green', alpha=0.7)
            ax2.bar_label(bars_2, padding=3, fontsize=10, color='black')

        ax2.set_xticks(x_2)
        ax2.set_xticklabels(labels_2, rotation=45)
        ax2.set_ylabel("Значення")
        ax2.set_title("ГРИЗУНИ НА ТЕРИТОРІЇ (місяці в яких гризуни відсутні не показані)")
        ax2.legend()
        st.pyplot(fig2)

        # Третья диаграмма (грызуны в живоловках)
        # data_3 = sql.grizuni_v_givolovkax(_pred, z_po=z_po, barier=bar)
        filtered_data_3 = [entry for entry in data_3 if entry[0] in months[start_idx:end_idx]]

        labels_3 = [entry[0] for entry in filtered_data_3]
        values1_3 = [entry[1] for entry in filtered_data_3]  # Мыши
        values2_3 = [entry[2] for entry in filtered_data_3]  # Крысы

        toggle_state_3 = st.toggle("Показати гризунів у живоловках по видах", value=False)

        fig3, ax3 = plt.subplots(figsize=(12, 6))
        x_3 = np.arange(len(labels_3))

        if toggle_state_3:
            bars1_3 = ax3.bar(x_3 - width/2, values1_3, width=width, label="Миші", color='blue', alpha=0.7)
            ax3.bar_label(bars1_3, padding=3, fontsize=10, color='black')

            bars2_3 = ax3.bar(x_3 + width/2, values2_3, width=width, label="Криси", color='orange', alpha=0.7)
            ax3.bar_label(bars2_3, padding=3, fontsize=10, color='black')
        else:
            total_values_3 = [entry[1] + entry[2] for entry in filtered_data_3]
            bars_3 = ax3.bar(x_3, total_values_3, width=width, label="Загальна кількість гризунів", color='green', alpha=0.7)
            ax3.bar_label(bars_3, padding=3, fontsize=10, color='black')

        ax3.set_xticks(x_3)
        ax3.set_xticklabels(labels_3, rotation=45)
        ax3.set_ylabel("Значення")
        ax3.set_title("ГРИЗУНИ У ЖИВОЛОВКАХ")
        ax3.legend()
        st.pyplot(fig3)
    else:

        # Получаем данные для первой диаграммы
        data = sql.dannie_iz_diagramma_1_2(_pred)
    
        # Извлекаем месяцы, отсортированные по дате
        months = sorted([i[0] for i in data], key=lambda date: datetime.strptime(date, "%m.%Y"))
        
        # Заголовок выбора диапазона
        st.markdown("<h3 style='text-align: center;'>Виберіть діапазон дат:</h3>", unsafe_allow_html=True)

        # Выбор диапазона
        selected_range = st.select_slider(
            "Виберіть необхідний діапазон", 
            options=months, 
            value=("07.2023", months[-1]), 
            label_visibility="collapsed"
        )

        # Фильтруем данные
        start_idx = months.index(selected_range[0])
        end_idx = months.index(selected_range[1]) + 1  # +1, чтобы включить последний месяц
        filtered_data = [entry for entry in data if entry[0] in months[start_idx:end_idx]]

        # Извлекаем данные для диаграммы
        labels = [entry[0] for entry in filtered_data]
        values1 = [entry[1] for entry in filtered_data]  # поедание первый барьер
        values2 = [entry[2] for entry in filtered_data]  # поедание второй барьер

        # Построение первой диаграммы
        fig, ax = plt.subplots(figsize=(12, 6))
        x = np.arange(len(labels))  # Позиции по оси X
        width = 0.4  # Ширина столбцов



        # Третья диаграмма (грызуны в живоловках)
        data_3 = sql.grizuni_v_givolovkax(_pred, z_po=z_po, barier=bar)
        filtered_data_3 = [entry for entry in data_3 if entry[0] in months[start_idx:end_idx]]

        labels_3 = [entry[0] for entry in filtered_data_3]
        values1_3 = [entry[1] for entry in filtered_data_3]  # Мыши
        values2_3 = [entry[2] for entry in filtered_data_3]  # Крысы
      

        toggle_state_3 = st.toggle("Показати гризунів у живоловках по видах", value=False)

        fig3, ax3 = plt.subplots(figsize=(12, 6))
        x_3 = np.arange(len(labels_3))

        if toggle_state_3:
            bars1_3 = ax3.bar(x_3 - width/2, values1_3, width=width, label="Миші", color='blue', alpha=0.7)
            ax3.bar_label(bars1_3, padding=3, fontsize=10, color='black')

            bars2_3 = ax3.bar(x_3 + width/2, values2_3, width=width, label="Криси", color='orange', alpha=0.7)
            ax3.bar_label(bars2_3, padding=3, fontsize=10, color='black')
        else:
            total_values_3 = [entry[1] + entry[2] for entry in filtered_data_3]
            bars_3 = ax3.bar(x_3, total_values_3, width=width, label="Загальна кількість гризунів", color='green', alpha=0.7)
            ax3.bar_label(bars_3, padding=3, fontsize=10, color='black')

        ax3.set_xticks(x_3)
        ax3.set_xticklabels(labels_3, rotation=45)
        ax3.set_ylabel("Значення")
        ax3.set_title("ГРИЗУНИ У ЖИВОЛОВКАХ")
        ax3.legend()
        st.pyplot(fig3)

        # krugovaya_diagr(predpr=_pred, dk_z_po= z_po)

# import streamlit as st
# import matplotlib.pyplot as plt
# import numpy as np
# import sql
# from datetime import datetime
# from danie_krugovaya_III import krugovaya_diagr


# def get_cached_data(_pred, z_po, bar):
#     """Загружаем данные и кэшируем их в session_state"""
#     if "diagram_data" not in st.session_state or st.session_state.get("cached_pred") != _pred:
#         st.session_state["diagram_data"] = sql.dannie_iz_diagramma_1_2(_pred)
#         st.session_state["grizuni_territory"] = sql.dannie_iz_grizuni_na_territorii(_pred)
#         st.session_state["grizuni_territory"] = sql.grizuni_v_givolovkax(_pred, z_po=z_po, barier=bar)
#         st.session_state["cached_pred"] = _pred  # Запоминаем, для какого предприятия данные
#     return st.session_state["diagram_data"], st.session_state["grizuni_territory"], st.session_state["grizuni_territory"]


# def diagramma(_pred, bar, z_po):
#     data, data_2, data_3 = get_cached_data(_pred, bar, z_po)

#     # Извлекаем месяцы, отсортированные по дате
#     months = sorted([i[0] for i in data], key=lambda date: datetime.strptime(date, "%m.%Y"))

#     # Проверяем, изменился ли диапазон дат
#     if "selected_range" not in st.session_state:
#         st.session_state["selected_range"] = (months[0], months[-1])

#     # Выбор диапазона
#     selected_range = st.select_slider(
#         "Виберіть необхідний діапазон", 
#         options=months, 
#         value=st.session_state["selected_range"], 
#         label_visibility="collapsed"
#     )

#     # Если диапазон не изменился — не пересчитываем данные
#     if selected_range != st.session_state["selected_range"]:
#         st.session_state["selected_range"] = selected_range
#         st.session_state.pop("cached_plots", None)  # Удаляем старые графики

#     # Фильтруем данные
#     start_idx = months.index(selected_range[0])
#     end_idx = months.index(selected_range[1]) + 1
#     filtered_data = [entry for entry in data if entry[0] in months[start_idx:end_idx]]
#     filtered_data_2 = [entry for entry in data_2 if entry[0] in months[start_idx:end_idx]]

#     # Если уже есть кэшированные графики — просто их отображаем
#     if "cached_plots" in st.session_state:
#         for fig in st.session_state["cached_plots"]:
#             st.pyplot(fig)
#         return

#     st.session_state["cached_plots"] = []

#     # Построение первой диаграммы
#     labels = [entry[0] for entry in filtered_data]
#     values1 = [entry[1] for entry in filtered_data]  # Первый барьер
#     values2 = [entry[2] for entry in filtered_data]  # Второй барьер

#     fig, ax = plt.subplots(figsize=(12, 6))
#     x = np.arange(len(labels))  
#     width = 0.4

#     bars1 = ax.bar(x - width / 2, values1, width=width, label="Перший бар'єр", color='blue', alpha=0.7)
#     ax.bar_label(bars1, padding=3, fontsize=10, color='black')

#     bars2 = ax.bar(x + width / 2, values2, width=width, label="Другий бар'єр", color='orange', alpha=0.7)
#     ax.bar_label(bars2, padding=3, fontsize=10, color='black')

#     ax.set_xticks(x)
#     ax.set_xticklabels(labels, rotation=45)
#     ax.set_ylabel("Значення")
#     ax.set_title("ПОРІВНЯЛЬНА ДІАГРАММА АКТИВНОСТІ ГРИЗУНІВ")
#     ax.legend()
#     st.pyplot(fig)
#     st.session_state["cached_plots"].append(fig)

#     # Вторая диаграмма
#     labels_2 = [entry[0] for entry in filtered_data_2]
#     values1_2 = [entry[1] for entry in filtered_data_2]  # Мыши
#     values2_2 = [entry[2] for entry in filtered_data_2]  # Крысы

#     fig2, ax2 = plt.subplots(figsize=(12, 6))
#     x_2 = np.arange(len(labels_2))

#     bars1_2 = ax2.bar(x_2 - width / 2, values1_2, width=width, label="Миші", color='blue', alpha=0.7)
#     ax2.bar_label(bars1_2, padding=3, fontsize=10, color='black')

#     bars2_2 = ax2.bar(x_2 + width / 2, values2_2, width=width, label="Криси", color='orange', alpha=0.7)
#     ax2.bar_label(bars2_2, padding=3, fontsize=10, color='black')

#     ax2.set_xticks(x_2)
#     ax2.set_xticklabels(labels_2, rotation=45)
#     ax2.set_ylabel("Значення")
#     ax2.set_title("ГРИЗУНИ НА ТЕРИТОРІЇ")
#     ax2.legend()
#     st.pyplot(fig2)
#     st.session_state["cached_plots"].append(fig2)

    # #третяя диаграмма

    # filtered_data_3 = [entry for entry in data_3 if entry[0] in months[start_idx:end_idx]]

    # labels_3 = [entry[0] for entry in filtered_data_3]
    # values1_3 = [entry[1] for entry in filtered_data_3]  # Мыши
    # values2_3 = [entry[2] for entry in filtered_data_3]  # Крысы
    

    # toggle_state_3 = st.toggle("Показати гризунів у живоловках по видах", value=False)

    # fig3, ax3 = plt.subplots(figsize=(12, 6))
    # x_3 = np.arange(len(labels_3))

    # if toggle_state_3:
    #     bars1_3 = ax3.bar(x_3 - width/2, values1_3, width=width, label="Миші", color='blue', alpha=0.7)
    #     ax3.bar_label(bars1_3, padding=3, fontsize=10, color='black')

    #     bars2_3 = ax3.bar(x_3 + width/2, values2_3, width=width, label="Криси", color='orange', alpha=0.7)
    #     ax3.bar_label(bars2_3, padding=3, fontsize=10, color='black')
    # else:
    #     total_values_3 = [entry[1] + entry[2] for entry in filtered_data_3]
    #     bars_3 = ax3.bar(x_3, total_values_3, width=width, label="Загальна кількість гризунів", color='green', alpha=0.7)
    #     ax3.bar_label(bars_3, padding=3, fontsize=10, color='black')

    # ax3.set_xticks(x_3)
    # ax3.set_xticklabels(labels_3, rotation=45)
    # ax3.set_ylabel("Значення")
    # ax3.set_title("ГРИЗУНИ У ЖИВОЛОВКАХ")
    # ax3.legend()
    # st.pyplot(fig3)

    # krugovaya_diagr(predpr=_pred, dk_z_po= z_po)

