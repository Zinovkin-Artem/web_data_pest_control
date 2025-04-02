import streamlit as st
import os
import hashlib
from pathlib import Path

def show_page_4(_predpr):

    # === Функция для генерации уникального ключа на основе MD5-хеша имени папки ===
    def generate_key(name):
        """Генерирует безопасный ключ на основе MD5-хеша имени папки"""
        return hashlib.md5(name.encode("utf-8", "surrogateescape")).hexdigest()

    # === Функция для получения списка папок и файлов в указанном пути ===
    def list_directory(path):
        """Сканирует указанную директорию и возвращает списки папок и файлов"""
        folders = []  # Список для папок
        files = []    # Список для файлов
        try:
            for item in Path(path).iterdir():  # Перебираем все элементы в директории
                if item.is_dir():  
                    folders.append(item.name)  # Если это папка — добавляем в список папок
                else:
                    files.append(item.name)  # Если это файл — добавляем в список файлов
        except Exception as e:
            st.error(f"Ошибка доступа к файлам: {e}")  # Выводим ошибку, если нет доступа к директории
        
        return sorted(folders, key=str.casefold), sorted(files, key=str.casefold)  # Возвращаем отсортированные списки

    # === Основная функция для отображения файлового браузера ===
    def show_file_browser(base_url, root_folder):
        """Отображает файловый браузер с возможностью раскрытия папок и скачивания файлов"""
        
        # Инициализируем состояние для отслеживания открытых папок
        if "opened_folders" not in st.session_state:
            st.session_state["opened_folders"] = {}

        # Вложенная функция для рекурсивного отображения папок и файлов
        def display_folder(path, relative_path=""):
            """Рекурсивно отображает папки и файлы"""
            folders, files = list_directory(path)  # Получаем списки папок и файлов
            
            
            # === Отображение папок ===
            for folder in folders:
                folder_key = generate_key(f"{relative_path}/{folder}")  # Создаем уникальный ключ для папки
                is_open = st.session_state["opened_folders"].get(folder_key, False)  # Проверяем, открыта ли папка

                # Создаем кнопку для раскрытия папки
                if st.button(f"📂 {folder}", key=folder_key):
                    st.session_state["opened_folders"][folder_key] = not is_open  # Переключаем состояние папки
                    
                # Если папка открыта, рекурсивно отображаем её содержимое
                if st.session_state["opened_folders"].get(folder_key, False):
                    display_folder(Path(path) / folder, relative_path=os.path.join(relative_path, folder))
            
            # === Отображение файлов ===
            for file in files:
                # Корректируем возможные ошибки с кодировкой
                file_safe = file.encode("utf-8", "surrogateescape").decode("utf-8", "surrogateescape")

                # Формируем URL-адрес для скачивания файлов
                file_url = f"{base_url}/{_predpr}/{relative_path}/{file_safe}".replace("//", "/")
                file_url = file_url.replace("https:/", "https://")  # Исправляем двойной слеш в URL
                
                # Если файл PDF, создаем ссылку для открытия в браузере
                if file.lower().endswith(".pdf"):
                    st.markdown(f'<a href="{file_url}" target="_blank">📄 {file_safe}</a>', unsafe_allow_html=True)
                
        
        display_folder(root_folder)  # Запускаем отображение файлов с корневой папки

    # === Интерфейс Streamlit ===
    st.title("📂 Файловый Браузер через HTTPS")

    # Базовый URL для скачивания файлов
    base_url = "https://app.dez-eltor.com.ua/files"

    # Корневая папка для отображения файлов
    root_folder = f"/home/ftpuser/doki_streamlit/{_predpr}"

    # Запускаем файловый браузер
    show_file_browser(base_url, root_folder)








    # def generate_key(name):
    #     """Генерирует безопасный ключ на основе MD5-хеша имени папки"""
    #     return hashlib.md5(name.encode("utf-8", "ignore")).hexdigest()

    # def list_directory(path):
    #     folders = []
    #     files = []
    #     try:
    #         for item in os.listdir(path):
    #             full_path = os.path.join(path, item)
    #             if os.path.isdir(full_path):
    #                 folders.append(item)
    #             else:
    #                 files.append(item)
    #     except Exception as e:
    #         st.error(f"Ошибка доступа к файлам: {e}")
    #     return folders, files

    # def show_file_browser(base_url, root_folder):
    #     if "opened_folders" not in st.session_state:
    #         st.session_state["opened_folders"] = {}

    #     def display_folder(path, relative_path=""):
    #         folders, files = list_directory(path)
            
    #         for folder in folders:
    #             folder_key = generate_key(f"{relative_path}/{folder}")
    #             if st.button(f"📂 {folder}", key=folder_key):
    #                 st.session_state["opened_folders"][folder_key] = not st.session_state["opened_folders"].get(folder_key, False)
                
    #             if st.session_state["opened_folders"].get(folder_key, False):
    #                 display_folder(os.path.join(path, folder), relative_path=f"{relative_path}/{folder}")
            
    #         for file in files:
    #             file_url = f"{base_url}/{relative_path}/{file}".replace("//", "/")
    #             file_url = file_url.replace("https:/", "https://")  # Исправляем двойной домен
    #             if file.lower().endswith(".pdf"):
    #                 st.markdown(f'<a href="{file_url}" target="_blank">📄 {file}</a>', unsafe_allow_html=True)
    #             else:
    #                 st.download_button(label=f"📄 {file}", data="", file_name=file, key=file_url)
        
    #     display_folder(root_folder)

    # st.title("Файловый Браузер через HTTPS")

    # base_url = "https://app.dez-eltor.com.ua/files"
    # root_folder = "/home/ftpuser/doki_streamlit"

    # show_file_browser(base_url, root_folder)








