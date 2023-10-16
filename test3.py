import streamlit as st

def virtual_keyboard():
    # バーチャルテンキーの数字を保持する変数
    number = 0

    # Streamlitアプリケーションのタイトル
    st.title("バーチャルテンキー")

    # 現在の数字を表示
    st.write(f"現在の数字: {number}")

    # 数字ボタンのレイアウトを定義
    col1, col2, col3, col4 = st.columns(4)

    # 数字ボタンを作成
    with col1:
        if st.button('7', key='7'):
            number = 7
    with col1:
        if st.button('4', key='4'):
            number = 4
    with col1:
        if st.button('1', key='1'):
            number = 1
    with col1:
        if st.button('0', key='0'):
            number = 0

    with col2:
        if st.button('8', key='8'):
            number = 8
    with col2:
        if st.button('5', key='5'):
            number = 5
    with col2:
        if st.button('2', key='2'):
            number = 2
    with col2:
        if st.button('-', key='-'):
            number = "-"

    with col3:
        if st.button('9', key='9'):
            number = 9
    with col3:
        if st.button('6', key='6'):
            number = 6
    with col3:
        if st.button('3', key='3'):
            number = 3
    with col3:
        if st.button('C', key='C'):
            number = 'c'

    # 結果を表示
    st.write(f"選択された数字: {number}")

if __name__ == '__main__':
    virtual_keyboard()
