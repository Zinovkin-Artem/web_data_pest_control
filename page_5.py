import os
import uuid
import streamlit as st
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import smtplib
from fpdf import FPDF  # для створення PDF
import sql


SAVE_FOLDER = "/var/www/dez-eltor-foto"
PUBLIC_URL_PREFIX = "https://app.dez-eltor.com.ua/foto_massege"

os.makedirs(SAVE_FOLDER, exist_ok=True)


def clear_inputs():
    st.session_state["topic"] = ""
    st.session_state["message"] = ""


def send_email(to_email_row: str, subject, message, _url, attachments=None):
    if "," in to_email_row:
        to_email = to_email_row.split(",")[0].strip()
        cc_email = to_email_row.split(",")[1].strip()
    else:
        to_email = to_email_row.strip()
        cc_email = None

    smtp_host = "mail.adm.tools"
    smtp_port = 587
    sender_email = "dez-eltor.message@dez-eltor.com.ua"
    sender_password = "Lala280508"

    email_body = f"{message}\nОзнайомитись з повідомленнями можна на сторінці {_url} в розділі повідомлення:"

    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(email_body, "plain"))

        recipients = [to_email]
        if cc_email:
            msg["Cc"] = cc_email
            recipients.append(cc_email)

        if attachments:
            for path in attachments:
                with open(path, "rb") as f:
                    image = MIMEImage(f.read())
                    image.add_header("Content-Disposition", "attachment", filename=os.path.basename(path))
                    msg.attach(image)

        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipients, msg.as_string())
        server.quit()
        st.success(f"✅ Лист відправлено на {to_email}")

    except Exception as e:
        st.error(f"❌ Помилка при надсиланні: {e}")


def generate_pdf(topic, date, message_text):
    font_path = "DejaVuSansMono.ttf"
    if not os.path.exists(font_path):
        st.error("❌ Шрифт не знайдено.")
        return None

    pdf = FPDF()
    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("DejaVu", size=12)

    # Заголовок (звичайний шрифт)
    pdf.set_font("DejaVu", size=14)
    pdf.cell(0, 10, f"{topic}", ln=True, align='L')
    pdf.set_font("DejaVu", size=11)
    pdf.cell(0, 8, f"Дата: {date}", ln=True)
    pdf.ln(5)

    # Основний текст
    for line in message_text.strip().split('\n'):
        line = line.strip()
        if line:
            pdf.multi_cell(0, 7, line)
        else:
            pdf.ln(3)

    # Зберігаємо
    temp_path = f"/tmp/{uuid.uuid4().hex}.pdf"
    pdf.output(temp_path)
    return temp_path

def show_page_5(predpriyatie, is_admin):
     

    _messages = sql.data_masege_blog(predpriyatie)
    messages = _messages[::-1][:150]

    __predpriyatie = "ПАТ «АДМ ІЛЛІЧІВСЬК»" if predpriyatie == "ТОВ 'АДМ'" else predpriyatie

    st.subheader(f"📢 ПОВІДОМЛЕННЯ {__predpriyatie} 📢")

    if is_admin:
        if "topic" not in st.session_state:
            st.session_state["topic"] = ""
        if "message" not in st.session_state:
            st.session_state["message"] = ""

        st.subheader("✍️ Створити нове повідомлення")

        topic = st.text_input("📌 Тема")
        message = st.text_area("💬 Повідомлення")

        uploaded_files = st.file_uploader(
            "📎 Додайте фото", type=["jpg", "jpeg", "png", "pdf"], accept_multiple_files=True
        )

        saved_paths = []
        public_links = []

        if uploaded_files:
            for uploaded_file in uploaded_files:
                file_ext = uploaded_file.name.split(".")[-1]
                unique_name = f"{uuid.uuid4().hex}.{file_ext}"
                save_path = os.path.join(SAVE_FOLDER, unique_name).replace("\\", "/")
                

                try:
                    with open(save_path, "wb") as f:
                        file_data = uploaded_file.getvalue()
                        f.write(file_data)
                        f.flush()
                        os.fsync(f.fileno())
                        print(f"[DEBUG] Файл записано, існує? {os.path.exists(save_path)}")
                    saved_paths.append(save_path)
                    public_links.append(f"{PUBLIC_URL_PREFIX}/{unique_name}")
                except Exception as e:
                    st.error(f"❌ Не вдалося зберегти файл: {e}")

        if st.button("💾 Зберегти і надіслати повідомлення"):
            if topic and message:
                blog_url = "https://app.dez-eltor.com.ua/"
                current_time = datetime.now().strftime('%Y-%m-%d')

                sql.zapis_masege_blog(
                    _pred=predpriyatie,
                    title=topic,
                    masage=message,
                    time=current_time,
                    file_path=";".join(public_links)
                )

                if _messages:
                    _email = _messages[-1][-1].strip()
                else:
                    _email = sql.get_email(predpriyatie)[-1][-1].strip()

                send_email(_email, topic, message, blog_url, attachments=saved_paths)

                st.success("✅ Повідомлення збережено та відправлено!")
                clear_inputs()
                st.rerun()
            else:
                st.warning("⚠️ Заповніть усі поля.")

    if messages:
        # Використовуємо enumerate для унікальних ключів
        for idx, (date, topic, text, image_path, *arg) in enumerate(messages):
            st.markdown(f"### {topic}")
            st.caption(f"🕒 {date.date().strftime('%d-%m-%Y')}")
            st.write(text)

            # Кнопка для генерації та завантаження PDF
            pdf_btn_label = f"📄 Згенерувати повідомлення '{topic}' у PDF"
            if st.button(pdf_btn_label, key=f"pdf_{idx}"):
                pdf_path = generate_pdf(topic, date.date().strftime('%d-%m-%Y'), text)
                if pdf_path:
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            label="⬇️ Завантажити PDF",
                            data=f,
                            file_name=f"{topic}.pdf",
                            mime="application/pdf",
                        )

            if image_path:
                for path in image_path.split(";"):
                    clean_path = path.strip().replace("\\", "/")
                    if clean_path:
                        st.markdown(f"[📸 Переглянути зображення]({clean_path})")
            st.markdown("---")
    else:
        st.info("💡 ПОВІДОМЛЕННЯ ПОКИ ВІДСУТНІ")
