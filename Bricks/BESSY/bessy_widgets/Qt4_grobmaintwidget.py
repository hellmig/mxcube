# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/Qt4_grobmaintwidget.ui'
#
# Created: Tue Aug 22 14:04:45 2017
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_GrobMaintWidget(object):
    def setupUi(self, GrobMaintWidget):
        GrobMaintWidget.setObjectName(_fromUtf8("GrobMaintWidget"))
        GrobMaintWidget.resize(1230, 855)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(GrobMaintWidget.sizePolicy().hasHeightForWidth())
        GrobMaintWidget.setSizePolicy(sizePolicy)
        self.vboxlayout = QtGui.QVBoxLayout(GrobMaintWidget)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.groupBox5 = QtGui.QGroupBox(GrobMaintWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox5.sizePolicy().hasHeightForWidth())
        self.groupBox5.setSizePolicy(sizePolicy)
        self.groupBox5.setObjectName(_fromUtf8("groupBox5"))
        self.hboxlayout = QtGui.QHBoxLayout(self.groupBox5)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.lblPowerState = QtGui.QLabel(self.groupBox5)
        self.lblPowerState.setAlignment(QtCore.Qt.AlignCenter)
        self.lblPowerState.setWordWrap(False)
        self.lblPowerState.setObjectName(_fromUtf8("lblPowerState"))
        self.hboxlayout.addWidget(self.lblPowerState)
        self.btPowerOn = QtGui.QPushButton(self.groupBox5)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btPowerOn.sizePolicy().hasHeightForWidth())
        self.btPowerOn.setSizePolicy(sizePolicy)
        self.btPowerOn.setObjectName(_fromUtf8("btPowerOn"))
        self.hboxlayout.addWidget(self.btPowerOn)
        self.btPowerOff = QtGui.QPushButton(self.groupBox5)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btPowerOff.sizePolicy().hasHeightForWidth())
        self.btPowerOff.setSizePolicy(sizePolicy)
        self.btPowerOff.setObjectName(_fromUtf8("btPowerOff"))
        self.hboxlayout.addWidget(self.btPowerOff)
        self.vboxlayout.addWidget(self.groupBox5)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName(_fromUtf8("hboxlayout1"))
        self.groupBox2 = QtGui.QGroupBox(GrobMaintWidget)
        self.groupBox2.setObjectName(_fromUtf8("groupBox2"))
        self.vboxlayout1 = QtGui.QVBoxLayout(self.groupBox2)
        self.vboxlayout1.setObjectName(_fromUtf8("vboxlayout1"))
        self.btLid1Open = QtGui.QPushButton(self.groupBox2)
        font = QtGui.QFont()
        self.btLid1Open.setFont(font)
        self.btLid1Open.setObjectName(_fromUtf8("btLid1Open"))
        self.vboxlayout1.addWidget(self.btLid1Open)
        self.btLid1Close = QtGui.QPushButton(self.groupBox2)
        font = QtGui.QFont()
        self.btLid1Close.setFont(font)
        self.btLid1Close.setObjectName(_fromUtf8("btLid1Close"))
        self.vboxlayout1.addWidget(self.btLid1Close)
        self.hboxlayout1.addWidget(self.groupBox2)
        self.groupBox2_2 = QtGui.QGroupBox(GrobMaintWidget)
        self.groupBox2_2.setObjectName(_fromUtf8("groupBox2_2"))
        self.vboxlayout2 = QtGui.QVBoxLayout(self.groupBox2_2)
        self.vboxlayout2.setObjectName(_fromUtf8("vboxlayout2"))
        self.btLid2Open = QtGui.QPushButton(self.groupBox2_2)
        font = QtGui.QFont()
        self.btLid2Open.setFont(font)
        self.btLid2Open.setObjectName(_fromUtf8("btLid2Open"))
        self.vboxlayout2.addWidget(self.btLid2Open)
        self.btLid2Close = QtGui.QPushButton(self.groupBox2_2)
        font = QtGui.QFont()
        self.btLid2Close.setFont(font)
        self.btLid2Close.setObjectName(_fromUtf8("btLid2Close"))
        self.vboxlayout2.addWidget(self.btLid2Close)
        self.hboxlayout1.addWidget(self.groupBox2_2)
        self.vboxlayout.addLayout(self.hboxlayout1)
        self.groupBox6 = QtGui.QGroupBox(GrobMaintWidget)
        self.groupBox6.setObjectName(_fromUtf8("groupBox6"))
        self.hboxlayout2 = QtGui.QHBoxLayout(self.groupBox6)
        self.hboxlayout2.setObjectName(_fromUtf8("hboxlayout2"))
        self.lblMessage = QtGui.QLabel(self.groupBox6)
        self.lblMessage.setWordWrap(False)
        self.lblMessage.setObjectName(_fromUtf8("lblMessage"))
        self.hboxlayout2.addWidget(self.lblMessage)
        self.vboxlayout.addWidget(self.groupBox6)
        self.groupBox13 = QtGui.QGroupBox(GrobMaintWidget)
        self.groupBox13.setObjectName(_fromUtf8("groupBox13"))
        self.hboxlayout3 = QtGui.QHBoxLayout(self.groupBox13)
        self.hboxlayout3.setObjectName(_fromUtf8("hboxlayout3"))
        self.btAckManualUnmount = QtGui.QPushButton(self.groupBox13)
        self.btAckManualUnmount.setObjectName(_fromUtf8("btAckManualUnmount"))
        self.hboxlayout3.addWidget(self.btAckManualUnmount)
        self.btAckError = QtGui.QPushButton(self.groupBox13)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btAckError.sizePolicy().hasHeightForWidth())
        self.btAckError.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        self.btAckError.setFont(font)
        self.btAckError.setObjectName(_fromUtf8("btAckError"))
        self.hboxlayout3.addWidget(self.btAckError)
        self.btBack = QtGui.QPushButton(self.groupBox13)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btBack.sizePolicy().hasHeightForWidth())
        self.btBack.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        self.btBack.setFont(font)
        self.btBack.setObjectName(_fromUtf8("btBack"))
        self.hboxlayout3.addWidget(self.btBack)
        self.btSafe = QtGui.QPushButton(self.groupBox13)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btSafe.sizePolicy().hasHeightForWidth())
        self.btSafe.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        self.btSafe.setFont(font)
        self.btSafe.setObjectName(_fromUtf8("btSafe"))
        self.hboxlayout3.addWidget(self.btSafe)
        self.vboxlayout.addWidget(self.groupBox13)
        self.groupBox5_2 = QtGui.QGroupBox(GrobMaintWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox5_2.sizePolicy().hasHeightForWidth())
        self.groupBox5_2.setSizePolicy(sizePolicy)
        self.groupBox5_2.setObjectName(_fromUtf8("groupBox5_2"))
        self.hboxlayout4 = QtGui.QHBoxLayout(self.groupBox5_2)
        self.hboxlayout4.setObjectName(_fromUtf8("hboxlayout4"))
        self.lblRegulationState = QtGui.QLabel(self.groupBox5_2)
        self.lblRegulationState.setAlignment(QtCore.Qt.AlignCenter)
        self.lblRegulationState.setWordWrap(False)
        self.lblRegulationState.setObjectName(_fromUtf8("lblRegulationState"))
        self.hboxlayout4.addWidget(self.lblRegulationState)
        self.btRegulationOn = QtGui.QPushButton(self.groupBox5_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btRegulationOn.sizePolicy().hasHeightForWidth())
        self.btRegulationOn.setSizePolicy(sizePolicy)
        self.btRegulationOn.setObjectName(_fromUtf8("btRegulationOn"))
        self.hboxlayout4.addWidget(self.btRegulationOn)
        self.vboxlayout.addWidget(self.groupBox5_2)

        self.retranslateUi(GrobMaintWidget)
        QtCore.QMetaObject.connectSlotsByName(GrobMaintWidget)
        GrobMaintWidget.setTabOrder(self.btPowerOn, self.btPowerOff)
        GrobMaintWidget.setTabOrder(self.btPowerOff, self.btLid1Open)
        GrobMaintWidget.setTabOrder(self.btLid1Open, self.btLid1Close)
        GrobMaintWidget.setTabOrder(self.btLid1Close, self.btLid2Open)
        GrobMaintWidget.setTabOrder(self.btLid2Open, self.btLid2Close)
        GrobMaintWidget.setTabOrder(self.btLid2Close, self.btBack)
        GrobMaintWidget.setTabOrder(self.btBack, self.btSafe)

    def retranslateUi(self, GrobMaintWidget):
        GrobMaintWidget.setWindowTitle(QtGui.QApplication.translate("GrobMaintWidget", "Form1", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox5.setTitle(QtGui.QApplication.translate("GrobMaintWidget", "Arm Power", None, QtGui.QApplication.UnicodeUTF8))
        self.lblPowerState.setText(QtGui.QApplication.translate("GrobMaintWidget", "Power", None, QtGui.QApplication.UnicodeUTF8))
        self.btPowerOn.setText(QtGui.QApplication.translate("GrobMaintWidget", "Power On", None, QtGui.QApplication.UnicodeUTF8))
        self.btPowerOff.setText(QtGui.QApplication.translate("GrobMaintWidget", "Power Off", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox2.setTitle(QtGui.QApplication.translate("GrobMaintWidget", "Robot Lid", None, QtGui.QApplication.UnicodeUTF8))
        self.btLid1Open.setText(QtGui.QApplication.translate("GrobMaintWidget", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.btLid1Close.setText(QtGui.QApplication.translate("GrobMaintWidget", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox2_2.setTitle(QtGui.QApplication.translate("GrobMaintWidget", "User Lid", None, QtGui.QApplication.UnicodeUTF8))
        self.btLid2Open.setText(QtGui.QApplication.translate("GrobMaintWidget", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.btLid2Close.setText(QtGui.QApplication.translate("GrobMaintWidget", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox6.setTitle(QtGui.QApplication.translate("GrobMaintWidget", "Robot message", None, QtGui.QApplication.UnicodeUTF8))
        self.lblMessage.setText(QtGui.QApplication.translate("GrobMaintWidget", "Dummy message", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox13.setTitle(QtGui.QApplication.translate("GrobMaintWidget", "Recovery Commands", None, QtGui.QApplication.UnicodeUTF8))
        self.btAckManualUnmount.setText(QtGui.QApplication.translate("GrobMaintWidget", "Manual Unmount", None, QtGui.QApplication.UnicodeUTF8))
        self.btAckError.setText(QtGui.QApplication.translate("GrobMaintWidget", "Ack System Error", None, QtGui.QApplication.UnicodeUTF8))
        self.btBack.setText(QtGui.QApplication.translate("GrobMaintWidget", "Back", None, QtGui.QApplication.UnicodeUTF8))
        self.btSafe.setText(QtGui.QApplication.translate("GrobMaintWidget", "Safe", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox5_2.setTitle(QtGui.QApplication.translate("GrobMaintWidget", "LN2 Regulation", None, QtGui.QApplication.UnicodeUTF8))
        self.lblRegulationState.setText(QtGui.QApplication.translate("GrobMaintWidget", "Regulation", None, QtGui.QApplication.UnicodeUTF8))
        self.btRegulationOn.setText(QtGui.QApplication.translate("GrobMaintWidget", "Regulation On", None, QtGui.QApplication.UnicodeUTF8))

