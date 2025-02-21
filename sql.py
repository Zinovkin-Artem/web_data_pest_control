import pymysql
pymysql.install_as_MySQLdb()

from datetime import datetime
# from decimal import Decimal


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




# подключение и отключение к бд
def connection_bd():
    try:
        conn = MySQLdb.connect(
            host = "dezeltor.mysql.tools",
            user = "dezeltor_pestcontrol",
            password = "lala280508",
            database= "dezeltor_pestcontrol",
        )


        # conn = MySQLdb.connect(
        #     host = "195.138.73.12",
        #     port = 3306,
        #     user = "user1",
        #     password = "lala280508",
        #     database = "dez",
        # )

        return conn

    except MySQLdb.OperationalError:
        pass


# показать из таблицы авторизации
def show_login(login):
    conn = connection_bd()
    cursor = conn.cursor()
    cursor.execute(f"""SELECT login, password, enterprise FROM `authentication` WHERE authentication.login = '{login}' """)
    row = cursor.fetchall()

    if  not row:
        return False
    
    return row[0]

# получаем id из таблицы предприятий
def receive_id(request):
    conn = connection_bd()
    cursor = conn.cursor()
    cursor.execute(request)
    try:
        return cursor.fetchall()[0][0]
    except:
        return False

# получение данных из БД таблица skan_dk для формирования чек-листа
def value_from_db_for_cheklist(_month, _year, _barier, _predpr):
    conn = connection_bd()
    cursor = conn.cursor()

    _idbaza_pidpriemstv = receive_id(
        f"""SELECT  idbaza_pidpriemstv FROM baza_pidpriemstv WHERE  nazva_pidriemstva =
         "{_predpr}" """
    )

    namber = []
    month_list = set()
    value = []

    cursor.execute(
        f"""SELECT scan_dk.value_dk, DAY(time), MONTH(time),YEAR(time), baza_obladnanya.number_obladnanya
                     FROM scan_dk JOIN baza_obladnanya
                     ON scan_dk.idbaza_obladnanya = baza_obladnanya.idbaza_obladnanya 
                     WHERE MONTH(time) = '{_month}' AND YEAR(time) = '{_year}' AND baza_obladnanya.barier = '{_barier}' 
                     AND scan_dk.idbaza_pidpriemstv = {_idbaza_pidpriemstv}  ORDER BY `scan_dk`.`idscan_dk` ASC
                    """
    )

    row = cursor.fetchall()

    for value_dk, day, month, year, number in row:
        namber.append(str(day).zfill(2))
        month_list.add(str(month).zfill(2))

    namber = sorted(list(set(namber)))

    for i in namber:
        value_test = []
        value_test.clear()
        test_dict = {}
        test_dict.clear()
        cursor.execute(
            f"""SELECT scan_dk.value_dk, time, baza_obladnanya.number_obladnanya, spesialisti.surnames
                     FROM scan_dk JOIN baza_obladnanya
                     ON scan_dk.idbaza_obladnanya = baza_obladnanya.idbaza_obladnanya 
                     JOIN spesialisti ON scan_dk.idspestalisti = spesialisti.idspesialisti
                     WHERE MONTH(time) = '{_month}' AND YEAR(time) = '{_year}' AND DAY(time) = '{i}'
                      AND baza_obladnanya.barier = '{_barier}' 
                     AND scan_dk.idbaza_pidpriemstv = {_idbaza_pidpriemstv}
                    """
        )
        row = cursor.fetchall()

        for value_dk, _time, number_dk, name in row:
            if value_dk.split("-")[0].lower().lstrip().find("м") != -1:
                value_dk = f"M-{value_dk.split('-')[1]}"

            if value_dk.split("-")[0].lower().lstrip().find("к") != -1:
                value_dk = f"K-{value_dk.split('-')[1]}"
            value_test.append(
                {str(number_dk): (value_dk, (str(_time).split(" ")[1], name))}
            )

        for _ in value_test:
            test_dict.update(_)

        value.append(test_dict)
       

    conn.close()

    
    
    return namber, str(*month_list), value

#выдает все предприятия если вошел админ
def show_login_admin():
    spisok_predpr = ""
    conn = connection_bd()
    cursor = conn.cursor()
    cursor.execute(f"""SELECT enterprise FROM `authentication` """)
    row = cursor.fetchall()
 
    if not row:
        return False
  
    for i in row:
        if i[0]:
            spisok_predpr += f"{i[0]},"  # Тут виправлено
      

    spisok_predpr = spisok_predpr.rstrip(',')
    
    return spisok_predpr 



# из таблицы подпись данных берем данные для подписи номеров контэйнеов


def podpis_danix(_predpr):
    conn = connection_bd()
    cursor = conn.cursor()
    _idbaza_pidpriemstv = receive_id(
        f"""SELECT  idbaza_pidpriemstv FROM baza_pidpriemstv WHERE  nazva_pidriemstva =
            "{_predpr}" """
    )
    cursor.execute(
        f"""SELECT numbers_cont, coment, color, barier FROM podppis_danih
                WHERE idbaza_pidpriemstv= '{_idbaza_pidpriemstv}' """
    )
    row = cursor.fetchall()

    return row


#из таблицы база предприятий берем данные 
def baza_predpr(_predpr):
    
    conn = connection_bd()
    cursor = conn.cursor()
    _predpr = _predpr.replace("'", "''")
    cursor.execute(
        f""" SELECT * FROM `baza_pidpriemstv` WHERE `nazva_pidriemstva` = '{_predpr}' """
    )
    row = cursor.fetchall()
    
    return row[0]

#из таблицы база предприятий берем все предприятия и их id
def baza_vsex_predpr():
    
    conn = connection_bd()
    cursor = conn.cursor()
    
    
    cursor.execute(
        f""" SELECT idbaza_pidpriemstv, nazva_pidriemstva FROM `baza_pidpriemstv` """
    )
    row = cursor.fetchall()
    
        
    return row

#записываем в таблицу диаграмма 1-2барьер
import MySQLdb

