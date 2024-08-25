import streamlit as st
import datetime
import pandas as pd
import numpy as np
import soramame


st.title("ソラマメLab")

st.write("""
### ここでは、ソラマメAPIデータを解析しやすくするためのデータ整理を行います。


#### データフレーム処理の説明

この関数では、以下の手順でデータフレームを処理しています：

1. データ中の `"-"` を `NaN` に置き換えます。これは、欠損値を明示するためです。
2. 時間データが `"24"` となっている部分を `"00"` に置き換えます。
3. 日付と時間を結合し、`datetime`型に変換します。
4. `"00:00"` のデータは実際には翌日のデータなので、1日繰り上げます。

このようにして、データを分析しやすい形に整えています。
""")

# dataframes辞書のキーを表示
st.write("#### 既存のデータフレームリスト")
for key, df in st.session_state.dataframes.items():
    st.write(f"・{key}")
    
# セッションステートの初期化
if "df" not in st.session_state:
    st.session_state["df"] = {}

# データフレームすべてを解析可能な形式に変換
if st.button("データを解析可能な形式に変換"):
    for key, df in st.session_state.dataframes.items():
        st.session_state.df[key] = soramame.soramame_dataframe(df)
    st.write("データフレームが解析可能な形式に変換されました。")

    
# 変換後のデータフレームを表示
st.write("#### 変換後のデータフレーム")
for key, df in st.session_state.df.items():
    st.write(f"・{key}")
    st.write(df)

    # CSVに変換
    csv = df.to_csv(index=True)

    # CSVをダウンロードできるボタン
    st.download_button(
        label=f"Download {key} as CSV",
        data=csv,
        file_name=f"{key}.csv",
        mime='text/csv'
    )

    