import streamlit as st

def error_check_num(target,value,goal):
    if target < value:
        st.error(f"{goal}が{target}なので、{value}以上の値を入力して下さい。")
        return 0
    
    return 1

def error_check_str(target,meisyou):
    if target == "":
        st.error(f"{meisyou}が空白です。")
        return 0
    
    return 1