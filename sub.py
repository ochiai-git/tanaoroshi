import csv
import smtplib
import os
import shutil
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import mailsousin2
import datetime
import pandas as pd

def calculate_future_date(number_of_days):
    # 本日からnumber_of_days後はいつかを求める関数
    today = datetime.date.today()
    future_date = today + datetime.timedelta(days=number_of_days)
    return future_date

def calculate_days(text):
    # 賞味期限のテキストから日数に変換する関数
    # 日数計算用の辞書
    month_to_days = {
        'か月': 30,
        'カ月': 30,
        'ヵ月': 30,
        'ヶ月': 30,
        'かわ': 30,
        'わ': 30,
        '日': 1,
        '年': 365,
    }
    # 入力テキストを空白で分割して各要素を処理
    parts = text.split()
    total_days = 0

    for part in parts:
        # 数値部分と単位を分割
        value = ""
        unit = ""

        for char in part:
            if char.isdigit():
                value += char
            else:
                unit += char

        if value and unit in month_to_days:
            total_days += int(value) * month_to_days[unit]

    return total_days



def send_email_with_attachment():
    # ダウンロードしたファイルをメールで送信する
    mail_lib = mailsousin2.MailLib()
    from_address = 'tochiyuki.ochiai@gmail.com'  # ←変えるとメール送信できない
    to_address = 'ochiai@tochiyuki.co.jp'
    dt_now = datetime.datetime.now()
    nitizi = dt_now.strftime('%m月%d日 %H:%M')
    title = '在庫数CSVファイル ' + nitizi
    contents = '在庫数CSVファイル'

    # ★data.csvがない場合の処理を追加する必要あり。

    file_path = './data.csv'
    msg = mail_lib.create_multipart_message(from_address, to_address, title, contents, file_path)
    mail_lib.send_mail(from_address, to_address, msg)
    print('件名:{}でメールを送信しました。'.format(title))


    """    # ファイルのバックアップ
    backup_folder = 'backup'
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
    shutil.move('data.csv', os.path.join(backup_folder, 'data.csv'))
    print("File moved to backup folder.")"""

    backup_folder = 'backup'
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    current_datetime = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    new_filename = f'data_{current_datetime}.csv'

    shutil.move('data.csv', os.path.join(backup_folder, new_filename))
    print("csvファイルをメール送信後、backupフォルダーに移動しました。ファイル名:", new_filename)

"""def write_to_csv(barcode, number, filename='data.csv'):
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    data = [current_date, barcode, number]

    try:
        with open(filename, 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(data)
        return True
    except Exception as e:
        print(f"Error writing to CSV: {e}")
        return False"""

# なんか文字化け問題が出るが、pandasを使ってcsvに書き込みすれば問題発生しないのでは？
def write_to_csv(barcode, item_name, number, filename='data.csv'):
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = [current_datetime, barcode, item_name, number]

    try:
        with open(filename, 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(data)
        return True
    except Exception as e:
        print(f"Error writing to CSV: {e}")
        return False

def add_data_to_csv(filename, barcode, product_name, stock):
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # CSVファイルを読み込み
    df = pd.read_csv(filename)
    # 新しいデータを1行追加
    new_data = {"日付": current_datetime, "バーコード": barcode, "商品名": product_name, "在庫数": stock}
    # df = df.append(new_data, ignore_index=True)
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    # 更新されたDataFrameをCSVファイルに書き込み
    df.to_csv(filename, index=False)

def create_data_csv(filename):
    # 空のDataFrameを作成
    df = pd.DataFrame(columns=["日付", "バーコード", "商品名", "在庫数"])
    # CSVファイルに書き込み
    df.to_csv(filename, index=False)

# テストコード
if __name__ == "__main__":
    barcode = "123456"
    number = "111"
    success = write_to_csv(barcode, number)

    if success:
        print("Data written to CSV successfully.")
    else:
        print("Failed to write data to CSV.")