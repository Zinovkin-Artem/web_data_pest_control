import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from datetime import date
from sql import show_pidpriemstvo, write_scan_dk


def show_page_8():
    # =========================================================
    # 1) Определяем ширину экрана (телефон / не телефон)
    # =========================================================
    if "is_mobile" not in st.session_state:
        st.session_state.is_mobile = False

    st.markdown("""
    <script>
    const w = window.innerWidth;
    const isMobile = w < 900;
    const url = new URL(window.location);
    url.searchParams.set("mobile", isMobile ? "1" : "0");
    window.history.replaceState({}, "", url);
    </script>
    """, unsafe_allow_html=True)

    mobile_q = st.query_params.get("mobile", ["0"])[0]
    st.session_state.is_mobile = (mobile_q == "1")

    # =========================================================
    # 2) Размеры кнопок (на мобиле меньше)
    # =========================================================
    if st.session_state.is_mobile:
        BTN_W = 150
        BTN_H = 78
        GRID_COLS = 2
        GAP = "small"
        LOG_H = 260
    else:
        BTN_W = 220
        BTN_H = 90
        GRID_COLS = 4
        GAP = "small"
        LOG_H = 370

    # =========================================================
    # 3) CSS
    # =========================================================
    st.markdown(f"""
    <style>
    .banner{{
      background:#1d3cff;color:#fff;font-size:22px;font-weight:900;
      padding:10px 16px;border-radius:6px;border:2px solid #0b1fb8;
      display:inline-block;
    }}

    .km-header{{
        font-weight:900;
        font-size:14px;
        height:18px;
        line-height:18px;
        margin:0 0 4px 0;
    }}

    .left-yellow{{
      background:#ffea00;border:2px solid #c9b800;border-radius:6px;
      padding:8px;height: {LOG_H + 50}px;
    }}

    .log-title{{font-weight:900;margin-bottom:4px;}}

    .log-box{{
      height:{LOG_H}px; overflow-y:auto;
      background:rgba(255,255,255,0.45);
      border:2px solid rgba(0,0,0,0.25);
      border-radius:8px; padding:6px;
      font-family:Consolas, monospace; font-size:12px; line-height:1.2;
      white-space:pre-wrap;
    }}

    /* --- K/M блоки: только цифра + кнопки --- */
    .km-value {{
      width:48px;
      height:34px;
      border:2px solid rgba(0,0,0,0.25);
      border-radius:8px;
      background:#f2f2f2;
      display:flex;
      align-items:center;
      justify-content:center;
      font-weight:900;
      font-size:16px;
    }}

    /* --- мини-окно ввода количества --- */
    .rodent-value {{
      width:70px;
      height:40px;
      border:2px solid rgba(0,0,0,0.25);
      border-radius:10px;
      background:#fff;
      display:flex;
      align-items:center;
      justify-content:center;
      font-weight:900;
      font-size:18px;
    }}
    </style>
    """, unsafe_allow_html=True)

    # =========================================================
    # 4) STATE
    # =========================================================
    if "current_container" not in st.session_state:
        st.session_state.current_container = 1
    if "log_lines" not in st.session_state:
        st.session_state.log_lines = {}
    if "log_lines_sql" not in st.session_state:
        st.session_state.log_lines_sql = {}

    def log(txt: str):
        st.session_state.log_lines[st.session_state.current_container] = txt
    
    def log_from_sql(txt: str):
        st.session_state.log_lines_sql[st.session_state.current_container] = txt

    if "k_val" not in st.session_state:
        st.session_state.k_val = 0
    if "m_val" not in st.session_state:
        st.session_state.m_val = 0

    # --- мини-окно для Миша/Криса ---
    if "rodent_active" not in st.session_state:
        st.session_state.rodent_active = False
    if "rodent_type" not in st.session_state:
        st.session_state.rodent_type = ""
    if "rodent_qty" not in st.session_state:
        st.session_state.rodent_qty = 1

    LOCK_UI = st.session_state.rodent_active

    # --- флаги уведомлений (чтобы переживали st.rerun) ---
    if "toast_ok" not in st.session_state:
        st.session_state.toast_ok = False
    if "toast_err" not in st.session_state:
        st.session_state.toast_err = ""

    # --- показать уведомления после rerun ---
    if st.session_state.toast_ok:
        st.success("✅ Записано")
        st.session_state.toast_ok = False

    if st.session_state.toast_err:
        st.error(st.session_state.toast_err)
        st.session_state.toast_err = ""


    # =========================================================
    # 5) Header
    # =========================================================
    h1, h2, h3, h4 = st.columns([3.2, 1.2, 1, 1.6])
    with h1:

        spisok_predpriyatiy = [" ",]
        _PIDPRIEMSTVO = show_pidpriemstvo()
        for i in _PIDPRIEMSTVO:
            spisok_predpriyatiy.append(i[0])
           
        pidpr = st.selectbox("ПІДПРИЄМСТВО", spisok_predpriyatiy, disabled=LOCK_UI)
    with h2:
        _date = st.date_input("ДАТА", value=date.today(), format="DD-MM-YYYY", disabled=LOCK_UI)
    with h3:
        barier = st.selectbox("БАР'ЄР", [" ", "I - II", "III"], disabled=LOCK_UI)
    with h4:
        c_inp, c_btn = st.columns([4, 1], gap="small")
        with c_inp:
            container_txt = st.text_input("№ КОНТЕЙНЕРУ", key="container_input", disabled=LOCK_UI)
        with c_btn:
            st.write("")
            with stylable_container(
                key="wrap_small_submit",
                css_styles="""
                div[data-testid="stButton"]{
                    display:flex;
                    justify-content:flex-start;
                    align-items:flex-end;
                }
                button{
                    width:70px !important;
                    height:32px !important;
                    padding:0 !important;
                    font-size:12px !important;
                    font-weight:800 !important;
                    border-radius:8px !important;
                    border:2px solid #222 !important;
                }
                """
            ):
                if st.button("ВВОД", key="container_submit", disabled=LOCK_UI):
                    val = container_txt.strip()
                    if val.isdigit():
                        st.session_state.current_container = max(1, int(val))
                                           
                        # log(f"перейшли на контейнер №{st.session_state.current_container}")
                    else:
                       pass
                    st.rerun()

    st.write("")

    # =========================================================
    # 6) Баннер + K + M
    # =========================================================
    def km_block(btn_prefix: str, state_key: str, plus_key: str, minus_key: str):
        c_val, c_btn = st.columns([0.55, 1.1], gap="small")

        with c_val:
            st.markdown(f'<div class="km-value">{int(st.session_state[state_key])}</div>', unsafe_allow_html=True)

        with c_btn:
            p1, p2 = st.columns(2, gap="small")

            with p1:
                with stylable_container(
                    key=f"wrap_{plus_key}",
                    css_styles="""
                    button{
                        width:44px !important;
                        height:32px !important;
                        padding:0 !important;
                        font-size:12px !important;
                        font-weight:900 !important;
                        border-radius:8px !important;
                        border:2px solid #222 !important;
                    }"""
                ):
                    if st.button(f"{btn_prefix}+", key=plus_key, disabled=LOCK_UI):
                        st.session_state[state_key] = min(99, st.session_state[state_key] + 1)
                        st.rerun()

            with p2:
                with stylable_container(
                    key=f"wrap_{minus_key}",
                    css_styles="""
                    button{
                        width:44px !important;
                        height:32px !important;
                        padding:0 !important;
                        font-size:12px !important;
                        font-weight:900 !important;
                        border-radius:8px !important;
                        border:2px solid #222 !important;
                    }"""
                ):
                    if st.button(f"{btn_prefix}-", key=minus_key, disabled=LOCK_UI):
                        st.session_state[state_key] = max(0, st.session_state[state_key] - 1)
                        st.rerun()

    b1, b2, b3 = st.columns([3.6, 1.35, 1.35], gap="small")

    with b1:
        st.markdown(
            f'<div class="banner">значення контейнера №{st.session_state.current_container}</div>',
            unsafe_allow_html=True
        )

    with b2:
        st.markdown('<div class="km-header">Гризуни на території</div>', unsafe_allow_html=True)
        km_block("K", "k_val", "k_plus", "k_minus")

    with b3:
        st.markdown('<div class="km-header">&nbsp;</div>', unsafe_allow_html=True)
        km_block("M", "m_val", "m_plus", "m_minus")

    st.write("")

    # =========================================================
    # 7) Универсальная кнопка (фикс ширина/высота)
    # =========================================================
    def ui_button(label: str, key: str, bg: str, allow_wrap: bool = False, disabled: bool = False) -> bool:
        wrap = "normal" if allow_wrap else "nowrap"
        with stylable_container(
            key=f"wrap_{key}",
            css_styles=f"""
            div[data-testid="stButton"] {{
              display:flex;
              justify-content:center;
            }}
            button {{
              width:{BTN_W}px !important;
              height:{BTN_H}px !important;
              background:{bg} !important;
              color:white !important;
              font-size: 18px !important;
              font-weight:900 !important;
              border-radius:12px !important;
              border:3px solid #222 !important;
              white-space:{wrap} !important;
              text-align:center !important;
              line-height:1.05 !important;
              padding:6px 8px !important;
            }}
            button:hover{{filter:brightness(1.1);}}
            """
        ):
            return st.button(label, key=key, disabled=disabled)

    action = False

    # =========================================================
    # 8) Данные кнопок
    # =========================================================
    value_buttons = [
        "0", "25", "50", "75",
        "100", "інша", "НД", "Миша",
        "Криса", "Відсутній", "НВ"
    ]
    ctrl_buttons = ["Повернутися -", "Повернутися +", "Видалити", "Зберегти"]

    # =========================================================
    # 9) ЛОГ
    # =========================================================
    def render_log():
        # txt = "\n".join(st.session_state.log_lines[-120:])

        vals = list(st.session_state.log_lines.values())[::-1]   # берём значения и разворачиваем (новые сверху)
        txt = "\n".join(map(str, vals[:120]))                    # каждое значение -> отдельная строка

        st.markdown(
            f"""
            <div class="left-yellow">
              <div class="log-title">Лог вводу</div>
              <div class="log-box">{txt if txt else "—"}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # =========================================================
    # 10) Разная раскладка для телефона и ПК
    # =========================================================
    if st.session_state.is_mobile:
        render_log()
        st.write("")

        cols_count = GRID_COLS
        for i in range(0, len(value_buttons), cols_count):
            row = value_buttons[i:i + cols_count]
            cols = st.columns(cols_count, gap=GAP)
            for j, lab in enumerate(row):
                with cols[j]:
                    if lab in ("Миша", "Криса"):
                        if ui_button(lab, f"g_m_{i+j}", "#0b6b0b", disabled=LOCK_UI):
                            st.session_state.rodent_active = True
                            st.session_state.rodent_type = lab
                            st.session_state.rodent_qty = 1
                            st.rerun()
                    else:
                        if ui_button(lab, f"g_m_{i+j}", "#0b6b0b", disabled=LOCK_UI):
                            log(f"конт. №{st.session_state.current_container} = {lab}")
                            log_from_sql(lab)
                            action = True

        st.write("")
        for i in range(0, len(ctrl_buttons), cols_count):
            row = ctrl_buttons[i:i + cols_count]
            cols = st.columns(cols_count, gap=GAP)
            for j, lab in enumerate(row):
                with cols[j]:
                    if ui_button(lab, f"p_m_{i+j}", "#7a1fa2", allow_wrap=True, disabled=LOCK_UI):
                        if lab == "Повернутися -":
                            st.session_state.current_container = max(1, st.session_state.current_container - 1)
                            # log(f"перейшли на контейнер №{st.session_state.current_container}")
                        elif lab == "Повернутися +":
                            st.session_state.current_container += 1
                            # log(f"перейшли на контейнер №{st.session_state.current_container}")
                        elif lab == "Видалити":
                            # log(f"очистили контейнер №{st.session_state.current_container}")
                            pass
                        else:
                            # log("ЗБЕРЕГТИ натиснуто (далі буде БД)")
                            pass
                        action = True
    else:
        left, right = st.columns([1.4, 3.6])

        with left:
            render_log()

        with right:
            rows = [
                ["0", "25", "50", "75"],
                ["100", "ІН", "НД", "Миша"],
                ["Криса", "Відсутній", "НВ", ""]
            ]

            for r, row in enumerate(rows):
                cols = st.columns(4, gap=GAP)
                for c, lab in enumerate(row):
                    with cols[c]:
                        if lab != "":
                            if lab in ("Миша", "Криса"):
                                if ui_button(lab, f"g_{r}_{c}", "#0b6b0b", disabled=LOCK_UI):
                                    st.session_state.rodent_active = True
                                    st.session_state.rodent_type = lab
                                    st.session_state.rodent_qty = 1
                                    
                                    st.rerun()
                                    
                            else:
                                if ui_button(lab, f"g_{r}_{c}", "#0b6b0b", disabled=LOCK_UI):
                                    
                                    log(f"конт. №{st.session_state.current_container} = {lab}")
                                    log_from_sql(lab)
                                    st.session_state.current_container +=1
                                    action = True

            st.write("")
            ctrl = st.columns(4, gap=GAP)
            for i, lab in enumerate(ctrl_buttons):
                with ctrl[i]:
                    if ui_button(lab, f"p_{i}", "#7a1fa2", allow_wrap=True, disabled=LOCK_UI):
                        if lab == "Повернутися -":
                            st.session_state.current_container = max(1, st.session_state.current_container - 1)
                            # log(f"перейшли на контейнер №{st.session_state.current_container}")
                        elif lab == "Повернутися +":
                            st.session_state.current_container += 1
                            # log(f"перейшли на контейнер №{st.session_state.current_container}")
                        elif lab == "Видалити":
                            st.session_state.log_lines.pop(st.session_state.current_container, None)
                            # log(f"очистили контейнер №{st.session_state.current_container}")
                        else:
                            # --- проверки обязательных полей ---
                            if (not pidpr) or (pidpr.strip() == "") or (pidpr.strip() == " "):
                                st.session_state.toast_err = "Заповніть поле: ПІДПРИЄМСТВО"
                                action = True
                                continue

                            if (not barier) or (barier.strip() == "") or (barier.strip() == " "):
                                st.session_state.toast_err = "Заповніть поле: БАР'ЄР"
                                action = True
                                continue

                            _date_str = _date.strftime("%d-%m-%Y")

                            a = write_scan_dk(pidpr,
                                           st.session_state.log_lines_sql,
                                           st.session_state.k_val,
                                           st.session_state.m_val,
                                           _date_str, barier
                                          )

                            # --- если дошли сюда — считаем, что успешно ---
                            st.session_state.toast_ok = True
                            if a[1]:
                                st.session_state.toast_err = f"контейнери {a[1]} не записані в базу"
                                action = True
                            
                            

                            st.session_state.log_lines = {}
                            st.session_state.log_lines_sql = {}
                            st.session_state.current_container = 1
                            st.session_state.k_val = 0
                            st.session_state.m_val = 0
                        action = True

    # =========================================================
    # 10.5) Мини-окно (внизу) — + / - / ВВОД / СКАСУВАТИ
    # =========================================================
    if st.session_state.rodent_active:
        st.markdown(f"Введіть кількість: **{st.session_state.rodent_type}**")

        a, b, c, d, e = st.columns([1.0, 1.4, 1.4, 1.6, 1.8], gap="small")

        with a:
            st.markdown(f'<div class="rodent-value">{int(st.session_state.rodent_qty)}</div>', unsafe_allow_html=True)

        # ВАЖНО: делаем + / - шириной 100px и пробиваем цвет всем вложенным элементам
        plusminus_css_100 = """
        div[data-testid="stButton"]{ display:flex; justify-content:flex-start; }

        button{
            width:100px !important;
            height:40px !important;
            padding:0 !important;
            border-radius:10px !important;
            border:2px solid #222 !important;
            background:#7a1fa2 !important;

            color:#ffffff !important;
            -webkit-text-fill-color:#ffffff !important;

            display:flex !important;
            align-items:center !important;
            justify-content:center !important;
            line-height:1 !important;
            font-size:28px !important;
            font-weight:900 !important;
        }

        button *{
            color:#ffffff !important;
            -webkit-text-fill-color:#ffffff !important;
            fill:#ffffff !important;
        }

        button:focus, button:focus-visible{
            outline:none !important;
            box-shadow:none !important;
        }
        """

        with b:
            with stylable_container(key="rodent_plus_wrap", css_styles=plusminus_css_100):
                # полноширинный символ "＋" виднее, чем "+"
                if st.button("＋", key="rodent_plus"):
                    st.session_state.rodent_qty = min(99, int(st.session_state.rodent_qty) + 1)
                    st.rerun()

        with c:
            with stylable_container(key="rodent_minus_wrap", css_styles=plusminus_css_100):
                # полноширинный символ "－" виднее, чем "-"
                if st.button("－", key="rodent_minus"):
                    st.session_state.rodent_qty = max(0, int(st.session_state.rodent_qty) - 1)
                    st.rerun()

        with d:
            with stylable_container(
                key="rodent_enter_wrap",
                css_styles="""
                div[data-testid="stButton"]{display:flex; justify-content:flex-start;}
                button{
                    width:140px !important;
                    height:40px !important;
                    padding:0 !important;
                    font-size:14px !important;
                    font-weight:900 !important;
                    border-radius:10px !important;
                    border:2px solid #222 !important;
                    background:#7a1fa2 !important;
                    color:#fff !important;
                    display:flex !important;
                    align-items:center !important;
                    justify-content:center !important;
                }"""
            ):
                if st.button("ВВОД", key="rodent_enter"):
                    qty = int(st.session_state.rodent_qty)
                    typ = st.session_state.rodent_type
                    if typ == "Криса":
                        typ = "K"
                    if typ == "Миша":
                        typ= "M"
                    log(f"конт. №{st.session_state.current_container} = {typ}-{qty}")
                    log_from_sql(f"{typ}-{qty}")
                    st.session_state.rodent_active = False
                    st.session_state.rodent_type = ""
                    st.session_state.rodent_qty = 1
                    st.session_state.current_container +=1
                    st.rerun()

        with e:
            with stylable_container(
                key="rodent_cancel_wrap",
                css_styles="""
                div[data-testid="stButton"]{display:flex; justify-content:flex-start;}
                button{
                    width:160px !important;
                    height:40px !important;
                    padding:0 !important;
                    font-size:14px !important;
                    font-weight:900 !important;
                    border-radius:10px !important;
                    border:2px solid #222 !important;
                    background:#444 !important;
                    color:#fff !important;
                    display:flex !important;
                    align-items:center !important;
                    justify-content:center !important;
                }"""
            ):
                if st.button("СКАСУВАТИ", key="rodent_cancel"):
                    st.session_state.rodent_active = False
                    st.session_state.rodent_type = ""
                    st.session_state.rodent_qty = 1
                    st.rerun()

    # =========================================================
    # 11) Перерисовка после клика
    # =========================================================
    if action:
        st.rerun()


