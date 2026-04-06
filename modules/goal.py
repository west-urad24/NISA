import streamlit as st
from datetime import datetime
from services.common_error_check import error_check_num
import math
from logging import getLogger
logger = getLogger(__name__)

def settingGoal():
    st.title("目標管理画面")
    st.text('目標に対していつまでに積立目標が達成できるかシュミレートします。')
    st.text('')

    year = st.number_input(
        "目標開始年度",
        value=datetime.now().year
    )

    month = st.selectbox(
        "目標開始月",
        range(1, 13, 1)
    )

    month_money = st.number_input(
        "月積立額",
        min_value = 0
    )

    rate = st.number_input(
        "理想利益率(5%~10%が現実的)",
        min_value = 0
    )

    now_money = st.number_input(
        "現在積立額",
        min_value = 0
    )

    goal_money = st.number_input(
        "目標積立額",
        min_value = 0
    )

    btn = st.button("表示")
    if btn:
        error1 = error_check_num(year,datetime.now().year,"目標開始年度")
        error2 = error_check_num(month_money,0,"月積立額")
        error3 = error_check_num(now_money,0,"現在積立額")
        error4 = error_check_num(goal_money,0,"目標積立額")
        error5 = error_check_num(rate,0,"理想利益率")

        if error1 == 0 or error2 == 0 or error3 == 0 or error4 == 0 or error5 == 0:
            return
        

        left = goal_money - now_money # 目標額-現在額
        if left <= 0:
            st.write("既に目標達成しています。")
            st.write(f"目標額={goal_money} 現在額={now_money}")
            return
        
        rate_money = month_money * (rate/100) # 月積立*利益率
        result = month_money + rate_money
        
        
        total_month = math.ceil(left / result) # (目標額-現在額) / 月積立額 切り上げ
        # 目標開始年度、目標開始月とtotal_monthからX年Y月に実現できる

        # ▼ 年月計算
        # monthは1〜12なので -1 してから計算するとズレない
        start_index = (year * 12) + (month - 1)
        target_index = start_index + total_month

        target_year = target_index // 12
        target_month = (target_index % 12) + 1

        st.write(f"{target_year}年{target_month}月に達成できます！")

