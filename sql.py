import MySQLdb
from datetime import datetime
# from decimal import Decimal
from chek_list import list_dk


# подключение и отключение к бд
def connection_bd():
    try:
        conn = MySQLdb.connect(
            "dezeltor.mysql.tools",
            "dezeltor_pestcontrol",
            "lala280508",
            "dezeltor_pestcontrol",
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
def podpis_danix(_predpr):
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

















if __name__ == "__main__":

    # value_from_db_for_cheklist( "06", "2024", "III", "ТОВ 'АДМ'")
    # print(baza_predpr("ТОВ 'АДМ'"))
    # show_login_admin()
    # print(baza_vsex_predpr())
    # grizuni_v_givolovkax("ТОВ 'АДМ'","1-73", 'I - II')
    nugnie_dk = list_dk("1-1000") # Номера контейнеров
    barier = "III"  # Фильтр по барьеру

    # grizuni_v_givolovkax("ТОВ 'АДМ'", "1-1000", barier)
    podpis_danix("ТОВ 'АДМ'")
