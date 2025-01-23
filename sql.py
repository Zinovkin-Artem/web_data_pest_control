import MySQLdb


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



if __name__ == "__main__":

    # value_from_db_for_cheklist( "06", "2024", "III", "ТОВ 'АДМ'")
    print(podpis_danix("ТОВ 'АДМ'"))