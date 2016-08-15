
# FAERS 前置處理流程 #

1. FAERSdownloader.py 

    從 FAERS 爬取所有資料並解壓縮成文字檔。

2. clean.py

    檢查每一行資料，並將欄位名稱更新至最新版本。

3. import_db.py & metadata.py

    把文字檔資料匯入資料庫。

4. set_age_type.py

    年齡資料離散化並加入在DEMO表格中新增的 AGE_TYPE 欄位。

----------

## 其他腳本用途 ##


- data_length.py

計算七個表格中每個欄位的最大長度，方便設定metadata.py。


