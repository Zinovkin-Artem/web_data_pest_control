# page_9_table_danix.py
import streamlit as st
import pandas as pd  # оставил, но в этой странице больше не используем
from datetime import date
from sql import show_pidpriemstvo, ckan_dk_tabl_rows, del_ckan_dk_many


def empty_table_data():
    # пустая “таблица” (список словарей)
    return []


def _init_defaults():
    today = date.today()
    st.session_state.setdefault("f_enterprise", "")
    st.session_state.setdefault("f_date_from", today)
    st.session_state.setdefault("f_date_to", today)
    st.session_state.setdefault("f_barrier", "ВСІ")
    st.session_state.setdefault("f_equipment", "")
    st.session_state.setdefault("pending_delete_ids", [])
    st.session_state.setdefault("show_n", 10)

    # источник данных = table_data (list[dict])
    st.session_state.setdefault("table_data", empty_table_data())
    st.session_state.setdefault("selected_ids", set())
    st.session_state.setdefault("visible_ids", [])


def _reset_filters():
    today = date.today()
    st.session_state["f_enterprise"] = ""
    st.session_state["f_date_from"] = today
    st.session_state["f_date_to"] = today
    st.session_state["f_barrier"] = "ВСІ"
    st.session_state["f_equipment"] = ""


@st.dialog("Підтвердження видалення")
def confirm_delete_dialog():
    n = len(st.session_state.get("pending_delete_ids", []))
    st.write(f"Ви дійсно хочете видалити **{n}** запис(ів) з бази даних?")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("✅ OK, видалити", width="stretch"):
            ids = [int(x) for x in st.session_state.get("pending_delete_ids", [])]

            deleted = del_ckan_dk_many(ids)  # удалили в БД

            # ✅ обновляем данные на странице: убираем удалённые строки из table_data
            idset = set(ids)
            st.session_state["table_data"] = [
                r for r in st.session_state.get("table_data", [])
                if int(r.get("id", 0)) not in idset
            ]

            # ✅ чистим выделения
            st.session_state["selected_ids"] = set()
            st.session_state["pending_delete_ids"] = []

            st.success(f"Видалено: {deleted} запис(ів)")
            st.rerun()

    with c2:
        if st.button("❌ Скасувати", width="stretch"):
            st.session_state["pending_delete_ids"] = []
            st.rerun()


def _on_editor_change():
    ed = st.session_state.get("editor_loaded", {})
    edited_rows = ed.get("edited_rows", {})
    visible_ids = st.session_state.get("visible_ids", [])
    selected_ids: set = st.session_state.get("selected_ids", set())

    for row_idx_str, changes in edited_rows.items():
        if "_select" in changes:
            row_idx = int(row_idx_str)
            if 0 <= row_idx < len(visible_ids):
                row_id = int(visible_ids[row_idx])
                if changes["_select"]:
                    selected_ids.add(row_id)
                else:
                    selected_ids.discard(row_id)

    st.session_state["selected_ids"] = selected_ids

def parse_equipment_input(s: str):
    s = (s or "").strip()
    if not s:
        return []

    nums = set()

    # разделяем по запятым
    parts = [p.strip() for p in s.split(",") if p.strip()]

    for part in parts:
        # диапазон: "5-12"
        if "-" in part:
            a, b = part.split("-", 1)
            a, b = a.strip(), b.strip()
            if a.isdigit() and b.isdigit():
                start, end = int(a), int(b)
                if start <= end:
                    for x in range(start, end + 1):
                        nums.add(x)
                else:
                    for x in range(end, start + 1):
                        nums.add(x)
        else:
            # одиночное число
            if part.isdigit():
                nums.add(int(part))

    return sorted(nums)




