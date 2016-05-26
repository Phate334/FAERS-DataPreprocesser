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
    files = get_files_url()
    for u in files:
        file_name = re.search("\d{4}[qQ]\d", u).group()
        print(file_name)
        urlretrieve(files[u], os.path.join(source_dir, file_name.lower() + ".zip"))

if __name__ == "__main__":
    main()
