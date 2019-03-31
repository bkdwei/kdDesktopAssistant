'''
Created on 2019年3月30日

@author: bkd
'''
try:
    from os import startfile
except Exception as e:
    pass
import webbrowser,os,subprocess
from PyQt5.QtWidgets import QWidget,QSizePolicy,QPushButton,QLabel,QVBoxLayout,QMenu,QAction,QMessageBox
from PyQt5.QtCore import QSize,Qt,QPoint,pyqtSignal
from PyQt5.QtGui import QIcon,QCursor,QPalette
from .fileutil import get_file_realpath 
from . import app_data
class launch_item(QWidget):
#     删除组件信号
        del_item_signal = pyqtSignal(QWidget)
        edit_item_signal = pyqtSignal(dict,QWidget)
        def __init__(self,item):
            print(item)
            super().__init__()
            self.item  = item
            sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
            self.setSizePolicy(sizePolicy)
            
            self.setMinimumSize(QSize(200, 100))
            self.setMaximumSize(QSize(200, 200))
            
            self.pushButton = QPushButton(self)
            if not item["ico"]:
                icon = QIcon(get_file_realpath('data/image/firefox64.png'))
                self.pushButton.setIcon(icon)
            else :
                icon = QIcon(item["ico"])
                self.pushButton.setIcon(icon)
            self.pushButton.setIconSize(QSize(64,64))
            self.pushButton.clicked.connect(self.on_clicked)
            
            self.label = QLabel(self)
            self.label.setText(item["name"])
#             self.label.setWordWrap(True)
            self.label.setSizePolicy(sizePolicy)
            self.label.setMaximumSize(QSize(150, 50))
            pe = QPalette()
#             self.label.setAutoFillBackground(True)
            pe.setColor(QPalette.WindowText,Qt.white)
            self.label.setPalette(pe)
            
            self.verticalLayout = QVBoxLayout(self)
            self.verticalLayout.addWidget(self.pushButton,0,Qt.AlignCenter)
            self.verticalLayout.addWidget(self.label,0,Qt.AlignCenter)
            
            self.item_popup_menu = QMenu()
            self.setContextMenuPolicy(Qt.CustomContextMenu)
            self.customContextMenuRequested[QPoint].connect(self.handle_pop_menu)
            self.menu_item =[QAction("修改"),QAction("删除")]
        def on_clicked(self):
            url = self.item["url"]
            item_type = self.item["type"]
            if item_type == 1 :
                if not "http" in url :
                    url = "http://" + url
                webbrowser.open_new_tab(url)
            elif item_type in( 2,4) :
                if os.name == "nt":
                    os.startfile(url)
                elif os.name == "posix":
                    subprocess.call(["xdg-open", url])
        def handle_pop_menu(self):
            action = self.item_popup_menu.exec_(self.menu_item,QCursor.pos())
            if action:
                text = action.text()
                if text == "删除":
                    print(text)
                    app_data.delete_launch_item(self.item["name"])
                    self.del_item_signal.emit(self)
                    QMessageBox.information(self, "删除启动项",   "删除启动项成功", QMessageBox.Yes)
                elif text == "修改" :
                    self.edit_item_signal.emit(self.item,self)
        def update_item(self,item):
            self.item = item
            if not item["ico"]:
                icon = QIcon(get_file_realpath('data/image/firefox64.png'))
                icon = self.pushButton.icon() 
                del icon
                self.pushButton.setIcon(icon)
            else :
                icon = QIcon(item["ico"])
                self.pushButton.setIcon(icon)
            self.label.setText(item["name"])