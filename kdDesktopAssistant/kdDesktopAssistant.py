'''
Created on 2019年3月30日

@author: bkd
'''
import  sys,math,os
from os.path import expanduser,isfile,isdir, basename, splitext,exists,join
from PyQt5.uic import loadUi
from PyQt5.QtGui import  QIcon,QCursor,QPalette, QBrush, QPixmap
from PyQt5.QtCore import Qt,QPoint,QSize,pyqtSlot,QFileInfo
from PyQt5.QtWidgets import QMainWindow, QApplication,QGraphicsOpacityEffect,QMessageBox,QFileDialog,QAction,QMenu,QSizePolicy,QPushButton,QSystemTrayIcon,QDesktopWidget,QGridLayout,QWidget,QFrame,QFileIconProvider
from .fileutil import  get_file_realpath
from .launch_item import launch_item
from .dl_launch_item_detail import dl_launch_item_detail
from .session import session
from . import app_data
from  .kdconfig import set_home_session,set_web_mode,get_option_value,get_option_int,config_dir
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
#         TODO 待实现的右键功能：QAction("导出配置"),QAction("导入配置")
        self.pop_menu_item = [QAction("新增启动项"),QAction("新增桌面"),QAction("设置背景图片"),QAction("修改桌面"),QAction("删除桌面"),QAction("设置为主桌面"),QAction("小程序模式"),QAction("退出")]
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
        self.vetical_widget_number = math.floor((QDesktopWidget().screenGeometry().height() - 150) / get_option_int("item_size"))
        self.home_session = get_option_value("home_session")
        self.init_session()
        
#         初始化对话框对象
        self.dl_launch_item_detail = dl_launch_item_detail()
        self.session = session()
        self.wg_catelog = QFrame()
        self.wg_catelog.setWindowFlags(Qt.Popup)
        self.gl_catelog = QGridLayout()
        self.wg_catelog.setLayout(self.gl_catelog)
#         self.gl_catelog.setWindowOpacity(0.5)
#         self.wg_catelog.setAttribute(Qt.WA_TranslucentBackground,True )
        self.wg_catelog.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.wg_catelog.setAutoFillBackground(True)
        
#         self.wg_catelog.setStyleSheet("background-image:url("+get_file_realpath("data/image/bg_catelog.gif") + ");background-size:cover;}")
        p = QPalette()
        p.setBrush(QPalette.Background, QBrush(QPixmap(get_file_realpath("data/image/bg_catelog.jpg"))))
        self.wg_catelog.setPalette(p)
#         op = QGraphicsOpacityEffect()  
#         op.setOpacity(0.9)    
#         self.wg_catelog.setGraphicsEffect(op)  
#         self.wg_catelog.setStyleSheet("QWidget#wg_catelog{background-color:#99cc99;}")
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
        li.repaint_session_signal.connect(self.repaint_session)
        self.gl_apps.addWidget(li, self.row, self.col, 1, 1)
        self.row += 1
        if self.row >= self.vetical_widget_number:
            self.row = 0
            self.col += 1
    def repaint_session(self):
        self.init_launch_items(self.cur_session)
    def on_catelog_clicked(self,catelog_id):
#         清空layout上的组件
        if not self.wg_catelog.isHidden():
            self.wg_catelog.hide()
            return
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
            
#         p = QCursor.pos()
#         if p.y() > self.gl_apps.geometry().height() /2 :
#             self.wg_catelog.move(p.x() + 10,p.y() - self.wg_catelog.geometry().height())
#         else :
#             self.wg_catelog.move(p.x() + 10,p.y()+10)
            
        self.wg_catelog.show()
#         self.wg_catelog.active()
            
    def init_launch_items(self,item):
#         高亮当前桌面的按钮
        count = self.hl_session.count()
        for i in reversed(range(count)) :
            self.hl_session.itemAt(i).widget().setStyleSheet("QPushButton{background-color:#FFFFFF}")
        self.cur_pb_session.setStyleSheet("QPushButton{background-color:#FF9900}")
        
        self.row = 0
        self.col = 0
        
#         清空gridlayout上的所有组件
        count = self.gl_apps.count()
        print("gl_apps:" , count)
#         一个老外给的方法，很棒。https://stackoverflow.com/questions/4528347/clear-all-widgets-in-a-layout-in-pyqt
        for i in reversed(range(count)) :
            self.gl_apps.itemAt(i).widget().setParent(None)
        
