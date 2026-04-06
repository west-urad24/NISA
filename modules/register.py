import streamlit as st
from datetime import datetime
from services.db import db_access
from logging import getLogger
logger = getLogger(__name__)

def resisterData():
    st.title("登録 / 削除画面")
    st.text('各年度/月の銘柄のデータを登録/削除をします。')
    st.text('')

    reg_or_del = st.radio(
        "登録/削除",
        ['登録', '削除']
    )

    # 今年度を表示
    year = st.number_input(
        "年度",
        value=datetime.now().year
    )

    # ▼ 登録のときだけ「月」、「掛け金」、「結果」を表示
    if reg_or_del == '登録':
        month = st.selectbox(
            "月",
            range(1, 13, 1)
        )

        money = st.number_input(
            "月積立額",
            min_value = 0
        )

        result = st.number_input(
            "損益結果",
            min_value = 0
        )

    title = st.text_input(
        "任意のタイトルを入力してください",
        ""
    )

    meigara = st.text_input(
        "銘柄を入力してください",
        ""
    )

    # 登録/削除によって、ボタン名を切り替え
    button_label = "登録" if reg_or_del == "登録" else "削除"

    btn = st.button(button_label)

    if btn:
        if reg_or_del == "登録":
            db_access(year,month,title,meigara,money,result,"登録")
        else:
            # 削除時、month不要。yearで全体を消したいから。
            db_access(year,"",title,meigara,0,0,"削除")