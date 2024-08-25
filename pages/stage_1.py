import streamlit as st
import datetime
import calendar
import requests
import pandas as pd
import numpy as np
import soramame

st.title("ソラマメLab")
st.write("### ソラマメAPIからのデータ取得フォーム")

# セッションステートの初期化
if 'dataframes' not in st.session_state:
    st.session_state['dataframes'] = {}


with st.form(key = "soramame"):
    
    year = st.selectbox("取得年", soramame.years, index=len(soramame.years) - 1)  
    start_month = st.selectbox("取得月", range(1, 13), index = None, placeholder="選んでください")  
    choice = st.multiselect('取得したい属性を選んでください',
            soramame.options,
            default=["NO", "NOX", "SPM", "WD", "WS"],
            placeholder="選んでください")    
    selected_prefecture = st.selectbox("都道府県を選んでください", list(soramame.prefecture_codes.keys()), index = None, placeholder="選んでください")
    site = st.text_input("測定局のコードを入力してください", value="33202170")

    submit_btn = st.form_submit_button("データを取得")


    if submit_btn:
        start = str(year) + f"{start_month:02d}"
        end = str(year) + f"{start_month:02d}"
        station = soramame.prefecture_codes[selected_prefecture]
        request_data = ','.join(choice)

        url = f"https://soramame.env.go.jp/soramame/api/data_search?Start_YM={start}&End_YM={end}&TDFKN_CD={station}&SKT_CD={site}&REQUEST_DATA={request_data}"
        r = requests.get(url)
        data = r.json()
        df = pd.DataFrame(data)

        key = f"{selected_prefecture}_{site}_{start}"
        st.session_state.dataframes[key] = df
        st.write(f"データフレームが次のキーで保存されました: {key}")

for key, df in st.session_state.dataframes.items():
    st.write(f"データフレーム: {key}")
    st.write(df)

