from image_client import *
from local_server import back_process
from image import Image

from ui.main_window import Ui_MainWindow as FMainWindow
from ui.choose_class import Ui_ChooseClass as ChooseClass

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QDialog

import sys
import os
import zlib
import pickle as pkl
from glob import glob


Title = "CoLabel Version 0.1.0"
IconName = glob("./utils/icon.*")[0] if len(glob("./utils/icon.*")) else "./utils/icon.jpg"
MinSize = (1600, 900)
AutoUpdateTimeInterval = 0.2    # sec
AutoRequestTimeInterval = 5     # sec
DataFile = "./utils/data.dat"

TIPS = """快捷键
Ctrl+W   创建/取消创建 目标框
Ctrl+Q   上一张图片
Ctrl+E   下一张图片
Ctrl+S   保存到标签文件
Delete   删除当前选中目标框"""


class Choose(QDialog, ChooseClass):
    ret = -1

    def __init__(self, classes, last_index=0, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.classes_list.clear()
        self.ret = -1
        for this_class in classes:
            self.classes_list.addItem(this_class)
        if len(classes) >= last_index:
            self.classes_list.setCurrentRow(last_index)


class MainWindow(QtWidgets.QMainWindow, FMainWindow):

    isLogin = False
    ListUpdate = False
    _dir_list = []
    _image_list = []
    _user = ""
    _pwd = ""

    isPressed = False
    isAddMode = False
    press_start_point = [0, 0]
    dxdy = [0, 0]
    newbox = [0, 0, 0, 0]
    last_class_index = 0
    userdata = {}
    welcome = False

    current_image = Image()
    local_server = None

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        FMainWindow.__init__(self)
        self.setupUi(self)

        self.init_display()
        self.init_params()
        self.init_connection()
        self.init_timer()

        self._check_local_service()

    def _generate_base_dict(self, **kwargs):
        data = {
            "user": self.user.text(),
            "pwd": self.password.text(),
            "ip": self.ip.text(),
            "port": self.port.value()
        }
        for name in kwargs:
            data[name] = kwargs[name]
        return data

    def _get_classes_list(self):
        labels = []
        [labels.append(label_name) if len(label_name) else None
         for label_name in self.labels_name.toPlainText().split("\n")]
        return labels

    def _auto_save_data(self):
        data = {
            "user": self.user.text(),
            "pwd": self.password.text(),
            "ip": self.ip.text(),
            "port": self.port.value(),
            "labels": self.labels_name.toPlainText(),
            "local_user": self.local_user.text(),
            "local_pwd": self.local_pwd.text(),
            "local_host": self.local_host.text(),
            "local_port": self.local_port.value(),
            "service_open": self.localService.isChecked(),
            "root_path": self.rootPath.text()
        }
        if not self.userdata == data:
            self.userdata = data
            open(DataFile, "wb").write(zlib.compress(pkl.dumps(data), 5))

    def _check_anno_save(self):
        if not self.current_image.isSaved:
            reply = QtWidgets.QMessageBox.question(
                self,
                "Warning",
                "Current change not saved. Do you need to save those changes?",
                QtWidgets.QMessageBox.Yes,
                QtWidgets.QMessageBox.No
            )
            if reply == QtWidgets.QMessageBox.Yes:
                self.current_image.save(**self._generate_base_dict(
                    image_type=self.current_image.img_type,
                    image_name=self.current_image.img_name,
                    image_size=self.current_image.img.shape,
                    items=self.current_image.get_items()
                ))

    def _load_data(self):
        if os.path.isfile(DataFile):
            data = pkl.loads(zlib.decompress(open(DataFile, "rb").read()))
            if not self.userdata == data:
                self.userdata = data
            self.user.setText(data["user"])
            self.password.setText(data["pwd"])
            self.ip.setText(data["ip"])
            self.port.setValue(data["port"])
            self.labels_name.setPlainText(data["labels"])

            self.local_user.setText(data["local_user"])
            self.local_pwd.setText(data["local_pwd"])
            self.local_host.setText(data["local_host"])
            self.local_port.setValue(data["local_port"])
            self.localService.setChecked(data["service_open"])
            self.rootPath.setText(data["root_path"]) if "root_path" in data else None
        else:
            self.welcome = True

    def _check_local_service(self):
        if self.localService.isChecked():
            if not os.path.isdir(self.rootPath.text()):
                self.localService.setChecked(False)
                return
            if self.local_server is None:
                self.local_server = back_process(
                    user=self.local_user.text(),
                    password=self.local_pwd.text(),
                    host=self.local_host.text(),
                    port=self.local_port.value(),
                    root_path=self.rootPath.text()
                )
            if not self.local_server.is_alive():
                print("start local service")
                self.local_server.start()

                self.local_user.setEnabled(False)
                self.local_pwd.setEnabled(False)
                self.local_host.setEnabled(False)
                self.local_port.setEnabled(False)
                self.rootPath.setEnabled(False)

        else:
            if self.local_server is not None:
                if self.local_server.is_alive():
                    self.local_server.terminate()
                    self.local_server = None

                    self.local_user.setEnabled(True)
                    self.local_pwd.setEnabled(True)
                    self.local_host.setEnabled(True)
                    self.local_port.setEnabled(True)
                    self.rootPath.setEnabled(True)
                    print("stop local service")

    def init_display(self):
        self.setWindowTitle(Title)
        if os.path.isfile(IconName):
            self.setWindowIcon(QIcon(IconName))
        self.setMinimumSize(*MinSize)
        self.Tips.setText(TIPS)

    def init_params(self):
        self.isLogin = False
        self.ListUpdate = False
        self._dir_list = []
        self._image_list = []
        self._user = ""
        self._pwd = ""
        self._load_data()
        self._auto_save_data()

    def init_connection(self):

        def login_out_ClickFun():
            self.isLogin = not self.isLogin

        def getImageList():
            image_type = self.dir_list.currentItem().text()
            now_image_list = get_image_list(image_type=image_type, **self._generate_base_dict())
            if not now_image_list == self._image_list:
                self._image_list = now_image_list
                self.image_list.clear()
                for image_name in self._image_list:
                    self.image_list.addItem(image_name)

        def showImage():
            # print(self.image_list.currentIndex().column())
            if self.image_list.currentRow() < 0:
                return
            if self.main_tab.currentIndex():
                self.main_tab.setCurrentIndex(0)
            if not self.tag_tab.currentIndex():
                self.tag_tab.setCurrentIndex(1)
            self._check_anno_save()

            if self.image_list.currentIndex().column() < 0:
                return
            image_type = self.dir_list.currentItem().text()
            image_name = self.image_list.currentItem().text()

            self.current_image = Image(
                msg=self._generate_base_dict(
                    image_type=image_type,
                    image_name=image_name,
                    all_labels=self._get_classes_list()
                )
            )

            self.current_image.to(self.image)
            self.current_image.anno2list(self.anno_list)
            self.current_image.draw_bbox(self.image)

            self.image_name.setText(f"{self.current_image.img_type}: {self.current_image.img_name}")

        def repaintAnno():
            self.current_image.draw_bbox(self.image, self.anno_list.currentIndex().row())
            # self.anno_list.setCurrentIndex()

        self.login_out.clicked.connect(login_out_ClickFun)
        self.dir_list.doubleClicked.connect(getImageList)
        self.image_list.currentItemChanged.connect(showImage)
        self.anno_list.clicked.connect(repaintAnno)

        self.localService.clicked.connect(self._check_local_service)

        def mousePress(a0: QtGui.QMouseEvent):
            self.isPressed = True
            this_x, this_y = a0.x(), a0.y()
            self.press_start_point = [this_x, this_y]
            if self.isAddMode:
                # print("press")
                self.newbox = [this_x, this_y] * 2
                # pass
                # print("ok")
            else:
                index = self.current_image.changeMode(this_x, this_y, self.anno_list.currentIndex().row())
                if index >= 0:
                    self.anno_list.setCurrentRow(index)
                    self.current_image.draw_bbox(self.image, index)
                # print(a0.source(), mode)

        def mouseMove(a0: QtGui.QMouseEvent):
            # print("move")
            nx, ny = a0.x(), a0.y()

            if self.isPressed:
                if self.isAddMode:
                    # index = -1
                    self.newbox[2], self.newbox[3] = nx, ny
                    x1, y1, x2, y2 = self.newbox
                    self.current_image.current_box(x1, y1, x2, y2, self.image)
                else:
                    index = self.anno_list.currentIndex().row()
                    # print(nx, ny)
                    self.current_image.runMode(
                        nx,
                        ny,
                        index,
                        self.image
                    )
            else:
                if self.isAddMode:
                    # TODO: draw vertical and horizontal line
                    # print(nx, ny)
                    self.current_image.vh_line(nx, ny, self.image)
                    # pass

        def mouseRelease(a0: QtGui.QMouseEvent):
            self.isPressed = False
            self.current_image.clearMode()
            self.press_start_point = [0, 0]

            if self.isAddMode:
                self.isAddMode = False
                x1, y1, x2, y2 = self.newbox
                if x1 > x2:
                    x1, x2 = x2, x1
                if y1 > y2:
                    y1, y2 = y2, y1
                if (x2 - x1) < 3 or (y2 - y1) < 3:
                    self.newbox = [0, 0, 0, 0]
                    repaintAnno()
                else:
                    dlog = Choose(self._get_classes_list(), self.last_class_index, self)

                    def yes():
                        label_idx = dlog.classes_list.currentIndex().row()
                        if label_idx >= 0:
                            self.last_class_index = label_idx
                            anno_index = self.current_image.add_bbox(
                                self.newbox,
                                self._get_classes_list()[self.last_class_index]
                            )
                            self.current_image.anno2list(self.anno_list)
                            self.anno_list.setCurrentRow(anno_index)
                            repaintAnno()
                        else:
                            repaintAnno()
                        dlog.close()

                    def no():
                        repaintAnno()
                        dlog.close()

                    def keyPress(a0: QtGui.QKeyEvent):
                        if a0.key() == 16777220:
                            yes()
                        elif a0.key() == 16777216:
                            no()

                    dlog.buttonBox.accepted.connect(yes)
                    dlog.classes_list.doubleClicked.connect(yes)
                    dlog.buttonBox.rejected.connect(no)
                    dlog.keyPressEvent = keyPress
                    dlog.show()

            else:
                repaintAnno()

            # print(self.current_image.mode)


        # self.image.mouseDoubleClickEvent = mouseDoubleClick
        self.image.mousePressEvent = mousePress
        self.image.mouseMoveEvent = mouseMove
        self.image.mouseReleaseEvent = mouseRelease
        self.image.setMouseTracking(True)


        def changeLabel():
            anno_idx = self.anno_list.currentIndex().row()
            if anno_idx >= 0:
                try:
                    cls_idx = self._get_classes_list().index(self.current_image.items[anno_idx]["name"])
                except:
                    cls_idx = 0
                dlog = Choose(
                    self._get_classes_list(),
                    cls_idx,
                    self
                )

                def yes():
                    label_idx = dlog.classes_list.currentIndex().row()
                    if label_idx >= 0:
                        self.last_class_index = label_idx
                        self.current_image.change_label(anno_idx, self._get_classes_list()[label_idx])
                        self.current_image.anno2list(self.anno_list)
                        self.anno_list.setCurrentRow(anno_idx)
                        repaintAnno()
                    else:
                        repaintAnno()
                    dlog.close()

                def no():
                    repaintAnno()
                    dlog.close()

                def keyPress(a0: QtGui.QKeyEvent):
                    if a0.key() == 16777220:
                        yes()
                    elif a0.key() == 16777216:
                        no()

                dlog.buttonBox.accepted.connect(yes)
                dlog.classes_list.doubleClicked.connect(yes)
                dlog.buttonBox.rejected.connect(no)
                dlog.keyPressEvent = keyPress
                dlog.show()

        self.anno_list.doubleClicked.connect(changeLabel)

        # def keyPress(a0: QtGui.QKeyEvent):
        #     print(a0.text(), a0.key())
        #
        # self.image.keyPressEvent = keyPress

    def init_timer(self):
        self.count = 0

        def timeoutFun0():
            serverEnableFlag = os.path.isdir(self.rootPath.text())
            self.wrongrootpath.setVisible(not serverEnableFlag)
            self.localService.setEnabled(serverEnableFlag)

            if not self.count and self.welcome:
                QtWidgets.QMessageBox.information(
                    self,
                    "欢迎",
                    "欢迎使用远程标注工具！如遇到问题请联系作者\nGitHub主页: https://github.com/LSH9832",
                    QtWidgets.QMessageBox.Ok
                )

            self.count += 1
            if self.count % 1 == 0:
                self._auto_save_data()
            if self.isLogin:
                if self.current_image.img is not None:
                    msg = self.image_name.text()
                    if self.current_image.isSaved:
                        if msg.endswith("*"):
                            self.image_name.setText(msg[:-1])
                    else:
                        if not msg.endswith("*"):
                            self.image_name.setText(msg + "*")

                if not (self.user.text() == self._user and self.password.text() == self._pwd):
                    self._user, self._pwd = self.user.text(), self.password.text()
                    self.isLogin, error = test_connect(**self._generate_base_dict())
                    if self.isLogin:
                        self.user.setEnabled(False)
                        self.password.setEnabled(False)
                        self.ip.setEnabled(False)
                        self.port.setEnabled(False)
                        self.login_out.setText("注销")
                        self.connection_status.setStyleSheet("QLabel{background-color: rgb(25, 240, 76);}")
                        self.connection_status.setText("connect")
                        self.ListUpdate = True
                        timeoutFun1()
                    else:
                        QtWidgets.QMessageBox.warning(
                            self,
                            "错误",
                            error,
                            QtWidgets.QMessageBox.Ok
                        )

            else:
                self._user = ""
                self._pwd = ""

                self.ListUpdate = False
                if not self.login_out.text() == "登录":
                    self.login_out.setText("登录")
                    self.connection_status.setStyleSheet("QLabel{background-color: rgb(255, 80, 47);}")
                    self.connection_status.setText("disconnect")

                if len(self._dir_list):
                    self._dir_list = []
                    self._image_list = []

                if self.dir_list.count():
                    self.dir_list.clear()
                if self.image_list.count():
                    self.image_list.clear()
                if self.anno_list.count():
                    self.anno_list.clear()

                if not self.user.isEnabled():
                    self.user.setEnabled(True)
                if not self.password.isEnabled():
                    self.password.setEnabled(True)
                if not self.ip.isEnabled():
                    self.ip.setEnabled(True)
                if not self.port.isEnabled():
                    self.port.setEnabled(True)

        self.timer0 = QTimer()
        self.timer0.timeout.connect(timeoutFun0)
        self.timer0.start(int(AutoUpdateTimeInterval * 1000))

        def timeoutFun1():

            if self.ListUpdate:
                new_dir_list = get_type_list(**self._generate_base_dict())
                if not new_dir_list == self._dir_list:
                    self._dir_list = new_dir_list
                    self.dir_list.clear()
                    self.image_list.clear()
                    for this_dir in self._dir_list:
                        self.dir_list.addItem(this_dir)

        self.timer1 = QTimer()
        self.timer1.timeout.connect(timeoutFun1)
        self.timer1.start(int(AutoRequestTimeInterval * 1000))

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        # print(a0.text(), a0.key())
        if self.current_image.img is not None:
            if a0.matches(QKeySequence.Save):
                self.current_image.save(**self._generate_base_dict(
                    image_type=self.current_image.img_type,
                    image_name=self.current_image.img_name,
                    image_size=self.current_image.img.shape,
                    items=self.current_image.get_items()
                ))
                # pass
            elif a0.matches(QKeySequence.Delete):
                anno_idx = self.anno_list.currentIndex().row()
                if anno_idx >= 0:
                    self.current_image.remove_item(anno_idx)
                    self.current_image.anno2list(self.anno_list)
                    self.current_image.draw_bbox(self.image, self.anno_list.currentIndex().row())

            elif not a0.text() == "w" and a0.key() == 87:
                self.isAddMode = not self.isAddMode
                # print(self.isAddMode)
            elif not a0.text() == "q" and a0.key() == 81:
                img_idx = self.image_list.currentRow()
                if img_idx > 0:
                    self.image_list.setCurrentRow(img_idx - 1)
            elif not a0.text() == "e" and a0.key() == 69:
                img_idx = self.image_list.currentRow()
                if img_idx < len(self._image_list) - 1:
                    self.image_list.setCurrentRow(img_idx + 1)

    def resizeEvent(self, a0: QtGui.QResizeEvent):
        self.current_image.to(self.image)
        self.current_image.draw_bbox(self.image, self.anno_list.currentIndex().row())

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self._check_anno_save()
        if self.local_server is not None:
            if self.local_server.is_alive():
                self.local_server.terminate()
                print("stop local service before closing")
        a0.accept()


if __name__ == '__main__':

    def main():
        app = QtWidgets.QApplication(sys.argv)
        w = MainWindow()
        w.show()
        sys.exit(app.exec_())

    main()
