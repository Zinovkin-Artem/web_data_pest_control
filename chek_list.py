import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
# from sql import value_from_db_for_cheklist, podpis_danix
from PestControl import sql_bd_copy 

# Функция для проверки, попадает ли номер в диапазон
def check_range(number, range_str):
    ranges = range_str.split(', ')
    for r in ranges:
        if '-' in r:
            start, end = map(int, r.split('-'))
            if start <= number <= end:
                return True
        else:
            if int(r) == number:
                return True
    return False

# Основная функция для отображения страницы
def chek_list(_date, year, barier, predpr):
    _dates, _month, _data_dict = sql_bd_copy.value_from_db_for_cheklist(_date, year, barier, predpr)
    _podpis_danix = sql_bd_copy.podpis_danix(predpr)
    
    #"10","2024", "III", "ТОВ 'М.В. КАРГО' ГОЛОВНА ТЕРІТОРІЯ"

    # Исходные данные
    dates = _dates  # Дни
    month = str(*_month)  # Месяц (берём как строку)
    data_dicts = _data_dict

    # 1. Собираем все уникальные контейнеры
    container_ids = sorted(set().union(*[d.keys() for d in data_dicts]))

    # 2. Создаём таблицу
    columns = ['Контейнер'] + [f"{day}.{month}" for day in dates]
    table_data = {col: [] for col in columns}

    # Диапазоны для контейнеров
    container_ranges = _podpis_danix

    # 3. Заполняем таблицу
    tooltip_data = {col: [] for col in columns}  # Подсказки

    # Добавляем комментарии для контейнеров в колонку "Контейнер"
    container_comment_data = []
    for container in container_ids:
        container_comment = "Нет данных"
        for range_str, comment, color, _ in container_ranges:
            if check_range(int(container), range_str):
                container_comment = comment
                break
        # Добавляем контейнер с комментариями
        container_comment_data.append(f"{container} - {container_comment}")

    # Добавляем контейнеры в таблицу и оставляем пустые значения для остальных колонок
    table_data['Контейнер'] = container_comment_data
    for i, date in enumerate(dates):  # Для каждого дня
        col_name = f"{date}.{month}"
        for container in container_ids:
            if container in data_dicts[i]:  # Если есть данные для контейнера
                value, tooltip = data_dicts[i][container]
                table_data[col_name].append(value)  # Основное значение
                tooltip_data[col_name].append(tooltip)  # Всплывающая подсказка
            else:
                table_data[col_name].append("")  # Пустая ячейка
                tooltip_data[col_name].append("Нет данных")  # Подсказка

    # 4. Преобразуем в DataFrame
    df = pd.DataFrame(table_data)

    # 5. Настроим AgGrid для отображения таблицы с комментариями
    gb = GridOptionsBuilder.from_dataframe(df)
    
    # Настроим рендеринг для столбца 'Контейнер' с комментариями
    gb.configure_column('Контейнер', 
                        tooltipField="tooltip_Контейнер")  # Подсказка для колонки "Контейнер"

    # Настроим tooltips для других столбцов без добавления столбцов tooltip_*
    for col in df.columns:
        if col != 'Контейнер':  # Пропускаем столбец "Контейнер"
            # Не добавляем новый столбец tooltip, но настраиваем подсказку для текущего столбца
            gb.configure_column(col, tooltipField=f"tooltip_{col}")

    # 6. Убедимся, что мы добавляем всплывающие подсказки в основной DataFrame для правильного отображения
    for col in df.columns:
        if col != 'Контейнер':  # Пропускаем "Контейнер"
            df[f"tooltip_{col}"] = tooltip_data[col]

    # 7. Скрываем столбцы tooltip_*
    for col in df.columns:
        if col.startswith('tooltip_'):
            gb.configure_column(col, hide=True)

    grid_options = gb.build()

    # 8. Отображаем таблицу с комментариями, без добавления столбцов tooltip_*
    AgGrid(df, gridOptions=grid_options, height=550, width='2000', allow_unsafe_jscode=True)