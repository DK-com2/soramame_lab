import streamlit as st
import datetime
import pandas as pd
import numpy as np
import soramame

st.title("ソラマメLab")

st.write("""
このアプリケーションでは、選択したデータフレームから特定の属性を解析し、リサンプリング処理を行うことができます。
以下の手順で解析を開始してください：

1. **解析したいデータフレームを選択**: 解析対象のデータフレームを選んでください。
2. **属性の選択**: 解析したい属性（カラム）を選んでください。
3. **リサンプリングの間隔を選択**: データのリサンプリング間隔（日単位、週単位、月単位など）を選んでください。
4. **リサンプリングの方法を選択**: 平均、合計、最大値、最小値など、リサンプリング時に使用する集計方法を選んでください。
5. **解析開始**: 提出ボタンをクリックして解析を開始します。

解析結果は画面に表示されます。"""
)
    
    
# データフレーム名を選択するセレクトボックス
serected_df_name = st.selectbox(
    "解析したいデータフレームを選んでください", 
    list(st.session_state.df.keys()), 
    index=None, 
    placeholder="選んでください"
)

# フォームを作成
with st.form(key="stage_3"):
    
    if serected_df_name:
        serected_df = st.session_state.df[serected_df_name]
        serected_columns = st.multiselect('解析したい属性を選んでください',
                                          options=serected_df.columns.tolist(), 
                                          # 選択されたデータフレームのカラムをリストとして提供
                                          default=None)
    else:
        # デフォルトで空のリストを表示
        serected_columns = st.multiselect('解析したい属性を選んでください',
                                          options=[],
                                          default=None)    

    serected_interval = st.selectbox('リサンプリングの間隔を選んでください',
                                    options=["D", "W", "M"],
                                    index=None,
                                    placeholder="選んでください")
    
    serected_resample_method = st.selectbox('リサンプリングの方法を選んでください',
                                             options=["mean", "sum", "max", "min"],
                                             index=None,
                                             placeholder="選んでください")
        

    # 提出ボタン
    submit_btn = st.form_submit_button(label="解析開始")

if submit_btn:    
    #選択されたリストを表示
    st.write("選択された属性")
    st.write(serected_columns)
    st.write("選択されたリサンプリングの間隔")
    st.write(serected_interval)
    st.write("選択されたリサンプリングの方法")
    st.write(serected_resample_method)
    # カラムのデータ型を表示
    # 数値型に変換できるカラムをすべて数値型に変換
    for column in serected_df.columns:
        serected_df[column] = pd.to_numeric(serected_df[column], errors='coerce')
    
    resample_df = serected_df[serected_columns].resample(serected_interval).agg(serected_resample_method)
    st.write("リサンプリング後のデータフレーム")
    st.write(resample_df)
    
    
    
    
else:
    st.write("解析を開始するには、フォームから選択してください。")
    
    