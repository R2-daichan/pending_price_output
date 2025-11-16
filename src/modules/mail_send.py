from  smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os


def send_mail(from_address, to_address,  subject, body, ip ,port, attachment_path, cc_address):
    """SMTPサーバーを使用してメールを送信する

    Args:
        from_address (_type_): 送信元アドレス
        to_address (_type_):Toアドレス
        subject (_type_): 件名
        body (_type_): 本文
        ip (_type_): SMTPサーバーのIPアドレス
        port (_type_): SMTPサーバーのポート番号
        attachment_path (_type_, optional): 添付ファイルパス. Defaults to None.
        cc_address (_type_, optional): CCアドレス. Defaults to None.
    """

    msg = MIMEMultipart()  # MIMEMultipartオブジェクトを作成
    msg['From'] = from_address
    msg['To'] = ", ".join(to_address) if isinstance(to_address, (list, tuple)) else to_address
    msg['Subject'] = subject

    # cc_addressesが提供されている場合、カンマで結合する
    if cc_address:
        msg['Cc'] = ", ".join(cc_address) if isinstance(cc_address, (list, tuple)) else cc_address

    # メールの本文を追加
    body_part = MIMEText(body, "plain", "utf-8")
    msg.attach(body_part)

    # 添付ファイルが指定されている場合にファイルを添付
    if attachment_path:
        with open(attachment_path, 'rb') as file:
            attach = MIMEApplication(file.read())
            attach.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment_path))
            msg.attach(attach)

    try:
        smtp = SMTP(host=ip, port=port)
        smtp.send_message(msg)
        smtp.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")