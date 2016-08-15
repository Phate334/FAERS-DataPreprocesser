# -*- coding:utf-8 -*-
# 把資料中不正常的換行符號刪除
import os
import time

input = "FAERSdata"
output = "clean"
log_dir = "log"

# 要替換的舊欄位放在key，新版本的欄位名稱放value
new_title_version = {
    "ISR":"PRIMARYID",
    "CASE":"CASEID",
    "I_F_COD":"I_F_CODE",
    "GNDR_COD":"SEX",
    "ROUTE":"ROUTE_",
    "DRUG_SEQ":["DSG_DRUG_SEQ","INDI_DRUG_SEQ"],  # 0:THER(THERAPY),1:INDI(INDICATIONS)
    "LOT_NBR":"LOT_NUM",  # 2012Q4資料比較多問題
    "OUTC_CODE":"OUTC_COD"
    }

def clean(quarter):
    in_dir = os.path.join(input, quarter)
    out_dir = os.path.join(output, quarter)
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    # 開始處理每張表格
    for table in os.listdir(in_dir):
        tags = ""
        with open(os.path.join(in_dir, table)) as f:
            title = f.readline().strip().upper()
            tags = title.split("$")
            # 刪除 2012Q4 檔案開頭的 utf-8 BOM 標記
            tags[0] = tags[0].replace("\xef\xbb\xbf","")
            data = []
            # 開始處理資料
            line = f.readline()
            while line:
                line = line.strip()
                row = line.split("$")
                #資料欄位有少代表資料被換行符號切開了，用下一行嘗試拼回來
                if len(row) < len(tags):
                    temp = f.readline()
                    if temp != None:
                        temp = temp.strip()
                    else:
                        break
                    row = (line + temp).split("$")
                    # 如果拚回來的太多欄則檢查下一行是否完整
                    if len(row) > len(tags) +1:
                        if len(temp.split("$")) == len(tags) + 1 or len(temp.split("$")) == len(tags):
                            row = temp.split("$")
                        else:  # 如果下一行temp也不完整，這兩行都丟掉
                            line = f.readline()
                            continue
                # 如果只多一欄是因為前幾季資料結尾都多一個$，直接把最後一欄刪掉
                if len(row) == len(tags) + 1:
                    row = row[:len(tags)]
                if len(row) == len(tags):
                    data.append("$".join(row))
                line = f.readline()
        # 寫到輸出目錄
        with open(os.path.join(out_dir, table), "w") as f:
            # 更新欄位名稱
            for index, t in enumerate(tags):
                tags[index] = tags[index].strip()
                if t in new_title_version:
                    if t == "DRUG_SEQ":
                        if table[:4] == "THER":
                            tags[index] = new_title_version[t][0]
                        elif table[:4] == "INDI":
                            tags[index] = new_title_version[t][1]
                    else:
                        tags[index] = new_title_version[t]
            f.write("{0}\n".format("$".join(tags)))
            f.write("\n".join(data))
            

def main():
    for quarter in os.listdir(input):
        clean(quarter)

if __name__ == "__main__":
    print(time.asctime(time.localtime(time.time())))
    print("cleaing...")
    main()
    print(time.asctime(time.localtime(time.time())))