def zapis_diagramma_1_2(_id_pid, _monse, _I_bar, _II_bar):
    conn = connection_bd()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            f"""
            INSERT INTO diagramma_1_2_barier (idbaza_pidpriemstv, monse, perviy_barier, vtoroy_barier)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                perviy_barier = VALUES(perviy_barier), 
                vtoroy_barier = VALUES(vtoroy_barier)
            """, 
            (_id_pid, _monse, _I_bar, _II_bar)
        )
        
        conn.commit()
    except MySQLdb.Error as e:
        print(f"Ошибка MySQL: {e}")
        return False
    finally:
        conn.close()
    
    return True



#из таблицы diagramma_1-2 берем данные для диаграммы

def dannie_iz_diagramma_1_2(_pred):

    conn = connection_bd()
    cursor = conn.cursor()

    cursor.execute(f"""SELECT monse, perviy_barier, vtoroy_barier  FROM diagramma_1_2_barier JOIN baza_pidpriemstv ON 
         diagramma_1_2_barier.idbaza_pidpriemstv = baza_pidpriemstv.idbaza_pidpriemstv  WHERE baza_pidpriemstv.nazva_pidriemstva = "{_pred}"  """
    )
    row = cursor.fetchall()
    # ✅ Сортировка списка по дате (преобразуем в datetime для корректного порядка)
    row_ = list(row)
    row_.sort(key=lambda x: datetime.strptime(x[0], "%m.%Y"))

    return tuple(row_)


#берем данные из таблици диаграмма только 3 барьер


def diagr_tretiy_how_mishi(_pred):
    trans_date = {
        "січень": 1, "лютий": 2, "березень": 3, "квітень": 4, "травень": 5, "червень": 6,
        "липень": 7, "серпень": 8, "вересень": 9, "жовтень": 10, "листопад": 11, "грудень": 12
    }

    conn = connection_bd()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT diagramma_time, poidannya, kilkist_grizuniv_za_misyac  
        FROM diagramma 
        JOIN baza_pidpriemstv 
        ON diagramma.idbaza_pidpriemstv = baza_pidpriemstv.idbaza_pidpriemstv  
        WHERE baza_pidpriemstv.nazva_pidriemstva = "{_pred}"
    """)

    row = cursor.fetchall()
    date = []

    for i_1, i_2, i_3 in row:
        _ = i_1.split(" ")
        formatted_date = f"{str(trans_date[_[0].lower()]).zfill(2)}.{_[1]}"
        date.append((formatted_date, i_2, i_3))

    # ✅ Сортировка списка по дате (преобразуем в datetime для корректного порядка)
    date.sort(key=lambda x: datetime.strptime(x[0], "%m.%Y"))
    
    return date

# берем данные из таблицы грызуны на територии
def dannie_iz_grizuni_na_territorii(_pred):
    conn = connection_bd()
    cursor = conn.cursor()
    

    cursor.execute(f"""
        SELECT DATE_FORMAT(time, '%m.%Y') as month, 
            CAST(SUM(CASE WHEN LOWER(vid_grizuna) LIKE 'миша' THEN kilkist ELSE 0 END) AS UNSIGNED) as total_misha,
            CAST(SUM(CASE WHEN LOWER(vid_grizuna) LIKE 'криса' THEN kilkist ELSE 0 END) AS UNSIGNED) as total_krisa
        FROM grizuni_na_territorii 
        JOIN baza_pidpriemstv 
        ON grizuni_na_territorii.idbaza_pidpriemstv = baza_pidpriemstv.idbaza_pidpriemstv  
        WHERE baza_pidpriemstv.nazva_pidriemstva = "{_pred}" 
        AND kilkist > 0
        GROUP BY month
        ORDER BY DATE_FORMAT(time, '%Y-%m')  -- Сортировка по полной дате (год-месяц)
    """)




    row = cursor.fetchall()
    return row


#достаем грызунов из живоловок по барьерам
def grizuni_v_givolovkax(_pred, z_po, barier):
    if barier == "I" or barier == "II":
        barier = "I - II"
    conn = connection_bd()
    cursor = conn.cursor()
    nugnie_dk = list_dk(z_po) 
    # Преобразуем список номеров контейнеров в кортеж
    nugnie_dk_tuple = tuple(map(str, nugnie_dk))

    sql_query = """
    SELECT 
        DATE_FORMAT(sd.time, '%%m.%%Y') AS month,  
        SUM(
            CASE 
                WHEN LOWER(TRIM(sd.value_dk)) REGEXP '^(м|миша|m)-[0-9]+$' 
                THEN CAST(SUBSTRING_INDEX(sd.value_dk, '-', -1) AS UNSIGNED) 
                ELSE 0 
            END
        ) AS mouse_count,
        SUM(
            CASE 
                WHEN LOWER(TRIM(sd.value_dk)) REGEXP '^(к|криса|k)-[0-9]+$' 
                THEN CAST(SUBSTRING_INDEX(sd.value_dk, '-', -1) AS UNSIGNED) 
                ELSE 0 
            END
        ) AS rat_count
    FROM 
        scan_dk sd
    JOIN 
        baza_pidpriemstv bp
        ON sd.idbaza_pidpriemstv = bp.idbaza_pidpriemstv  
    JOIN 
        baza_obladnanya bo
        ON sd.idbaza_obladnanya = bo.idbaza_obladnanya
    JOIN 
        (
            -- Выбираем самое последнее значение для каждого контейнера на каждую дату
            SELECT idbaza_obladnanya, MAX(time) AS latest_time
            FROM scan_dk
            GROUP BY idbaza_obladnanya, DATE_FORMAT(time, '%%Y-%%m-%%d')
        ) latest 
        ON sd.idbaza_obladnanya = latest.idbaza_obladnanya
        AND sd.time = latest.latest_time
    WHERE 
        bp.nazva_pidriemstva = %s
        AND bo.barier = %s
        AND bo.number_obladnanya IN %s
        AND sd.value_dk NOT IN ('НД', 'ІН', '--', 'I', '0')
    GROUP BY 
        month
    ORDER BY 
        STR_TO_DATE(month, '%%m.%%Y') ASC;
    """

    # Выполняем SQL-запрос
    cursor.execute(sql_query, (_pred, barier, nugnie_dk_tuple))
    row = cursor.fetchall()
    
    # Обрабатываем Decimal и None значения
    sorted_data = sorted(
        [(r[0], int(r[1] or 0), int(r[2] or 0)) for r in row], 
        key=lambda x: datetime.strptime(x[0], "%m.%Y")
    )

    result = tuple(sorted_data)
    
    return result


  # из таблицы подпись данных берем данные для подписи номеров контэйнеов
def podpis_danix_1(_predpr):
    conn = connection_bd()
    cursor = conn.cursor()
    
    sql_query = """
    SELECT numbers_cont, coment
    FROM podppis_danih 
    JOIN baza_pidpriemstv 
    ON podppis_danih.idbaza_pidpriemstv = baza_pidpriemstv.idbaza_pidpriemstv  
    WHERE baza_pidpriemstv.nazva_pidriemstva = %s 
    AND podppis_danih.barier = 'III'
