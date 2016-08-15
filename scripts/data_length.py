# -*- coding:utf-8 -*-
"""
這份腳本用來掃描清洗過的資料，列出該欄位在所有資料中的最大長度，可以幫助你在編輯metadata時決定型態。
"""
import os
import json

in_dir = "clean"

metadata={}
for quarter in os.listdir(in_dir):
    quar_dir = os.path.join(in_dir, quarter)
    for table in os.listdir(quar_dir):
        metadata.setdefault(table[:4], {})
        with open(os.path.join(quar_dir, table)) as f:
            tags = f.readline().strip().split("$")
            for t in tags:
                metadata[table[:4]].setdefault(t, 0)
            for line in f:
                row = line.strip().split("$")
                for i, r in enumerate(row):
                    metadata[table[:4]][tags[i]] = max(metadata[table[:4]][tags[i]], len(row[i]))
with open("meta.json", "w") as f:
    f.write(json.dumps(metadata))