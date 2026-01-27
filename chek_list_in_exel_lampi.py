import streamlit as st
import xlsxwriter
import io
import math
import sql as bd
from format_color_pidpriemctv import Formatcolor
from datetime import datetime

class Chek_list_in_exel_lamp:
    MONTH_1 = {
        "01": "СІЧЕНЬ",
        "02": "ЛЮТИЙ",
        "03": "БЕРЕЗЕНЬ",
        "04": "КВІТЕНЬ",
        "05": "ТРАВЕНЬ",
        "06": "ЧЕРВЕНЬ",
        "07": "ЛИПЕНЬ",
        "08": "СЕРПЕНЬ",
        "09": "ВЕРЕСЕНЬ",
        "10": "ЖОВТЕНЬ",
        "11": "ЛИСТОПАД",
        "12": "ГРУДЕНЬ",
    }

    BARIER = {"I": "I - II", "II": "I - II", "III": "III"}

    def __init__(self, predp, barier, monse, year):
        self.predpr = predp
        self.barier = barier
        self.monse = monse
        self.year = year

        self.book = None
        self.s = None
        self.podpis_barier = Formatcolor()
        self.podpis = self.podpis_barier.format(self.predpr)

        
        


    def create_excel(self):
        """Создаёт и возвращает Excel-файл в виде байтов"""

        output = io.BytesIO()
        self.book = xlsxwriter.Workbook(output)
        self.s = self.book.add_worksheet()
        
        self.format_1 = self.book.add_format(
            {
                "border": 1,
                "font_size": 7,
                "font_name": "Arial",
                "align": "center",
                "valign": "vcenter",
                "bold": True,
                "text_wrap": True,
            }
        )
        self.format_1.set_shrink()
        self.format_2 = self.book.add_format(
            {
                "border": 2,
                "font_name": "Arial",
                "font_size": 12,
                "bold": True,
                "fg_color": "#D7E4BC",
                "align": "center",
                "valign": "vcenter",
                "text_wrap": True,
            }
        )
        self.format_2.set_shrink()
        self.format_3 = self.book.add_format(
            {
                "border": 2,
                "font_name": "Arial",
                "font_size": 6,
                "bold": False,
                "fg_color": "#D7E4BC",
                "align": "center",
                "valign": "vcenter",
                "text_wrap": True,
            }
        )
        self.format_3.set_shrink()
        self.format_4 = self.book.add_format(
            {
                "border": 1,
                "font_size": 8,
                "align": "center",
                "valign": "vcenter",
                "font_name": "Arial",
                "bold": True,
                "fg_color": "#D7E4BC",
                "text_wrap": None,
            }
        )
        self.format_4.set_shrink()
        self.format_5 = self.book.add_format(
            {
                "font_size": 7,
                "font_name": "Arial",
                "align": "center",
                "valign": "vcenter",
                "bold": True,
                "text_wrap": True,
            }
        )
        self.format_5.set_shrink()
        self.format_6 = self.book.add_format(
            {
                "font_size": 8,
                "font_name": "Arial",
                "align": "left",
                "valign": "vcenter",
                "bold": True,
                "text_wrap": True,
            }
        )
        self.format_6.set_shrink()
        self.format_7 = self.book.add_format(
            {
                "border": 1,
                "font_size": 8,
                "align": "center",
                "valign": "vcenter",
                "font_name": "Arial",
                "bold": True,
                "fg_color": "#D7E4BC",
            }
        )

        self.format_7.set_shrink()

        
        
        if self.barier == "I - II":
            text_grizuni = "загальна кількість гризунів на теріторії"
        elif self.barier == "III":
            text_grizuni = "загальна кількість відловлених гризунів"

        namber, month_list, value = bd.value_from_db_for_cheklist(
            _predpr=self.predpr,
            _year=self.year,
            _month=self.monse,
            _barier=self.barier,
        )
        

        if namber or value:
            numbers_cont = self.numb_conten(value)
            self.checklist_header()
            last_row = self.write_in_check_list(numbers_cont, namber, value)
            last_row = self.umovni_poznach(last_row)
            if self.barier == "I - II":
                d = bd.value_from_db_grizuni_for_cheklist(
                    _month=self.monse,
                    _predpr=self.predpr,
                    _year=self.year,
                )
                self.tabl_grizyni(
                    last_row,
                    2,
                    text_grizuni,
                    _data=namber,
                    _monse=self.monse,
                    value=d[0],
                )
            elif self.barier == "III":
                val = self.how_grizunov_III(namber, value)
                self.tabl_grizyni(
                    last_row,
                    2,
                    text_grizuni,
                    _data=namber,
                    _monse=self.monse,
                    value=val,
                )
            self.book.close()

        output.seek(0)
        return output.getvalue()

    def checklist_header(self):
        self.s.set_v_pagebreaks([31])
        self.s.set_h_pagebreaks([100])

        text = (
            f"Карта огляду інсектицидних ламп за \n"
            f"{self.MONTH_1[self.monse]} "
            f"{self.year} р. "
        )

        self.s.set_column(0, 100, 3)

        vidpovidalniy,how_lamp = bd._kilkict_lamp(self.predpr)

      

        log_1 = self.s.insert_image(
            0, 0, "логотип укр.png", {"x_scale": 0.25, "y_scale": 0.25}
        )
        self.s.merge_range(0, 0, 6, 4, log_1, self.format_2)
        self.s.merge_range(0, 5, 6, 19, text, self.format_2)
        self.s.merge_range(0,20, 9,30,
            f" загальна кількість  обладнання \n{how_lamp} шт. ",
            self.format_2,
        )
        if self.predpr == "ТОВ 'АДМ'":
            _predpr = "ПрАТ «АДМ ІЛЛІЧІВСЬК»"
        else:
            _predpr =  self.predpr

        # self.s.merge_range(6, 0, 6, 4, "Родетицид", self.format_3)
        # self.s.merge_range(6, 5, 6, 9, bd.preparat_yes()[0], self.format_3)
        # self.s.merge_range(6, 10, 6, 15, "придатний до", self.format_3)
        # self.s.merge_range(6, 16, 6, 19, bd.preparat_yes()[1], self.format_3)
        self.s.merge_range(7, 0, 7, 4, "Підприємство замовник", self.format_3)
        self.s.merge_range(7, 5, 7, 19, _predpr, self.format_3)
        self.s.merge_range(8, 0, 8, 4, "Дезінфектор", self.format_3)
        self.s.merge_range(9, 0, 9, 4, "Відповідальний", self.format_3)
        self.s.merge_range(8, 5, 8, 19, "Янчоглов Іван", self.format_3)
        self.s.merge_range(9, 5, 9, 19, vidpovidalniy, self.format_3)

        first_row = 11

    # получает из бд словарь с скнароваными значениями возвращает все номера сканированых
    # контейнеров без повторенний и по порядку
    def numb_conten(self, ckan_cont: list):

        nun_cont = []
        for i in ckan_cont:
            for j in list(i.keys()):
                if int(j) not in nun_cont:
                    nun_cont.append(int(j))

        return sorted(nun_cont)
    
    #  # получает из бд словарь с скнароваными значениями возвращает все номера сканированых
    # # контейнеров без повторенний и по порядку
    # def numb_conten(self, ckan_cont: list):

    #     nun_cont = []
    #     for i in ckan_cont:
    #         for j in list(i.keys()):
    #             if int(j) not in nun_cont:
    #                 nun_cont.append(int(j))

    #     return sorted(nun_cont)

    # рисует под таблицами условные обозначения
    def umovni_poznach(
        self,
        row,
    ):
        text_1 = (
            "Умовнi позначення: 0 - відсутність комах, "
            "Н - низька чисельність комах, С - середня чисельність комах,\nВ - висока чисельність комах"
        )
        self.s.merge_range(row, 0, row + 1, 26, text_1, self.format_6)  #добавил!!!!!!!!1
        # if row > 74:
        #     for i in (74, row):
        #         self.s.merge_range(i, 0, i + 1, 26, text_1, self.format_6)
        # else:
        #     self.s.merge_range(row, 0, row + 1, 26, text_1, self.format_6)
        return row + 1  # каким рядом закончилось

    # записывает данные в таблицу чек листа
    def write_in_check_list(self, _numbers_cont, _data: list, value):
        """_numbers_cont: список всех контейнеров без повторенний
        _data: список всех дат за запрошеный месяц
        value: значение из базы данных контейнер значение
        """

        row_start = 12  # с какого ряда стартовать таблице
        coll_start = 0
        count_row = 0
        count_coll = 0
        # расчет количества колонок в блоке
        how_coll_in_block = len(_data) + 1
        # расчет количества блоков в таблице
        how_block_in_tabl = math.trunc(31 / how_coll_in_block)
        
        # расчет количества строк в таблице
        how_row_in_tabl = math.ceil(len(_numbers_cont) / how_block_in_tabl)
        # количество грызунов в контэцнерах по 3 барьеру

        _data.insert(0, "№")

        #  рисует даты выходов в таблицу
        def dati_vixod_in_tabl(_row_start=row_start):
            count_coll = 0

            for j in range(0, how_block_in_tabl):
                # self.s.set_row(count_row + row_start - 1, 10)  # установка ширины строки
                for i in _data:
                    if i.isdigit():
                        i = f"{i}.{self.monse}"
                    self.s.write(_row_start - 1, count_coll, i, self.format_3)

                    count_coll += 1

        dati_vixod_in_tabl()

        count_coll = 0
        max_row = []  # сохраняет все номера рядо что бы вернуть максимальный

        for j in _numbers_cont:

            max_row.append(count_row + row_start)
            if count_row == how_row_in_tabl:
                coll_start += how_coll_in_block
                count_row = 0

            # if coll_start >= how_coll_in_block * how_block_in_tabl:

            #     dati_vixod_in_tabl(79)
            #     coll_start = 0
            #     row_start = 79
            #     how_row_in_tabl = math.ceil(
            #         len(_numbers_cont[_numbers_cont.index(j) :]) / how_block_in_tabl
            #     )

            # установка цвета и коментария к ячейке с номером контейнера

            if len(self.podpis) == 0:

                self.s.write(
                    count_row + row_start, coll_start + count_coll, j, self.format_3
                )
            else:

                for key, podpis in self.podpis.items():

                    if j in key and self.barier == self.BARIER[key[-1]]:
                        form_ = key[-2]

                        self.s.write_comment(
                            count_row + row_start,
                            coll_start + count_coll,
                            podpis,
                            {"x_scale": 0.8, "y_scale": 0.8},
                        )

                        format_ = self.podpis_barier.color(self.book, form_)
                        # запсь номера контэйнеров в таблицу
                        self.s.write(
                            count_row + row_start, coll_start + count_coll, j, format_
                        )
                        break
                    else:

                        # запсь номера контэйнеров в таблицу
                        self.s.write(
                            count_row + row_start,
                            coll_start + count_coll,
                            j,
                            self.format_3,
                        )

            self.s.set_row(count_row + row_start, 10)  # установка ширины строки

            for i in value:
                try:
                    _value: str = i[str(j)][0]  # значения контейнеров
                    _comment = (
                        f"{i[str(j)][1][0]}\n{i[str(j)][1][1]}"  # комментарий к ячейке
                    )
                    if _value.isdigit():
                        _value = int(_value)
                    elif _value.find("миша") != -1:
                        _value = f"M-{_value.split('-')[1]}"
                    elif _value.find("криса") != -1:
                        _value = f"K-{_value.split('-')[1]}"
                    # запись значений в таблицу

                    self.s.write(
                        count_row + row_start,
                        coll_start + count_coll + 1,
                        _value,
                        self.format_1,
                    )
                    self.s.write_comment(
                        count_row + row_start,
                        coll_start + count_coll + 1,
                        _comment,
                        {"x_scale": 0.5, "y_scale": 0.6},
                    )

                except KeyError:
                    pass

                count_coll += 1

            count_row += 1
            count_coll = 0

        return max(max_row)

    # считает количество грызунов по 3 барьеру
    def how_grizunov_III(self, _number, _value):
        count_numb = 1
        grizunov_za_mes = {}

        how_mish = 0
        how_kris = 0
        for j in _value:
            for n, f in j.items():
                if (
                    f[0].lower().lstrip().find("м") != -1
                    or f[0].lower().lstrip().find("m") != -1
                ):
                    how_mish += int(f[0].split("-")[1])
                elif (
                    f[0].lower().lstrip().find("к") != -1
                    or f[0].lower().lstrip().find("k") != -1
                ):
                    how_kris += int(f[0].split("-")[1])

            grizunov_za_mes[_number[count_numb]] = f"M-{how_mish},K-{how_kris}"
            count_numb += 1

            how_mish = 0
            how_kris = 0
        return grizunov_za_mes

    # рисует таблицу грызуны на территории
    def tabl_grizyni(self, _row, _coll, text, _data, _monse, value):
        
        self.s.merge_range(_row + 1, _coll, _row + 1, _coll + 7, text, self.format_5)
       

        # рисуем  таблицу грызуны на теритотии

        for i in _data[1:]:
           
            self.s.merge_range(
                _row + 1,
                _coll + 9,
                _row + 1,
                _coll + 10,
                f"{i}.{_monse}",
                self.format_1,
            )

            self.s.merge_range(
                _row + 2, _coll + 9, _row + 2, _coll + 10, value[i], self.format_1
            )
            _coll += 2


    def main(self):
        if "show_form" not in st.session_state:
            st.session_state["show_form"] = False

        # Кнопка для отображения/скрытия формы
        if st.button("📝 Генерація чек-листа", key="generate_checklist_lamp"):
            st.session_state["show_form"] = not st.session_state["show_form"]  # Инвертируем значение

        # Если кнопка нажата, показываем форму
        if st.session_state["show_form"]:
           

        # predp = "ТОВ 'М.В. КАРГО' ГОЛОВНА ТЕРІТОРІЯ"
        # barier = "I - II"
        # current_year = datetime.today().year
        
        # monse = st.selectbox("Місяць", ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"])
        # year = st.number_input("Оберіть рік", min_value=2000, max_value=2100, value=current_year, step=1)

        
            try:
                excel_data = Chek_list_in_exel_lamp(self.predpr, self.barier, self.monse, self.year).create_excel()
                if excel_data == b'':
                    st.warning("📭 Даних для звіту немає.")
                # Кнопка скачивания
                else:
                    st.download_button(
                        label="📥 Завантажити Excel",
                        data=excel_data,
                        file_name=f"чек-лист_{self.predpr}_{self.barier}_{self.monse}_{self.year}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    st.session_state["show_form"] = not st.session_state["show_form"]  # Инвертируем значение
            except Exception:
                    st.write(f"Щось пішло не так!!!")