import streamlit as st
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Seleniumの設定
chrome_options = Options()
chrome_options.add_argument("--headless")  # ブラウザを表示しない

# Streamlitアプリのタイトル
st.title("在庫チェックアプリ")

# 画像のURLを取得
image_url = st.text_input("画像のURLを入力してください:",  key="text")

if image_url:
    # Seleniumで画像を取得
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(image_url)

    # 画像をバイト形式で取得
    image_data = driver.get_screenshot_as_png()

    # 画像を表示
    st.image(Image.open(BytesIO(image_data)), caption="画像", use_column_width=True)

    st.session_state["text"] = ""
    # ブラウザを閉じる
    driver.quit()
else:
    st.warning("画像のURLを入力してください。")