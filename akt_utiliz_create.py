from akti_utiliz import Akti_utiliz
import tkinter as tk
from tkinter import messagebox, ttk
import xlsxwriter
import io
import sql as bd
import os
import tempfile
import webbrowser
import streamlit as st
from datetime import datetime



class Akti_utiliz_create:

    MONTH = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    MES = {
        "12": "грудня",
        "01": "січня",
        "02": "лютого",
        "03": "березня",
        "04": "квітня",
        "05": "травня",
        "06": "червня",
        "07": "липня",
        "08": "серпня",
        "09": "вересня",
        "10": "жовтня",
        "11": "листопада",
    }
   

    

    
        
    def __init__(self, _predpr = "ТОВ 'АДМ'", _month = "11", _year = "2024"):
        self._predpr = _predpr
        self._month = _month
        self._year = _year
        self.book = None
        self.s = None
        self.a = Akti_utiliz(_predpr, _month, _year)
        self.filtered = [item for item in self.a.grizuni_vsego() if any(v != 0 for v in list(item.values())[0])]
       

    def create_excel(self):
        """Создаёт и возвращает Excel-файл в виде байтов"""
        if not self.filtered:
            return False
        output = io.BytesIO()
        self.book = xlsxwriter.Workbook(output)
        for i in self.filtered:
            self.s = self.book.add_worksheet(f"{int(list(i.keys())[0])}.{self._month}")
            self.s.set_column(0, 27, 2.6)  # тільки перші 30 колонок
            self.s.fit_to_pages(1, 1)
            self.s.set_portrait()
            self.s.set_margins(left=0.1, right=0.1, top=0.1, bottom=0.1)
            self.heder(i)

            # self.umovni_poznach()
     
        self.book.close()
        output.seek(0)
        return output.getvalue()
    
    
        
    def heder(self, date_grizuni):
        format_1 = self.book.add_format(
                    {
                        "border": 2,
                        "font_name": "Arial",
                        "font_size": 16,
                        "bold": True,
                        "fg_color": "#D7E4BC",
                        "align": "center",
                        "valign": "vcenter",
                        "text_wrap": True,
                        "shrink": True,
                    }
                )

        format_2 = self.book.add_format(
                    {
                        
                        "font_name": "Arial",
                        "font_size": 10,
                        "border": 2,
                        "fg_color": "#D7E4BC",
                        "align": "center",
                        "valign": "vcenter",
                        "text_wrap": True,
                        "shrink": True,
                    }
                )
        
        format_3 = self.book.add_format({
                'bold': False,
                'align': 'center',
                'valign': 'vcenter',
                'font_name': 'Calibri',
                'font_size': 12
            })
        
        format_4 = self.book.add_format({
                "border": 2,
                'bold': False,
                'align': 'center',
                'valign': 'vcenter',
                'font_name': 'Calibri',
                'font_size': 12,
                'text_wrap': True
            })

        log = self.s.insert_image(
            0, 0, "логотип укр.png", {"x_scale": 0.25, "y_scale": 0.25}
        )
        text = "67725 Одеська обл. Білгород - Дністровський р-н. с. Салгани, вул. Приморська, 57-А,  тел (04849) 99-2-99»\n" \
        "73025  Херсонське представництво: м. Херсон, вул. Воронцовська (Комунарів), 27, офіс 5, тел (0552)392-492\n" \
        "www.Dez-Eltor.com.ua, Email: Dez.eltor@gmail.com"

        self.s.merge_range(0, 0, 5, 4, log, format_1)
        self.s.merge_range(0, 5, 5, 28, "ПРИВАТНЕ ПІДПРИЄМСТВО \n «ДЕЗ-ЕЛЬТОР»", format_1)
        self.s.merge_range(6, 0, 8, 28, text, format_2 )
        self.s.merge_range(13, 0, 13, 28, f"АКТ УТИЛІЗАЦІЇ ГРИЗУНІВ № {int(list(date_grizuni.keys())[0])}/{self._month}",
            self.book.add_format({
                'bold': True,
                'align': 'center',
                'valign': 'vcenter',
                'font_name': 'Calibri',
                'font_size': 14
            })
        )

        self.s.merge_range(15, 0, 15, 28, f" від {int(list(date_grizuni.keys())[0])} {self.MES[self._month]} {self._year} року", format_3)
        self.s.merge_range(17, 0, 17, 28, f"Назва об'єкту: {self._predpr}",format_3)
        self.s.merge_range(19, 2, 22, 8, "ВИД ШКІДНИКА",format_4)
        self.s.merge_range(19, 9, 22, 17, "КІЛЬКІСТЬ (шт.)",format_4)
        self.s.merge_range(19, 18, 22, 27, "СПОСІБ УТИЛІЗАЦІЇ",format_4)
        def danie_v_tabl(vid_griz, kilkist, z, po):
            text = f"Згідно договору № 2435-У\n"\
            "з підрядною організацією" 
            self.s.merge_range(z, 2, po, 8, vid_griz,format_4)
            self.s.merge_range(z, 9, po, 17, kilkist,format_4)
            self.s.merge_range(z, 18, po, 27, text,format_4)

        misi = list(date_grizuni.values())[0][0]
        krisi = list(date_grizuni.values())[0][1]
        row_start = 23
        row_finish = 25
        for i in (("ПАЦЮК", krisi), ("МИША", misi)):
            if i[1] > 0:
                danie_v_tabl(i[0], i[1], row_start, row_finish)
                row_start += 3
                row_finish += 3
        self.s.merge_range(row_finish+6, 2, row_finish+6, 10, "Відповідальна особа")
        self.s.insert_image(
             row_finish, 12, "ПЕЧАТЬ-ПОДПИСЬ_png-removebg-preview.png", {"x_scale": 0.20, "y_scale": 0.21}
        )


    def main(self):
            
        if not self.create_excel():
            st.warning("📭 Даних для звіту немає.")
            return
        
            # Проверяем, если переменные ещё не существуют в session_state
        if "show_form_akt" not in st.session_state:
            st.session_state["show_form_akt"] = False

        if "last_month" not in st.session_state:
            st.session_state["last_month"] = None

        if "last_year" not in st.session_state:
            st.session_state["last_year"] = None

        # Кнопка для отображения/скрытия формы
        if st.button("📝 Генерація АКТУ УТИЛІЗАЦІЇ"):
            st.session_state["show_form_akt"] = not st.session_state["show_form_zvit"]

        # Если форма показывается
        if st.session_state["show_form_akt"]:
            current_year = datetime.today().year
                
                # Кнопка для скачивания отчета
            
                
            st.download_button(
                label="📥 Завантажити Excel",
                data=Akti_utiliz_create(self._predpr, self._month, self._year).create_excel(),
                file_name=f"Акт утилізації_{self._predpr}_{self._month}_{self._year}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            st.session_state["show_form_akt"] = not st.session_state["show_form_akt"]
            


            
                
    
    # def create_file(self):
            

    #     # Генерируем Excel-файл
    #     excel_data = self.create_excel()

    #     # Формируем название файла
    #     filename = f"Акт_утилізації_{self._predpr}_{self._month}_{self._year}.xlsx"
    #     filename = filename.replace(" ", "_")  # Убираем пробелы для корректности

    #     # Создаём временный файл в папке temp
    #     temp_dir = tempfile.gettempdir()
    #     file_path = os.path.join(temp_dir, filename)

    #     # Записываем данные в файл
    #     with open(file_path, "wb") as f:
    #         f.write(excel_data)

    #     # Открываем файл
    #     webbrowser.open(file_path)


if __name__ == "__main__":
    Akti_utiliz_create().create_file()