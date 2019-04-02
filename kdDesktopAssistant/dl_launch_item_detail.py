# -*- coding:utf-8 -*-
'''
Created on 2019年3月3日

@author: bkd
'''
import re
from os.path import exists,expanduser,basename
from urllib import parse,request
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog,QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QEvent, pyqtSlot
from .fileutil import get_file_realpath


class dl_launch_item_detail(QDialog):
    
    def __init__(self):
        super().__init__()
        loadUi(get_file_realpath("dl_launch_item_detail.ui"), self)
        self.le_url.installEventFilter(self)
        self.rb_url.type = 1
        self.rb_dir.type = 2
        self.rb_catelog.type = 3
        self.rb_other.type = 4
        self.set_icon(get_file_realpath("data/image/firefox64.png"))
    @pyqtSlot()
    def on_pb_icon_clicked(self):
        filename, _ = QFileDialog.getOpenFileName(self,"选择背景文件",expanduser('~') ,"*")   #设置文件扩展名过滤,注意用双分号间隔
        if filename:
            self.set_icon(filename)
    @pyqtSlot()
    def on_pb_url_clicked(self):
        if self.rb_dir.isChecked() :
            path = QFileDialog.getExistingDirectory(self, '选择文件夹', expanduser("~"))
            if path :
                self.le_url.setText(path)
                self.le_name.setText(basename(path))
                self.set_icon(get_file_realpath("data/image/folder.svg"))
        elif self.rb_url.isChecked():
            QMessageBox.information(self, "设置网址", "请直接文本框中输入你的网址")
        elif self.rb_other.isChecked() :
            filename,_ = QFileDialog.getOpenFileName(self, '选择文件', expanduser("~"))
            if filename :
                self.le_url.setText(filename)
                self.le_name.setText(basename(filename))
        
    @pyqtSlot()
    def on_rb_url_clicked(self):
        self.le_url.setEnabled(True)
        self.set_icon(get_file_realpath("data/image/firefox64.png"))
    @pyqtSlot()
    def on_rb_dir_clicked(self):
        self.le_url.setEnabled(True)
        self.set_icon(get_file_realpath("data/image/folder.svg"))
    @pyqtSlot()
    def on_rb_catelog_clicked(self):
        self.le_url.setEnabled(False)
        self.set_icon(get_file_realpath("data/image/catelog.svg"))
    @pyqtSlot()
    def on_rb_other_clicked(self):
        self.le_url.setEnabled(True)
        self.set_icon(get_file_realpath("data/image/file.png"))
    def set_item(self,item):
        if not item:
            return;
        if not item["ico"]:
            self.set_icon(get_file_realpath('data/image/firefox64.png'))
        else :
            self.set_icon(item["ico"])
        self.le_name.setText(item["name"])
        self.le_url.setText(item["url"])
        
        item_type = item["type"]
        if item_type == 1:
            self.rb_url.setChecked(True)
        elif item_type == 2:
            self.rb_dir.setChecked(True)
        if item_type == 3:
            self.rb_catelog.setChecked(True)
        if item_type == 4:
            self.rb_other.setChecked(True)
#     def on_le_url_focusOut(self):

    def set_icon(self,path):
            self.ico_path = path
            self.pb_icon.setText(None)
            icon = QIcon(self.ico_path)
            self.pb_icon.setIcon(icon)
    def eventFilter(self, qobject, qevent):
        qtype = qevent.type()
        if qtype == QEvent.FocusOut :
            if not self.rb_url.isChecked():
                return
            url = self.le_url.text()
            item = self.get_url_info(url)
            self.le_name.setText(item["name"])
            self.le_url.setText(item["url"])
            self.set_icon(item["ico"])
            item["id"] = self.item["id"]
            self.item = item
        return False
    def get_url_info(self,url):
        item = {}
        if not url.startswith("http") :
            url = "http://" + url
        parsed_url_dict = parse.urlsplit(url)
        print("parsed_url_dict:" ,parsed_url_dict)

#             获取标题
        html = request.urlopen(url).read().decode('utf-8')
        title=re.findall('<title>(.+)</title>',html)
        if not title :
#             有些https开头的网址有可能获取失败
            html = request.urlopen(url.replace("https:","http:")).read().decode('utf-8')
            title=re.findall('<title>(.+)</title>',html)
        item["name"] = title[0]
            
#             获取网站logo
        favicon_url = parsed_url_dict[0] + "://" +parsed_url_dict[1] + "/favicon.ico"
        print("favicon_path：" + favicon_url)
        favicon_path = get_file_realpath("data/image/netico/" + parsed_url_dict[1].replace(".","_") + ".ico")
        print("favicon_path:" + favicon_path)
        if not exists(favicon_path):
            print("正在下载网站logo")
            try:
                favicon = request.urlopen(favicon_url).read()
                with open(favicon_path,"wb") as fp:
                    fp.write(favicon)
#                 self.set_icon(favicon_path)
#                 self.ico_path = favicon_path
            except Exception as e:
                print("下载网站logo:" +str(e))
        else :
            self.ico_path = favicon_path
        item["ico"] = favicon_path
        item["url"] = url
        item["type"] = 1
        print("return item:" ,item)
        return item
        