'''
Created on 2019年3月30日

@author: bkd
'''
try:
    from os import startfile
except Exception as e:
    pass
import webbrowser,os,subprocess
from PyQt5.QtWidgets import QWidget,QSizePolicy,QPushButton,QLabel,QVBoxLayout,QMenu,QAction,QMessageBox,QGraphicsDropShadowEffect,QGraphicsOpacityEffect,QFileIconProvider
from PyQt5.QtCore import QSize,Qt,QPoint,pyqtSignal,QUrl,QFileInfo,QMimeData
from PyQt5.QtGui import QIcon,QCursor,QPalette,QPixmap,QFont,QDrag
try:
    from PyQt5.QtWebEngineWidgets import QWebEngineView
except Exception as e:
    print(str(e))
    pass
from .fileutil import get_file_realpath 
from . import app_data
from .kdconfig import get_option_boolean,get_option_int
class launch_item(QWidget):
#     删除组件信号
        del_item_signal = pyqtSignal(QWidget)
        edit_item_signal = pyqtSignal(dict,QWidget)
        click_catelog_signal = pyqtSignal(int)
        repaint_session_signal = pyqtSignal()
        def __init__(self,item):
            print(item)
            super().__init__()
            self.item  = item
#             sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
#             sizePolicy.setHorizontalStretch(0)
#             sizePolicy.setVerticalStretch(0)
#             sizePolicy.setHeightForWidth(self.session_bt_size_policy().hasHeightForWidth())
#             self.setSizePolicy(sizePolicy)
            
#             self.setMinimumSize(QSize(200, 100))
            item_size = get_option_int("item_size")
            self.setFixedSize(QSize(item_size, item_size))
            
            self.pushButton = QPushButton(self)
#             允许拖放
            if item["type"] == 3:
                self.setAcceptDrops(True)
#             self.pushButton.setAcceptDrops(True)
#             self.setDragEnabled(True)
            if not item["ico"]:
                self.set_icon(get_file_realpath('data/image/firefox64.png'))
            else :
                self.check_icon_path(item)
                self.set_icon(item["ico"])
            self.pushButton.setIconSize(QSize(item_size * 0.4,item_size * 0.4))
            self.pushButton.clicked.connect(self.on_clicked)
#             self.pushButton.setAttribute(Qt.WA_TranslucentBackground,True )
#             self.pushButton.setAutoFillBackground(True)
            self.pushButton.setStyleSheet("border: 0px;")
            op = QGraphicsOpacityEffect()
            op.setOpacity(0.5)
#             self.pushButton.setGraphicsEffect(op)
            
            self.label = QLabel(self)
#             self.label.setSizePolicy(sizePolicy)
            self.label.setFont(QFont("sans",10,QFont.Normal))
            self.label.setAttribute(Qt.WA_TranslucentBackground )
            pe = QPalette()
            self.label.setAutoFillBackground(True)
            pe.setColor(QPalette.WindowText,Qt.white)
            self.label.setPalette(pe)
            
            dse = QGraphicsDropShadowEffect(self.label)
            dse.setBlurRadius(10);
            dse.setColor(QPalette().color(QPalette.Shadow));
            dse.setOffset(0,0);
            self.label.setGraphicsEffect(dse);
            
#             self.label.setAlignment(Qt.AlignCenter)
#             sizePolicy=QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding);
#             sizePolicy.setHorizontalStretch(0);
#             sizePolicy.setVerticalStretch(0);
#             sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth());
#             self.label.setSizePolicy(sizePolicy);
#             self.label.setAlignment(Qt.AlignTop)
            self.label.setWordWrap(True)
