import sql as sql_bd_copy
# import pandas as pd
# import streamlit as st


def list_dk(_str: str):
    _str = _str.split(",")
    _list = []
    for i in _str:
        if "-" in i:
            a, b = map(int, i.split("-"))
            _list.extend(range(a, b + 1))
        else:
            _list.append(int(i))
    return _list

def dannie_po_barieram(z_po, monse, year, predpr):

    _dates, _month, _data_dict = sql_bd_copy.value_from_db_for_cheklist(monse, year, "I - II", predpr)
    
   
    
   
    if not _data_dict:
        return False
    
    if z_po == "100000":
        return 1

    # z_po = "1-100000"

    dates = _dates  # Список дней месяца (например, [1, 2, 3, ...])
    month = str(*_month)  # Получаем название месяца
    data_dicts = _data_dict  # Словарь данных по контейнерам

    number_nugnix_dk = list_dk(z_po)
    container_ids = sorted(
        (i for i in set().union(*[d.keys() for d in data_dicts]) if int(i) in number_nugnix_dk), key=int
    )


    columns = ['Контейнер'] + [f"{day}.{month}" for day in dates]
    table_data = {col: [] for col in columns}  # Основные данные таблицы

    # container_comment_data = []
    # for container in container_ids:
    #     container_comment_data.append(f"{container}")
    # table_data['Контейнер'] = container_comment_data 


    for i, date in enumerate(dates):
        col_name = f"{date}.{month}"
        for container in container_ids:
            if container in data_dicts[i]:
                value, tooltip = data_dicts[i][container]  # Берём значение и подсказку
                table_data[col_name].append(value)
                
            else:
                table_data[col_name].append("")  # Если данных нет, вставляем пустую строку
    table_data.pop('Контейнер')

    ser = []

    for value in table_data.values():
        if value:
            ser.append(sum([int(i) for i in value if i.isdigit()])/len(value))
    
    return(round (sum(ser)/len(table_data), 1))
           


def main():
    _list = []
    _mes = ["01","02","03","04","05","06","07","08","09","10","11","12",]
    
    vse_predpr = sql_bd_copy.baza_vsex_predpr() 
    

    _mes = ["01","02","03","04","05","06","07","08","09","10","11","12",]
    years = ["2023","2024","2025"]

    for _year in years:
        for pred in vse_predpr: 
                for i in _mes:
                    val = sql_bd_copy.baza_predpr(pred[1])
                    _ = []
                    for barier, z_po in enumerate(val[7:9]):
                        
                        if not z_po:
                            z_po="100000"
                            
                        data = dannie_po_barieram(z_po, i, _year, pred[1])
                        if data: 
                            
                            if data ==1:
                                data = 0
                            _.append(data)
                        
                    if _:

                        try:
                            perviy_bar = _[0]
                        except:
                            perviy_bar =  0

                        try:
                            vtoroy_bar = _[1]
                        except:
                            vtoroy_bar =  0

                       
                        # sql_bd_copy.zapis_diagramma_1_2(pred[0], i +"."+_year, perviy_bar, vtoroy_bar)
                        print(pred[0], i +"."+_year, perviy_bar, vtoroy_bar)

def main_cherz_zvit(pred, _mes, _year):
    val = sql_bd_copy.baza_predpr(pred)
    
    _ = []
    for barier, z_po in enumerate(val[7:9]):
        
        if not z_po:
            z_po="100000"
            
        data = dannie_po_barieram(z_po, _mes, _year, pred)
        if data: 
            
            if data ==1:
                data = 0
            _.append(data)
        
    if _:

        try:
            perviy_bar = _[0]
        except:
            perviy_bar =  0

        try:
            vtoroy_bar = _[1]
        except:
            vtoroy_bar =  0

        
        sql_bd_copy.zapis_diagramma_1_2(val[0], str(_mes) +"."+_year, perviy_bar, vtoroy_bar)
        
    

    

    # # Преобразуем в DataFrame
    # df = pd.DataFrame(_list, columns=["Месяц", "Поедаемость"])

    # # Отображаем столбчатую диаграмму
    # st.bar_chart(df.set_index("Месяц"))

if __name__ == "__main__":

    # val = sql.baza_predpr("ТОВ УКРЕЛЕВАТОРПРОМ І-ДІЛЯНКА")
    # print(val[7:9])
    # print(dannie_po_barieram("", "03", "2024","ТОВ УКРЕЛЕВАТОРПРОМ І-ДІЛЯНКА"))
    main_cherz_zvit("ТОВ УКРЕЛЕВАТОРПРОМ І-ДІЛЯНКА", "02", "2025" )
                