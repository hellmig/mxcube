#
#  Project: MXCuBE
#  https://github.com/mxcube.
#
#  This file is part of MXCuBE software.
#
#  MXCuBE is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  MXCuBE is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#  along with MXCuBE.  If not, see <http://www.gnu.org/licenses/>.

import new
import re
import logging

from PyQt4 import QtGui
from PyQt4 import QtCore

from BlissFramework import Qt4_Icons
from BlissFramework.Utils import Qt4_widget_colors
from BlissFramework.Qt4_BaseComponents import BlissWidget


__category__ = 'Qt4_General'


class Qt4_CatsPowerBrick(BlissWidget):

    STATES = {
        False: Qt4_widget_colors.LIGHT_RED,
        True:  Qt4_widget_colors.LIGHT_GREEN
    }

    def __init__(self, *args):
        BlissWidget.__init__(self,*args)

        # Hardware objects ----------------------------------------------------
        self.cats_hwobj=None

        # Internal values -----------------------------------------------------
        self.__expertMode = False
       
        # Properties ----------------------------------------------------------
        self.addProperty('mnemonic','string','')
        self.addProperty('forceNoControl','boolean',False)
        self.addProperty('expertModeControlOnly', 'boolean', False)
        self.addProperty('icons','string','')
        self.addProperty('username','string','')

        # Signals -------------------------------------------------------------

        # Slots ---------------------------------------------------------------
        self.defineSlot('allowControl',())
      
        # Graphic elements ----------------------------------------------------
        self.main_gbox = QtGui.QGroupBox("none", self)
        self.main_gbox.setAlignment(QtCore.Qt.AlignCenter)
        self.state_label = QtGui.QLabel('<b>unknown</b>', self.main_gbox)

        self.buttons_widget = QtGui.QWidget(self.main_gbox)
        self.set_in_button = QtGui.QPushButton("On", self.buttons_widget)
        self.set_out_button = QtGui.QPushButton("Off",self.buttons_widget)
        self.regulation_state_label = QtGui.QLabel('<b>unknown</b>', self.main_gbox)

        # Layout -------------------------------------------------------------- 
        _buttons_widget_hlayout = QtGui.QHBoxLayout(self.buttons_widget)
        _buttons_widget_hlayout.addWidget(self.set_in_button)
        _buttons_widget_hlayout.addWidget(self.set_out_button)
        _buttons_widget_hlayout.setSpacing(0)
        _buttons_widget_hlayout.setContentsMargins(0, 0, 0, 0)

        _main_gbox_vlayout = QtGui.QVBoxLayout(self.main_gbox)
        _main_gbox_vlayout.addWidget(self.state_label)
        _main_gbox_vlayout.addWidget(self.buttons_widget)
        _main_gbox_vlayout.addWidget(self.regulation_state_label)
        _main_gbox_vlayout.setSpacing(2)
        _main_gbox_vlayout.setContentsMargins(4, 4, 4, 4)

        _main_vlayout = QtGui.QVBoxLayout(self)
        _main_vlayout.addWidget(self.main_gbox)
        _main_vlayout.setSpacing(0)
        _main_vlayout.setContentsMargins(0, 0, 0, 0)

        # SizePolicies --------------------------------------------------------

        # Qt signal/slot connections ------------------------------------------
        self.set_in_button.clicked.connect(self.set_in)
        self.set_out_button.clicked.connect(self.set_out)

        # Other ---------------------------------------------------------------
        self.state_label.setAlignment(QtCore.Qt.AlignCenter)
        self.regulation_state_label.setAlignment(QtCore.Qt.AlignCenter)
        self.state_label.setToolTip("Shows the current control state")
        self.set_in_button.setToolTip("Changes the control state")
        self.set_out_button.setToolTip("Changes the control state")           


    def setExpertMode(self, expert):
        self.__expertMode = expert
        self.buttons_widget.show()
        
        if not expert and self["expertModeControlOnly"]:
            self.buttons_widget.hide()

        
    def set_in(self, state):
        self.cats_hwobj._doPowerState(True)

    def set_out(self, state):
        self.cats_hwobj._doPowerState(False)

    def updateLabel(self,label):
        self.main_gbox.setTitle(label)

    def stateChanged(self, state):
        color=self.STATES[state]
        if color is None:
            color = Qt4_widget_colors.GROUP_BOX_GRAY

        Qt4_widget_colors.set_widget_color(self.state_label, color)

        self.set_in_button.setEnabled(not state)
        self.set_out_button.setEnabled(state)

        if state:
            self.state_label.setText("<b>On</b>")
        else:
            self.state_label.setText("<b>Off</b>")

    def regulationStateChanged(self, state):
        print "regulationStateChanged", state
        color=self.STATES[state]
        if color is None:
            color = Qt4_widget_colors.GROUP_BOX_GRAY

        Qt4_widget_colors.set_widget_color(self.regulation_state_label, color)

        if state:
            self.regulation_state_label.setText("<b>LN2 Regulation Enabled</b>")
        else:
            self.regulation_state_label.setText("<b>LN2 Regulation Disabled</b>")

    def allowControl(self,enable):
        if self['forceNoControl']:
            return
        if enable:
            self.buttons_widget.show()
        else:
            self.buttons_widget.hide()

    def propertyChanged(self,propertyName,oldValue,newValue):
        if propertyName=='mnemonic':
            if self.cats_hwobj is not None:
                self.disconnect(self.cats_hwobj, QtCore.SIGNAL("powerStateChanged"), self.stateChanged)
                self.disconnect(self.cats_hwobj, QtCore.SIGNAL("regulationStateChanged"), self.regulationStateChanged)

            h_obj=self.getHardwareObject(newValue)
            if h_obj is not None:
                self.cats_hwobj=h_obj
                self.main_gbox.show()
                

                self.stateChanged(self.cats_hwobj._chnPowered.getValue())
                self.regulationStateChanged(self.cats_hwobj._chnLN2Regulation.getValue())
                self.set_in_button.setToolTip("Enable power of the CATS robot")
                self.set_out_button.setToolTip("Enable power of the CATS robot")
                self.main_gbox.setTitle(self['username'])
                self.connect(self.cats_hwobj, QtCore.SIGNAL('powerStateChanged'), self.stateChanged)
                self.connect(self.cats_hwobj, QtCore.SIGNAL('regulationStateChanged'), self.regulationStateChanged)
            else:
                self.cats_hwobj=None
                #self.main_gbox.hide()
        elif propertyName=='expertModeControlOnly':
            if newValue:
                if self.__expertMode:
                    self.buttons_widget.show()
                else:
                    self.buttons_widget.hide()
            else:
                self.buttons_widget.show()
        elif propertyName=='forceNoControl':
            if newValue:
                self.buttons_widget.hide()
            else:
                self.buttons_widget.show()
        elif propertyName=='username':
            self.main_gbox.setTitle(self['username'])
        else:
            BlissWidget.propertyChanged(self,propertyName,oldValue,newValue)