#             self.label.adjustSize()
#             self.label.setScaledContents(True)
            if len(item["name"]) >9 :
                self.label.setText(item["name"][:9] + "\n" + item["name"][9:])
            else:
                self.label.setText(item["name"]+ " \n ")
            
            self.verticalLayout = QVBoxLayout(self)
            self.verticalLayout.addWidget(self.pushButton,5,Qt.AlignCenter)
            self.verticalLayout.addWidget(self.label,1,Qt.AlignCenter)
            
            self.item_popup_menu = QMenu()
            self.setContextMenuPolicy(Qt.CustomContextMenu)
            self.customContextMenuRequested[QPoint].connect(self.handle_pop_menu)
            self.menu_item =[QAction("修改"),QAction("删除")]
        def on_clicked(self):
            url = self.item["url"].strip()
            item_type = self.item["type"]
            if item_type == 1 :
                if not "http" in url :
                    url = "http://" + url

                if get_option_boolean("web_as_application") :
                    try:
                        self.webapp = QWebEngineView()
                        self.webapp.load(QUrl(url))
                        if self.item["ico"]:
                            try :
                                print("ico path:" + self.item["ico"])
                                self.webapp.setWindowIcon(QIcon(self.item["ico"]))
                            except Exception as e:
                                print("打开图标异常" +str(e))
                        self.webapp.show()
                    except Exception as e:
                        print(str(e))
                        webbrowser.open_new_tab(url)
                else :
                    webbrowser.open_new_tab(url)
            elif item_type in( 2,4) :
                if os.name == "nt":
                    os.startfile(url)
                elif os.name == "posix":
                    subprocess.call(["xdg-open", url])
            elif item_type == 3 :
                self.click_catelog_signal.emit(self.item["id"])
        def handle_pop_menu(self):
            action = self.item_popup_menu.exec_(self.menu_item,QCursor.pos())
            if action:
                text = action.text()
                if text == "删除":
                    print(text)
                    app_data.delete_launch_item(self.item["id"])
                    self.del_item_signal.emit(self)
                    self.repaint_session_signal.emit()
                    QMessageBox.information(self, "删除启动项",   "删除启动项成功", QMessageBox.Yes)
                elif text == "修改" :
                    self.edit_item_signal.emit(self.item,self)
        def update_item(self,item):
            self.item = item
            if not item["ico"]:
                icon = self.pushButton.icon() 
                del icon
                self.set_icon(get_file_realpath('data/image/firefox64.png'))
            else :
                self.set_icon(item["ico"])
            self.label.setText(item["name"])
        def set_icon(self,icon_path):
            icon = QIcon(icon_path)
            self.pushButton.setIcon(icon)
            
        def check_icon_path(self,item):
            if item["type"] in (2,4):
                if not os.path.exists(item["ico"]) :
                    save_path = get_file_realpath(os.path.join("data/image/sysico",os.path.splitext(item["url"])[1][1:]+".ico"))
                    print("save_path:" + save_path)
                    provider = QFileIconProvider()
                    fi = QFileInfo(item["url"])
                    icon = provider.icon(fi)
                    icon.pixmap(48).save(save_path)
                    item["ico"] = save_path
            if item["type"] == 1 :
                if not os.path.exists(item["ico"]):
                    item["ico"] = get_file_realpath("data/image/firefox64.png")
        def mousePresseEvent(self, event):
            print("on mousePresseEvent")
        def mouseMoveEvent(self, e):
            if e.buttons() != Qt.LeftButton:
                return
#             position = e.pos()
#             self.move(position)
    
            mimeData = QMimeData()
            mimeData.setImageData(self)
            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.setHotSpot(e.pos() - self.rect().topLeft())
    
            dropAcion = drag.exec_(Qt.MoveAction)
        def dragEnterEvent(self, event):
            launch_item = event.mimeData().imageData()
            item_data = launch_item.item
            print("dropEvent" ,item_data)
            if item_data["type"] != 3:
                event.acceptProposedAction()
            else : 
                event.ignore()
            print("on dragEnterEvent")

        def dropEvent(self, event):
            launch_item = event.mimeData().imageData()
            item_data = launch_item.item
            item_data["catelog_id"] = self.item["id"]
            app_data.update_launch_item(item_data)
#                 launch_item.setParent(None)
            launch_item.hide()
            
            print("on dropEvent")
            event.setDropAction(Qt.MoveAction)
            event.accept()
