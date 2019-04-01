'''
Created on 2019年3月30日

@author: bkd
'''
import  sys,os
from PyQt5.uic import loadUi
from PyQt5.QtGui import  QIcon,QPalette,QBrush,QPixmap,QCursor
from PyQt5.QtCore import Qt,QPoint,QSize
from PyQt5.QtWidgets import QMainWindow, QApplication,QGraphicsOpacityEffect,QMessageBox,QLineEdit,QFileDialog,QAction,QMenu,QSizePolicy,QPushButton
from .fileutil import  get_file_realpath
from .launch_item import launch_item
from .dl_launch_item_detail import dl_launch_item_detail
from .session import session
from . import app_data
class kdDesktopAssistant(QMainWindow):

    def __init__(self):
        super().__init__()
        loadUi(get_file_realpath("kdDesktopAssistant.ui"), self)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(get_file_realpath("data/image/S60922-232638.jpg"))))
        self.setWindowIcon(QIcon(get_file_realpath('data/image/logo.png')))
#         self.setPalette(palette)
#         self.gl_apps.setAutoFillBackground(True)
#         self.setWindowOpacity(0.01)
        self.gl_apps.setAlignment(Qt.AlignTop)
        self.setStyleSheet("#MainWindow{border-image:url("+get_file_realpath("data/image/S60922-232113.jpg").replace("\\","/") +");}")
        
#         右键菜单设置
        self.pop_menu = QMenu()
        self.pop_menu_item = [QAction("新增启动项"),QAction("新增桌面"),QAction("删除桌面"),QAction("设置桌面背景"),QAction("设置为主页"),QAction("导出配置"),QAction("导入配置"),QAction("退出")]
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested[QPoint].connect(self.handle_pop_menu)
        
#         初始化数据库连接
#         app_data.get_connection(get_file_realpath("data/db/kdDesktopAssistant.db"))
        self.row = 0
        self.col = 0
        self.sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.session_btn_size = QSize(100, 25)
        self.cur_session_id = None
#         self.init_launch_items()
        self.init_session()
        
        self.dl_launch_item_detail = dl_launch_item_detail()
        self.session = session()
    def remove_item(self,item):
        item.setParent(None)
        self.gl_apps.removeWidget(item)
        del item
    def edit_lauchn_item(self,item, widget):
        self.dl_launch_item_detail.set_item(item)
        promt_info = "修改"
        if self.dl_launch_item_detail.exec_():
            if not item:
                item = {}
                item["id"] = None
                promt_info = "新增"
                
            item["ico"] = self.dl_launch_item_detail.ico_path
            item["name"] = self.dl_launch_item_detail.le_name.text()
            item["url"] = self.dl_launch_item_detail.le_url.text()
            item["type"] = self.dl_launch_item_detail.bg_type.checkedButton().type
            item["session_id"] = self.cur_session_id
            try :
                if item["id"]:
                    app_data.update_launch_item(item)
                    widget.update_item(item)
                else:
                    app_data.insert_launch_item(item)
                    self.add_launch_item(item)
                QMessageBox.information(None, promt_info + "启动项",  promt_info + "启动项成功" , QMessageBox.Yes)
            except Exception as e:
                QMessageBox.warning(None, promt_info + "启动项失败",   str(e), QMessageBox.Yes)
                raise e
    def edit_session(self,item):
        self.session.set_session(item)
        promt_info = "修改"
        if self.session.exec_():
            if not item:
                item = {}
                item["id"] = None
                promt_info = "新增"
                item["type"] = 0
                item["color"] = None
                
            item["name"] = self.session.le_name.text()
            item["picture"] = self.session.le_picture.text()
        try :
            if item["id"]:
                app_data.update_session(item)
                self.setStyleSheet("#MainWindow{border-image:url("+item["picture"] + ");}")
#                 widget.update_item(item)
            else:
                app_data.insert_session_item(item)
                self.add_session(item)
            QMessageBox.information(None, promt_info + "桌面",  promt_info + "桌面成功" , QMessageBox.Yes)
        except Exception as e:
            QMessageBox.warning(None, promt_info + "桌面失败",   str(e), QMessageBox.Yes)
            raise e
    def add_launch_item(self,item):
        li = launch_item(item)
        li.del_item_signal.connect(self.remove_item)
        li.edit_item_signal.connect(self.edit_lauchn_item)
        self.gl_apps.addWidget(li, self.row, self.col, 1, 1)
        self.col += 1
        if self.col >= 3:
            self.col = 0
            self.row += 1
    def init_launch_items(self):
        count = self.gl_apps.count()
        self.row = 0
        self.col = 0
        
        print("gl_apps:" , count)
#         一个老外给的方法，很棒。https://stackoverflow.com/questions/4528347/clear-all-widgets-in-a-layout-in-pyqt
        for i in reversed(range(count)) :
            self.gl_apps.itemAt(i).widget().setParent(None)
        session_id = self.sender().session_id
        picture = self.sender().picture
        self.cur_session = self.sender().item
        if picture :
            self.setStyleSheet("#MainWindow{border-image:url("+picture + ");}")
        print(session_id)
        if not session_id :
            return
        self.item_list = app_data.get_launch_item_list(session_id)
        for item in self.item_list:
            item_dict = app_data.tuple2dict_launch_item(item)
            self.add_launch_item(item_dict)
    def init_session(self):
        self.session_list = app_data.get_session_list()
        for item in self.session_list:
            item_dict = app_data.tuple2dict_session(item)
            self.add_session(item_dict)
    def add_session(self,item):
        pb_session = QPushButton(item["name"])
        pb_session.setSizePolicy(self.sizePolicy)
        pb_session.setMaximumSize(self.session_btn_size)
        op = QGraphicsOpacityEffect()  
        op.setOpacity(0.7)    
        pb_session.setGraphicsEffect(op)  
        pb_session.setAutoFillBackground(True)
#         TODO 待删除
        pb_session.session_id = item["id"]
        pb_session.picture = item["picture"]
        pb_session.item = item
        pb_session.clicked.connect(self.init_launch_items)
        self.hl_session.addWidget(pb_session)
#         TODO 待修正
        self.cur_session_id = item["id"]
    def handle_pop_menu(self):
        action = self.pop_menu.exec_(self.pop_menu_item,QCursor.pos())
        if action:
            action_text = action.text()
            if action_text == "新增启动项" :
                self.edit_lauchn_item(None,None)
            elif action_text == "设置背景":
                filename, _ = QFileDialog.getOpenFileName(self,
                            "选择背景文件",
                            os.path.expanduser('~') , 
                            "(*.jpg);;(*.png)")   #设置文件扩展名过滤,注意用双分号间隔
                if filename:
                    print(filename)
                    self.set_background_image(filename)
            elif action_text == "新增桌面" :
                if self.session.exec_() :
                    session_item = {}
                    session_item["name"] = self.session.le_name.text()
                    session_item["picture"] = self.session.le_picture.text()
                    session_item["type"] = 0
                    session_item["color"] = None
                    app_data.insert_session_item(session_item)
                    QMessageBox.information(self, "新增桌面", "新增桌面成功")
            elif action_text == "设置桌面背景" :
                self.edit_session(self.cur_session)
def main():
    app = QApplication(sys.argv)
    win = kdDesktopAssistant()
#     win.showFullScreen()
#     win.showMaximized()
    win.show()
    sys.exit(app.exec_())