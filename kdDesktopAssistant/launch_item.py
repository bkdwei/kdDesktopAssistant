'''
Created on 2019年3月30日

@author: bkd
'''
import webbrowser
from PyQt5.QtWidgets import QWidget,QSizePolicy,QPushButton,QLabel,QVBoxLayout
from PyQt5.QtCore import QSize,Qt
from PyQt5.QtGui import QIcon
from .fileutil import get_file_realpath 
class launch_item(QWidget):
        def __init__(self,name):
            super().__init__()
            sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
            self.setSizePolicy(sizePolicy)
            
            self.setMinimumSize(QSize(200, 100))
            self.setMaximumSize(QSize(100, 200))
            
            self.pushButton = QPushButton(self)
            icon = QIcon(get_file_realpath('data/image/3574/linux.png'))
            self.pushButton.setIcon(icon)
            self.pushButton.setIconSize(QSize(64,64))
            self.pushButton.clicked.connect(self.on_clicked)
            
            self.label = QLabel(self)
            self.label.setText(name)
            
            self.verticalLayout = QVBoxLayout(self)
            self.verticalLayout.addWidget(self.pushButton,0,Qt.AlignCenter)
            self.verticalLayout.addWidget(self.label,0,Qt.AlignCenter)
            
            self.url ="http://www.sogou.com"
        def on_clicked(self):
            print(self.url)
            webbrowser.open_new_tab(self.url)