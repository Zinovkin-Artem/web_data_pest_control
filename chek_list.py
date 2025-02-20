import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from PestControl import sql_bd_copy
from datetime import datetime
from danie_krugovaya_III import krugovaya_diagr

def check_range(number, range_str):
    range_str = range_str.replace(',', ' ')  # ✅ Заменяем ВСЕ запятые на пробелы
    ranges = range_str.split()  # ✅ Теперь разбиваем по пробелам

    for r in ranges:
        if '-' in r:
            start, end = map(int, r.split('-'))  # ✅ Корректно разбиваем диапазон
            if start <= number <= end:
                return True
        else:
            if int(r) == number:
                return True
    return False

def list_dk(_str: str):
    _str = _str.replace(',', ' ')
    
    _str = _str.split()
   
    _list = []
    for i in _str:
        if "-" in i:
            a, b = map(int, i.split("-"))
            _list.extend(range(a, b + 1))
        else:
            _list.append(int(i))
   
    return _list

def chek_list(_date, year,  predpr, dk_z_po, barier):
    if barier in  "I - II":
        _barier = "I - II"
        _dates, _month, _data_dict = sql_bd_copy.value_from_db_for_cheklist(_date, year, _barier, predpr)

    elif barier == "III":
        _barier = "III"
        _dates, _month, _data_dict = sql_bd_copy.value_from_db_for_cheklist(_date, year, _barier, predpr)
    
        

    
    _podpis_danix = sql_bd_copy.podpis_danix(predpr)
    
    dates = _dates
    month = str(*_month)
    data_dicts = _data_dict
    
    
    number_nugnix_dk = list_dk(dk_z_po)
    container_ids = sorted(
        (i for i in set().union(*[d.keys() for d in data_dicts]) if int(i) in number_nugnix_dk), key=int
    )
    
    columns = ['Контейнер'] + [f"{day}.{month}" for day in dates]
    table_data = {col: [] for col in columns}
    tooltip_data = {col: [] for col in columns}
    
    container_comment_data = []
    for container in container_ids:
        container_comment = "Нет данных"
        for range_str, comment, color, _ in _podpis_danix:
            if check_range(int(container), range_str):
                container_comment = comment
                break
        container_comment_data.append(f"{container} - {container_comment}")
    
    table_data['Контейнер'] = container_comment_data
    for i, date in enumerate(dates):
        col_name = f"{date}.{month}"
        for container in container_ids:
           
            
            if container in data_dicts[i]:
                value, tooltip = data_dicts[i][container]
                table_data[col_name].append(value)
                tooltip_data[col_name].append(tooltip)
            else:
                table_data[col_name].append("")
                tooltip_data[col_name].append("Нет данных")
    
    df = pd.DataFrame(table_data)
    
    
    filter_data = st.radio("Виберіть фільтр", ["Показати все", "Тільки активні", "НД", "ІН"],key=f"{barier}", horizontal=True, label_visibility="collapsed")
   
    # Фильтрация данных
    if filter_data == "Тільки активні":
        df = df[df.iloc[:, 1:].apply(
            lambda row: any(pd.to_numeric(row, errors='coerce').fillna(0) > 0) or
                        any(row.astype(str).str.contains(r'[MKМК]', na=False)), 
            axis=1
        )]
        


    elif filter_data == "НД":
        df = df[df.iloc[:, 1:].apply(lambda row: any(row.astype(str) == "НД"), axis=1)]

    elif filter_data == "ІН":
        df = df[df.iloc[:, 1:].apply(lambda row: any(row.astype(str) == "ІН"), axis=1)]

    
    for col in df.columns:
        if col != 'Контейнер':
            tooltips = tooltip_data[col]
            if len(tooltips) != len(df):
                tooltips = tooltips[:len(df)] if len(tooltips) > len(df) else tooltips + [""] * (len(df) - len(tooltips))
            df[f"tooltip_{col}"] = tooltips
    
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_column('Контейнер', tooltipField="tooltip_Контейнер", flex= 1)
    
    for col in df.columns:
        if col != 'Контейнер':
            gb.configure_column(col, tooltipField=f"tooltip_{col}", width=100)
    
    for col in df.columns:
        if col.startswith('tooltip_'):
            gb.configure_column(col, hide=True)
    
    grid_options = gb.build()
    
    AgGrid(df, gridOptions=grid_options, height=400, width='80%', allow_unsafe_jscode=True)

    

def main(_barier, _predpr, z_po):
    # state_key = f"showform_{_barier}"  # ✅ Уникальный ключ для каждой страницы

    # # Инициализируем состояние формы (отдельное для каждого _barier)
    # if state_key not in st.session_state:
    #     st.session_state[state_key] = False

    # Кнопка для отображения формы
    # if st.button(f"📝 Дивитися чек_лист {_barier} бар'єр", key=f"download_chek_list_{_barier}"):
    #     st.session_state[state_key] = not st.session_state[state_key]  # ✅ Переключаем состояние только для текущего _barier

    # # Если форма активна, отображаем элементы
    # if st.session_state[state_key]:  # ✅ Проверяем только свое состояние
    current_year = datetime.today().year
    current_month = datetime.today().strftime("%m")  # Текущий месяц в формате "01", "02" и т.д.
    st.header(f"Чек-лист {_barier} бар'єр")
    # Выбор месяца (по умолчанию текущий)
    monse = st.selectbox(
        "Оберіть місяць", 
        ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"], 
        index=int(current_month) - 1,  # Устанавливаем индекс текущего месяца
        key=f"pokaz_chek_mons_{_barier}"  # ✅ Разные ключи для каждой страницы
    )

    # Выбор года (по умолчанию текущий)
    year = st.number_input(
        "Оберіть рік", 
        min_value=2000, 
        max_value=2100, 
        value=current_year, 
        step=1, 
        key=f"pokaz_chek_year_{_barier}"  # ✅ Разные ключи для каждой страницы
    )

    # Вызов функции
    chek_list(monse, year, barier=_barier, predpr=_predpr, dk_z_po=z_po)
    if _barier == "III":
        krugovaya_diagr(_predpr, monse, year)


