# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'choose_class.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ChooseClass(object):
    def setupUi(self, ChooseClass):
        ChooseClass.setObjectName("ChooseClass")
        ChooseClass.resize(400, 414)
        self.gridLayout = QtWidgets.QGridLayout(ChooseClass)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(ChooseClass)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 3, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 3, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(3, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)
        self.classes_list = QtWidgets.QListWidget(ChooseClass)
        self.classes_list.setObjectName("classes_list")
        self.gridLayout.addWidget(self.classes_list, 1, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(3, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 2, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 3, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem3, 0, 1, 1, 1)

        self.retranslateUi(ChooseClass)
        self.buttonBox.accepted.connect(ChooseClass.accept)
        self.buttonBox.rejected.connect(ChooseClass.reject)
        QtCore.QMetaObject.connectSlotsByName(ChooseClass)

    def retranslateUi(self, ChooseClass):
        _translate = QtCore.QCoreApplication.translate
        ChooseClass.setWindowTitle(_translate("ChooseClass", "Choose Class"))





if __name__ == '__main__':
    from PyQt5.QtWidgets import *

    class Choose(QDialog, Ui_ChooseClass):

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

            def yes():
                self.ret = self.classes_list.currentIndex().row()
                # print("yes", self.ret)

            def no():
                self.ret = -1
                # print("no", self.ret)

            def keyPress(a0: QtGui.QKeyEvent):
                # if a0.matches(QKeySequence.)
                # print(a0.text(), a0.key())
                if a0.key() == 16777220:
                    yes()
                    self.close()
                elif a0.key() == 16777216:
                    no()
                    self.close()

            self.buttonBox.accepted.connect(yes)
            self.buttonBox.rejected.connect(no)
            self.keyPressEvent = keyPress

    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Choose(classes=["test1", "test2"])
    w.show()
    sys.exit(app.exec_())
