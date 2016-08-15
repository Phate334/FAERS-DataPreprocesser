# -*- coding:utf-8 -*-
# 計算DEMO中的AGE_TYPE並寫入資料庫
import time
import pyodbc

db_name = "FAERS"

select_age = "SELECT PRIMARYID, AGE, AGE_COD FROM {0};"
get_columns = "SELECT Name FROM SysColumns WHERE id=Object_Id('{0}')"
add_type_column = "ALTER TABLE {0} ADD AGE_TYPE tinyint;"
update_age_type = "UPDATE {0} SET AGE_TYPE = {1} WHERE PRIMARYID = {2}"


def get_age_type(age_data):
    """輸入AGE跟AGE_COD，計算AGE_TYPE
    """
    age, age_cod = age_data
    if age == None or age_cod == None:
        return None
    # 單位從小到大，例如輸入AGE_COD是秒SEX，則會先被轉成分鐘MIN，最後會變成年YR
    if age_cod == "SEC":
        age/=60
        age_cod="MIN"
    if age_cod == "MIN":
        age/=60
        age_cod="HR"
    if age_cod == "HR":
        age/=24
        age_cod="DY"
    if age_cod == "DY":
        age/=7
        age_cod="WK"
    if age_cod == "WK":
        age/=4
        age_cod="MON"
    if age_cod == "MON":
        age/=12
        age_cod="YR"
    if age_cod == "DEC":
        age*=10
        age_cod="YR"
    if age_cod != "YR":
        return None
    # 年齡離散化規則參考網站上整理的表格
    if age < 0:  # 0代表有資料但是不合理
        return 0
    if age < 1 :#Infant, Newborn
        return 1
    if age < 2 :#Infant
        return 2
    if age < 5 :#Child Preschool
        return 3
    if age < 12:#Child
        return 4
    if age < 18:#Adolescent
        return 5
    if age < 24:#Young Adult
        return 6
    if age < 44:#Adult
        return 7
    if age < 64:#Middle Aged
        return 8
    if age < 79:#Aged
        return 9
    if age < 123:#Aged+
        return 10
    return 0

def set_db_age_type(quarter):
    """一次處理一季，在DEMO加入AGE_TYPE欄位，並依AGE和AGE_COD算出。
    """
    data = {}
    with pyodbc.connect("driver={SQL Server};server=localhost;Trusted_Connection=yes", database=db_name) as con:
        with con.cursor() as cursor:
            row = cursor.execute(select_age.format(quarter))
            for pid, age, age_type in row:  # 先把該季年齡值與單位取出
                try:
                    data[pid] = (float(age), age_type.strip())
                except:
                    continue
            print("{0} >> {1} records".format(quarter, len(data)))
            # 如果表內沒有 AGE_TYPE 欄位要先新增
            columns = [c for c, in cursor.execute(get_columns.format(quarter))]
            if "AGE_TYPE" not in columns:
                cursor.execute(add_type_column.format(quarter))
            # 設定AGE_TYPE
            for pid in data:
                age_type = get_age_type(data[pid])
                if age_type:  # 有回傳值
                    cursor.execute(update_age_type.format(quarter, age_type, pid))
                else:
                    cursor.execute(update_age_type.format(quarter, "NULL", pid))
            cursor.commit()

def main():
    with pyodbc.connect("driver={SQL Server};server=localhost;Trusted_Connection=yes", database=db_name) as con:
        with con.cursor() as cursor:
            tables = [t for t, in cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.Tables;") if "DEMO" in t]
    tables.sort()
    for quarter in tables:
        set_db_age_type(quarter)

if __name__ == "__main__":
    print(time.asctime(time.localtime(time.time())))
    main()
    print(time.asctime(time.localtime(time.time())))
