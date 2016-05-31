# -*-coding:utf-8-*-
# -------------------------------------------------------------------------------
# Name:        FAERS downloader
# Purpose:     check local data,and get the latest quarterly data files from 
#              FAERS
#
# Author:      Phate
#
# Created:     28/10/2015
# -------------------------------------------------------------------------------
import os
import re
import shutil
from zipfile import ZipFile
from urllib import urlretrieve
from urllib2 import urlopen
from bs4 import BeautifulSoup

# this script will find target in this list pages.
host_url = "http://www.fda.gov"
target_page = ["http://www.fda.gov/Drugs/GuidanceComplianceRegulatoryInformation/Surveillance/AdverseDrugEffects/ucm083765.htm",
               "http://www.fda.gov/Drugs/GuidanceComplianceRegulatoryInformation/Surveillance/AdverseDrugEffects/ucm082193.htm"]
# local directory to save file.
source_dir = "FAERSsrc"
data_dir = "FAERSdata"
if not os.path.isdir(source_dir):
    os.makedirs(source_dir)
if not os.path.isdir(data_dir):
    os.makedirs(data_dir)

def get_files_url():
    """ 找到target_page中所有需要下載的檔案路徑
    :return: {"name":"url"}
    """
    files = {}
    for page_url in target_page:
        try:
            page_bs = BeautifulSoup(urlopen(page_url), "lxml")
        except:
            page_bs = BeautifulSoup(urlopen(page_url))
        for url in page_bs.find_all("a"):
            a_string = unicode(url.string)
            if "ASCII" in a_string.upper():
                files[a_string.encode("utf-8")] = host_url + url["href"]
        for url in page_bs.find_all("linktitle"):
            a_string = unicode(url.string)
            if "ASCII" in a_string.upper():
                files[a_string.encode("utf-8")] = host_url + url.parent["href"]
    return files


def main():
    """
    1.找出FAERS線上可用的檔案，並下載本地端缺少的資料。
    2.解壓縮
    """
    faers_files = get_files_url()
    local_files = os.listdir(source_dir)
    # download
    for aTitle in faers_files:
        file_name = re.search("\d{4}[qQ]\d", aTitle).group().lower() + ".zip"
        if file_name not in local_files:
            print("download " + file_name)
            urlretrieve(faers_files[aTitle], os.path.join(source_dir, file_name))
    # unpack
    # 04年到15年的資料中FAERS並沒有檢查打包的內容，壓縮檔中的內容可能出現的狀況:
    # 1. 檔名與副檔名的大小寫並沒有統一。
    # 2. 大部分資料打包在壓縮檔中的ascii目錄，但13Q1和13Q2例外。
    # 3. 每一季需要其中的7個表格，檔名格式[A-Z]{4}\d{2}[qQ]\d.[txTX]{3}。
    # 壓縮檔中有兩個類似的檔案需要過濾 SIZEXXQX.TXT 和 ascii/STATXXQX.TXT
    unpacked_file = os.listdir(data_dir)
    for zip_file_name in os.listdir(source_dir):
        quarter_zip_file = ZipFile(os.path.join(source_dir, zip_file_name),"r")
        quarter_name = re.search("\d{2}[qQ]\d", zip_file_name).group()
        if quarter_name not in unpacked_file:  # 已解壓縮目錄中還沒有的資料
            print("extract " + zip_file_name)
            des_path = os.path.join(data_dir, quarter_name)
            os.mkdir(des_path)
            for member in quarter_zip_file.namelist():
                file_name = os.path.basename(member)
                if not file_name:  # member 是目錄不是檔案
                    continue
                if "SIZE" in file_name.upper() or "STAT" in file_name.upper():
                    continue
                if not re.search("[A-Z]{4}\d{2}[qQ]\d.[txTX]{3}", file_name):
                    continue
                src_file = quarter_zip_file.open(member)
                des_file = file(os.path.join(des_path, file_name.upper()), "wb")
                with src_file, des_file:
                    shutil.copyfileobj(src_file, des_file)
        quarter_zip_file.close()

if __name__ == "__main__":
    main()