"""

    cursor.execute(sql_query, (_predpr,))

    row = cursor.fetchall()
    data = [(list_dk(i[0]), i[1]) for i in row]
    
    return data


















##########################################################################################3
# перевод даты в таймстам
def data_in_timestamp(_data):
    _timestamp = datetime.fromisoformat(_data).timestamp()
    return _timestamp


# подключение и отключение к бд
# def connection_bd():

#     conn = MySQLdb.connect(
#         "dezeltor.mysql.tools",
#         "dezeltor_pestcontrol",
#         "lala280508",
#         "dezeltor_pestcontrol",
#     )


    # conn = MySQLdb.connect(
    #     host = "195.138.73.12",
    #     port = 3306,
    #     user = "user1",
    #     password = "lala280508",
    #     database = "dez",
    # )

    return conn

    

# показать всех специалистов из бд
def show_specialists():
    conn = connection_bd()
    cursor = conn.cursor()
    cursor.execute(f"""SELECT * FROM `spesialisti`""")
    row = cursor.fetchall()
    return row


# показать все предприятия из бд
def show_pidpriemstvo():
    conn = connection_bd()
    cursor = conn.cursor()
    cursor.execute(f"""SELECT nazva_pidriemstva FROM baza_pidpriemstv""")
    row = cursor.fetchall()

    return row


# показать все предприятия из бд для таблицы в киви
def show_pidpriemstvo_1():
    conn = connection_bd()
    cursor = conn.cursor()
    cursor.execute(
        f"""SELECT nazva_pidriemstva, idbaza_pidpriemstv, vidpovidalniy_pidriemstva FROM baza_pidpriemstv"""
    )
    row = cursor.fetchall()
    return row


# добавить специалиста
def add_spesialist(name, surnemes):
    conn = connection_bd()
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"""INSERT INTO spesialisti (name, surnames) VALUES ('{name}','{surnemes}')"""
        )
    except MySQLdb.IntegrityError:
        return False
    conn.commit()
    conn.close()


# удалить специалиста
def del_spesialist(_id):
    conn = connection_bd()
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"""DELETE FROM `spesialisti` WHERE `spesialisti`.`idspesialisti` = {_id}"""
        )
    except MySQLdb.ProgrammingError:
        return False
    conn.commit()
    conn.close()


# получаем id из таблицы предприятий
def receive_id(request):
    conn = connection_bd()
    cursor = conn.cursor()
    cursor.execute(request)
    try:
        return cursor.fetchall()[0][0]
    except:
        return False


# получаем из бд ответственного и количество оборудования по барьерам
def _vidpovidalniy(predpr):
    conn = connection_bd()
    cursor = conn.cursor()
    cursor.execute(
        f"""SELECT vidpovidalniy_pidriemstva, kilkist_dk_1_2, kilkist_dk_3
                        FROM baza_pidpriemstv WHERE nazva_pidriemstva = "{predpr}" """
    )
    row = cursor.fetchall()

    return row[0]


# Запись штрих кодов  с всеми данными в БД


def zapis_barcode(_barcode, _number_obladnanya, _barier, cod_pidpriemstva, _typy_dk):
    conn = connection_bd()
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"""INSERT INTO baza_obladnanya (barcode_obladnanya, number_obladnanya,barier,
        idbaza_pidpriemstv, type_dk ) VALUES ('{_barcode}', '{_number_obladnanya}', '{_barier}',
        '{cod_pidpriemstva}', '{_typy_dk}')"""
        )

        conn.commit()
        conn.close()
    except:
        pass


# получаем информацию из таблицы база обладнання для создания txt файла со штрихкодами
def barcode_in_txt(_predpr, barier, number:list):
    conn = connection_bd()
    cursor = conn.cursor()
    data = []
    

    
    _idbaza_pidpriemstv = receive_id(
        f"""SELECT  idbaza_pidpriemstv FROM baza_pidpriemstv WHERE  nazva_pidriemstva =
         "{_predpr}" """
    )
    
    if barier == "ВСІ" and len(number) == 0:
            cursor.execute(
                    f"""SELECT barcode_obladnanya, number_obladnanya
                                        FROM baza_obladnanya WHERE idbaza_pidpriemstv = "{_idbaza_pidpriemstv}"     
                            """
                )
            row = cursor.fetchall()
                
            for j in row:
                data.append(j)
                
            return tuple(data) 
            
    elif barier != "ВСІ" and len(number) == 0:
            cursor.execute(
                    f"""SELECT barcode_obladnanya, number_obladnanya
                                                FROM baza_obladnanya WHERE idbaza_pidpriemstv = "{_idbaza_pidpriemstv}" AND 
                                            barier = '{barier}' 
                                    """
                )
            row = cursor.fetchall()
                
            for j in row:
                data.append(j)
                
            return tuple(data)
            
    else:
        for i in number:
            
            if barier == "ВСІ":
                cursor.execute(
                f"""SELECT barcode_obladnanya, number_obladnanya
                                    FROM baza_obladnanya WHERE idbaza_pidpriemstv = "{_idbaza_pidpriemstv}" 
                                    AND  number_obladnanya = {i}    
                        """
            )
                    
            else:
                cursor.execute(
                    f"""SELECT barcode_obladnanya, number_obladnanya
                                                FROM baza_obladnanya WHERE idbaza_pidpriemstv = "{_idbaza_pidpriemstv}" AND 
                                            barier = '{barier}' AND  number_obladnanya = {i} 
                                    """
                )
            
            row = cursor.fetchall()
            for j in row:
                data.append(j)
                
        return tuple(data)


# запись предприятия в базу данных
def zapis_pidpriemstva(
    _nazva_pidriemstva, _vidpovidalniy_pidriemstva, _kilkist_dk_1_2, _kilkist_dk_3
):
    conn = connection_bd()
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"""INSERT INTO baza_pidpriemstv (nazva_pidriemstva, vidpovidalniy_pidriemstva,
                                                        kilkist_dk_1_2, kilkist_dk_3)
                                                        VALUES ('{_nazva_pidriemstva}','{_vidpovidalniy_pidriemstva}',
                                                        '{_kilkist_dk_1_2}', '{_kilkist_dk_3}')"""
        )
    except MySQLdb.IntegrityError:
        return False
    conn.commit()
    conn.close()


# запись данных введенных в ручную в таблицу scan_dk и grizuni_na_territorii
def write_scan_dk(
    _predpr, _diction, _krisi_teritori, _mishi_teritori, _combo_month, _baryer
):
    dk_false = []
    krisi_teritori = ("Криса", _krisi_teritori)
    mishi_teritori = ("Миша", _mishi_teritori)

    conn = connection_bd()
    cursor = conn.cursor()

    _idbaza_pidpriemstv = receive_id(
        f"""SELECT  idbaza_pidpriemstv FROM baza_pidpriemstv WHERE  nazva_pidriemstva =
     "{_predpr}" """
    )

    # запись в табл грызуни на территории

    for i in [krisi_teritori, mishi_teritori]:
        cursor.execute(
            f"""INSERT INTO grizuni_na_territorii (vid_grizuna, kilkist, idbaza_pidpriemstv, time) 
                            VALUES ('{i[0]}','{i[1]}','{_idbaza_pidpriemstv}', STR_TO_DATE('{_combo_month}',
                             '%d-%m-%Y'))"""
        )

    for number_dk, value_dk in _diction.items():
        if value_dk == "":
            pass
        else:
            _idbaza_obladnanya = receive_id(
                f"""SELECT  idbaza_obladnanya FROM baza_obladnanya
                        WHERE  number_obladnanya = '{number_dk}' AND idbaza_pidpriemstv ='{_idbaza_pidpriemstv}' 
                        AND barier ='{_baryer}' """
            )

            try:
                cursor.execute(
                    f"""INSERT INTO scan_dk (time, value_dk, idbaza_obladnanya, idbaza_pidpriemstv, idspestalisti) 
                                            VALUES (STR_TO_DATE('{_combo_month}','%d-%m-%Y'),'{value_dk}','{_idbaza_obladnanya}',
                                            '{_idbaza_pidpriemstv}', '1')"""
                )
            except MySQLdb.IntegrityError:
                dk_false.append(number_dk)

    conn.commit()

    conn.close()

    return dk_false


# получение данных из БД таблица skan_dk для формирования чек-листа
def value_from_db_for_cheklist(_month, _year, _barier, _predpr):
    
    conn = connection_bd()
    cursor = conn.cursor()

    _idbaza_pidpriemstv = receive_id(
        f"""SELECT  idbaza_pidpriemstv FROM baza_pidpriemstv WHERE  nazva_pidriemstva =
         "{_predpr}" """
    )
    

    namber = []
    month_list = set()
    value = []

    cursor.execute(
        f"""SELECT scan_dk.value_dk, DAY(time), MONTH(time),YEAR(time), baza_obladnanya.number_obladnanya
                     FROM scan_dk JOIN baza_obladnanya
                     ON scan_dk.idbaza_obladnanya = baza_obladnanya.idbaza_obladnanya 
                     WHERE MONTH(time) = '{_month}' AND YEAR(time) = '{_year}' AND baza_obladnanya.barier = '{_barier}' 
                     AND scan_dk.idbaza_pidpriemstv = {_idbaza_pidpriemstv}  ORDER BY `scan_dk`.`idscan_dk` ASC
                    """
    )

    row = cursor.fetchall()

    for value_dk, day, month, year, number in row:
        namber.append(str(day).zfill(2))
        month_list.add(str(month).zfill(2))

    namber = sorted(list(set(namber)))

    for i in namber:
        value_test = []
        value_test.clear()
        test_dict = {}
        test_dict.clear()
        cursor.execute(
            f"""SELECT scan_dk.value_dk, time, baza_obladnanya.number_obladnanya, spesialisti.surnames
                     FROM scan_dk JOIN baza_obladnanya
                     ON scan_dk.idbaza_obladnanya = baza_obladnanya.idbaza_obladnanya 
                     JOIN spesialisti ON scan_dk.idspestalisti = spesialisti.idspesialisti
                     WHERE MONTH(time) = '{_month}' AND YEAR(time) = '{_year}' AND DAY(time) = '{i}'
                      AND baza_obladnanya.barier = '{_barier}' 
                     AND scan_dk.idbaza_pidpriemstv = {_idbaza_pidpriemstv}
                    """
        )
        row = cursor.fetchall()

        for value_dk, _time, number_dk, name in row:
            if value_dk.split("-")[0].lower().lstrip().find("м") != -1:
                value_dk = f"M-{value_dk.split('-')[1]}"

            if value_dk.split("-")[0].lower().lstrip().find("к") != -1:
                value_dk = f"K-{value_dk.split('-')[1]}"
            value_test.append(
                {str(number_dk): (value_dk, (str(_time).split(" ")[1], name))}
            )

        for _ in value_test:
            test_dict.update(_)

        value.append(test_dict)
        

    conn.close()
    
    return namber, month_list, value


# получение данных из БД таблица грызуны на территории для формирования чек-листа и сразу считает обшее количество для
#  отчета


def value_from_db_grizuni_for_cheklist(_month, _year, _predpr):
    conn = connection_bd()
    cursor = conn.cursor()

    _idbaza_pidpriemstv = receive_id(
        f"""SELECT  idbaza_pidpriemstv FROM baza_pidpriemstv WHERE  nazva_pidriemstva =
            "{_predpr}" """
    )
    date = []
    cursor.execute(
        f"""SELECT  DAY(time) FROM grizuni_na_territorii
                         WHERE MONTH(time) = '{_month}' AND YEAR(time) = '{_year}' 
                         AND idbaza_pidpriemstv = '{_idbaza_pidpriemstv}' """
    )
    row = cursor.fetchall()
    for i in row:
        date.append(i[0])

    date = sorted(list(set(date)))
    value = {}
    kris_za_mes = 0
    mish_za_mes = 0

    for i in date:
        krisa = 0
        misha = 0

        cursor.execute(
            f"""SELECT  vid_grizuna, kilkist FROM grizuni_na_territorii
                             WHERE MONTH(time) = '{_month}' AND YEAR(time) = '{_year}'  AND DAY(time) = '{i}'
                             AND idbaza_pidpriemstv = '{_idbaza_pidpriemstv}' """
        )
        row = cursor.fetchall()

        for j in row:

            if j[0].lower().lstrip() == "миша":
                misha += int(j[1])
            if j[0].lower().lstrip() == "криса":
                krisa += int(j[1])
        kris_za_mes += krisa
        mish_za_mes += misha
        value[str(i).zfill(2)] = f"K-{krisa},M-{misha}"
    conn.close()
    vsego_grizunov_za_mes = [["M-", mish_za_mes], ["K-", kris_za_mes]]

    return value, vsego_grizunov_za_mes


# получение данных из БД таблица skan_dk для формирования отчета
def value_from_db_for_zvit(_month, _year, _predpr):
    conn = connection_bd()
    cursor = conn.cursor()

    _idbaza_pidpriemstv = receive_id(
        f"""SELECT  idbaza_pidpriemstv FROM baza_pidpriemstv WHERE  nazva_pidriemstva =
         "{_predpr}" """
    )

    _bariers = ["I - II", "III"]
    date = []
    value_I_II = []
    value_III = []

    _month = [str(_month).zfill(2)]

    cursor.execute(
        f"""SELECT  DAY(time) FROM scan_dk
                         WHERE MONTH(time) = '{_month[0]}' AND YEAR(time) = '{_year}'
                         AND idbaza_pidpriemstv = '{_idbaza_pidpriemstv}' """
    )
    row = cursor.fetchall()

    for i in row:
        date.append(str(i[0]).zfill(2))

    date = sorted(list(set(date)))

    for _barier in _bariers:
        for i in date:
            value_test = []
            # value_test.clear()
            test_dict = {}
            # test_dict.clear()

            cursor.execute(
                f"""SELECT scan_dk.value_dk, baza_obladnanya.number_obladnanya,
                    baza_obladnanya.barier, baza_obladnanya.idbaza_pidpriemstv
                    FROM scan_dk JOIN baza_obladnanya
                    ON scan_dk.idbaza_obladnanya = baza_obladnanya.idbaza_obladnanya
                    WHERE MONTH(time) = '{_month[0]}' AND YEAR(time) = '{_year}' AND DAY(time) = '{i}' 
                    AND baza_obladnanya.barier = '{_barier}'
                     AND baza_obladnanya.idbaza_pidpriemstv = '{_idbaza_pidpriemstv}'
                      ORDER BY `scan_dk`.`idscan_dk` ASC """
            )
            row = cursor.fetchall()

            for value_dk, number_dk, *args in row:
                if value_dk.split("-")[0] == " миша" and _barier == "I - II":
                    value_dk = f"М-{value_dk.split('-')[1]}"
                if value_dk.split("-")[0] == " криса" and _barier == "I - II":
                    value_dk = f"К-{value_dk.split('-')[1]}"
                value_test.append({str(number_dk): value_dk})

            for _ in value_test:
                test_dict.update(_)

            if _barier == "I - II":
                value_I_II.append({str(i): test_dict})
            else:

                value_III.append({str(i): test_dict})
    conn.close()

    return date, _month, value_I_II, value_III


# достает из бд количество контейнеров по первому второму барьеру
def count_dk_1_2(_pidpr):
    conn = connection_bd()
    cursor = conn.cursor()
    cursor.execute(
        f"""SELECT kilkist_dk_1_2 FROM baza_pidpriemstv WHERE nazva_pidriemstva = "{_pidpr}" """
    )

    row = cursor.fetchall()
    conn.close()

    return row[0][0]


# достает из бд количество контейнеров по третьему барьеру


def count_dk_3(_pidpr):
    conn = connection_bd()
    cursor = conn.cursor()

    cursor.execute(
        f"""SELECT kilkist_dk_3 FROM baza_pidpriemstv WHERE nazva_pidriemstva = "{_pidpr}" """
    )

    row = cursor.fetchall()
    conn.close()

    return row[0][0]


# готовим данные для диаграммы
def value_diagramma(poedaemoct, kolichestvo_grizunov, pidpriemstvo, date):
    conn = connection_bd()
    cursor = conn.cursor()
    _idbaza_pidpriemstv = receive_id(
        f"""SELECT  idbaza_pidpriemstv FROM baza_pidpriemstv WHERE  nazva_pidriemstva =
            "{pidpriemstvo}" """
    )

    test = 0
    id_flag = False
    _id = 0
    while test != 1:

        try:
            if not id_flag:
                cursor.execute(
                    f"""INSERT INTO diagramma ( idbaza_pidpriemstv, diagramma_time, poidannya,
                                        kilkist_grizuniv_za_misyac)
                                     VALUES ('{_idbaza_pidpriemstv}', '{date}','{poedaemoct}','{kolichestvo_grizunov}') """
                )
                conn.commit()
                test += 1
            else:
                cursor.execute(
                    f"""INSERT INTO diagramma (iddiagramma, idbaza_pidpriemstv, diagramma_time, poidannya,
                                                        kilkist_grizuniv_za_misyac)
                                                     VALUES ('{_id[0][0]}', '{_idbaza_pidpriemstv}',
                                                      '{date}','{poedaemoct}','{kolichestvo_grizunov}') """
                )
                conn.commit()
                test += 1

        except MySQLdb.IntegrityError:
            cursor.execute(
                f"""SELECT iddiagramma FROM diagramma WHERE idbaza_pidpriemstv = '{_idbaza_pidpriemstv}' AND
                                                        diagramma_time = '{date}'"""
            )
            _id = cursor.fetchall()
            id_flag = True

            cursor.execute(
                f"""DELETE FROM diagramma WHERE idbaza_pidpriemstv = '{_idbaza_pidpriemstv}' AND
                                            diagramma_time = '{date}'"""
            )

            conn.commit()

    cursor.execute(
        f"""SELECT diagramma_time, poidannya, kilkist_grizuniv_za_misyac FROM `diagramma`
                    WHERE idbaza_pidpriemstv= '{_idbaza_pidpriemstv}' ORDER BY `diagramma`.`iddiagramma` ASC """
    )

    diagramma = []
    row = cursor.fetchall()
    date_for_index = (
        []
    )  # в этот список добавится кортеж по которому мы узнаем индекс с которого нужно начать строить диаграмму
    # (row.index(('Квітень 2023', 0.0, 6)), "8888888888")

    for i in row:
        if date in i:
            date_for_index.append(row.index(i))
        diagramma.append({i[0]: [i[1], i[2]]})

    diagramma = diagramma[date_for_index[0] :: -1]
    if len(diagramma) < 12:
        pass
    else:
        diagramma = diagramma[0:12]
   
    return diagramma


# получаем данные для тайминга контейнеров
def timing_dk(_predpr, _month, _year):

    value_time_dk_1 = {}
    value_time_dk_3 = {}
    conn = connection_bd()
    cursor = conn.cursor()
    _idbaza_pidpriemstv = receive_id(
        f"""SELECT  idbaza_pidpriemstv FROM baza_pidpriemstv WHERE  nazva_pidriemstva =
               "{_predpr}" """
    )

    cursor.execute(
        f"""SELECT scan_dk.time, baza_obladnanya.number_obladnanya, baza_obladnanya.barier,  
                        spesialisti.surnames
                        FROM scan_dk JOIN baza_obladnanya JOIN  spesialisti
                        ON scan_dk.idbaza_obladnanya = baza_obladnanya.idbaza_obladnanya
                        AND scan_dk.idspestalisti = spesialisti.idspesialisti
                        WHERE MONTH(time) = '{_month.split('-')[0]}' AND YEAR(time) = '{_year}'
                         AND baza_obladnanya.idbaza_pidpriemstv = '{_idbaza_pidpriemstv}'
                          ORDER BY `scan_dk`.`idscan_dk` ASC """
    )
    row = cursor.fetchall()
    row = sorted(row)

    for i in row:
        if i[2] == "I - II":
            value_time_dk_1[(str(i[0].day).zfill(2), i[1], i[2])] = (str(i[0]), i[3])

        elif i[2] == "III":
            value_time_dk_3[(str(i[0].day).zfill(2), i[1], i[2])] = (str(i[0]), i[3])

    # return sorted(value_time_dk_1.items()), sorted(value_time_dk_3.items())

    return value_time_dk_1, value_time_dk_3

    # из таблицы подпись данных берем данные для подписи номеров контэйнеов


# def podpis_danix(_predpr):
#     conn = connection_bd()
#     cursor = conn.cursor()
#     _idbaza_pidpriemstv = receive_id(
#         f"""SELECT  idbaza_pidpriemstv FROM baza_pidpriemstv WHERE  nazva_pidriemstva =
#             "{_predpr}" """
#     )
#     cursor.execute(
#         f"""SELECT numbers_cont, coment, color, barier FROM podppis_danih
#                 WHERE idbaza_pidpriemstv= '{_idbaza_pidpriemstv}' """
#     )
#     row = cursor.fetchall()

