# -*- coding: utf-8 -*-
import os
from shutil import copyfile 
import json

input_dir = "replace_title"
extra_dir = "extra_data"
output_dir = "appended_data"
log_dir = "log"

def append_extra_demo(season, file):
    with open(os.path.join(extra_dir, "demo", "%s.json"%(file.split(".")[0])), "r") as f:
        extra = json.loads(f.read())
    
    src = open(os.path.join(input_dir, season, file), "r")
    with open(os.path.join(output_dir, season, file), "w") as des:
        first_line = src.readline().strip()
        fields = first_line.split("$")
        src_tag_num = len(fields)  # 原始欄位數量，用來避免結尾有$的資料。
        fields.append("WT_KG")
        fields.append("AGE_TYPE")
        des.write("%s\n" % ("$".join(fields)))
        for row in src:
            data = row.strip().split("$")[:src_tag_num]
            pid = data[fields.index("PRIMARYID")]
            try:
                wt, age = extra[pid]
                wt = str(wt) if wt else ""
                age = str(age) if age else ""
            except KeyError:
                with open(os.path.join(log_dir,"key_error",file), "a") as log:
                    log.write("%s\n"%pid)
                wt = ""
                age = ""
            data.append(wt)
            data.append(age)
            des.write("%s\n" % ("$".join(data)))
    src.close()
    
    
def append_extra_drug(season, file):
    with open(os.path.join(extra_dir, "drug", "chaotic_drug_list20%s.json"%(file.split(".")[0][4:8])), "r") as f:
        extra = json.loads(f.read())
    
    src = open(os.path.join(input_dir, season, file), "r")
    with open(os.path.join(output_dir, season, file), "w") as des:
        first_line = src.readline().strip()
        fields = first_line.split("$")
        src_tag_num = len(fields)  # 原始欄位數量，用來避免結尾有$的資料。
        fields.append("RXCUI")
        des.write("%s\n" % ("$".join(fields)))
        for row in src:
            data = row.strip().split("$")[:src_tag_num]
            d_name = data[fields.index("DRUGNAME")].strip()
            try:
                rxcui = extra[d_name]
            except:
                with open(os.path.join(log_dir,"key_error",file), "a") as log:
                    log.write("%s\n"%d_name)
                rxcui = ""
            data.append(rxcui)
            data = [str(d) for d in data]
            des.write("%s\n" % ("$".join(data)))
    src.close()

if __name__ == "__main__":
    for season in os.listdir(input_dir):
        season_dir = os.path.join(input_dir, season)
        if not os.path.isdir(os.path.join(output_dir, season)):
            os.makedirs(os.path.join(output_dir, season))
        for file in os.listdir(season_dir):
            print(file)
            if "DEMO" in file:
                append_extra_demo(season, file)
            elif "DRUG" in file:
                append_extra_drug(season, file)
            else:
                copyfile(os.path.join(season_dir,file), 
                         os.path.join(output_dir, season, file))
