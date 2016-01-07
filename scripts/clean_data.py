# -*- coding: utf-8 -*-
# 把資料中不正常的換行符號刪除
# 下次應該修改檔案寫入的部分，不要每行都開檔

import os

input_dir = "data"
output_dir = "C:\\temp\\clean"
log_dir = "log"

def write_clean(season, name, data):
    with open(os.path.join(output_dir, season, name), "a") as f:
        f.write(data + "\n")

def write_error(name, data):
    with open(os.path.join(log_dir, name), "a") as f:
        f.write(data + "\n")

for season in os.listdir(input_dir):
    season_dir = os.path.join(input_dir, season)
    # create output directory
    try:
        os.makedirs(os.path.join(output_dir, season))
    except:
        pass
        # print("issue:" + season)
    # 單獨處理檔案
    for file in os.listdir(season_dir):
        print(file)
        with open(os.path.join(season_dir, file)) as f:
            file = file.upper()
            quarter = file[4:8]
            title = f.readline().strip()
            write_clean(season, file, title)
            title_num = len(title.split("$"))
            buf = ""
            for line in f:
                buf += line.replace("\n", "")
                temp = buf.split("$")
                if len(temp) > (title_num+1):
                    write_error(file, buf)
                    buf = ""
                    continue
                if "04Q1" <= quarter and quarter <= "12Q3":
                    if file[0:4] == "INDI":
                        if len(temp) == title_num:
                            write_clean(season, file, buf)
                            buf = ""
                    else:
                        if len(temp) == (title_num+1):
                            write_clean(season, file, buf)
                            buf = ""
                elif "12Q4" <= quarter and quarter <= "14Q2":
                    if len(temp) == title_num:
                        write_clean(season, file, buf)
                        buf = ""