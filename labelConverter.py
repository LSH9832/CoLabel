from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.uic import loadUi


from glob import glob
from multiprocessing import Process, freeze_support, Queue
import os
import datetime
import time

from utils.voc2coco import voc2coco, COCO
from utils.coco2voc import coco2voc
from ui.labelConverter import Ui_MainWindow as labelConverter

freeze_support()


class LabelConverter(QtWidgets.QMainWindow, labelConverter):

    voc2coco = False
    coco2voc = False

    voc2cocoProgress: Process = None
    voc2cocoProgressQueue = Queue(maxsize=1)

    coco2vocProgress: Process = None
    coco2vocProgressQueue = Queue(maxsize=1)

    msgs = []

    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        # loadUi("ui/datasetConverter.ui", self)
        self.msg.setVisible(False)
        self.p = parent
        if self.p is not None:
            self.setWindowIcon(self.p.windowIcon())

        def init_connect():

            # VOC2COCO
            def browseVOCPath():
                path = self.VOCdatasetPath.text() if os.path.isdir(self.VOCdatasetPath.text()) else "./"
                ret = QFileDialog.getExistingDirectory(self, "Choose VOC Dataset Path", path)
                if len(ret):
                    self.VOCdatasetPath.setText(ret.replace("\\", "/"))

            self.browseVOCPath.clicked.connect(browseVOCPath)

            def browseCOCOPath():
                path = self.COCODistPath.text() if os.path.isdir(self.COCODistPath.text()) else "./"
                ret = QFileDialog.getExistingDirectory(self, "Choose COCO Dataset Save Path", path)
                if len(ret):
                    self.COCODistPath.setText(ret.replace("\\", "/"))

            self.browseCOCODistPath.clicked.connect(browseCOCOPath)

            def browseCOCOPath2():
                path = self.COCOdatasetPath.text() if os.path.isdir(self.COCOdatasetPath.text()) else "./"
                ret = QFileDialog.getExistingDirectory(self, "Choose COCO Dataset Path", path)
                if len(ret):
                    self.COCOdatasetPath.setText(ret.replace("\\", "/"))

            self.browseCOCOPath.clicked.connect(browseCOCOPath2)

            def browseVOCPath2():
                path = self.VOCDistPath.text() if os.path.isdir(self.VOCDistPath.text()) else "./"
                ret = QFileDialog.getExistingDirectory(self, "Choose VOC Dataset Save Path", path)
                if len(ret):
                    self.VOCDistPath.setText(ret.replace("\\", "/"))

            self.browseVOCDistPath.clicked.connect(browseVOCPath2)

            def updateVOCSubPath():
                path = self.VOCdatasetPath.text()
                if os.path.isdir(path):
                    self.VOCImagePath.clear()
                    self.VOCAnnotationPath.clear()
                    dirs = []
                    [dirs.append(this_dir.replace("\\", "/").split("/")[-1]) if os.path.isdir(this_dir) else None
                     for this_dir in glob(os.path.join(path, "*"))]
                    # self.VOCImagePath = QtWidgets.QComboBox()
                    self.VOCImagePath.addItems(dirs)
                    self.VOCAnnotationPath.addItems(dirs)

            self.VOCdatasetPath.textChanged.connect(updateVOCSubPath)

            def updateCOCOSubPath():
                path = self.COCOdatasetPath.text()
                if os.path.isdir(path):
                    try:
                        self.COCOImagePath.clear()
                        self.COCOAnnotationFile.clear()
                        dirs = []
                        for this_dir in glob(os.path.join(path, "*")):
                            name = this_dir.replace("\\", "/").split("/")[-1]
                            if not name == "annotations":
                                dirs.append(name)
                        json_list = glob(os.path.join(path, "annotations", "*.json"))
                        self.COCOImagePath.addItems(dirs)
                        self.COCOAnnotationFile.addItems([s.replace("\\", "/").split("/")[-1] for s in json_list])
                    except Exception as e:
                        print(e)

            self.COCOdatasetPath.textChanged.connect(updateCOCOSubPath)

            def voc2coco_start_stop():
                if not self.voc2coco:
                    # TODO 检查目标文件夹是否为空文件夹，如果不是是否覆盖还是合并续写
                    target_dir = os.path.join(self.COCODistPath.text(), self.COCODatasetName.text())

                    self.voc2cocoProgressQueue.get() if not self.voc2cocoProgressQueue.empty() else None
                    kwargs = {
                        "image_dirs": os.path.join(self.VOCdatasetPath.text(),
                                                   self.VOCImagePath.currentText()),
                        "annotation_dirs": os.path.join(self.VOCdatasetPath.text(),
                                                        self.VOCAnnotationPath.currentText()),
                        "class_file": None,
                        "data_name": self.COCODatasetName.text(),
                        "image_target_dir": os.path.join(target_dir, self.COCODistImagePath.text()),
                        "image_type": "jpg",
                        "version": self.COCOVersion.text(),
                        "url": "",
                        "author": self.COCOAuthor.text(),
                        "save": False,
                        "coco_dataset": None,
                        "q": self.voc2cocoProgressQueue
                    }

                    if os.path.isdir(os.path.join(target_dir, "annotations")):
                        json_file = os.path.join(target_dir,
                                                 "annotations",
                                                 f"{self.COCODatasetName.text()}.json")
                        if os.path.isfile(json_file):
                            if QtWidgets.QMessageBox.warning(
                                self,
                                "警告",
                                f"标签文件夹下{self.COCODatasetName.text()}已存在，确定继续转换？",
                                QtWidgets.QMessageBox.Yes,
                                QtWidgets.QMessageBox.No
                            ) == QtWidgets.QMessageBox.Yes:
                                # TODO 覆盖 or 续写
                                response = QtWidgets.QMessageBox.information(
                                    self,
                                    "请选择",
                                    "覆盖（Y）或续写（N）？（关闭此对话框为N）",
                                    QtWidgets.QMessageBox.Yes,
                                    QtWidgets.QMessageBox.No,
                                )
                                if response == QtWidgets.QMessageBox.No:
                                    kwargs["coco_dataset"] = COCO(json_file)
                                elif not response == QtWidgets.QMessageBox.Yes:
                                    return
                            else:
                                return

                    os.makedirs(target_dir, exist_ok=True)
                    os.makedirs(kwargs["image_target_dir"], exist_ok=True)
                    os.makedirs(os.path.join(target_dir, "annotations"), exist_ok=True)

                    print("start voc2coco")
                    self.voc2cocoProgress = Process(target=voc2coco, kwargs=kwargs)
                    self.voc2cocoProgress.start()
                    self.voc2coco = True
                    self.setVOC2COCOEnabled(False)
                    self.VOC2COCOButton.setText("停止转换")
                    self.addMsg("转换开始")

                else:
                    if self.voc2cocoProgress is not None:
                        self.voc2cocoProgress.terminate()
                    self.voc2coco = False
                    self.setVOC2COCOEnabled(True)
                    self.progressBar.setValue(0)
                    self.VOC2COCOButton.setText("开始转换")
                    self.addMsg("转换中止，需手动删除已转换的文件")

            self.VOC2COCOButton.clicked.connect(voc2coco_start_stop)

            def coco2voc_start_stop():
                if not self.coco2voc:
                    dataset_dir = os.path.join(self.VOCDistPath.text(), self.VOCDatasetName.text())

                    self.coco2vocProgressQueue.get() if not self.coco2vocProgressQueue.empty() else None

                    kwargs = {
                        "image_path": os.path.join(self.COCOdatasetPath.text(), self.COCOImagePath.currentText()),
                        "json_file": os.path.join(self.COCOdatasetPath.text(),
                                                  "annotations", self.COCOAnnotationFile.currentText()),
                        "target_dir": self.VOCDistPath.text(),
                        "dataset_name": self.VOCDatasetName.text(),
                        "q": self.coco2vocProgressQueue
                    }

                    if len(glob(os.path.join(dataset_dir, "annotations", "*.xml"))):
                        if QtWidgets.QMessageBox.warning(
                            self,
                            "警告",
                            f"目标文件夹下已存在标签文件，转换将覆盖同名文件，确定继续转换？",
                            QtWidgets.QMessageBox.Yes,
                            QtWidgets.QMessageBox.No
                        ) == QtWidgets.QMessageBox.No:
                            return

                    self.coco2vocProgress = Process(target=coco2voc, kwargs=kwargs)
                    self.coco2vocProgress.start()
                    self.coco2voc = True
                    # TODO setEnabled(False)  setText("停止转换")
                    self.setCOCO2VOCEnabled(False)
                    self.COCO2VOCButton.setText("停止转换")
                    self.addMsg("转换开始")
                else:
                    if self.coco2vocProgress is not None:
                        self.coco2vocProgress.terminate()
                    self.coco2voc = False
                    self.setCOCO2VOCEnabled(True)
                    self.progressBar2.setValue(0)
                    self.COCO2VOCButton.setText("开始转换")
                    self.addMsg("转换中止，需手动删除已转换的文件")

            self.COCO2VOCButton.clicked.connect(coco2voc_start_stop)

        init_connect()
        self.addMsg("开始运行")

        def init_timer():

            def timeoutFun0():
                is_voc2coco_complete = self.check_complete(voc2coco=True)
                self.VOC2COCOButton.setEnabled(is_voc2coco_complete)
                is_coco2voc_complete = self.check_complete(voc2coco=False)
                self.COCO2VOCButton.setEnabled(is_coco2voc_complete)

            self.timer0 = QTimer()
            self.timer0.timeout.connect(timeoutFun0)
            self.timer0.start(200)

            def timeoutFun1():
                if self.voc2coco:
                    if not self.voc2cocoProgressQueue.empty():
                        try:
                            per = self.voc2cocoProgressQueue.get()
                            # self.progressBar = QtWidgets.QProgressBar()
                            if self.progressBar.value() < per:
                                self.progressBar.setValue(per)
                            if int(per) == self.progressBar.maximum():

                                # print(self.progressBar.maximum())

                                json_file = os.path.join(self.COCODistPath.text(),
                                                         self.COCODatasetName.text(),
                                                         "annotations",
                                                         f"{self.COCODatasetName.text()}.json")
                                self.voc2cocoProgressQueue.put(json_file)
                                self.voc2coco = False

                                time.sleep(0.08)
                                self.addMsg(self.voc2cocoProgressQueue.get())

                                self.update()

                                QtWidgets.QMessageBox.information(
                                    self,
                                    "完成",
                                    "转换完成",
                                    QtWidgets.QMessageBox.Ok
                                )
                                self.progressBar.setValue(0)
                                self.setVOC2COCOEnabled(True)
                                self.VOC2COCOButton.setText("开始转换")

                        except Exception as e:
                            print(e)
                if self.coco2voc:
                    if not self.coco2vocProgressQueue.empty():
                        per = self.coco2vocProgressQueue.get()
                        if self.progressBar2.value() < per:
                            self.progressBar2.setValue(per)
                        if int(per) == self.progressBar2.maximum():
                            self.coco2voc = False
                            self.addMsg(self.coco2vocProgressQueue.get())
                            self.update()
                            QtWidgets.QMessageBox.information(
                                self,
                                "完成",
                                "转换完成",
                                QtWidgets.QMessageBox.Ok
                            )
                            self.progressBar2.setValue(0)
                            self.setCOCO2VOCEnabled(True)
                            self.VOC2COCOButton.setText("开始转换")

            self.timer1 = QTimer()
            self.timer1.timeout.connect(timeoutFun1)
            self.timer1.start(30)

        init_timer()

    def addMsg(self, msg: str):
        self.msgs.append(f"[{str(datetime.datetime.now()).split('.')[0]}] {msg}")
        show_str = ""
        for m in self.msgs:
            show_str += f"{m}\n"
        self.msg.setText(show_str)
        # self.msg = QtWidgets.QTextBrowser()
        self.msg.moveCursor(QtGui.QTextCursor.End)

    def setVOC2COCOEnabled(self, flag: bool):
        self.VOCdatasetPath.setEnabled(flag)
        self.browseVOCPath.setEnabled(flag)
        self.VOCImagePath.setEnabled(flag)
        self.VOCAnnotationPath.setEnabled(flag)
        self.COCODistPath.setEnabled(flag)
        self.browseCOCODistPath.setEnabled(flag)
        self.COCODistImagePath.setEnabled(flag)
        self.COCODatasetName.setEnabled(flag)
        self.COCOAuthor.setEnabled(flag)
        self.COCOVersion.setEnabled(flag)

    def setCOCO2VOCEnabled(self, flag: bool):
        self.COCOdatasetPath.setEnabled(flag)
        self.browseCOCOPath.setEnabled(flag)
        self.COCOImagePath.setEnabled(flag)
        self.COCOAnnotationFile.setEnabled(flag)
        self.VOCDistPath.setEnabled(flag)
        self.browseVOCDistPath.setEnabled(flag)
        self.VOCDatasetName.setEnabled(flag)

    def check_complete(self, voc2coco=True):

        flag = False
        if voc2coco:
            ori_path = self.VOCdatasetPath.text()
            dist_path = self.COCODistPath.text()
            img_dir = self.COCODatasetName.text()
            if len(ori_path) * len(dist_path) * len(img_dir) and os.path.isdir(ori_path) and os.path.isdir(dist_path):
                ori_img_path = os.path.join(ori_path, self.VOCImagePath.currentText())
                ori_anno_path = os.path.join(ori_path, self.VOCAnnotationPath.currentText())
                dist_img_dir = self.COCODistImagePath.text()
                if os.path.isdir(ori_img_path) and os.path.isdir(ori_anno_path) and len(dist_img_dir):
                    if len(self.COCODatasetName.text()) * len(self.COCOAuthor.text()) * len(self.COCOVersion.text()):
                        flag = True
        else:
            ori_path = self.COCOdatasetPath.text()
            dist_path = self.VOCDistPath.text()
            img_dir = self.VOCDatasetName.text()
            if len(ori_path) * len(dist_path) * len(img_dir) and os.path.isdir(ori_path) and os.path.isdir(dist_path):
                ori_img_path = os.path.join(ori_path, self.COCOImagePath.currentText())
                anno_file = os.path.join(ori_path, "annotations", self.COCOAnnotationFile.currentText())
                if os.path.isdir(ori_img_path) and os.path.isfile(anno_file):
                    flag = True
        return flag

    def closeEvent(self, a0: QtGui.QCloseEvent):
        if self.p is not None:
            self.p.show()


def main():
    import sys

    app = QtWidgets.QApplication(sys.argv)

    w = LabelConverter()
    w.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
