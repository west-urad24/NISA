import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.model import Base, History
from datetime import datetime
from .common_error_check import error_check_num,error_check_str
from logging import getLogger
logger = getLogger(__name__)

# DB接続
engine = create_engine("sqlite:///sample.db", echo=False)
Session = sessionmaker(bind=engine)

# 初期化（テーブル作成）
Base.metadata.create_all(engine)

# DB登録
def db_access(year,month,title,meigara,money,result,flag):
    session = Session()
    
    # 削除時にerror2,error3が未定義になるから
    error2 = 1
    error3 = 1

    # ▼ エラーチェック
    error1 = error_check_num(year,datetime.now().year,"年度")
    
    if flag == "登録":
        # 月掛け金が0以下か？
        error2 = error_check_num(money,0,"月掛け金")
        # 損益金額が0以下か？
        error3 = error_check_num(result,0,"損益金額")

    # タイトルが空白か？
    error4 = error_check_str(title,"タイトル")
    # 銘柄が空白か？
    error5 = error_check_str(meigara,"銘柄")

    if error1 == 0 or error2 == 0 or error3 == 0 or error4 == 0 or error5 == 0:
        return
    # ▲ エラーチェック
    
    if flag == "登録":
        data = session.query(History).filter(
            History.year == year,
            History.month == month,
            History.title == title
        ).first()

        if data:
            # 更新
            data.money = money
            data.meigara = meigara
            data.result = result
        else:
            # 新規
            data = History(
                year=year,
                month=month,
                title=title,
                money=money,
                result=result,
                meigara=meigara
            )
            session.add(data)
    else:
        deleted_count = session.query(History).filter(
            History.year == year,
            History.title == title,
            History.meigara == meigara
        ).delete()

        if deleted_count == 0:
            st.error("対象データがありません。")
            return
    
    session.commit()
    session.close()
    st.write(f"{flag}しました。")
