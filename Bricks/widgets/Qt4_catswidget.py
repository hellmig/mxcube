# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/Qt4_catswidget.ui'
#
# Created: Wed Jan 13 15:45:35 2016
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_CatsWidget(object):
    def setupUi(self, CatsWidget):
        CatsWidget.setObjectName(_fromUtf8("CatsWidget"))
        CatsWidget.resize(370, 859)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CatsWidget.sizePolicy().hasHeightForWidth())
        CatsWidget.setSizePolicy(sizePolicy)
        self.vboxlayout = QtGui.QVBoxLayout(CatsWidget)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setObjectName(_fromUtf8("vboxlayout1"))
        self.lvSC = QtGui.QTreeWidget(CatsWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lvSC.setFont(font)
        self.lvSC.setObjectName(_fromUtf8("lvSC"))
        item_0 = QtGui.QTreeWidgetItem(self.lvSC)
        self.vboxlayout1.addWidget(self.lvSC)
        self.ckShowEmptySlots = QtGui.QCheckBox(CatsWidget)
        font = QtGui.QFont()
        self.ckShowEmptySlots.setFont(font)
        self.ckShowEmptySlots.setObjectName(_fromUtf8("ckShowEmptySlots"))
        self.vboxlayout1.addWidget(self.ckShowEmptySlots)
        self.vboxlayout2 = QtGui.QVBoxLayout()
        self.vboxlayout2.setObjectName(_fromUtf8("vboxlayout2"))
        spacerItem = QtGui.QSpacerItem(21, 6, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.vboxlayout2.addItem(spacerItem)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.btLoadSample = QtGui.QPushButton(CatsWidget)
        font = QtGui.QFont()
        self.btLoadSample.setFont(font)
        self.btLoadSample.setObjectName(_fromUtf8("btLoadSample"))
        self.hboxlayout.addWidget(self.btLoadSample)
        self.btUnloadSample = QtGui.QPushButton(CatsWidget)
        font = QtGui.QFont()
        self.btUnloadSample.setFont(font)
        self.btUnloadSample.setObjectName(_fromUtf8("btUnloadSample"))
        self.hboxlayout.addWidget(self.btUnloadSample)
        self.vboxlayout2.addLayout(self.hboxlayout)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName(_fromUtf8("hboxlayout1"))
        self.vboxlayout2.addLayout(self.hboxlayout1)
        self.btAbort = QtGui.QPushButton(CatsWidget)
        font = QtGui.QFont()
        self.btAbort.setFont(font)
        self.btAbort.setObjectName(_fromUtf8("btAbort"))
        self.vboxlayout2.addWidget(self.btAbort)
        spacerItem1 = QtGui.QSpacerItem(21, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.vboxlayout2.addItem(spacerItem1)
        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setObjectName(_fromUtf8("hboxlayout2"))
        self.textLabel1 = QtGui.QLabel(CatsWidget)
        font = QtGui.QFont()
        self.textLabel1.setFont(font)
        self.textLabel1.setWordWrap(False)
        self.textLabel1.setObjectName(_fromUtf8("textLabel1"))
        self.hboxlayout2.addWidget(self.textLabel1)
        self.txtState = QtGui.QLineEdit(CatsWidget)
        self.txtState.setEnabled(True)
        font = QtGui.QFont()
        self.txtState.setFont(font)
        self.txtState.setAlignment(QtCore.Qt.AlignHCenter)
        self.txtState.setReadOnly(True)
        self.txtState.setObjectName(_fromUtf8("txtState"))
        self.hboxlayout2.addWidget(self.txtState)
        self.vboxlayout2.addLayout(self.hboxlayout2)
        self.vboxlayout1.addLayout(self.vboxlayout2)
        self.vboxlayout.addLayout(self.vboxlayout1)

        self.retranslateUi(CatsWidget)
        QtCore.QMetaObject.connectSlotsByName(CatsWidget)

    def retranslateUi(self, CatsWidget):
        CatsWidget.setWindowTitle(QtGui.QApplication.translate("CatsWidget", "Form1", None, QtGui.QApplication.UnicodeUTF8))
        self.lvSC.headerItem().setText(0, QtGui.QApplication.translate("CatsWidget", "Column 1", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled = self.lvSC.isSortingEnabled()
        self.lvSC.setSortingEnabled(False)
        self.lvSC.topLevelItem(0).setText(0, QtGui.QApplication.translate("CatsWidget", "New Item", None, QtGui.QApplication.UnicodeUTF8))
        self.lvSC.setSortingEnabled(__sortingEnabled)
        self.ckShowEmptySlots.setText(QtGui.QApplication.translate("CatsWidget", "Show empty slots", None, QtGui.QApplication.UnicodeUTF8))
        self.btLoadSample.setText(QtGui.QApplication.translate("CatsWidget", "Load", None, QtGui.QApplication.UnicodeUTF8))
        self.btUnloadSample.setText(QtGui.QApplication.translate("CatsWidget", "Unload", None, QtGui.QApplication.UnicodeUTF8))
        self.btAbort.setText(QtGui.QApplication.translate("CatsWidget", "Abort", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1.setText(QtGui.QApplication.translate("CatsWidget", "State:", None, QtGui.QApplication.UnicodeUTF8))