def show_page_9():
    # список предприятий
    PIDPRIEMSTVO = [""]
    _PIDPRIEMSTVO = show_pidpriemstvo()
    for i in _PIDPRIEMSTVO:
        PIDPRIEMSTVO.append(i[0])

    st.title("Таблиця даних")
    _init_defaults()

    # CSS: фиксируем ширины и обрезаем длинный текст
    st.markdown(
        """
        <style>
        div[data-testid="stDataFrame"] table { table-layout: fixed !important; width: 100% !important; }
        div[data-testid="stDataFrame"] th, div[data-testid="stDataFrame"] td {
            overflow: hidden !important; text-overflow: ellipsis !important;
            white-space: nowrap !important; max-width: 1px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ===== ФИЛЬТРЫ =====
    r1_col1, r1_col2, r1_col3 = st.columns([4, 1.5, 1.5])
    with r1_col1:
        _pidpr = st.selectbox("ПІДПРИЄМСТВО", PIDPRIEMSTVO, key="f_enterprise")
    with r1_col2:
        _date_z = st.date_input("ДАТА З", key="f_date_from")
    with r1_col3:
        _date_po = st.date_input("ДАТА ПО", key="f_date_to")

    r2_col1, r2_col2, r2_col3, r2_col4, r2_col5 = st.columns([2, 2, 1.4, 1.4, 1.6])
    with r2_col1:
        _barier = st.selectbox("БАРʼЄР", ["ВСІ", "I - II", "III"], key="f_barrier")
    with r2_col2:
        _namber_oblad = st.text_input("№ ОБЛАДНАННЯ", key="f_equipment")

    with r2_col3:
        if st.button("ВИВЕСТИ ДАНІ", width="stretch"):
            _numbers = parse_equipment_input(_namber_oblad)
            rows = ckan_dk_tabl_rows(_pidpr, _date_z, _date_po, _barier, _numbers)



            data = []
            for r in rows:
                data.append({
                    "_select": False,
                    "id": r[0],
                    "Дата": r[1].strftime("%Y-%m-%d %H:%M:%S") if r[1] else "",
                    "Підприємство": r[2] or "",
                    "№ Обладнання": r[3] if r[3] is not None else "",
                    "Значення": r[4] if r[4] is not None else "",
                    "Барʼєр": r[5] or "",
                })

            st.session_state["table_data"] = data
            st.session_state["selected_ids"] = set()
            st.rerun()

    with r2_col5:
        st.button("СКИНУТИ ФІЛЬТРИ", width="stretch", on_click=_reset_filters)

    # ===== ДАННЫЕ ДЛЯ ТАБЛИЦЫ (источник = table_data) =====
    table_data = st.session_state.get("table_data", [])
    total_rows = len(table_data)

    # ===== “Показати” зависит от количества строк =====
    if total_rows == 0:
        opts = [10]
        show_n = 10
    else:
        opts = [x for x in range(10, 101, 10) if x <= total_rows]
        if total_rows not in opts:
            opts.append(total_rows)
        opts = sorted(set(opts))
        if st.session_state["show_n"] not in opts:
            st.session_state["show_n"] = opts[0]
        show_n = min(int(st.session_state["show_n"]), total_rows)

    ncol1, ncol2 = st.columns([1.4, 2.6])
    with ncol1:
        st.selectbox("Показати", opts, key="show_n")
    with ncol2:
        st.caption(f"Показано на екрані: {min(show_n, total_rows)} з {total_rows}")

    # ===== то, что “на экране” = первые show_n строк =====
    view_rows = table_data[:show_n]
    st.session_state["visible_ids"] = [r["id"] for r in view_rows] if total_rows else []

    selected_ids: set = st.session_state["selected_ids"]

    # синхронизируем _select (чтобы не слетало)
    for r in view_rows:
        r["_select"] = (int(r["id"]) in selected_ids)

    # ===== КНОПКИ: выделить только “на экране” =====
    m1, m2 = st.columns([1, 1])
    with m1:
        if st.button("✅ ВИДІЛИТИ ВСІ (на екрані)", width="stretch", disabled=(total_rows == 0)):
            st.session_state["selected_ids"] = selected_ids.union(set(map(int, st.session_state["visible_ids"])))
            st.rerun()
    with m2:
        if st.button("❌ ЗНЯТИ ВСІ (на екрані)", width="stretch", disabled=(total_rows == 0)):
            st.session_state["selected_ids"] = selected_ids.difference(set(map(int, st.session_state["visible_ids"])))
            st.rerun()

    # ===== ТАБЛИЦА (всегда видна, но показывает только view_rows) =====
    st.data_editor(
        view_rows,
        key="editor_loaded",
        width="stretch",
        hide_index=True,
        height=420,
        on_change=_on_editor_change if total_rows else None,
        column_config={
            "_select": st.column_config.CheckboxColumn("✔", width="small"),
            "id": st.column_config.NumberColumn("id", width="small"),
            "Дата": st.column_config.TextColumn("Дата", width="small"),
            "Підприємство": st.column_config.TextColumn("Підприємство", width="medium"),
            "№ Обладнання": st.column_config.NumberColumn("№ Обл", width="small"),
            "Значення": st.column_config.TextColumn("Знач", width="small"),
            "Барʼєр": st.column_config.TextColumn("Бар", width="small"),
        },
        disabled=["id", "Дата", "Підприємство", "№ Обладнання", "Значення", "Барʼєр"],
    )

    # ===== УДАЛЕНИЕ (пока без БД) =====
    total_selected = len(st.session_state["selected_ids"])
    st.caption(f"Обрано рядків (всього): {total_selected}")

    with r2_col4:
        if st.button("ВИДАЛИТИ", width="stretch", disabled=(total_selected == 0)):
            st.session_state["pending_delete_ids"] = sorted(list(st.session_state["selected_ids"]))
            confirm_delete_dialog()
