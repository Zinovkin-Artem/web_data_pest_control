import streamlit as st
from datetime import datetime
import math
import os
# from tkinter import messagebox
import io
from collections import defaultdict
import re
import xlsxwriter
from number_akti_in_zvit import stroka_dly_zvita
from zapis_v_tabl_diagramma_1_2 import main_cherz_zvit
import sql as bd

# from PestControl.format_color_adm import Formatadm
from format_color_pidpriemctv import Formatcolor
import time    
import tempfile
import webbrowser




class Zvit():
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
    INSHI_I = 0
    INSHI_III = 0

    def __init__(self, _predpr, _month = "11", _year = "2025"):
        self.row_value, self.vixodi = bd.value_from_zvit_new(_predpr, _month, _year)
        self.kilkist_obladn_I, self.kilkist_obladn_III = bd.baza_predpr(_predpr)[3:5]
        self.grizyni_na_teritor = bd.grizuni_na_terit_from_new_zvit(_predpr, _month, _year)

        self._predpr = _predpr
        self._month = _month
        self._year = _year
        self.book = None
        self.s = None
        self.podpis_barier = Formatcolor()
        self.podpis = self.podpis_barier.format(_predpr)



    def create_excel(self):
                """Создаёт и возвращает Excel-файл в виде байтов"""

                output = io.BytesIO()
                self.book = xlsxwriter.Workbook(output)
                self.s = self.book.add_worksheet()
                self.s.set_column(0, 27, 2.6)  # тільки перші 30 колонок
                self.s.fit_to_pages(1, 1)
                self.s.set_portrait()
                self.s.set_margins(left=0.1, right=0.1, top=0.1, bottom=0.1)




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
        ################################################
                danie_v_tabl_I, poidannie_za_mes_I, kilkist_grizuniv_v_pastkax_I, zamina_z_inshix_I = self.value_from_tabl_zvit("I - II")
                
                danie_v_tabl_III, poidannie_za_mes_III, kilkist_grizuniv_v_pastkax_III, zamina_z_inshix_III = self.value_from_tabl_zvit("III")
                
                self.value_from_tabl_zvit("III")
                akti_util = stroka_dly_zvita(self._predpr, self._month, self._year)
                
                self.checklist_header()
                self.s.merge_range(12, 0, 12, 27, f"І, ІІ - бар’єр {self.kilkist_obladn_I} одиниць", self.format_6)
                self.shapka_tabl(13,"поїд в %")
                new_row_start = self.write_value_in_tabl(14,danie_v_tabl_I, barier= ("I", "II"))
                text_tabl_1 = f"Кількість гризунів: На території K-{self.grizyni_na_teritor['К']}, M-{self.grizyni_na_teritor['М']}; В механічних пастках {kilkist_grizuniv_v_pastkax_I}"
                self.s.merge_range(new_row_start, 0, new_row_start, 27, text_tabl_1, self.format_6)
                

                self.s.merge_range(new_row_start+2, 0, new_row_start+2, 27, f"ІІІ - бар’єр {self.kilkist_obladn_III} одиниць", self.format_6)
                self.shapka_tabl(new_row_start+3,"вид шкідника")
                new_row_start = self.write_value_in_tabl(new_row_start+4,danie_v_tabl_III, barier= ("III"))
                text_tabl_2 = f"Кількість гризунів: В механічних пастках {kilkist_grizuniv_v_pastkax_III}"
                self.s.merge_range(new_row_start, 0, new_row_start, 27, text_tabl_2, self.format_6)
                text_umovni = "Умовні позначення : (0-100%) - кількість поїдання принад в  % за місяць; М – миша, К – криса"
                self.s.merge_range(new_row_start+1, 0, new_row_start+1, 27, text_umovni,self.format_5)

                text_utiliz = f"Акти утилізації: {akti_util}"
                self.s.merge_range(new_row_start+3, 0, new_row_start+3, 27,text_utiliz, self.format_5 )
                text_poidanit = f"Загальне поїдання принади за місяць(%):  І - ІІ бар’єр – {poidannie_za_mes_I}%."
                self.s.merge_range(new_row_start+4, 0, new_row_start+4, 27,text_poidanit, self.format_5 )

                griz_za_mic = int(self.grizyni_na_teritor['М']) + int(self.grizyni_na_teritor['К']) + int(kilkist_grizuniv_v_pastkax_III.split(",")[0].split("-")[1]) + int(kilkist_grizuniv_v_pastkax_III.split(",")[1].split("-")[1])  + int(kilkist_grizuniv_v_pastkax_I.split(",")[1].split("-")[1]) + int(kilkist_grizuniv_v_pastkax_I.split(",")[0].split("-")[1])

                text_grizuni_za_mic = f"Загальна кількість гризунів за місяць: {griz_za_mic} шт."
                self.s.merge_range(new_row_start+5, 0, new_row_start+5, 27,text_grizuni_za_mic, self.format_5 )
                text_insi_I = f"Заміна принади з інших причин (І-ІІ бар’єр) - {zamina_z_inshix_I} одиниць обладнання."
                self.s.merge_range(new_row_start+6, 0, new_row_start+6, 27,text_insi_I, self.format_5 )
                text_insi_III = f"Заміна принади з інших причин (ІІІ бар’єр) - {zamina_z_inshix_III} одиниць обладнання."
                self.s.merge_range(new_row_start+7, 0, new_row_start+7, 27,text_insi_III, self.format_5 )
                self.diaramma(new_row_start+8,griz_za_mic,  poidannie_za_mes_I)


        ###########################################################    
                self.book.close()
                output.seek(0)
                return output.getvalue()
        
    #функция для надписи  шапки таблицы
    def shapka_tabl(self, hou_row, text_2):
       for col in range(0, 28, 2):
            self.s.write(hou_row, col, "№ обл", self.format_3)
            self.s.write(hou_row, col + 1, text_2, self.format_1)

    #функция для записывания данных в таблицу
    def write_value_in_tabl(self, hou_row, value:dict, barier):
        vsegj_strok = math.ceil(len(value)/14)
        
        col = 0
        hou_row_start = hou_row
        for key, _value in value.items():
            try:
                _value = _value[0]
            except:
                pass
            if not self.podpis:
                self.s.write(hou_row_start, col, key, self.format_3)
                
            else:
                for _key, _podpis in self.podpis.items():
                    
                    if isinstance(_key, tuple) and key in _key and _key[-1] in barier:
                        
                        form_ = _key[-2]  # передостанній елемент — це колір

                        self.s.write_comment(
                            hou_row_start, col,
                            _podpis,
                            {"x_scale": 0.8, "y_scale": 0.8},
                        )
                    
                        format_ = self.podpis_barier.color(self.book, form_)
                        
                        self.s.write(hou_row_start, col, key, format_)
                    
                    # else:
                    #     print(1111, key)
                        
                    #     self.s.write(hou_row_start, col, key, self.format_3)
                        
            self.s.set_row(hou_row_start, 10)
            self.s.write(hou_row_start, col+1, _value, self.format_1)
            hou_row_start += 1 
            if hou_row_start  >= vsegj_strok + hou_row:
                col += 2
                hou_row_start = hou_row

            
        return hou_row+vsegj_strok

                

  

    def checklist_header(self):
        

        # self.s.set_v_pagebreaks([31])
        # self.s.set_h_pagebreaks([100])

        text = "Аналіз ефективності програми з контролю шкідників \n (Pest control)"
        text2 = (
            f"Щомісячний  звіт  активності  шкідників  за "
            f"{self.MONTH_1[self._month]} "
            f"{self._year} року"
        )

        # self.s.set_column(0, 100, 3)

        log = self.s.insert_image(
            0, 0, "логотип укр.png", {"x_scale": 0.25, "y_scale": 0.25}
        )
        shtamp = self.s.insert_image(
             0, 21, "ПЕЧАТЬ-ПОДПИСЬ_png-removebg-preview.png", {"x_scale": 0.20, "y_scale": 0.21}
        )
        

        self.s.merge_range(0, 0, 5, 4, log, self.format_2)
        self.s.merge_range(0, 5, 5, 20, text, self.format_2)
        self.s.merge_range(0, 21, 10, 28, shtamp, self.format_7)
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
        self.data_vidviduvan(self.s, self.format_3)

    def data_vidviduvan(self, s_1, format_3_1):
        """
        формує в графі кількість виходів необхідну кількість ячеєк
        :param s_1:
        :param format_3_1:
        :return:
        """
    
        namber = self.vixodi
        month = self._month

        how_ycheek = math.floor(16 / len(namber))
        namber_1 = sorted(namber)
        tab = 0
        i = 4
        while tab < len(namber):
            if len(namber) - tab == 1:
                s_1.merge_range(
                    10, i + 1, 10, 20, f"{namber_1[tab]}.{month}", format_3_1
                )
            else:
                s_1.merge_range(
                    10,
                    i + 1,
                    10,
                    i + how_ycheek,
                    f"{namber_1[tab]}.{month}",
                    format_3_1,
                )
            i += how_ycheek
            tab += 1

    def value_from_tabl_zvit(self, barier):

        value_filter_barier = [i for i in self.row_value if i[2] == barier]
        grouped = defaultdict(list)
        inshi = 0
        for num, val, *arg in value_filter_barier:
           
            if val in ("ІН", "I"):
                inshi += 1
               
            if any(char.isdigit() for char in val):  # <- ось умова
                grouped[num].append(val)
        
        normalized = {}
        

        for key, values in grouped.items():
            new_vals = []
            for val in values:
                val_clean = val.strip()

                # Спочатку перевіряємо на "м"
                match_m = re.search(r'\b\w*[мmMМ]\w*?-([0-9]+)', val_clean, re.IGNORECASE)
                if match_m:
                    new_vals.append(f"M-{match_m.group(1)}")
                    continue  # не перевіряємо далі, якщо вже знайшли "м"

                # Потім перевіряємо на "к"
                match_k = re.search(r'\b\w*[кkKК]\w*?-([0-9]+)', val_clean, re.IGNORECASE)
                if match_k:
                    new_vals.append(f"K-{match_k.group(1)}")
                else:
                    new_vals.append(val_clean)

            normalized[key] = new_vals
        
        result = {}
        total_sum = 0
        grizyniv_v_pastkax_M = 0
        grizyniv_v_pastkax_K = 0

        if barier == "I - II":
           

            for key, values in normalized.items():
                if all(val.isdigit() for val in values):
                    avg = round(sum(int(val) for val in values) / len(self.vixodi), 1)
                    result[key] = avg
                    total_sum += avg
                else:
                    
                    
                    k_sum = 0
                    m_sum = 0

                    for val in values:
                        match = re.match(r'([MK])-([0-9]+)', val, re.IGNORECASE)
                    
                        if match:
                            letter = match.group(1).upper()
                            number = int(match.group(2))

                            if letter == 'K':
                                k_sum += number
                            elif letter == 'M':
                                m_sum += number

                    if k_sum > 0:
                        result[key] = [f"K-{k_sum}"]
                    if m_sum > 0:
                        result[key] = [f"M-{m_sum}"]
                    grizyniv_v_pastkax_M += m_sum
                    grizyniv_v_pastkax_K +=k_sum
                    
        else:
            
            for key, values in normalized.items():
                if all(val.isdigit() for val in values):
                    avg = round(sum(int(val) for val in values) / len(self.vixodi), 1)
                    result[key] = avg
                    total_sum += avg
                else:
                    k_sum = 0
                    m_sum = 0

                    for val in values:
                        match = re.match(r'([MK])-([0-9]+)', val, re.IGNORECASE)
                        
                        if match:
                            letter = match.group(1).upper()
                            number = int(match.group(2))

                            if letter == 'K':
                                k_sum += number
                            elif letter == 'M':
                                m_sum += number

                    if k_sum > 0:
                        result[key] = [f"K-{k_sum}"]
                    if m_sum > 0:
                        result[key] = [f"M-{m_sum}"]
                    grizyniv_v_pastkax_M += m_sum
                    grizyniv_v_pastkax_K +=k_sum

        danie_v_tablisu = result
        poidannya_za_misac = round(total_sum/self.kilkist_obladn_I, 1)
        grizyniv_v_pastkax = f"K-{grizyniv_v_pastkax_K}, M-{grizyniv_v_pastkax_M}"
        return danie_v_tablisu, poidannya_za_misac, grizyniv_v_pastkax, inshi
                    
        # print("Гризунів на теріторії:", self.grizyni_na_teritor)  
        # print("Кількість обладнання:", self.kilkist_obladn_I, self.kilkist_obladn_III)         
        # print("гризунів в пастках:", grizyniv_v_pastkax) # return
        # print("данні таблиці:", result)#return
        # print("Загальна сума:", round(total_sum/self.kilkist_obladn_I, 1)) #return
        # print("Заміна з інших причин:", self.INSHI_I, self.INSHI_III)#return

    def dannie_dlya_diagrammi(self, grizni_za_mes_2, poedaemoct_za_mes_2):

        date = bd.value_diagramma(
            poedaemoct=poedaemoct_za_mes_2,
            kolichestvo_grizunov=grizni_za_mes_2,
            pidpriemstvo=self._predpr,
            date=f"{Zvit.MONTH_1[self._month]}" f" {self._year}",
        )

        return date[::-1]
    
    # def shtamp(self, row):
    #     self.s.insert_image(
    #          row, 17, "ПЕЧАТЬ ПОДПИСЬ_page-0001.png", {"x_scale": 0.30, "y_scale": 0.31}
    #     )

    def diaramma(self,row_last, grizni_za_mes_1, poedaemoct_za_mes_1):
        """
        створює та розміщує діаграмму
        :param poedaemoct_za_mes_1:
        :param grizni_za_mes_1:
        :param row_last:
        :param book_1:
        :param s_1:
        :return:
        """

        data_diagram = self.dannie_dlya_diagrammi(grizni_za_mes_1, poedaemoct_za_mes_1)


        chart = self.book.add_chart({"type": "column"})
        chart.set_size({"width": 670, "height": 250})
        chart.set_x_axis(
            {
                "num_font": {"name": "Arial", "size": 7},
                "major_gridlines": {
                    "visible": True,
                    "line": {"width": 0.25, "dash_type": "dash"},
                },
            }
        )

        chart.set_legend({"position": "top"})
        chart.set_title(
            {
                "name": "ПОРІВНЯЛЬНА ДІАГРАММА АКТИВНОСТІ ГРИЗУНІВ ЗА РІК",
                "layout": {
                    "x": 0.1,
                    "y": 0.02,
                },
                "name_font": {"name": "Arial", "size": 12, "color": "#00CC00"},
            }
        )

        data = [
            [],
            [],
            [],
        ]

        for i in data_diagram:
            for key, value in i.items():
                data[0].append(key)
                data[1].append((value[0]))
                data[2].append((value[1]))

        legend = [
            ["Загальна кількість поїдання принади за місяць %"],
            ["Загальна кількість гризунів за місяць шт"],
        ]
        # if 48 >= row_last >= 37:
        #     row_last = 49

        self.s.write_column("A" + f"{row_last + 2}", data[0])
        self.s.write_column("B" + f"{row_last + 2}", data[1])
        self.s.write_column("C" + f"{row_last + 2}", data[2])
        self.s.write_column("D" + f"{row_last + 2}", legend[0])
        self.s.write_column("E" + f"{row_last + 2}", legend[1])

        chart.add_series(
            {
                "categories": [self.s.name, row_last + 1, 0, row_last + 12, 0],
                "values": [self.s.name, row_last + 1, 1, row_last + 12, 1],
                "name": [self.s.name, row_last + 1, 3],
                "data_labels": {"value": True},
                "line": {"color": "red"},
                "fill": {"color": "#FFFF33"},
                "border": {"color": "black"},
            }
        )

        chart.add_series(
            {
                "values": [self.s.name, row_last + 1, 2, row_last + 12, 2],
                "name": [self.s.name, row_last + 1, 4],
                "line": {"color": "red"},
                "data_labels": {"value": True},
                "fill": {"color": "#0080FF"},
                "border": {"color": "black"},
            }
        )
        self.s.insert_chart("A" + f"{row_last + 2}", chart)
        

        
    # открываем файл
    def create_file(self):

        # Генерируем Excel-файл
        excel_data = self.create_excel()

        # Формируем название файла
        filename = f"Звіт_{self._predpr}_{self._year}_{self._month}.xlsx"
        filename = filename.replace(" ", "_")  # Убираем пробелы для корректности

        # Создаём временный файл в папке temp
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, filename)

        # Записываем данные в файл
        with open(file_path, "wb") as f:
            f.write(excel_data)

        # Открываем файл
        webbrowser.open(file_path)
        main_cherz_zvit(self._predpr,self._month, self._year)

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

            # monse = st.selectbox("Місяць", ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"], index=int(datetime.today().month)-2, key="zvit_selekt")
            # year = st.number_input("Оберіть рік", min_value=2000, max_value=2100, value=current_year, step=1, key="number_input_zvit")

            # Проверка изменения данных
            # if monse != st.session_state["last_month"] or year != st.session_state["last_year"]:
            #     st.session_state["last_month"] = monse
            #     st.session_state["last_year"] = year
                
                # Кнопка для скачивания отчета
            try:
                
                st.download_button(
                    label="📥 Завантажити Excel",
                    data=Zvit(self._predpr, self._month, self._year).create_excel(),
                    file_name=f"Звіт_{self._predpr}_{self._month}_{self._year}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                st.session_state["show_form_zvit"] = not st.session_state["show_form_zvit"]
                main_cherz_zvit(self._predpr,self._month, self._year)


            except Exception:
                 st.warning("📭 Даних для звіту немає.")

if __name__ == "__main__":
    a = Zvit("ТОВ УКРЕЛЕВАТОРПРОМ І-ДІЛЯНКА", "02", "2025") 
    a.create_file()
    #"ТОВ 'М.В. КАРГО' ГОЛОВНА ТЕРІТОРІЯ", "11","2024" "ТОВ УКРЕЛЕВАТОРПРОМ І-ДІЛЯНКА", "02", "2025""ФГ ОРГАНІК СІСТЕМС ПІВНІЧНИЙ"