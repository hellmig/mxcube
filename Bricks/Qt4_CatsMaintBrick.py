import logging
import sys

from PyQt4 import QtGui
from PyQt4 import QtCore

import BlissFramework
from BlissFramework.Qt4_BaseComponents import BlissWidget

from widgets.Qt4_catsmaintwidget import Ui_CatsMaintWidget


__category__ = "Sample changer"


class Qt4_CatsMaintWidget(QtGui.QWidget, Ui_CatsMaintWidget):
    def __init__(self):
	QtGui.QWidget.__init__(self)
	self.setupUi(self)
  
    
class Qt4_CatsMaintBrick(BlissFramework.Qt4_BaseComponents.BlissWidget):
    def __init__(self, *args):
        BlissFramework.Qt4_BaseComponents.BlissWidget.__init__(self, *args)
        
        self.addProperty("hwobj", "string", "")
        
        self.widget = Qt4_CatsMaintWidget()
        QtGui.QHBoxLayout(self)
        self.layout().addWidget(self.widget)
        
        QtCore.QObject.connect(self.widget.btPowerOn, QtCore.SIGNAL('clicked()'), self._powerOn)        
        QtCore.QObject.connect(self.widget.btPowerOff, QtCore.SIGNAL('clicked()'), self._powerOff)       
        QtCore.QObject.connect(self.widget.btLid1Open, QtCore.SIGNAL('clicked()'), self._lid1Open)
        QtCore.QObject.connect(self.widget.btLid1Close, QtCore.SIGNAL('clicked()'), self._lid1Close)
        QtCore.QObject.connect(self.widget.btLid2Open, QtCore.SIGNAL('clicked()'), self._lid2Open)
        QtCore.QObject.connect(self.widget.btLid2Close, QtCore.SIGNAL('clicked()'), self._lid2Close)
        QtCore.QObject.connect(self.widget.btLid3Open, QtCore.SIGNAL('clicked()'), self._lid3Open)
        QtCore.QObject.connect(self.widget.btLid3Close, QtCore.SIGNAL('clicked()'), self._lid3Close)
        QtCore.QObject.connect(self.widget.btResetError, QtCore.SIGNAL('clicked()'), self._resetError)
        QtCore.QObject.connect(self.widget.btBack, QtCore.SIGNAL('clicked()'), self._backTraj)                     
        QtCore.QObject.connect(self.widget.btSafe, QtCore.SIGNAL('clicked()'), self._safeTraj)                     
        QtCore.QObject.connect(self.widget.btRegulationOn, QtCore.SIGNAL('clicked()'), self._regulationOn)                     
                
        self.device=None
        self._pathRunning = False
        self._poweredOn = False
        self._regulationOn = False

        self._lid1State = False
        self._lid2State = False
        self._lid3State = False

        self._updateButtons()

    def propertyChanged(self, property, oldValue, newValue):
        logging.getLogger("user_level_log").info("Property Changed: " + str(property) + " = " + str(newValue))
        if property == 'hwobj':
            if self.device is not None:
                self.disconnect(self.device, QtCore.SIGNAL('lid1StateChanged'), self._updateLid1State)
                self.disconnect(self.device, QtCore.SIGNAL('lid2StateChanged'), self._updateLid2State)
                self.disconnect(self.device, QtCore.SIGNAL('lid3StateChanged'), self._updateLid3State)
                self.disconnect(self.device, QtCore.SIGNAL('runningStateChanged'), self._updatePathRunningFlag)
                self.disconnect(self.device, QtCore.SIGNAL('powerStateChanged'), self._updatePowerState)
                self.disconnect(self.device, QtCore.SIGNAL('messageChanged'), self._updateMessage)
                self.disconnect(self.device, QtCore.SIGNAL('regulationStateChanged'), self._updateRegulationState)
            # load the new hardware object
            self.device = self.getHardwareObject(newValue)                                    
            if self.device is not None:
                self.connect(self.device, QtCore.SIGNAL('regulationStateChanged'), self._updateRegulationState)
                self.connect(self.device, QtCore.SIGNAL('messageChanged'), self._updateMessage)
                self.connect(self.device, QtCore.SIGNAL('powerStateChanged'), self._updatePowerState)
                self.connect(self.device, QtCore.SIGNAL('runningStateChanged'), self._updatePathRunningFlag)
                self.connect(self.device, QtCore.SIGNAL('lid1StateChanged'), self._updateLid1State)
                self.connect(self.device, QtCore.SIGNAL('lid2StateChanged'), self._updateLid2State)
                self.connect(self.device, QtCore.SIGNAL('lid3StateChanged'), self._updateLid3State)

    def _updateRegulationState(self, value):
        self._regulationOn = value
        if value:
            self.widget.lblRegulationState.setStyleSheet('background: green')
        else:
            self.widget.lblRegulationState.setStyleSheet('background: red')
        self._updateButtons()

    def _updatePowerState(self, value):
        self._poweredOn = value
        if value:
            self.widget.lblPowerState.setStyleSheet('background: green')
        else:
            self.widget.lblPowerState.setStyleSheet('background: red')
        self._updateButtons()

    def _updateMessage(self, value):
        self.widget.lblMessage.setText(str(value))

    def _updatePathRunningFlag(self, value):
        self._pathRunning = value
        self._updateButtons()

    def _updateLid1State(self, value):
        self._lid1State = value
        if self.device is not None and not self._pathRunning:
            self.widget.btLid1Open.setEnabled(not value)
            self.widget.btLid1Close.setEnabled(value)
        else:
            self.widget.btLid1Open.setEnabled(False)
            self.widget.btLid1Close.setEnabled(False)

    def _updateLid2State(self, value):
        self._lid2State = value
        if self.device is not None and not self._pathRunning:
            self.widget.btLid2Open.setEnabled(not value)
            self.widget.btLid2Close.setEnabled(value)
        else:
            self.widget.btLid2Open.setEnabled(False)
            self.widget.btLid2Close.setEnabled(False)

    def _updateLid3State(self, value):
        self._lid3State = value
        if self.device is not None and not self._pathRunning:
            self.widget.btLid3Open.setEnabled(not value)
            self.widget.btLid3Close.setEnabled(value)
        else:
            self.widget.btLid3Open.setEnabled(False)
            self.widget.btLid3Close.setEnabled(False)

    def _updateButtons(self):
        if self.device is None:
            # disable all buttons
            self.widget.btPowerOn.setEnabled(False)
            self.widget.btPowerOff.setEnabled(False)
            self.widget.btLid1Open.setEnabled(False)
            self.widget.btLid1Close.setEnabled(False)
            self.widget.btLid2Open.setEnabled(False)
            self.widget.btLid2Close.setEnabled(False)
            self.widget.btLid3Open.setEnabled(False)
            self.widget.btLid3Close.setEnabled(False)
            self.widget.btResetError.setEnabled(False)
            self.widget.btBack.setEnabled(False)
            self.widget.btSafe.setEnabled(False)
            self.widget.btRegulationOn.setEnabled(False)
            self.widget.lblMessage.setText('')
        else:
            ready = not self._pathRunning
            #ready = not self.device.isDeviceReady()
            self.widget.btPowerOn.setEnabled(ready and not self._poweredOn)
            self.widget.btPowerOff.setEnabled(ready and self._poweredOn)
            self.widget.btResetError.setEnabled(ready)
            self.widget.btBack.setEnabled(ready and self._poweredOn)
            self.widget.btSafe.setEnabled(ready and self._poweredOn)

            self.widget.btRegulationOn.setEnabled(not self._regulationOn)

            self._updateLid1State(self._lid1State)
            self._updateLid2State(self._lid2State)
            self._updateLid3State(self._lid3State)

    def _regulationOn(self):
        logging.getLogger("user_level_log").info("CATS: Regulation On")
        try:
            if self.device is not None:
                self.device._doEnableRegulation()
        except:
            QtGui.QMessageBox.warning( self, "Error",str(sys.exc_info()[1]))

    def _powerOn(self):
        logging.getLogger("user_level_log").info("CATS: Power On")
        try:
            if self.device is not None:
                self.device._doPowerState(True)
        except:
            QtGui.QMessageBox.warning( self, "Error",str(sys.exc_info()[1]))

    def _powerOff(self):
        logging.getLogger("user_level_log").info("CATS: Power Off")
        try:
            if self.device is not None:
                self.device._doPowerState(False)
        except:
            QtGui.QMessageBox.warning( self, "Error",str(sys.exc_info()[1]))

    def _lid1Open(self):
        logging.getLogger("user_level_log").info("CATS: Open Lid 1")
        try:
            if self.device is not None:
                self.device._doLid1State(True)
        except:
            QtGui.QMessageBox.warning( self, "Error",str(sys.exc_info()[1]))

    def _lid1Close(self):
        logging.getLogger("user_level_log").info("CATS: Close  Lid 1")
        try:
            if self.device is not None:
                self.device._doLid1State(False)
        except:
            QtGui.QMessageBox.warning( self, "Error",str(sys.exc_info()[1]))

    def _lid2Open(self):
        logging.getLogger("user_level_log").info("CATS: Open Lid 2")
        try:
            if self.device is not None:
                self.device._doLid2State(True)
        except:
            QtGui.QMessageBox.warning( self, "Error",str(sys.exc_info()[1]))

    def _lid2Close(self):
        logging.getLogger("user_level_log").info("CATS: Close  Lid 2")
        try:
            if self.device is not None:
                self.device._doLid2State(False)
        except:
            QtGui.QMessageBox.warning( self, "Error",str(sys.exc_info()[1]))

    def _lid3Open(self):
        logging.getLogger("user_level_log").info("CATS: Open Lid 3")
        try:
            if self.device is not None:
                self.device._doLid3State(True)
        except:
            QtGui.QMessageBox.warning( self, "Error",str(sys.exc_info()[1]))

    def _lid3Close(self):
        logging.getLogger("user_level_log").info("CATS: Close  Lid 3")
        try:
            if self.device is not None:
                self.device._doLid3State(False)
        except:
            QtGui.QMessageBox.warning( self, "Error",str(sys.exc_info()[1]))

    def _resetError(self):
        logging.getLogger("user_level_log").info("CATS: Reset")
        try:
            if self.device is not None:
                self.device._doReset()
        except:
            QtGui.QMessageBox.warning( self, "Error",str(sys.exc_info()[1]))

    def _backTraj(self):
        logging.getLogger("user_level_log").info("CATS: Transfer sample back to dewar.")
        try:
            if self.device is not None:
                #self.device._doBack()
                self.device.backTraj()
        except:
            QtGui.QMessageBox.warning( self, "Error",str(sys.exc_info()[1]))

    def _safeTraj(self):
        logging.getLogger("user_level_log").info("CATS: Safely move robot arm to home position.")
        try:
            if self.device is not None:
                #self.device._doSafe()
                self.device.safeTraj()
        except:
            QtGui.QMessageBox.warning( self, "Error",str(sys.exc_info()[1]))