#     return row


# пишем в таблицу подпись данных введенные данные
def zapis_v_podpis_dannix(_predpr, namb_cont, coment, barier, color):
    conn = connection_bd()
    cursor = conn.cursor()
    _idbaza_pidpriemstv = receive_id(
        f"""SELECT  idbaza_pidpriemstv FROM baza_pidpriemstv WHERE  nazva_pidriemstva =
            "{_predpr}" """
    )

    try:
        cursor.execute(
            f"""INSERT INTO podppis_danih (numbers_cont, coment,color,idbaza_pidpriemstv,barier) 
            VALUES ('{namb_cont}', "{coment}", '{color}', '{_idbaza_pidpriemstv}', '{barier}')"""
        )
    except MySQLdb.IntegrityError:
        return False

    conn.commit()

    conn.close()


# обновляем в таблицу подпись данных введенные данные


def zmini_v_podpis_dannix(_predpr, namb_cont, coment: str, barier, color, _id):
    conn = connection_bd()
    cursor = conn.cursor()
    _idbaza_pidpriemstv = receive_id(
        f"""SELECT  idbaza_pidpriemstv FROM baza_pidpriemstv WHERE  nazva_pidriemstva =
            "{_predpr}" """
    )

    try:
        coment = coment.replace("'", "''")

        cursor.execute(
            f""" UPDATE podppis_danih SET 
                       numbers_cont ='{namb_cont}',
                         coment ='{coment.strip()}',
                         color ='{color}', idbaza_pidpriemstv = '{_idbaza_pidpriemstv}', barier = "{barier}" WHERE idpodpis_danih = '{_id}' """
        )
    except MySQLdb.IntegrityError:
        return False

    conn.commit()

    conn.close()


