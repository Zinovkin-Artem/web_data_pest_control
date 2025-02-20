import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import sql
import openai  # Для запроса в ИИ
from datetime import datetime

# Создаём клиента OpenAI
client = openai.OpenAI(api_key="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")

def diagramma(_pred):
    data = sql.diagr_tretiy_how_mishi(_pred)

    months = sorted([i[0] for i in data], key=lambda date: datetime.strptime(date, "%m.%Y"))

    st.markdown("<h3 style='text-align: center;'>Виберіть діапазон дат:</h3>", unsafe_allow_html=True)

    selected_range = st.select_slider(
        "Виберіть необхідний діапазон", 
        options=months, 
        value=("07.2023", months[-1]), 
        label_visibility="collapsed"
    )

    start_idx = months.index(selected_range[0])
    end_idx = months.index(selected_range[1]) + 1
    filtered_data = [entry for entry in data if entry[0] in months[start_idx:end_idx]]

    labels = [entry[0] for entry in filtered_data]
    values1 = [entry[1] for entry in filtered_data]  # Поедание приманки (%)
    values2 = [entry[2] for entry in filtered_data]  # Количество грызунов (шт)

    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(labels))
    width = 0.4

    bars1 = ax.bar(x - width/2, values1, width=width, label="Поедание приманки (%)", color='blue', alpha=0.7)
    ax.bar_label(bars1, padding=3, fontsize=10, color='black')

    bars2 = ax.bar(x + width/2, values2, width=width, label="Количество грызунов (шт)", color='orange', alpha=0.7)
    ax.bar_label(bars2, padding=3, fontsize=10, color='black')

    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45)
    ax.set_ylabel("Значення")
    ax.set_title("ПОРІВНЯЛЬНА ДІАГРАММА АКТИВНОСТІ ГРИЗУНІВ")
    ax.legend()

    st.pyplot(fig)

    # КНОПКА АНАЛИЗА ОТ ИИ
    if st.button("Получить анализ"):
        prompt = f"""
        У нас есть данные о популяции грызунов и потреблении приманки за разные месяцы.
        Данные:
        {[(l, v1, v2) for l, v1, v2 in zip(labels, values1, values2)]}
        
        - Поедание приманки выражено в процентах.
        - Количество грызунов указано в штуках.

        Проанализируй:
        1. Как изменяется активность грызунов?
        2. Есть ли сезонные тренды?
        3. Как потребление приманки связано с числом грызунов?
        4. Какой прогноз можно сделать на ближайшие месяцы?
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )

            st.markdown("### 📊 Анализ и прогноз от ИИ:")
            st.write(response.choices[0].message.content)

        except Exception as e:
            st.error(f"Ошибка при запросе к ИИ: {e}")

if __name__ == "__main__":
    diagramma("ТОВ 'АДМ'")
