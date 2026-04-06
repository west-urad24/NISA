import streamlit as st
from modules.register import resisterData
from modules.visual import visualizeData
from modules.goal import settingGoal
from modules.predict import predictData


st.sidebar.title("メニュー")

# サイドバー　ラジオボタン
page = st.sidebar.radio(
    "機能選択",
    ["登録 / 削除", "目標管理", "グラフ", "予測"]
)

# ラジオボタン押したら各機能のページに飛ぶ
if page == "登録 / 削除":
    resisterData()

elif page == "グラフ":
    visualizeData()

elif page == "目標管理":
    settingGoal()

else:
    predictData()