# из таблицы подпись данных берем все данные  для таблицы


def podpis_danix_tabl():
    conn = connection_bd()
    cursor = conn.cursor()

    cursor.execute(
        f"""SELECT idpodpis_danih,numbers_cont, coment, color, nazva_pidriemstva, barier FROM podppis_danih JOIN baza_pidpriemstv
          ON podppis_danih.idbaza_pidpriemstv = baza_pidpriemstv.idbaza_pidpriemstv"""
    )
    row = cursor.fetchall()
    return row


# из таблицы подпись данных удаляем данные


def del_podpis_danix_tabl(_id):
    conn = connection_bd()
    cursor = conn.cursor()

    cursor.execute(f"""DELETE FROM `podppis_danih` WHERE `idpodpis_danih` = '{_id}' """)
    conn.commit()


# выводим данные из таблицы ckan_dk
def ckan_dk_tabl(_predpr, _data, data_1, _barier, _number_dk):
    
    conn = connection_bd()
    cursor = conn.cursor()
    data_1 += datetime.timedelta(days=1)
    a = "0"
    b = "0"
    c = "0"
    _kay = ""
    if _predpr:
        a = "1"
    if _barier:
        c = "1"
    if _number_dk:
        b = "1"
    
    _kay = a + b + c

    if len (_number_dk) ==1:
        _number_dk = tuple((_number_dk[0], 1000000))
        
    
    _sql_zapros = {
      
        
        "000": f"""SELECT idscan_dk,time,  nazva_pidriemstva,number_obladnanya,value_dk, barier FROM scan_dk 
                JOIN baza_pidpriemstv ON scan_dk.idbaza_pidpriemstv = baza_pidpriemstv.idbaza_pidpriemstv 
                JOIN baza_obladnanya ON scan_dk.idbaza_obladnanya =  baza_obladnanya.idbaza_obladnanya
                WHERE scan_dk.time  BETWEEN   '{_data}' AND   '{data_1}' ORDER BY time ASC, number_obladnanya, number_obladnanya """,

        "001": f"""SELECT idscan_dk,time,  nazva_pidriemstva,number_obladnanya,value_dk, barier FROM scan_dk 
                JOIN baza_pidpriemstv ON scan_dk.idbaza_pidpriemstv = baza_pidpriemstv.idbaza_pidpriemstv 
                JOIN baza_obladnanya ON scan_dk.idbaza_obladnanya =  baza_obladnanya.idbaza_obladnanya
                WHERE  baza_obladnanya.barier =  '{_barier}' AND   scan_dk.time  BETWEEN   '{_data}' AND   '{data_1}'ORDER BY time ASC, number_obladnanya, number_obladnanya """,

        "100": f"""SELECT idscan_dk,time, nazva_pidriemstva,number_obladnanya, value_dk, barier FROM scan_dk JOIN baza_pidpriemstv
             ON scan_dk.idbaza_pidpriemstv = baza_pidpriemstv.idbaza_pidpriemstv JOIN baza_obladnanya ON scan_dk.idbaza_obladnanya =    baza_obladnanya.idbaza_obladnanya
               WHERE scan_dk.time  BETWEEN   '{_data}' AND   '{data_1}' AND baza_pidpriemstv.nazva_pidriemstva = "{_predpr}"ORDER BY time ASC, number_obladnanya, number_obladnanya """,

        "101": f"""SELECT idscan_dk,time,  nazva_pidriemstva,number_obladnanya,value_dk, barier FROM scan_dk JOIN baza_pidpriemstv ON 
        scan_dk.idbaza_pidpriemstv = baza_pidpriemstv.idbaza_pidpriemstv    JOIN baza_obladnanya ON scan_dk.idbaza_obladnanya =  baza_obladnanya.idbaza_obladnanya
                WHERE baza_pidpriemstv.nazva_pidriemstva = "{_predpr}" AND  baza_obladnanya.barier =  '{_barier}' AND scan_dk.time  BETWEEN   '{_data}' AND   '{data_1}' ORDER BY time ASC, number_obladnanya, number_obladnanya """,

        "010": f"""SELECT idscan_dk,time,  nazva_pidriemstva,number_obladnanya,value_dk, barier FROM scan_dk JOIN baza_pidpriemstv ON 
        scan_dk.idbaza_pidpriemstv = baza_pidpriemstv.idbaza_pidpriemstv JOIN baza_obladnanya ON scan_dk.idbaza_obladnanya =  baza_obladnanya.idbaza_obladnanya WHERE baza_obladnanya.number_obladnanya in {_number_dk}   AND scan_dk.time  BETWEEN   '{_data}' AND   '{data_1}'  ORDER BY time ASC, number_obladnanya """, 

        "011": f"""SELECT idscan_dk,time,  nazva_pidriemstva,number_obladnanya,value_dk, barier FROM scan_dk JOIN baza_pidpriemstv ON 
        scan_dk.idbaza_pidpriemstv = baza_pidpriemstv.idbaza_pidpriemstv JOIN baza_obladnanya ON scan_dk.idbaza_obladnanya =  baza_obladnanya.idbaza_obladnanya WHERE baza_obladnanya.number_obladnanya in {_number_dk}  AND  baza_obladnanya.barier =  '{_barier}' AND scan_dk.time  BETWEEN   '{_data}' AND   '{data_1}' ORDER BY time ASC, number_obladnanya""", 

        "110": f"""SELECT idscan_dk,time,  nazva_pidriemstva,number_obladnanya,value_dk, barier FROM scan_dk JOIN baza_pidpriemstv ON 
        scan_dk.idbaza_pidpriemstv = baza_pidpriemstv.idbaza_pidpriemstv JOIN baza_obladnanya ON scan_dk.idbaza_obladnanya =  baza_obladnanya.idbaza_obladnanya WHERE baza_pidpriemstv.nazva_pidriemstva = "{_predpr}" AND baza_obladnanya.number_obladnanya in {_number_dk} AND scan_dk.time  BETWEEN   '{_data}' AND   '{data_1}' ORDER BY number_obladnanya ASC, time ASC """,

        "111": f"""SELECT idscan_dk,time,  nazva_pidriemstva,number_obladnanya,value_dk, barier FROM scan_dk JOIN baza_pidpriemstv ON 
        scan_dk.idbaza_pidpriemstv = baza_pidpriemstv.idbaza_pidpriemstv JOIN baza_obladnanya ON scan_dk.idbaza_obladnanya =  baza_obladnanya.idbaza_obladnanya WHERE baza_pidpriemstv.nazva_pidriemstva = "{_predpr}" AND baza_obladnanya.number_obladnanya in {_number_dk}  AND  baza_obladnanya.barier =  '{_barier}' AND scan_dk.time  BETWEEN   '{_data}' AND   '{data_1}' ORDER BY time ASC,number_obladnanya  """,
                  
    }

    cursor.execute(_sql_zapros[_kay])
    row = cursor.fetchall()

    return row


