import streamlit as st
from datetime import datetime
import math
# import os
# from tkinter import messagebox
import io

import xlsxwriter
from number_akti_in_zvit import stroka_dly_zvita

import sql as bd
from chek_list_in_exel_copy import Chek_list_in_exel
# from PestControl.format_color_adm import Formatadm
from format_color_pidpriemctv import Formatcolor
import time

class Zvit(Chek_list_in_exel):
    MES = {
        "12": "Грудень",
        "01": "Січень",
        "02": "Лютий",
        "03": "Березень",
        "04": "Квітень",
        "05": "Травень",
        "06": "Червень",
        "07": "Липень",
        "08": "Серпень",
        "09": "вересень",
        "10": "Жовтень",
        "11": "Листопад",
    }

    def __init__(self, _predpr, _month = None, _year = None):

        self._predpr = _predpr
        self._month = _month
        self._year = _year
        self.book = None
        self.s = None
        # self.book = xlsxwriter.Workbook(
        #     f"save zvit\\Звіт {self._predpr} {self._month}.xlsx"
        # )
        # self.s = self.book.add_worksheet("Звіт.xlsx")
        self.podpis_barier = Formatcolor()
        self.podpis = self.podpis_barier.format(self._predpr)

    def create_excel(self):
        """Создаёт и возвращает Excel-файл в виде байтов"""

        output = io.BytesIO()
        self.book = xlsxwriter.Workbook(output)
        self.s = self.book.add_worksheet()

        self.format_1 = self.book.add_format(
            {
                "font_size": 7,
                "border": 2,
                "font_name": "Arial",
                "align": "center",
                "valign": "vcenter",
                "bold": True,
                "text_wrap": True,
                "shrink": True,
            }
        )

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
                "shrink": True,
            }
        )
        # format_2.set_shrink()
        self.format_3 = self.book.add_format(
            {
                "border": 2,
                "font_name": "Arial",
                "font_size": 8,
                "bold": False,
                "fg_color": "#D7E4BC",
                "align": "center",
                "valign": "vcenter",
                "text_wrap": True,
                "shrink": True,
            }
        )
        # format_3.set_shrink()
        self.format_4 = self.book.add_format(
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
        self.format_4.set_shrink()
        self.format_5 = self.book.add_format(
            {"font_size": 8, "font_name": "Arial", "bold": True, "text_wrap": True}
        )
        self.format_5.set_shrink()
        self.format_6 = self.book.add_format(
            {
                "border": 2,
                "font_name": "Arial",
                "font_size": 12,
                "bold": True,
                "fg_color": "#B2FF66",
                "align": "center",
                "valign": "vcenter",
                "text_wrap": True,
                "shrink": True,
            }
        )

        self.format_7 = self.book.add_format(
            {
                "fg_color": "#FFFFFF",
                "border": 2,
                "font_name": "Arial",
                "font_size": 12,
                "bold": True,
                "align": "center",
                "valign": "vcenter",
                "text_wrap": True,
                "shrink": True,
            }
        )

        self.command_batt_stvoriti()
        output.seek(0)
        return output.getvalue()
        

    def checklist_header(self):
        

        self.s.set_v_pagebreaks([31])
        self.s.set_h_pagebreaks([100])

        text = "Аналіз ефективності програми з контролю шкідників \n (Pest control)"
        text2 = (
            f"Щомісячний  звіт  активності  шкідників  за "
            f"{self.MONTH_1[self._month]} "
            f"{self._year} року"
        )

        self.s.set_column(0, 100, 3)

        log = self.s.insert_image(
            0, 0, "логотип укр.png", {"x_scale": 0.25, "y_scale": 0.25}
        )
        shtamp = self.s.insert_image(
             0, 21, "PestControl\ПЕЧАТЬ-ПОДПИСЬ_png-removebg-preview.png", {"x_scale": 0.20, "y_scale": 0.21}
        )

        self.s.merge_range(0, 0, 5, 4, log, self.format_2)
        self.s.merge_range(0, 5, 5, 20, text, self.format_2)
        self.s.merge_range(0, 21, 10, 29, shtamp, self.format_7)
        self.s.merge_range(6, 0, 6, 20, text2, self.format_3)
        self.s.merge_range(7, 0, 7, 4, "Підприємство замовник", self.format_3)
        self.s.merge_range(7, 5, 7, 20, self._predpr, self.format_3)
        self.s.merge_range(8, 0, 8, 4, "Виконавець", self.format_3)
        self.s.merge_range(8, 5, 8, 20, "ПП ДЕЗ-ЕЛЬТОР", self.format_3)
        self.s.merge_range(9, 0, 9, 4, "Родетицид", self.format_3)
        self.s.merge_range(9, 5, 9, 9, bd.preparat_yes()[0], self.format_3)
        self.s.merge_range(9, 10, 9, 14, "придатний до", self.format_3)
        self.s.merge_range(9, 15, 9, 20, bd.preparat_yes()[1], self.format_3)
        self.s.merge_range(10, 0, 10, 4, "Дати відвідувань", self.format_3)
        for i in range(6, 12):
            self.s.set_row(i, 12)
        self.data_vidviduvan(self.s, self.format_3)
        row, grizni_za_mes, poedaemoct_za_mes = self.tabl_zvit(
            s_1=self.s,
            format_3_1=self.format_3,
            format_1_1=self.format_1,
            format_6_1=self.format_6,
            format_5_1=self.format_5,
            book_1=self.book,
        )
        self.diaramma(
            s_1=self.s,
            row_last=row,
            grizni_za_mes_1=grizni_za_mes,
            poedaemoct_za_mes_1=poedaemoct_za_mes,
        )

        self.book.close()

    def information_from_combo(self):
        """
        здирає та аналізує інормацію з комбобоксів
        :return:
        """

        namber, month, value_I_II, value_III = bd.value_from_db_for_zvit(
            _month=self._month,
            _predpr=self._predpr,
            _year=self._year,
        )

        if len(value_I_II) == 0 and len(value_III) == 0:
            return 
        else:

            return namber, month, value_I_II, value_III

    def count_dk_1_2(self):
        """
         достає с жейсона кількість контейнерів по 1 - 2 бар'єру для обчислення середньої поїдаїмості за місяць
        :return:
        """

        return bd.count_dk_1_2(_pidpr=self._predpr)

    def count_dk_3(self):
        """
         достає с жейсона кількість контейнерів по 3 бар'єру
        :return:
        """

        return bd.count_dk_3(_pidpr=self._predpr)
    
    def all_in_one(self, value_1: list, number_1: str) -> dict:
        """
        якщо  за один вихід було багато збережень  функція зєднає все в один словник
        :param number_1: число по якому збираємо словник
        :param value_1: список словників в якому данні з ДК за всі виходи в місяц
        :return: обєднанний словник за одне число
        """
        list_new = []
        for i in value_1:
            if i.get(number_1) is None:
                pass
            else:
                list_new.append(i.get(number_1))
        for i in range(0, len(list_new) - 1):
            list_new[0].update(list_new[i + 1])
        try:
            list_new = list_new[0]
        except:
            pass

        return list_new

    def chast_spisok_znachen(self, namber_2, value1_2, value3):

        key1_2 = []
        key3 = []
        finaly_value_I_II = []
        finaly_value_III = []
        how_inshe_1_2 = 0
        how_inshe_3 = 0
        
        for value in [value1_2, value3]:

            for cc in namber_2:
                vvv = self.all_in_one(value_1=value, number_1=cc)

                if len(vvv) != 0:

                    for i, f in vvv.items():
                        if value == value1_2:
                            if i not in key1_2 and f != "":
                                key1_2.append({i: []})
                                # (key1_2)
                        else:
                            if i not in key3 and f != "":
                                key3.append({i: []})

            for cc in namber_2:
                vvv = self.all_in_one(value_1=value, number_1=cc)

                if len(vvv) != 0:
                    for kay_vvv, value_vvv in vvv.items():
                        if value == value1_2:

                            if value_vvv == "I" or value_vvv == "ІН":
                                how_inshe_1_2 += 1
                        elif value == value3:
                            if value_vvv == "I" or value_vvv == "ІН":
                                how_inshe_3 += 1
                        try:
                            value_vvv = int(value_vvv)
                        except:
                            pass

                        if value == value1_2:

                            for j in key1_2:
                                try:
                                    # (value_vvv.startswith(" миша"))

                                    if (
                                        isinstance(value_vvv, int)
                                        or value_vvv.startswith("М")
                                        or value_vvv.startswith("К")
                                        or value_vvv.startswith(" криса")
                                        or value_vvv.startswith(" миша")
                                    ):

                                        j[kay_vvv].append(value_vvv)
                                except:
                                    pass

                            for key_1 in key1_2:

                                if key_1 not in finaly_value_I_II:
                                    finaly_value_I_II.append(key_1)

                        else:

                            for j in key3:

                                try:
                                    #!!!!!!!!! если будут затыки с грызунами возможно они тут
                                    # Возможно нужно вводить украинские буквы а не английские смотри на пробелы

                                    if (
                                        "М" in value_vvv
                                        or "K" in value_vvv
                                        or "К" in value_vvv
                                        or " криса" in value_vvv
                                        or " миша" in value_vvv
                                        or "M" in value_vvv
                                    ):
                                        if value_vvv.rpartition("-")[0] == " миша":
                                            value_vvv = (
                                                f"М-{value_vvv.rpartition('-')[2]}"
                                            )
                                        elif value_vvv.rpartition("-")[0] == " криса":
                                            value_vvv = (
                                                f"K-{value_vvv.rpartition('-')[2]}"
                                            )

                                        j[kay_vvv].append(value_vvv.rpartition("-"))

                                except:
                                    pass

                            for key_1 in key3:
                                if key_1 not in finaly_value_III:

                                    finaly_value_III.append(key_1)

        return finaly_value_I_II, finaly_value_III, how_inshe_1_2, how_inshe_3

    def count_grizini_na_teritiri_I_II(self):
        """
        # збирає інформацію скільки гризунів на теріторії за кожен вихід записуватися в таблицю буде лише остання запись
        # :return:
        #"""

        grizuni_na_territri_1, grizuni_na_territri_1_finsh = (
            bd.value_from_db_grizuni_for_cheklist(
                _month=self._month,
                _predpr=self._predpr,
                _year=self._year,
            )
        )
        
        return grizuni_na_territri_1_finsh

    def podgotovka_k_zapisi_v_tablicu(self, finaly_value1, finaly_value3, namber_1):

        value_in_tabl_1 = []
        value_in_tabl_3 = []
        vsego_grizunv_za_mes_I = [["M-", 0], ["K-", 0]]
        vsego_grizunv_za_mes_III = [["M-", 0], ["K-", 0]]
        summa_poedaemosti_za_mes = 0
        how_dk_1_2 = self.count_dk_1_2()
        grizuni_na_territri_1 = self.count_grizini_na_teritiri_I_II()

        for i in finaly_value1:
            for j, v in i.items():
                if len(v) != 0 and v != [0]:
                    try:
                        if sum(v) / len(namber_1) != 0:
                            value_in_tabl_1.append(
                                (int(j), round(sum(v) / len(namber_1), 1))
                            )
                            summa_poedaemosti_za_mes += round(sum(v) / len(namber_1), 1)
                    except:
                        v_1 = []
                        for d in v:
                            if isinstance(d, str):
                                v_1.append(d)
                        if len(v_1) == 1:
                            value_in_tabl_1.append((int(j), v_1[0]))
                            if v_1[0].split("-")[0] == "М":
                                vsego_grizunv_za_mes_I[0][1] += int(
                                    v_1[0].split("-")[1]
                                )
                            elif v_1[0].split("-")[0] == "К":
                                vsego_grizunv_za_mes_I[1][1] += int(
                                    v_1[0].split("-")[1]
                                )
                        else:
                            m = []
                            k = []
                            for p in v_1:
                                if p[0] == "М":
                                    m.append(int(p[2]))
                                if p[0] == "К":
                                    k.append(int(p[2]))
                            sum_m = sum(m)
                            sum_k = sum(k)
                            vsego_grizunv_za_mes_I[0][1] += sum_m
                            vsego_grizunv_za_mes_I[1][1] += sum_k
                            if sum_m == 0:
                                value_in_tabl_1.append((int(j), f"K-{sum_k}"))
                            if sum_k == 0:
                                value_in_tabl_1.append((int(j), f"М-{sum_m}"))
                            else:
                                value_in_tabl_1.append((int(j), f"М-{sum_m} K-{sum_k}"))

        for i in finaly_value3:

            for j, v in i.items():

                if len(v) != 0 and v != [0]:

                    if len(v) == 1:
                        value_in_tabl_3.append((int(j), "".join(v[0])))
                        if v[0][0] == "М":
                            vsego_grizunv_za_mes_III[0][1] += int(v[0][2])
                        elif v[0][0] == "K" or v[0][0] == "К":
                            vsego_grizunv_za_mes_III[1][1] += int(v[0][2])
                    else:
                        m = []
                        k = []
                        for p in v:
                            if p[0] == "М":
                                m.append(int(p[2]))
                            if p[0] == "К":
                                k.append(int(p[2]))
                        sum_m = sum(m)
                        sum_k = sum(k)
                        vsego_grizunv_za_mes_III[0][1] += sum_m
                        vsego_grizunv_za_mes_III[1][1] += sum_k
                        if sum_m == 0:
                            value_in_tabl_3.append((int(j), f"K-{sum_k}"))
                        if sum_k == 0:
                            value_in_tabl_3.append((int(j), f"М-{sum_m}"))
                        else:
                            value_in_tabl_3.append((int(j), f"М-{sum_m} K-{sum_k}"))
        srednya_poedaemosti_za_mes = round(summa_poedaemosti_za_mes / how_dk_1_2, 1)

        return (
            sorted(value_in_tabl_1, key=lambda x: x[0]),
            sorted(value_in_tabl_3, key=lambda x: x[0]),
            vsego_grizunv_za_mes_I,
            vsego_grizunv_za_mes_III,
            grizuni_na_territri_1,
            srednya_poedaemosti_za_mes,
        )

    def spisok_znachen(self):
        namber, month, value_I_II, value_III = self.information_from_combo()

        finaly_value_I_II, finaly_value_III, how_inshe_1_2, how_inshe_3 = (
            self.chast_spisok_znachen(
                namber_2=namber, value1_2=value_I_II, value3=value_III
            )
        )

        (
            value_in_tabl_1,
            value_in_tabl_3,
            vsego_grizunv_za_mes_I,
            vsego_grizunv_za_mes_III,
            grizuni_na_territri_1,
            srednya_poedaemosti_za_mes,
        ) = self.podgotovka_k_zapisi_v_tablicu(
            finaly_value_I_II, finaly_value_III, namber_1=namber
        )

        return (
            value_in_tabl_1,
            value_in_tabl_3,
            vsego_grizunv_za_mes_I,
            vsego_grizunv_za_mes_III,
            grizuni_na_territri_1,
            srednya_poedaemosti_za_mes,
            how_inshe_1_2,
            how_inshe_3,
        )

    def tabl_zvit(self, s_1, format_3_1, format_1_1, format_6_1, format_5_1, book_1):
        """
        заисує данні в таблицю звіту
        :return:
        """

        akti_util = stroka_dly_zvita(self._predpr, self._month, self._year)
        # adm = Formatadm()

        (
            value_in_tabl_1,
            value_in_tabl_3,
            vsego_grizunv_za_mes_I,
            vsego_grizunv_za_mes_III,
            grizuni_na_territri_1,
            srednya_poedaemosti_za_mes,
            how_inshe_1_2,
            how_inshe_3,
        ) = self.spisok_znachen()

        ROW_START = 14
        vsego_grizuniv_za_mis = (
            vsego_grizunv_za_mes_I[0][1]
            + vsego_grizunv_za_mes_I[1][1]
            + vsego_grizunv_za_mes_III[0][1]
            + vsego_grizunv_za_mes_III[1][1]
            + grizuni_na_territri_1[0][1]
            + grizuni_na_territri_1[1][1]
        )

        row_last = 0  # значення номеру рядку для заповнення останнього рядку в таблці
        coll = 0
        how_row_1_2 = math.ceil(len(value_in_tabl_1) / 15)

        how_row_3 = math.ceil(len(value_in_tabl_3) / 15)
        s_1.merge_range(
            12, 0, 12, 29, f"І, ІІ - бар’єр {self.count_dk_1_2()} одиниць", format_6_1
        )
        for i in range(0, 30, 2):
            s_1.write(13, i, "№ ДК", format_3_1)
            s_1.write(13, i + 1, "Поїд в %", format_1_1)

        row_start = ROW_START
        for j in value_in_tabl_1:
            s_1.write(row_start, coll + 1, j[1], format_1_1)

            if len(self.podpis) == 0:
                s_1.write(row_start, coll, j[0], format_3_1)
            else:
                for key, podpis in self.podpis.items():
                    if j[0] in key and key[-1] in (
                        "II",
                        "I",
                    ):  # and  self.barier == self.BARIER[key[-1]]: нужно отсечь повторения по барьерам
                        form_ = key[-2]
                        self.s.write_comment(
                            row_start,
                            coll,
                            podpis,
                            {"x_scale": 0.8, "y_scale": 0.8},
                        )
                        format_ = self.podpis_barier.color(self.book, form_)
                        s_1.write(row_start, coll, j[0], format_)
                        break
                    else:
                        s_1.write(row_start, coll, j[0], format_3_1)

            s_1.set_row(row_start, 10)
            row_start += 1
            if row_start > row_last:
                row_last = row_start
            if row_start == ROW_START + how_row_1_2:
                coll += 2
                row_start = ROW_START
        if len(value_in_tabl_1) == 0:
            row_last = row_start
        s_1.merge_range(
            row_last,
            0,
            row_last,
            29,
            f"Кількість гризунів (територія + МП): {grizuni_na_territri_1[0][0]}"
            f"{grizuni_na_territri_1[0][1] + vsego_grizunv_za_mes_I[0][1]}, {grizuni_na_territri_1[1][0]}"
            f"{grizuni_na_territri_1[1][1] + vsego_grizunv_za_mes_I[1][1]}",
            format_6_1,
        )
        # if row_last >= 44:
        #     row_last = 48
        s_1.merge_range(
            row_last + 2,
            0,
            row_last + 2,
            29,
            f"ІІІ - бар’єр {self.count_dk_3()} одиниць",
            format_6_1,
        )
        for i in range(0, 30, 2):
            s_1.write(row_last + 3, i, "№ МП", format_3_1)
            s_1.write(row_last + 3, i + 1, "вид шкідника", format_1_1)
        row_start_1 = row_last + 4
        row_start = row_start_1
        coll = 0
        row_last = row_last + 4
        if len(value_in_tabl_3) != 0:
            for j in value_in_tabl_3:

                if len(self.podpis) == 0:
                    s_1.write(row_start, coll, j[0], format_3_1)
                else:

                    for key, podpis in self.podpis.items():

                        if (
                            j[0] in key and key[-1] == "III"
                        ):  # and  self.barier == self.BARIER[key[-1]]: нужно отсечь повторения по барьерам
                            form_ = key[-2]
                            self.s.write_comment(
                                row_start,
                                coll,
                                podpis,
                                {"x_scale": 0.8, "y_scale": 0.8},
                            )
                            format_ = self.podpis_barier.color(self.book, form_)
                            s_1.write(row_start, coll, j[0], format_)
                            break
                        else:
                            s_1.write(row_start, coll, j[0], format_3_1)

                s_1.write(row_start, coll + 1, j[1], format_1_1)
                s_1.set_row(row_start, 10)
                row_start += 1
                if row_start > row_last:
                    row_last = row_start
                if row_start == row_start_1 + how_row_3:
                    coll += 2
                    row_start = row_start_1

        s_1.merge_range(
            row_last,
            0,
            row_last,
            29,
            f"Кількість гризунів III - бар'єр: {vsego_grizunv_za_mes_III[0][0]}"
            f"{vsego_grizunv_za_mes_III[0][1]}, {vsego_grizunv_za_mes_III[1][0]}"
            f"{vsego_grizunv_za_mes_III[1][1]}",
            format_6_1,
        )
        s_1.merge_range(
            row_last + 1,
            0,
            row_last + 1,
            29,
            f"Умовні позначення : (0-100%) - кількість поїдання принад в  % за місяць;"
            f" М – миша, К – криса",
            format_5_1,
        )

        s_1.merge_range(
            row_last + 3, 0, row_last + 3, 25, f"Акти утилізації: {str(akti_util)} ", format_5_1
        )
        s_1.merge_range(
            row_last + 4,
            0,
            row_last + 4,
            25,
            f"Загальне поїдання принади за місяць"
            f"(%):  І - ІІ бар’єр – {srednya_poedaemosti_za_mes}%.",
            format_5_1,
        )
        s_1.merge_range(
            row_last + 5,
            0,
            row_last + 5,
            25,
            f"Загальна кількість гризунів за місяць:" f" {vsego_grizuniv_za_mis} шт.",
            format_5_1,
        )
        s_1.merge_range(
            row_last + 6,
            0,
            row_last + 6,
            25,
            f"Заміна принади з інших причин (І-ІІ бар’єр)"
            f" - {how_inshe_1_2} одиниць обладнання.",
            format_5_1,
        )
        s_1.merge_range(
            row_last + 7,
            0,
            row_last + 7,
            25,
            f"Заміна липкої вкладки  з інших причин (ІІІ бар’єр)"
            f" - {how_inshe_3} одиниць обладнання.",
            format_5_1,
        )
        for i in range(1, 8):
            self.s.set_row(row_last + i, 12)
        return row_last + 7, vsego_grizuniv_za_mis, srednya_poedaemosti_za_mes

    def dannie_dlya_diagrammi(self, grizni_za_mes_2, poedaemoct_za_mes_2):

        date = bd.value_diagramma(
            poedaemoct=poedaemoct_za_mes_2,
            kolichestvo_grizunov=grizni_za_mes_2,
            pidpriemstvo=self._predpr,
            date=f"{Zvit.MES[self._month]}" f" {self._year}",
        )

        return date[::-1]
    
    # def shtamp(self, row):
    #     self.s.insert_image(
    #          row, 17, "ПЕЧАТЬ ПОДПИСЬ_page-0001.png", {"x_scale": 0.30, "y_scale": 0.31}
    #     )

      

    def diaramma(self, s_1, row_last, grizni_za_mes_1, poedaemoct_za_mes_1):
        """
        Создает и вставляет диаграмму в Excel
        """
        data_diagram = self.dannie_dlya_diagrammi(grizni_za_mes_1, poedaemoct_za_mes_1)
        

        # Разбираем данные
        categories = []
        values1 = []
        values2 = []

        for item in data_diagram:
            for key, value in item.items():
                categories.append(key)
                values1.append(value[0])
                values2.append(value[1])

        legend = [
            "Загальна кількість поїдання принади за місяць %",
            "Загальна кількість гризунів за місяць шт"
        ]

        # Записываем данные в таблицу
        start_row = row_last + 2
        s_1.write_column(f"A{start_row}", categories)
        s_1.write_column(f"B{start_row}", values1)
        s_1.write_column(f"C{start_row}", values2)
        s_1.write(f"D{start_row}", legend[0])
        s_1.write(f"E{start_row}", legend[1])
        
        # Создаем диаграмму
        chart = self.book.add_chart({"type": "column"})
        chart.set_size({"width": 700, "height": 250})
        chart.set_x_axis({
            "num_font": {"name": "Arial", "size": 7},
            "major_gridlines": {"visible": True, "line": {"width": 0.25, "dash_type": "dash"}}
        })
        chart.set_legend({"position": "top"})
        chart.set_title({
            "name": "ПОРІВНЯЛЬНА ДІАГРАММА АКТИВНОСТІ ГРИЗУНІВ ЗА РІК",
            "layout": {"x": 0.1, "y": 0.02},
            "name_font": {"name": "Arial", "size": 12, "color": "#00CC00"},
        })

        # Добавляем серии данных
       
       

        chart.add_series({ 
            "categories": [s_1.name, start_row-1, 0, start_row + len(categories) - 2, 0],
            "values": [s_1.name, start_row-1, 1, start_row + len(values1) - 2, 1],
            "name": legend[0],
            "line": {"color": "red"},
            "data_labels": {"value": True},
            "fill": {"color": "#FFFF33"},
            "border": {"color": "black"},
        })

        chart.add_series({
            "values": [s_1.name, start_row-1, 2, start_row + len(values2) - 2, 2],
            "name": legend[1],
            "line": {"color": "red"},
            "data_labels": {"value": True},
            "fill": {"color": "#0080FF"},
            "border": {"color": "black"},
        })

        # Вставляем диаграмму
        s_1.insert_chart(f"A{start_row}", chart)
            
    def command_batt_stvoriti(self):

        self.checklist_header()
        # os.startfile(f"PestControl\save zvit\Звіт {self._predpr} {self._month}.xlsx")

    def data_vidviduvan(self, s_1, format_3_1):
        """
        формує в графі кількість виходів необхідну кількість ячеєк
        :param s_1:
        :param format_3_1:
        :return:
        """

        namber, month, value_I_II, value = self.information_from_combo()

        how_ycheek = math.floor(16 / len(namber))
        namber_1 = sorted(namber)
        tab = 0
        i = 4
        while tab < len(namber):
            if len(namber) - tab == 1:
                s_1.merge_range(
                    10, i + 1, 10, 20, f"{namber_1[tab]}.{month[0]}", format_3_1
                )
            else:
                s_1.merge_range(
                    10,
                    i + 1,
                    10,
                    i + how_ycheek,
                    f"{namber_1[tab]}.{month[0]}",
                    format_3_1,
                )
            i += how_ycheek
            tab += 1


    def main(self):
            
            # Проверяем, если переменные ещё не существуют в session_state
        if "show_form_zvit" not in st.session_state:
            st.session_state["show_form_zvit"] = False

        if "last_month" not in st.session_state:
            st.session_state["last_month"] = None

        if "last_year" not in st.session_state:
            st.session_state["last_year"] = None

        # Кнопка для отображения/скрытия формы
        if st.button("📝 Генерація Звіту"):
            st.session_state["show_form_zvit"] = not st.session_state["show_form_zvit"]

        # Если форма показывается
        if st.session_state["show_form_zvit"]:
            current_year = datetime.today().year

            monse = st.selectbox("Місяць", ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"], index=int(datetime.today().month)-2, key="zvit_selekt")
            year = st.number_input("Оберіть рік", min_value=2000, max_value=2100, value=current_year, step=1, key="number_input_zvit")

            # Проверка изменения данных
            if monse != st.session_state["last_month"] or year != st.session_state["last_year"]:
                st.session_state["last_month"] = monse
                st.session_state["last_year"] = year
                
                # Кнопка для скачивания отчета
                try:
                    with st.spinner('Дчекайтесь завантаження, не натискайте нічого'):
                        st.download_button(
                            label="📥 Завантажити Excel",
                            data=Zvit(self._predpr, monse, year).create_excel(),
                            file_name=f"Звіт_{self._predpr}_{monse}_{year}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                except Exception:
                    st.write(f"Щось пішло не так!!!")
            