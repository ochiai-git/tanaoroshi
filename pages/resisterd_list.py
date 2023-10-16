import streamlit as st
import pandas as pd
import sub

def csvlist():

    csvfile = "./data.csv"

    # CSVファイルをデータフレームに読み込む
    df = pd.read_csv(csvfile)

    # 読み込んだデータフレームを表示
    st.write("### 在庫数を入力した商品一覧")
    st.write(df)

    if st.button("上記をメールで送信する"):
        sub.send_email_with_attachment()
        # ↑のメール送信で、データはbackupフォルダに移動されるため、新たに空のcsvファイルを作成する。
        sub.create_data_csv(csvfile)
        st.rerun()

if __name__ == "__main__":
    csvlist()
