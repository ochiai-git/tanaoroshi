import streamlit as st

def main():
    st.title("在庫数登録")

    # 選択された数字を保持する変数
    if "count" not in st.session_state:  # (C)
        st.session_state.count = ""  # (A)

    # 0から9までのボタンを表示
    """for i in range(0, 10):
        button_label = str(i)
        button_clicked = st.button(button_label)"""

    col1, col2, col3 = st.columns(3)
    with col1:
        button_clicked = st.button("7")
    with col2:
        button_clicked = st.button("8")
    with col3:
        button_clicked = st.button("9")



        # ボタンがクリックされた場合の処理
        #if button_clicked:
        #    st.session_state.count += button_label


    # 選択された数字を表示
    st.write(f"選択された数字: {st.session_state.count}")
    print(f"選択された数字: {st.session_state.count}")

if __name__ == "__main__":
    main()
