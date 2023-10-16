import streamlit as st
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


    # with句でくくると、入力後クリアされるらしい。
    # バーコードを入力するテキストボックス
    with st.form("my_form", clear_on_submit=True):
        barcode_input = st.text_input('バーコードを入力してください。')
        submitted = st.form_submit_button("商品データ表示")


    if submitted:
        # 入力されたバーコードがすべて数字で構成されているかチェックする。
        if barcode_input.isdigit():
            print("数字が読み込まれました")
        else:
            print("数字が以外が読み込まれました")
            return 1

        result = get_item_data(barcode_input)

        st.write(result)
        # Seleniumで画像を取得
        driver.get(result.iloc[3])
        # 画像をバイト形式で取得
        image_data = driver.get_screenshot_as_png()
        # 画像を表示
        st.image(Image.open(BytesIO(image_data)), caption="画像", use_column_width=True)
        # ブラウザを閉じる
        driver.quit()

    else:
        st.warning("画像のURLを入力してください。")



if __name__ == "__main__":
    main()


