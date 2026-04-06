import streamlit as st
from services.common_error_check import error_check_str
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.model import Base, History
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Hiragino Sans'

# DB接続
engine = create_engine("sqlite:///sample.db", echo=False)
Session = sessionmaker(bind=engine)

# 初期化（テーブル作成）
Base.metadata.create_all(engine)

def visualizeData():
    session = Session()
    st.title("グラフ画面")
    st.text('登録した積立額と損益結果を可視化します。')
    st.text('')

    now_money = st.number_input(
        "現在積立額",
        min_value = 0
    )

    title = st.text_input(
        "タイトルを入力してください",
        ""
    )

    meigara = st.text_input(
        "銘柄を入力してください",
        ""
    )

    btn = st.button("表示")
    if btn:
        # ▼ エラーチェック
        error1 = error_check_str(title,"タイトル")
        error2 = error_check_str(meigara,"銘柄")

        if error1 == 0 or error2 == 0:
            return
        # ▲ エラーチェック
        
        data = session.query(History).filter(
            History.meigara == meigara,
            History.title == title
        ).order_by(History.year, History.month).all()

        if not data:
            st.error("データがありません。")
            return

        date_label = [] # 日付ラベル
        tsumitate_list = [] # 積立結果
        result_list = [] # 損益結果

        total = now_money  # 現在積立額スタート

        for row in data:
            total += row.money
            date_label.append(f"{row.year}/{row.month}")
            tsumitate_list.append(total)
            result_list.append(row.result)

        profit_list = []
        profit_rate_list = []

        for i in range(len(tsumitate_list)):
            profit = result_list[i] - tsumitate_list[i]
            rate = (profit / tsumitate_list[i]) * 100 if tsumitate_list[i] != 0 else 0

            profit_list.append(profit)
            profit_rate_list.append(rate)

        fig = go.Figure()

        # 棒グラフ（積立額）
        fig.add_trace(go.Bar(
            x=date_label,
            y=tsumitate_list,
            name="積立額"
        ))

        # 折れ線（損益）
        fig.add_trace(go.Scatter(
            x=date_label,
            y=result_list,
            mode='lines+markers',
            name="損益",
            line=dict(color='green'),
            
            # 折線グラフにカーソル当てたら表示
            customdata=list(zip(profit_list, profit_rate_list)),
            hovertemplate=
                "日付: %{x}<br>" +
                "評価額: %{y:,}円<br>" +
                "損益: %{customdata[0]:+,}円<br>" +
                "損益率: %{customdata[1]:.2f}%<extra></extra>"
        ))

        st.plotly_chart(fig)