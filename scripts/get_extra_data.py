#-*- coding:utf-8 -*-
import os
import json
import pyodbc

output_demo_dir = "extra_data\\demo"
output_drug_dir = "extra_data\\drug"

def get_demo(table_name):
    fields = ["PRIMARYID", "WT_KG", "AGE_TYPE"]
    select_demo_sql = "SELECT %s FROM %s;" % (",".join(fields), table_name)
    
    data = {}
    with pyodbc.connect(driver = '{SQL Server}', server = '192.168.1.2', database = 'FAERS', UID="ciluser", PWD="ciluser411") as con:
        with con.cursor() as cursor:
            cur = cursor.execute(select_demo_sql)
            for pid, wt, age in cur:
                data[pid] = (wt,age)
    with open(os.path.join(output_demo_dir,"%s.json"%(table_name)),"w") as f:
        f.write(json.dumps(data))
            
def get_drug(table_name):
    fields = ["drug_name", "rxcui"]
    select_drug_sql = "SELECT %s FROM %s" % (",".join(fields), table_name)
    
    data = {}
    with pyodbc.connect('Trusted_Connection=yes', driver = '{SQL Server}',server = 'localhost', database = 'Generalized_Drug') as con:
        with con.cursor() as cursor:
            cur = cursor.execute(select_drug_sql)
            for d_name, rxcui in cur:
                data[d_name.strip()] = rxcui
    with open(os.path.join(output_drug_dir,"%s.json"%(table_name)),"w") as f:
        f.write(json.dumps(data))

if __name__ == "__main__":
    with pyodbc.connect(driver = '{SQL Server}', server = '192.168.1.2', database = 'FAERS', UID="ciluser", PWD="ciluser411") as con:
        with con.cursor() as cursor:
            cur = cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.Tables")
            demo_tables = [t for t, in cur if "DEMO" in t]
            demo_tables.sort()
    with pyodbc.connect('Trusted_Connection=yes', driver = '{SQL Server}',server = 'localhost', database = 'Generalized_Drug') as con:
        with con.cursor() as cursor:
            cur = cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.Tables")
            drug_tables = [t for t, in cur if "chaotic_drug_list" in t]
            drug_tables.sort()
    for t_name in demo_tables:
        print(t_name)
        get_demo(t_name)
    for t_name in drug_tables:
        print(t_name)
        get_drug(t_name)