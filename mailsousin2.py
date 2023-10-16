# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

import os


class MailLib():
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_password = 'byfvqmlwyjewufzy'

    def create_message(self, from_addr: str, to_addr, subject, body) -> MIMEText:
        '''
        メール送信用メッセージを生成する
        Parameters
        ----------
        from_addr : str
            送信元アドレス  \n
        to_addr : str
            送信先アドレス(複数ある場合はカンマ区切り)  \n
        subject : str
            メール件名  \n
        body : str
            メール本文
        '''

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = from_addr
        msg['To'] = to_addr
        msg['Date'] = formatdate()

        return msg

    def create_multipart_message(self, from_addr: str, to_addr: str, subject: str, body: str,
                                 file_path: str) -> MIMEMultipart:
        '''
        メール送信用メッセージを生成する
        Parameters
        ----------
        from_addr : str
            送信元アドレス  \n
        to_addr : str
            送信先アドレス(複数ある場合はカンマ区切り)  \n
        subject : str
            メール件名  \n
        body : str
            メール本文 \n
        file_path: str
            添付ファイルのフルパス
        '''

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = from_addr
        msg['To'] = to_addr
        msg['Date'] = formatdate()
        msg.attach(MIMEText(body, 'plain'))  # メール本文はテキスト形式で送信する

        with open(file_path, "rb") as f:
            mb = MIMEApplication(f.read())

        filename = os.path.basename(file_path)
        mb.add_header("Content-Disposition", "attachment", filename=filename)
        msg.attach(mb)
        return msg

    def send_mail(self, from_addr, to_addr, body_msg) -> None:
        '''
        メールを送信する
        '''
        smtp_obj = smtplib.SMTP(self.smtp_server, self.smtp_port)
        smtp_obj.ehlo()
        smtp_obj.starttls()
        smtp_obj.login(from_addr, self.smtp_password)
        # 元smtp_obj.sendmail(from_addr, to_addr.split(','), body_msg.as_string())　
        # 案1 to_addrs = [to_addr,'shop@tochiyuki.co.jp'] # BCCで自店舗にも送信する
        to_addrs_list = []
        to_addrs_list = to_addr.split(',')
        # to_addrs_list.append('shop@tochiyuki.co.jp')  # ccつける場合に使う
        smtp_obj.sendmail(from_addr, to_addrs_list, body_msg.as_string())
        smtp_obj.close()