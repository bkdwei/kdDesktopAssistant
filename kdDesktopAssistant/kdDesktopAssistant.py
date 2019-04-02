'''
Created on 2019年3月30日

@author: bkd
'''
import  sys,math
from os.path import expanduser,isfile,isdir, basename
from PyQt5.uic import loadUi
from PyQt5.QtGui import  QIcon,QCursor,QPalette, QBrush, QPixmap,QClipboard
from PyQt5.QtCore import Qt,QPoint,QSize,pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication,QGraphicsOpacityEffect,QMessageBox,QFileDialog,QAction,QMenu,QSizePolicy,QPushButton,QSystemTrayIcon,QDesktopWidget,QGridLayout,QWidget,QFrame
from .fileutil import  get_file_realpath
from .launch_item import launch_item
from .dl_launch_item_detail import dl_launch_item_detail
from .session import session
from . import app_data
from  .kdconfig import set_home_session,set_web_mode,get_option_value,get_option_int
from .kdconfig import get_option_boolean
class kdDesktopAssistant(QMainWindow):

    def __init__(self):
        super().__init__()
        loadUi(get_file_realpath("kdDesktopAssistant.ui"), self)
        icon = QIcon(get_file_realpath('data/image/logo.png'))
        self.setWindowIcon(icon)
        self.setWindowFlag(Qt.FramelessWindowHint)
        
#         self.setStyleSheet("#MainWindow{border-image:url("+get_file_realpath("data/image/S60922-232113.jpg").replace("\\","/") +");}")
        self.gl_apps.setAlignment(Qt.AlignTop)
        
#         右键菜单设置
        self.pop_menu = QMenu()
        self.pop_menu_item = [QAction("新增启动项"),QAction("新增桌面"),QAction("设置背景图片"),QAction("修改桌面"),QAction("删除桌面"),QAction("设置为主桌面"),QAction("小程序模式"),QAction("导出配置"),QAction("导入配置"),QAction("退出")]
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested[QPoint].connect(self.handle_pop_menu)
        
#         系统托盘
        sys_tray = QSystemTrayIcon(self)
        self.sys_tray = sys_tray
        sys_tray.setIcon(icon)
        sys_tray.activated.connect(self.sys_tray_handler)
        sys_tray_menu = QMenu()
        sys_tray_menu.menu_items   =[ QAction("退出",self,triggered=sys.exit)]
        sys_tray.setContextMenu(sys_tray_menu)
        sys_tray.show()

        self.session_bt_size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.session_btn_size = QSize(100, 25)
#         初始化桌面
        print(QDesktopWidget().screenGeometry().height())
        print(self.gl_apps.geometry().height())
        self.vetical_widget_number = math.floor((QDesktopWidget().screenGeometry().height() - 250) / get_option_int("item_size"))
        self.home_session = get_option_value("home_session")
        self.init_session()
        
#         初始化对话框对象
        self.dl_launch_item_detail = dl_launch_item_detail()
        self.session = session()
        self.wg_catelog = QFrame()
        self.gl_catelog = QGridLayout()
        self.wg_catelog.setLayout(self.gl_catelog)
#         self.gl_catelog.setWindowOpacity(0.5)
#         self.wg_catelog.setAttribute(Qt.WA_TranslucentBackground,True )
        self.wg_catelog.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.wg_catelog.setAutoFillBackground(True)
        
#         self.wg_catelog.setStyleSheet("background-image:url("+get_file_realpath("data/image/bg_catelog.gif") + ");background-size:cover;}")
        p = QPalette()
        p.setBrush(QPalette.Background, QBrush(QPixmap(get_file_realpath("data/image/bg_catelog.gif"))))
        self.wg_catelog.setPalette(p)
#         self.wg_catelog.setStyleSheet("QWidget#wg_catelog{border-image:url("+get_file_realpath("data/image/S60922-232113.jpg") + ");background-size:cover;}")
        
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
            item["url"] = self.dl_launch_item_detail.le_url.text().strip()
            item["type"] = self.dl_launch_item_detail.bg_type.checkedButton().type
            item["session_id"] = self.cur_session["id"]
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
        li.click_catelog_signal.connect(self.on_catelog_clicked)
        self.gl_apps.addWidget(li, self.row, self.col, 1, 1)
        self.row += 1
        if self.row >= self.vetical_widget_number:
            self.row = 0
            self.col += 1
    def on_catelog_clicked(self,catelog_id):