# удаляем данные из таблицы ckan_dk
def del_ckan_dk(_id):
    conn = connection_bd()
    cursor = conn.cursor()

    cursor.execute(f"""DELETE FROM `scan_dk` WHERE idscan_dk = {_id}""")
    conn.commit()


# из таблицы  authentication берем данные для таблицы уровень доступа
def riven_doctupa():
    conn = connection_bd()
    cursor = conn.cursor()

    cursor.execute(f"""SELECT * FROM `authentication` """)

    row = cursor.fetchall()
    return row


# удаляем данные из таблицы authentication
def del_riven_dostupa(_id):
    conn = connection_bd()
    cursor = conn.cursor()

    cursor.execute(f"""DELETE FROM `authentication` WHERE id_authentication = {_id}""")
    conn.commit()


# # вставляем данные в таблицу authentication
# def into_riven_dostupa(_log, _passw, _dostup, _predpr):
#     conn = connection_bd()
#     cursor = conn.cursor()
#     _predpr = _predpr.replace("'", "''")
#     try:
#         cursor.execute(
#             f"""INSERT INTO `authentication`(`login`, `password`, `access_level`, `enterprise`)
#             VALUES ('{_log}','{_passw}','{_dostup}','{_predpr}') """
#         )
#         conn.commit()
#         messagebox.showinfo("УВАГА", "ЗАПИСАНО!")
#     except MySQLdb.IntegrityError:
#         messagebox.showinfo("УВАГА", "Такий логін вже існує")
#         return False


