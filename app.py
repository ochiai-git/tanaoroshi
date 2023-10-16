import streamlit as st
import pandas as pd



def get_item_data(barcode):
    print("関数内に入りました")
    # Excelファイルを読み込み
    file_path = '棚卸アプリ用のDB.xlsx'  # Excelファイルのパスを指定してください
    sheet_name = 'Sheet'  # シート名を適宜変更してください
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    print(f'入力されたバーコードは{barcode}')
    print(df)

    # 条件に一致する行を抽出
    filtered_rows = df[df['バーコード'] == barcode]

    # 値を取得
    if not filtered_rows.empty:
        print("該当するを発見")
        column_values = filtered_rows.iloc[:, [1, 3, 4, 5]]
        return column_values.iloc[0]

    else:
        print("該当する行が見つかりませんでした。")


def test():
    item_data = get_item_data(3259426035081)
    print(item_data)

def main():
    user_input = st.text_input("バーコードを入力")  # 文字入力(1行) 3259426035081
    item_data = get_item_data(int(user_input))
    print(f"該当する商品は{item_data}")
    # テキストが入力された場合の処理
    if item_data is not None:
        st.write("アイテムデータ:", item_data)
    else:
        st.write("該当するアイテムが見つかりませんでした。")

        # 文章を表示
        st.write(user_input)

if __name__ == "__main__":
    main()