#         清空layout上的组件
        count = self.gl_catelog.count()
        for i in reversed(range(count)) :
            self.gl_catelog.itemAt(i).widget().setParent(None)
            
        item_list = app_data.get_launch_item_list_by_catelog(catelog_id)
        if not item_list :
            return
        max_column =  math.floor(len(item_list) ** 0.5)
        row, col = 1, 0
        for i in item_list :
            item_dict = app_data.tuple2dict_launch_item(i)
            li = launch_item(item_dict)
            li.del_item_signal.connect(self.remove_item)
            li.edit_item_signal.connect(self.edit_lauchn_item)
            li.click_catelog_signal.connect(self.on_catelog_clicked)
            self.gl_apps.addWidget(li, self.row, self.col, 1, 1)
            self.gl_catelog.addWidget(li)
        self.wg_catelog.show()
        self.wg_catelog.isActiveWindow()
            
    def init_launch_items(self,item):
        self.row = 0
        self.col = 0
        
#         清空gridlayout上的所有组件
        count = self.gl_apps.count()
        print("gl_apps:" , count)
#         一个老外给的方法，很棒。https://stackoverflow.com/questions/4528347/clear-all-widgets-in-a-layout-in-pyqt
        for i in reversed(range(count)) :
            self.gl_apps.itemAt(i).widget().setParent(None)
            
        session_id = item["id"]
        picture = item["picture"]
        if picture :
            self.setStyleSheet("#MainWindow{background-image:url("+picture + ");background-size:cover;}")
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
            if item_dict["name"] == self.home_session :
                self.init_launch_items(item_dict)
                self.cur_session = item_dict
    def add_session(self,item):
#         新建桌面按钮
        pb_session = QPushButton(item["name"])
        pb_session.setSizePolicy(self.session_bt_size_policy)
        pb_session.setMaximumSize(self.session_btn_size)
#         设置桌面按钮为半透明
        op = QGraphicsOpacityEffect()  
        op.setOpacity(0.9)    
        pb_session.setGraphicsEffect(op)  
        pb_session.setAutoFillBackground(True)
#         TODO 待删除
#         pb_session.session_id = item["id"]
#         pb_session.picture = item["picture"]
        pb_session.item = item
        pb_session.clicked.connect(self.on_pb_session_clicked)
        self.hl_session.addWidget(pb_session)
    def on_pb_session_clicked(self):
        self.cur_session = self.sender().item
        self.init_launch_items(self.cur_session)
    def handle_pop_menu(self):
        action = self.pop_menu.exec_(self.pop_menu_item,QCursor.pos())
        if action:
            action_text = action.text()
            if action_text == "新增启动项" :
                self.edit_lauchn_item(None,None)
            elif action_text == "设置背景":
                filename, _ = QFileDialog.getOpenFileName(self,
                            "选择背景文件",
                            expanduser('~') , 
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
            elif action_text == "设置背景图片" :
                self.edit_session(self.cur_session)
            elif action_text == "设置为主桌面" :
                set_home_session(self.cur_session["name"])
                QMessageBox.information(self, "主桌面设置", "设置为主桌面成功")
            elif action_text == "小程序模式" :
                web_as_application = get_option_boolean("web_as_application")
                set_web_mode(not web_as_application)
                if not web_as_application:
                    QMessageBox.information(self, "启动小程序模式", "每个网页将作为一个应用程序打开")
                else :
                    QMessageBox.information(self, "关闭小程序模式", "每个网页将作为一个标签也打开")
            elif action_text == "退出" :
                sys.exit()
            
            
            
                    
                
                
    def toggle_window_status(self):
        if self.isHidden() :
            self.showMaximized()
            self.activateWindow()
        else :
            self.hide()
    def sys_tray_handler(self,reason):
        if reason ==  2 or reason == 3 :
            self.toggle_window_status()
        elif reason == 1 :
            menu = self.sender().contextMenu()
            menu.exec_(menu.menu_items,QCursor.pos()) 
        else :
            sys.exit()
    def closeEvent(self,event):
        self.hide()
        self.sys_tray.show()
        event.ignore()
    def mouseReleaseEvent(self,event):
        print("on mouseReleaseEvent")
        self.wg_catelog.hide()
        
    def keyReleaseEvent(self,event):
        key = event.key()
        if event.modifiers()== Qt.ControlModifier and key == Qt.Key_V :
            clipboard = QApplication.clipboard()
            mimeData = clipboard.mimeData()
            if mimeData.hasText():
                print("准备粘贴" + clipboard.text())
                path = clipboard.text().replace("file:///","")
#                 print("其他文件" ,mineData.urls()[0].path())
                item = {}
#                 if not isfile(path) and not isdir(path) :
#                     return
                if isfile(path):
                    item["ico"] = get_file_realpath("data/image/file.png")
                else :
                    item["ico"] = get_file_realpath("data/image/folder.svg")
                item["name"] = basename(path)
                item["url"] = path
                item["type"] = 3
                item["session_id"] = self.cur_session["id"]
                app_data.insert_launch_item(item)
                self.add_launch_item(item)
                
            
def main():
    app = QApplication(sys.argv)
    win = kdDesktopAssistant()
#     win.showFullScreen()
    win.showMaximized()
#     win.show()
#     app.exec_()
    sys.exit(app.exec_())