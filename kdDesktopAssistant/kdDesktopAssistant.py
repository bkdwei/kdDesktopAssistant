'''
Created on 2019年3月30日

@author: bkd
'''
import  sys,os
from PyQt5.uic import loadUi
from PyQt5.QtGui import  QIcon,QPalette,QBrush,QPixmap,QCursor
from PyQt5.QtCore import Qt,QPoint
from PyQt5.QtWidgets import QMainWindow, QApplication,QGraphicsOpacityEffect,QInputDialog,QLineEdit,QFileDialog,QAction,QMenu
from .fileutil import  get_file_realpath
from .launch_item import launch_item
class kdDesktopAssistant(QMainWindow):

    def __init__(self):
        super().__init__()
        loadUi(get_file_realpath("kdDesktopAssistant.ui"), self)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(get_file_realpath("data/image/S60922-232638.jpg"))))
        self.setWindowIcon(QIcon(get_file_realpath('data/image/logo.png')))
#         self.setPalette(palette)
#         self.gl_apps.setAttribute(Qt.WA_TranslucentBackground, False)
#         self.gl_apps.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
#         self.gl_apps.setAttribute(Qt.WA_TranslucentBackground)
        op = QGraphicsOpacityEffect()  
        op.setOpacity(0.7)  
        op2 = QGraphicsOpacityEffect()  
        op2.setOpacity(0.7)  
        op3 = QGraphicsOpacityEffect()  
        op3.setOpacity(0.7)  
        self.pb1.setGraphicsEffect(op)  
        self.pb1.setAutoFillBackground(True)
        self.pb2.setGraphicsEffect(op2)  
        self.pb2.setAutoFillBackground(True)
        self.setWindowOpacity(0.01)
#         self.gl_apps.setAutoFillBackground(True)
        self.gl_apps.setAlignment(Qt.AlignTop)
        li = launch_item("abc")
        self.gl_apps.addWidget(li, 0, 3, 1, 1)
        li2 = launch_item("edf")
        self.gl_apps.addWidget(li2, 0, 4, 1, 1)
        self.setStyleSheet("#MainWindow{border-image:url("+get_file_realpath("data/image/S60922-232113.jpg").replace("\\","/") +");}")
        
#         右键菜单设置
        self.pop_menu = QMenu()
        self.pop_menu_item = [QAction("新增启动项"),QAction("修改启动项"),QAction("新增桌面"),QAction("删除桌面"),QAction("设置桌面背景"),QAction("设置为主页"),QAction("导出配置"),QAction("导入配置"),QAction("退出")]
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested[QPoint].connect(self.handle_pop_menu)
    def handle_pop_menu(self):
        action = self.pop_menu.exec_(self.pop_menu_item,QCursor.pos())
        if action:
            action_text = action.text()
            if action_text == "新增启动项" :
                value, ok = QInputDialog.getText(self, "启动项", "请输入会话标题:", QLineEdit.Normal)
                if ok:
                    pass
            elif action_text == "设置背景":
                filename, _ = QFileDialog.getOpenFileName(self,
                            "选择背景文件",
                            os.path.expanduser('~') , 
                            "(*.jpg);;(*.png)")   #设置文件扩展名过滤,注意用双分号间隔
                if filename:
                    print(filename)
                    self.set_background_image(filename)
def main():
    app = QApplication(sys.argv)
    win = kdDesktopAssistant()
#     win.showFullScreen()
    win.show()
    sys.exit(app.exec_())