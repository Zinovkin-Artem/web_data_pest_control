import ftplib
import streamlit as st
from io import BytesIO

def show_page_4():

 


    # Параметры FTP-сервера
    ftp_host = '195.138.73.12'
    ftp_port = 21
    ftp_username = 'ln'
    ftp_password = 'lala280508'
    folders = ["/o", "/Пацанам нещего делать", "/фотки", "/Фотки мои!", "/перед экзаменом", "/Images"]  # Список папок

    # Функция для подключения к FTP
    def connect_ftp():
        ftp = ftplib.FTP()
        ftp.connect(ftp_host, ftp_port)
        ftp.login(ftp_username, ftp_password)
        ftp.set_pasv(False)
        return ftp

    # Функция для загрузки файла
    def read_file(ftp, filename):
        file_data = BytesIO()
        ftp.retrbinary(f'RETR {filename}', file_data.write)
        file_data.seek(0)
        return file_data

    # Фильтрация изображений
    image_extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp")

    # Подключаемся к FTP
    ftp = connect_ftp()

    # Переменная состояния для скрытия фото
    if "opened_folders" not in st.session_state:
        st.session_state["opened_folders"] = {}
    if "show_images" not in st.session_state:
        st.session_state["show_images"] = {}

    # Отображаем папки в четыре колонки с одинаковыми кнопками
    cols = st.columns(4)
    for idx, folder in enumerate(folders):
        with cols[idx % 4]:
            if st.button(f"📂 {folder}", key=f"folder_{folder}", help="Нажмите, чтобы открыть/закрыть папку"):
                st.session_state["opened_folders"][folder] = not st.session_state["opened_folders"].get(folder, False)
                # При закрытии папки скрываем все изображения внутри нее
                if not st.session_state["opened_folders"][folder]:
                    st.session_state["show_images"][folder] = {}

    # Отображение содержимого папок под соответствующими папками
    for idx, folder in enumerate(folders):
        if st.session_state["opened_folders"].get(folder, False):
            with cols[idx % 4]:
                st.subheader(f"📁 {folder}")
                ftp.cwd(folder)
                files = ftp.nlst()  # Получаем список файлов
                image_files = [file for file in files if file.lower().endswith(image_extensions)]  # Фильтруем изображения

                if not image_files:
                    st.write("Нет изображений в этой папке.")
                else:
                    for img_file in image_files:
                        if st.button(f"📷 Просмотреть {img_file}", key=f"view_{folder}_{img_file}"):
                            if folder not in st.session_state["show_images"]:
                                st.session_state["show_images"][folder] = {}
                            st.session_state["show_images"][folder][img_file] = not st.session_state["show_images"][folder].get(img_file, False)

                        if st.session_state["show_images"].get(folder, {}).get(img_file, False):
                            img_data = read_file(ftp, img_file)
                            st.image(img_data, caption=img_file, use_container_width=True)

                            # Кнопка для скачивания
                            st.download_button(
                                label=f"📥 Скачать {img_file}",
                                data=img_data,
                                file_name=img_file,
                                mime="image/jpeg",
                                key=f"download_{folder}_{img_file}"
                            )

    ftp.quit()






   