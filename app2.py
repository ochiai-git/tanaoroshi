import streamlit as st
import pandas as pd
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import base64
from io import BytesIO

def url_to_image_selenium(driver,url):
    # URLの画像データを読み込む
    driver.get(url)
    # 画像データを取得

    img_data_base64 = driver.get_screenshot_as_base64()
    img_data = base64.b64decode(img_data_base64)
    return Image.open(BytesIO(img_data))

# ダミーの関数（実際の処理をここに追加）
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


    # st.title("賞味期限チェックアプリ")

    # st.session_stateを初期化
    if 'last_entered' not in st.session_state:
        st.session_state.last_entered = None

    # バーコードを入力するテキストボックス
    barcode_input = st.text_input("バーコードを入力してください:")

    # テキストボックスがフォーカスされている時にEnterが押されたときの処理　3259426035081
    if barcode_input and st.session_state.last_entered != barcode_input:
        st.session_state.last_entered = barcode_input
        # ダミーの関数を呼び出してバーコードを処理
        result = get_item_data(barcode_input)
        st.write(result)
        st.write(result.iloc[0])
        st.write(result.iloc[1])
        st.write(result.iloc[2])
        st.write(result.iloc[3])
        print(type(result.iloc[3]))
        st.write("テスト")

        image = url_to_image_selenium(driver, result.iloc[3])
        image.thumbnail((400, 400))  # サイズを調整
        image_bytes = BytesIO()
        image.save(image_bytes, format="PNG")
        img_base64 = base64.b64encode(image_bytes.getvalue())
        st.image(img_base64, caption='サンプル', use_column_width=True)

if __name__ == "__main__":
    main()