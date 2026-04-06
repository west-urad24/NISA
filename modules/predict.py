import streamlit as st
from services.common_error_check import error_check_str
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.model import Base, History
import numpy as np
from sklearn.linear_model import LinearRegression


# DB接続
engine = create_engine("sqlite:///sample.db", echo=False)
Session = sessionmaker(bind=engine)

def predictData():
    session = Session()
    st.title("予測画面")
    st.text('翌月の積立結果を予測します。')
    st.text('')

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

        if len(data) < 5:
            st.error("学習データ不足のため、データを5件以上登録してください。")
            st.error(f"データ数:{len(data)}件")
            return
        
        X = []
        Y = []

        for row in data:
            X.append(row.id)
            Y.append(row.result)

        X = np.array(X).reshape(-1, 1)
        Y = np.array(Y)

        model = LinearRegression()
        model.fit(X,Y)

        next_index = len(data)+1
        predicted = model.predict([[next_index]])

        st.write(f"最終月の積立額: {data[-1].year}年{data[-1].month}月:{data[-1].result}円")
        st.write(f"翌月の予測積立額: {int(predicted[0]):,} 円")
        
