from modules import get_csv, mail_send
import os



if __name__ == "__main__":
    # データベースからCSVデータを取得
    driver="DRIVER={Oracle in instantclient_21_9};DBQ=202.15.66.219:1522/GTAP;UID=GTAPPROD;PWD=PATGPROD"

    # 現在のスクリプトのディレクトリ
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 1つ上のディレクトリ
    parent_dir = os.path.dirname(current_dir)
    
    month = get_csv.get_target_csv(driver)[0]
    year = get_csv.get_target_csv(driver)[1]


    df_part_pending_price = get_csv.get_target_csv(driver)[2]

    csv_path = os.path.join(parent_dir, 'output_csv', f'part_pending_price_{year}_{month}.csv')

    df_part_pending_price.to_csv(csv_path, index=False, encoding='utf-8-sig')

    # メール送信の設定

    from_address = 'dx.auto-mail@kyushu.toyoda-gosei.co.jp'
    to_address = ["akio.harada@kyushu.toyoda-gosei.co.jp", "tomoki.haya@kyushu.toyoda-gosei.co.jp","taro.kuwamori@kyushu.toyoda-gosei.co.jp","ayumi.shinohara@kyushu.toyoda-gosei.co.jp", "rodo.suzuki@kyushu.toyoda-gosei.co.jp", "ryotaro.matsuo@kyushu.toyoda-gosei.co.jp", "daisuke.matsuo@kyushu.toyoda-gosei.co.jp"]
    subject = "単価未定 Report"
    body = "単価未定情報送付します."
    ip = "202.15.64.205"
    port = 25
    attachment_path = csv_path
    cc_address = ["daisuke.matsuo@kyushu.toyoda-gosei.co.jp"]

    mail_send.send_mail(
        from_address=from_address,
        to_address=to_address,
        subject=subject,
        body=body,
        ip=ip,
        port=port,
        attachment_path=attachment_path,
        cc_address=cc_address
    )