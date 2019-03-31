# -*- coding:utf-8 -*-
'''
Created on 2019年3月3日

@author: bkd
'''
import requests,re
from os.path import exists 
from urllib import parse,request
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QEvent
from .fileutil import get_file_realpath
from nltk.corpus import reuters


class dl_launch_item_detail(QDialog):
    
    def __init__(self):
        super().__init__()
        loadUi(get_file_realpath("dl_launch_item_detail.ui"), self)
        self.le_url.installEventFilter(self)
        self.rb_url.type = 1
        self.rb_dir.type = 2
        self.rb_catelog.type = 3
        self.rb_other.type = 4
        self.ico_path = None
    def set_item(self,item):
        if not item:
            return;
        if not item["ico"]:
            self.ico_path = get_file_realpath('data/image/firefox64.png')
        else :
            self.ico_path = item["ico"]
        icon = QIcon(self.ico_path)
        self.pb_icon.setIcon(icon)
        self.le_name.setText(item["name"])
        self.le_url.setText(item["url"])
#     def on_le_url_focusOut(self):

    def eventFilter(self, qobject, qevent):
        qtype = qevent.type()
        if qtype == QEvent.FocusOut :
            url = self.le_url.text()
            parsed_url_dict = parse.urlsplit(url)
            print("parsed_url_dict:" ,parsed_url_dict)

#             获取标题
            html = request.urlopen(url).read().decode('utf-8')
            title=re.findall('<title>(.+)</title>',html)
            if not title :
                html = request.urlopen(url.replace("https:","http:")).read().decode('utf-8')
                title=re.findall('<title>(.+)</title>',html)
            self.le_name.setText(title[0])
            
#             获取网站logo
            favicon_url = parsed_url_dict[0] + "://" +parsed_url_dict[1] + "/favicon.ico"
            print("favicon_path：" + favicon_url)
            favicon_path = get_file_realpath("data/image/netico/" + parsed_url_dict[1].replace(".","_") + ".ico")
            print("favicon_path:" + favicon_path)
            self.ico_path = favicon_path
            if not exists(favicon_path):
                print("正在下载网站logo")
                favicon = request.urlopen(favicon_url).read()
                with open(favicon_path,"wb") as fp:
                    fp.write(favicon)
            icon = QIcon(favicon_path)
            self.pb_icon.setIcon(icon)
        return False
        