# # обнавляем данные в таблице authentication:
# def update__authentication(_id, _log, _passw, _dostup, _predpr):
#     conn = connection_bd()
#     cursor = conn.cursor()
#     _predpr = _predpr.replace("'", "''") # делаем это для экранирования запятой в названии предприятия 
#     try:
#         cursor.execute(
#             f"""UPDATE `authentication` SET
#             `login`='{_log}',`password`='{_passw}',`access_level`='{_dostup}',`enterprise`='{_predpr}'
#                 WHERE `id_authentication` = '{_id}' """
#         )
#         conn.commit()
#         messagebox.showinfo("УВАГА", "ЗАПИСАНО!")
#     except MySQLdb.IntegrityError:
#         messagebox.showinfo("УВАГА", "Такий логін вже існує")
#         return False
    
# # добовляем предприятия в таблице authentication:
# def update__authentication_predpr(__id, _predpr):
#     conn = connection_bd()
#     cursor = conn.cursor()
     
    
#     cursor.execute(
#         f"""UPDATE `authentication` SET `enterprise`='{_predpr}' WHERE `id_authentication` = '{__id}' """
#     )
#     conn.commit()
#     messagebox.showinfo("УВАГА", "ЗАПИСАНО!")



# # из таблицы  authentication берем уровень доступа и предприятие
# def _authentication(_log, _passw):
#     conn = connection_bd()
#     cursor = conn.cursor()

