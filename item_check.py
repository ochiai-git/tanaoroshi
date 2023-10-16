import streamlit as st
import pandas as pd
from PIL import Image
import base64
from io import BytesIO
import requests
import sub
import os

def url_to_image_selenium(driver,url):
    # URLの画像データを読み込む
    driver.get(url)
    # 画像データを取得

    img_data_base64 = driver.get_screenshot_as_base64()
    img_data = base64.b64decode(img_data_base64)
    return Image.open(BytesIO(img_data))

def get_item_data(barcode):
    # Excelファイルを読み込み
    # file_path = '棚卸アプリ用のDB.xlsx'  # Excelファイルのパスを指定してください
    file_path = 'item_db_2.csv'  # Excelファイルのパスを指定してください
    sheet_name = 'Sheet'  # シート名を適宜変更してください

    # df = pd.read_excel(file_path, sheet_name=sheet_name)  # エンコードを指定する必要はないとのこと。というか指定できない。
    df = pd.read_csv(file_path)  # streamlitでopenpyxlでエラーが出るのでcsvにした。

    # 条件に一致する行を抽出
    # filtered_rows = df[df['バーコード'] == int(barcode)]
    filtered_rows = df[df['バーコード'] == barcode]

    # 値を取得
    if not filtered_rows.empty:
        column_values = filtered_rows.iloc[:, [1, 3, 4, 5]]
        return column_values.iloc[0]
    else:
        print("該当する行が見つかりませんでした。")
        print(f"入力されたバーコード{barcode}、型{type(barcode)}")
        st.session_state.error_code = 1
        return None

def main():
    filename = "data.csv"
    # もしdata.csvファイルが存在しなかったら作成する。
    if not os.path.exists(filename):
        sub.create_data_csv(filename)

    if 'count' not in st.session_state:
        st.session_state["count"] = 0
        st.session_state.error_code = 0

    if st.session_state.error_code == 1:
        st.write("<span style='color:red'>　商品の登録がありません</span>", unsafe_allow_html=True)
        st.session_state.error_code = 0


    # ■■■■■■■■■■■ 画面1 バーコード入力 ■■■■■■■■■■■
    if st.session_state.count == 0:
        with st.form("my_form", clear_on_submit=True):
            # st.session_state.bcd = st.text_input('バーコードを入力してください。')
            bcd_tmp = str(st.number_input("バーコードを入力してください。", value=None, placeholder="0"))
            # streamlitの仕様でnumber_inputを使うと、.0までくっついてくる為、それを除去する。
            st.session_state.bcd = bcd_tmp.split(".")[0]
            submitted = st.form_submit_button("商品データ表示")

        if submitted:  # ボタンが押されたらカウントを1にする。
            if st.session_state.bcd == "":  # バーコード欄に何も入力が無ければ
                st.rerun()
            st.session_state.count = 1
            st.rerun()

    # ■■■■■■■■■■■ 画面2 詳細表示＋在庫数入力 ■■■■■■■■■■■
    if st.session_state["count"] == 1:
        result = get_item_data(st.session_state.bcd)
        if result is None:
            st.write(f"{st.session_state.bcd} のバーコードのデータがありませんでした。")
            st.session_state.count = 0
            st.rerun()

        # 期限日計算処理
        if pd.notnull(result.iloc[2]):  # 保証賞味期限がある場合
            days = sub.calculate_days(result.iloc[2])  # 賞味期限のテキストから日数に変換
            itu = sub.calculate_future_date(days)  # 本日から上記の日数後はいつか
        else:
            itu = None  # 保証賞味期限がないならNoneを代入

        #  ■■■　商品情報表示処理　■■■
        # ★処理追加★
        new_data = {
            "バーコード": st.session_state.bcd,
            "商品管理番号": result.iloc[0],
            "商品名": result.iloc[1],
            "保証賞味期限": result.iloc[2],
            "期限日": itu,
        }
        df = pd.DataFrame([new_data])

        # 行の名前（index）を削除
        df.index = ["" for _ in df.index]
        # 商品情報の表を表示

        # 画像表示処理
        response = requests.get(result.iloc[3])
        if response.status_code == 200:
            image_data = BytesIO(response.content)
            # 画像を小さく表示する（例: 幅を200pxに調整）
        else:
            st.error(f"画像の取得に失敗しました。ステータスコード: {response.status_code}")

        col1, col2 = st.columns(2)
        with col1:
            st.write(df.transpose())
        with col2:
            st.image(Image.open(image_data), caption="楽天商品画像", width=200)

        with st.form("my_form2", clear_on_submit=True):
            number = st.number_input("在庫数を入力", value=None, placeholder="0")
            submitted2 = st.form_submit_button("在庫数登録")

        if submitted2:
            # ★ここにCSV書き込み処理を入れる。
            # sub.write_to_csv(st.session_state.bcd, result.iloc[1], int(number),  filename='data.csv')
            sub.add_data_to_csv('data.csv', st.session_state.bcd, result.iloc[1], int(number))
            # ★または、別画面にして、バーチャルテンキーをつける。
            print("在庫数書き込み完了")
            st.session_state.count = 0
            st.rerun()

        if st.button("戻る"):
            st.session_state.count = 0
            st.rerun()







if __name__ == "__main__":
    main()