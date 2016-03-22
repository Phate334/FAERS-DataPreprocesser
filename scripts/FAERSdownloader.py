# -*-coding:utf-8-*-
# -------------------------------------------------------------------------------
# Name:        downloader.py
# Purpose:     check local data,and get the latest quarterly data files from 
#              FAERS
#
# Author:      Phate
#
# Created:     28/10/2015
# -------------------------------------------------------------------------------
import os
from urllib2 import urlopen
from bs4 import BeautifulSoup
import DownloadHelper as dh

# this script will find target in this list pages.
host_url = "http://www.fda.gov"
target_page = ["http://www.fda.gov/Drugs/GuidanceComplianceRegulatoryInformation/Surveillance/AdverseDrugEffects/"
              "ucm083765.htm",
              "http://www.fda.gov/Drugs/GuidanceComplianceRegulatoryInformation/Surveillance/AdverseDrugEffects/"
              "ucm082193.htm"]
# local directory to save file.
source_path = "I:\\Temp\\source"
data_path = "I:\\Temp\\data"
if not os.path.isdir(source_path):
    os.makedirs(source_path)
if not os.path.isdir(data_path):
    os.makedirs(data_path)


def get_files_url():
    """ get all file name and url in target_page
    :return: {"name":"url"}
    """
    files = {}
    for page_url in target_page:
        page_bs = BeautifulSoup(urlopen(page_url), "lxml")
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
    files = get_files_url()
    print(len(files))
    for u in files:
        file_name = u[u.find(".")-4:u.find(".")+4]
        print(file_name)
        dh.start(files[u], os.path.join(source_path, file_name.lower()))

if __name__ == "__main__":
    main()