#     cursor.execute(
#         f"""SELECT access_level, enterprise FROM `authentication`WHERE `login`='{_log}' AND `password` = '{_passw}'
#           """
#     )

#     row = cursor.fetchall()

#     if len(row) == 0:
#         messagebox.showinfo("УВАГА", "Данного користувача не існує")
#         return False

#     if row[0][0] == None:
#         messagebox.showinfo("УВАГА", "У вас не встановлен рівень доступу")
#         return False
#     return row[0]


# # регестрация в таблице аутентификации
# def reg_authentication(_log, _passw):
#     conn = connection_bd()
#     cursor = conn.cursor()
#     try:
#         cursor.execute(
#             f"""INSERT INTO authentication (login, password)VALUES ('{_log}','{_passw}')"""
#         )
#         conn.commit()
#         conn.close()
#         return True

#     except MySQLdb.IntegrityError:

#         messagebox.showinfo("УВАГА", "Такий логін вже існує")
#         return False
    
# выводим данные из таблицы грызуны на територии
def tabl_grizuni_na_terr(_predpr, date_1, date_2):
    conn = connection_bd()
    cursor = conn.cursor()
    date_2 += datetime.timedelta(days=1)

    cursor.execute( f"""SELECT idgrizuni_na_territorii,time, vid_grizuna,  kilkist,nazva_pidriemstva FROM grizuni_na_territorii JOIN baza_pidpriemstv ON 
        grizuni_na_territorii.idbaza_pidpriemstv = baza_pidpriemstv.idbaza_pidpriemstv WHERE baza_pidpriemstv.nazva_pidriemstva = "{_predpr}" AND grizuni_na_territorii.time  BETWEEN   '{date_1}' AND   '{date_2}' """)
    row = cursor.fetchall()

    return row


#удаляем данные из таблицы грызуны на територии
def del_grizuni_na_terr(_id):
    conn = connection_bd()
    cursor = conn.cursor()

    cursor.execute(f"""DELETE FROM `grizuni_na_territorii` WHERE idgrizuni_na_territorii = {_id}""")
    conn.commit()


# выводим данные из таблицы препараты
def preparati():
    conn = connection_bd()
    cursor = conn.cursor()

    cursor.execute(f"""SELECT * FROM `preperati` """)

    row = cursor.fetchall()
    return row

# выводим данные из таблицы препараты только тот который отечен yes
def preparat_yes():
    prep = preparati()
    for  i in prep:
        if i[3] == "yes":
            return i[1],i[2]
        

# удаляем данные из таблицы препараты
def del_preparati(_id):
    conn = connection_bd()
    cursor = conn.cursor()

    cursor.execute(f"""DELETE FROM `preperati` WHERE id_preparati = {_id}""")
    conn.commit()


# пишем в таблицу  препараты введенные данные
def zapis_v_preparati(_nazva, _termin,_yes_no):
    conn = connection_bd()
    cursor = conn.cursor()
    

   
    cursor.execute(
        f"""INSERT INTO `preperati`(`nazva_preparata`, `termin_pridatnosti`, `yes_or_no`) VALUES ('{_nazva}','{_termin}','{_yes_no}')"""
    )
    

    conn.commit()

    conn.close()

# изменяем в таблицу  препараты введенные данные
def zmini_v_preparati(_id, _nazva, _termin,_yes_no):
    conn = connection_bd()
    cursor = conn.cursor()
    

   
    cursor.execute(
        f"""UPDATE `preperati` SET `id_preparati`='{_id}',`nazva_preparata`='{_nazva}',`termin_pridatnosti`='{_termin}',`yes_or_no`='{_yes_no}' WHERE `id_preparati` = '{_id}' """
    )
    

    conn.commit()

    conn.close()