

# セッションテスト中
import streamlit as st
import pandas as pd
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import base64
from io import BytesIO
import requests
import sub

# pyautoguiを一緒に使うことでフォーカス周りを調整する。

def url_to_image_selenium(driver,url):
    # URLの画像データを読み込む
    driver.get(url)
    # 画像データを取得

    img_data_base64 = driver.get_screenshot_as_base64()
    img_data = base64.b64decode(img_data_base64)
    return Image.open(BytesIO(img_data))

def get_item_data(barcode):
    # Excelファイルを読み込み
    file_path = '棚卸アプリ用のDB.xlsx'  # Excelファイルのパスを指定してください
    sheet_name = 'Sheet'  # シート名を適宜変更してください
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    # 条件に一致する行を抽出
    filtered_rows = df[df['バーコード'] == int(barcode)]

    # 値を取得
    if not filtered_rows.empty:
        column_values = filtered_rows.iloc[:, [1, 3, 4, 5]]
        return column_values.iloc[0]
    else:
        print("該当する行が見つかりませんでした。")
        return None

def main():
    # ChromeDriverのパスを変数に設定
    # CHROMEDRIVER = "./chromedriver.exe"
    # ChromeDriverのstartとstopを制御するServiceオブジェクトを介してパスを渡す
    # chrome_service = service.Service(executable_path=CHROMEDRIVER)
    # ヘッドレスモード設定
    options = Options()
    options.add_argument("--headless=new")  # ヘッドレスモードを有効にする。=newをつけないとcsvのDLができない。
    # Chromeを起動
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    # ★★★★セッション初期化★★★
    if "count" not in st.session_state:
        st.session_state.count = 0

    # with句でくくると、入力後クリアされるらしい。
    # バーコードを入力するテキストボックス

    if st.session_state.count == 0:
        with st.form("my_form", clear_on_submit=True):
            barcode_input = st.text_input('バーコードを入力してください。')
            submitted = st.form_submit_button("商品データ表示")

        if submitted:  # ボタンが押されたら
            st.session_state.count = 1
            print("セッションカウントが1になりました")
            st.session_state.bcd = barcode_input
            print("セッションバーコードにバーコードが入力されました")
            st.rerun()

    elif st.session_state.count == 1:
        # 入力されたバーコードがすべて数字で構成されているかチェックする。
        if st.session_state.bcd.isdigit():
            print("数字が読み込まれました")
        else:
            return 1

        result = get_item_data(st.session_state.bcd)
        if result is None:
            st.write(f"{st.session_state.bcd} のバーコードのデータがありませんでした。")
            return 1

        # 期限日計算処理
        if pd.notnull(result.iloc[2]):  # 保証賞味期限がある場合
            print("チェック1")
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

        st.session_state.count = 2

    else:
        pass

    print("ifを抜けて最後まで来ました")
    print(st.session_state.count)

if __name__ == "__main__":
    main()