#         设置背景图片    
        session_id = item["id"]
        picture = item["picture"]
        if picture :
            self.setStyleSheet("#MainWindow{background-image:url("+picture + ");background-size:cover;}")

        if not session_id :
            return
#         初始化启动项
        self.item_list = app_data.get_launch_item_list(session_id)
        for item in self.item_list:
            item_dict = app_data.tuple2dict_launch_item(item)
            self.add_launch_item(item_dict)
        
    def init_session(self):
#         清空旧的桌面按钮
        count = self.hl_session.count()
        for i in reversed(range(count)) :
            self.hl_session.itemAt(i).widget().setParent(None)
        self.session_list = app_data.get_session_list()
        initedSession = False
        first_pb_session = None
        for item in self.session_list:
            item_dict = app_data.tuple2dict_session(item)
            pb_session = self.add_session(item_dict)
            if not first_pb_session:
                first_pb_session = pb_session
            if item_dict["name"] == self.home_session :
                initedSession = True
                self.cur_pb_session = pb_session
                self.init_launch_items(item_dict)
                self.cur_session = item_dict
            
#       默认桌面未初始化，默认初始化第一个桌面
        if not initedSession and len(self.session_list) > 0:
            item = self.session_list[0]
            item_dict = app_data.tuple2dict_session(item)
            self.cur_pb_session = first_pb_session
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
        return pb_session
    def on_pb_session_clicked(self):
        sender = self.sender()
        self.cur_session = sender.item

        
        self.cur_pb_session = sender
        self.init_launch_items(self.cur_session)
    def handle_pop_menu(self):
        action = self.pop_menu.exec_(self.pop_menu_item,QCursor.pos())
        if action:
            action_text = action.text()
            if action_text == "新增启动项" :
                self.edit_lauchn_item(None,None)
            elif action_text == "新增桌面" :
                if self.session.exec_() :
                    session_item = {}
                    session_item["name"] = self.session.le_name.text()
                    session_item["picture"] = self.session.le_picture.text()
                    session_item["type"] = 0
                    session_item["color"] = None
                    session_item["id"] = app_data.insert_session_item(session_item)
                    print(session_item)
                    pb_session = self.add_session(session_item)
                    self.init_launch_items(session_item)
                    self.cur_session = session_item
                    QMessageBox.information(self, "新增桌面", "新增桌面成功")
            elif action_text in ( "设置背景图片","修改桌面") :
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
                    QMessageBox.information(self, "关闭小程序模式", "每个网页将作为一个标签也打开")
            elif action_text == "退出" :
                sys.exit()
            elif action_text == "删除桌面" :
                reply = QMessageBox.warning(self, "确认删除桌面？", "该桌面的所有启动项都会被删除，并不可还原，确认删除?",QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes :
                    app_data.delete_session(self.cur_session["id"])
                    self.init_session()
                    QMessageBox.information(self, "删除桌面", "删除桌面成功",QMessageBox.Ok)
            
            
                    
                
                
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
                print("准备粘贴:" + clipboard.text())
                path = clipboard.text()
                item = {}
                if  not path.startswith("file") :
                    item = self.dl_launch_item_detail.get_url_info(path)
                    item["session_id"] = self.cur_session["id"]
                    item["id"] = app_data.insert_launch_item(item)
                    self.add_launch_item(item)
                    return
                
                path = path.replace("file:///","")
                if os.name == "posix" :
                    path = "/" + path
                provider = QFileIconProvider()
                fi = QFileInfo(path)
                icon = provider.icon(fi)
#                     t = icon.pixmap().toImage().text()
                save_path = join(config_dir ,"data/image/sysico",splitext(path)[1][1:]+".ico")
                print("save_path:" + save_path)
                icon.pixmap(48).save(save_path)
                t = icon.name()
                t1 = icon.themeName()
                t2 = icon.themeSearchPaths()
                print("icon path:" + t+"," + t1,t2)
                if not icon.isNull() :
                    item["ico"] = save_path
                item["name"] = basename(path)
                item["url"] = path
                item["type"] = 2
                if not self.cur_session["id"]:
                    QMessageBox.information(self, "新桌面", "新桌面需重启后才能添加启动项")
                    return
                item["session_id"] = self.cur_session["id"]
                print("add other launch item:" ,item)
                item["id"] = app_data.insert_launch_item(item)
                print(item)
                self.add_launch_item(item)
                
            
def main():
    app = QApplication(sys.argv)
    win = kdDesktopAssistant()
#     win.showFullScreen()
    win.showMaximized()
#     win.show()
#     app.exec_()
    sys.exit(app.exec_())