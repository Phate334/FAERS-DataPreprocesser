# -*- coding:utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        DownloadHelper.py
# Purpose:     give a simple progress bar when you downloading.
#
# Author:      Phate
#
# Created:     16/09/2014
# Copyright:   (c) Phate 2014
# -------------------------------------------------------------------------------
import urllib


def callback(blocknum, blocksize, totalsize):
    """
    @blocknum: 已下載數量
    @blocksize: 每部分大小
    @totalsize: 總大小
    """
    percent = 100.0 * blocknum * blocksize / totalsize
    if percent > 100:
        percent = 100
    print "%s/%s (%.2f%%)\r" % (blocknum*blocksize, totalsize, percent),


def start(url, local):
    """call this method.
    :param url: get from their.
    :param local: save to this local path.
    """
    urllib.urlretrieve(url, local, callback)
