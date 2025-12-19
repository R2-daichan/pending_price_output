import pyodbc
import pandas as pd
from datetime import datetime



def get_target_csv(driver):
    # 現在の月から次の月の1日を計算
    today = datetime.today()
    next_month = (today.month % 12) + 1  # 次の月の計算
    next_month_year = today.year if next_month > today.month else today.year + 1  # 次の月の年を考慮
    next_month_first_day = datetime(next_month_year, next_month, 1)
    formatted_date = next_month_first_day.strftime('%Y-%m-%d')
    print(f"Next month first day: {formatted_date}")    


    with pyodbc.connect(
        driver
    ) as conn:
        conn.setencoding("shift_jis")  # データベースのエンコーディング設定
        
        # SQL クエリを定義する（'INVAL_DATE' >= next_month_first_day AND 'VALID_DATE' = next_month_first_day）
        sql_query_price = f"""
            SELECT * 
            FROM GTAPPROD.TGV_PART_PUR_PRICE 
            WHERE INVAL_DATE = '{formatted_date}' 
            AND SUPP != '4001'
            AND VALID_DATE != '{formatted_date}'
        """
        #有効日が次月初日のデータチェック用
        sql_query_price_valid_data_check = f"""
            SELECT *
            FROM GTAPPROD.TGV_PART_PUR_PRICE 
            WHERE VALID_DATE = '{formatted_date}'
        """

        sql_query_supp = f"""
            SELECT *
            FROM GTAPPROD.TGM_SUPP
        """
        sql_query_part_base = f"""
            SELECT DEPT, PARTNO, PART_NM, MODEL FROM GTAPPROD.TGM_PART_BASE
        """

        # データを取得してデータフレームに読み込む
        price_df = pd.read_sql(sql_query_price, conn)
        price_df['KEY'] = price_df['DEPT'] + price_df['PARTNO']

        supp_df = pd.read_sql(sql_query_supp, conn)
        supp_df=supp_df[['SUPP','SUPP_NM']]
        
        part_base_df = pd.read_sql(sql_query_part_base, conn)
        part_base_df['KEY'] = part_base_df['DEPT'] + part_base_df['PARTNO']
        part_base_df = part_base_df.drop(['DEPT', 'PARTNO'], axis=1)

        price_df_valid_data_check = pd.read_sql(sql_query_price_valid_data_check, conn)
        price_df_valid_data_check['KEY'] = price_df_valid_data_check['DEPT'] + price_df_valid_data_check['PARTNO']
        price_df_valid_data_check = price_df_valid_data_check[['KEY','VALID_DATE']]
        price_df_valid_data_check = price_df_valid_data_check.rename(columns={'VALID_DATE':'VALID_DATE_CHECK'})
       #KEYの重複削除
        price_df_valid_data_check = price_df_valid_data_check.drop_duplicates(subset=['KEY'])
      


       # データフレームをマージする
        merged_price_df = pd.merge(price_df, supp_df, on='SUPP', how='left')
        merged_price_df = pd.merge(merged_price_df, part_base_df, on='KEY', how='left')
        merged_price_df = pd.merge(merged_price_df, price_df_valid_data_check, on='KEY', how='left')
        #VALID_DATE_CHECKが空白のもののみ抽出
        merged_price_df = merged_price_df[merged_price_df['VALID_DATE_CHECK'].isna()]
        merged_price_df = merged_price_df.drop(['KEY'], axis=1)

    return next_month,next_month_year,merged_price_df
       

if __name__ == "__main__":
    
    driver="DRIVER={Oracle in instantclient_21_9};DBQ=202.15.66.219:1522/GTAP;UID=GTAPPROD;PWD=PATGPROD"
    get_target_csv(driver)
