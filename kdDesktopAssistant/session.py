'''
Created on 2019年3月31日

@author: bkd
'''
from os.path import expanduser
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import  QDialog,QFileDialog
from PyQt5.QtGui import QPixmap 
from .fileutil import get_file_realpath

class session(QDialog):
    def __init__ (self):
        super().__init__()
        loadUi(get_file_realpath("session.ui"), self)

    @pyqtSlot()
    def on_pb_picture_clicked(self):
        filename,_ = QFileDialog.getOpenFileName(self, '选择文件', expanduser("~"))
        if filename :
            self.le_picture.setText(filename)
            p = QPixmap(filename).scaled(300,300)
            self.lb_preview.setPixmap(p)
    def set_session(self,item):
        if not item:
            return;
        self.le_name.setText(item["name"])
        self.le_picture.setText(item["picture"])