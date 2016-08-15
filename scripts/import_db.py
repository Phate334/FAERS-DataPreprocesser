# -*- coding:utf-8 -*-
import time
from os import listdir, path
import pyodbc
import metadata

input_dir = "clean"  # 整理過斷行問題且欄位名稱統一成最新，但未加age_type和rxcui。
db_name = "FAERS"

def import_quarter(quarter):
    """ sql generator
    輸入季別名稱 e.q. 2004Q1，把該季目錄下的檔案輸入資料庫。
    會將每筆資料編成SQL回傳。
    """
    tables = listdir(path.join(input_dir, quarter))
    for file_name in tables:  # e.q. DEMO04Q1.TXT
        table_name = file_name.split(".")[0]
        table_type = file_name[:4]  # 表格的類型 e.q. DEMO、DRUG
        with open(path.join(input_dir, quarter, file_name)) as f:
            tags = f.readline().strip().split("$")
            #  為了相容舊方體，SEX欄位維持用舊名稱
            if "SEX" in tags:
                tags[tags.index("SEX")] = "GNDR_COD"
            # 回傳該筆資料的sql語句
            fields = [" ".join([t, metadata.ms_meta[table_type][t]]) for t in tags]
            yield metadata.create_table.format(table_name, ",".join(fields))

            # 開始讀取資料
            for line in f:
                row = line.strip().split("$")
                # SQL語法相關處理
                for i, data in enumerate(row):
                    if row[i] == "":  # 空值設NULL
                        row[i] = "NULL"
                    row[i] = row[i].replace("'", "''")  # 資料中的單引號要換成兩個
                # 把字串欄位的資料前後加上引號
                for i, tag in enumerate(tags):
                    if "char" in metadata.ms_meta[table_type][tag] and row[i] != "NULL":
                        row[i] = "'{0}'".format(row[i])
                row = row[:len(tags)]
                yield metadata.insert_data.format(table_name, ",".join(tags), ",".join(row))

def drop_all():
    with pyodbc.connect("driver={SQL Server};server=localhost;Trusted_Connection=yes", database=db_name) as con:
        with con.cursor() as cursor:
            row = cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.Tables")
            tables = [t for t, in row]
            for t in tables:
                cursor.execute("DROP TABLE {0}".format(t))
            cursor.commit()

if __name__ == "__main__":
    print(time.asctime(time.localtime(time.time())))
    # drop_all()  # 將資料庫清空
    with pyodbc.connect("driver={SQL Server};server=localhost;Trusted_Connection=yes", database=db_name) as con:
        cursor = con.cursor()
        # for quarter in listdir(input_dir):
        qs = listdir(input_dir)
        qs.sort(reverse = True)
        for quarter in qs:
            print(quarter)
            for sql in import_quarter(quarter):
                try:
                    cursor.execute(sql)
                    if "CREATE TABLE" in sql:
                        table_sql = sql
                except:
                    with open(path.join("log","import",quarter+".txt"), "a") as f:
                        f.write(table_sql + "\n")
                        f.write(sql + "\n\n")
            cursor.commit()
        cursor.close()
    print(time.asctime(time.localtime(time.time())))
