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
    cursor.execute(f"""SELECT login, password FROM `authentication` WHERE authentication.login = '{login}' """)
    row = cursor.fetchall()

    if  not row:
        return False
    return row[0]



if __name__ == "__main__":

    show_login()