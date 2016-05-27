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
    """ 找到target_page中所有需要下載的檔案
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
            print(file_name)
            urlretrieve(faers_files[aTitle], os.path.join(source_dir, file_name))
    # unpack
    unpacked_file = os.list(data_dir)
    for zip_file_name in os.listdir(source_dir):
        quarter_zip_file = ZipFile(os.path.join(source_dir, zip_file_name),"r")
        dir_name = re.search("\d{4}[qQ]\d", zip_file_name).group()
        os.mkdir(dir_name)
        for file_name in quarter_zip_file.namelist():
            file_name = file_name.lower()
            # 未完成

if __name__ == "__main__":
    main()
