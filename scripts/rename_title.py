# -*- coding: utf-8 -*-
import os

input_dir = "clean"
output_dir = "replace_title"
log_dir = "log"

new_title_tag = {
    "ISR":"PRIMARYID",
    "CASE":"CASEID",
    "I_F_COD":"I_F_CODE",
    "GNDR_COD":"SEX",
    "ROUTE":"ROUTE_",
    "DRUG_SEQ":["DSG_DRUG_SEQ","INDI_DRUG_SEQ"]  # 0:THER(THERAPY),1:INDI(INDICATIONS)
    }

def replace_title_tag(season, file):
    with open(os.path.join(input_dir, season, file),"r") as f:
        title = f.readline().upper()
        title_tag = [t.strip() for t in title.split("$")]  # DEMO12Q4有欄位前面多一個空格
        for index, tag in enumerate(title_tag):
            if tag in new_title_tag:
                if tag == "DRUG_SEQ":
                    if file[0:4] == "THER":
                        title_tag[index] = new_title_tag[tag][0]
                    elif file[0:4] == "INDI":
                        title_tag[index] = new_title_tag[tag][1]
                else:
                    title_tag[index] = new_title_tag[tag]
        if not os.path.isdir(os.path.join(output_dir, season)):
            os.makedirs(os.path.join(output_dir, season))
        output = open(os.path.join(output_dir, season, file),"w")
        output.write("%s\n"%"$".join(title_tag))
        for line in f:
            output.write(line)
        output.close()

def get_title(dir_path, file):
    title = ""
    with open(os.path.join(dir_path, file),"r") as f:
        title = f.readline()
    return title
        
if __name__ == "__main__":
    log = open(os.path.join(log_dir,"replace_title.txt"),"a")
    for season in os.listdir(input_dir):
        season_dir = os.path.join(input_dir, season)
        for file in os.listdir(season_dir):
            print(file)
            log.write("%s\n"%file)
            log.write("%s"%get_title(season_dir, file))
            replace_title_tag(season, file)
            log.write("%s\n"%get_title(os.path.join(output_dir, season), file))
    log.close()
