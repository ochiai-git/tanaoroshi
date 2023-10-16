import streamlit as st


def virtual_keyboard():
    # バーチャルテンキーの数字を保持する変数
    number = 0

    # Streamlitアプリケーションのタイトル
    st.title("バーチャルテンキー")

    # 現在の数字を表示
    st.write(f"現在の数字: {number}")

    # 数字ボタンのレイアウトを定義
    col1, col2, col3, col4 = st.columns([1,1,1,8])

    # 数字ボタンを作成
    with col1:
        if st.button('７'):
            number = 7
        if st.button('４'):
            number = 4
        if st.button('１'):
            number = 1
        if st.button('０'):
            number = 0
    with col2:
        if st.button('８'):
            number = 8
        if st.button('５'):
            number = 5
        if st.button('２'):
            number = 2
        if st.button('―'):
            number = "-"
    with col3:
        if st.button('９'):
            number = 9
        if st.button('６'):
            number = 6
        if st.button('３'):
            number = 3
        if st.button('Ｃ'):
            number = 'c'



    # 結果を表示
    st.write(f"選択された数字: {number}")


if __name__ == '__main__':
    virtual_keyboard()
