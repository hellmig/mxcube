from BlissFramework import BaseComponents
from qt import *
import logging
import time

from BlissFramework.Utils import widget_colors

__category__ = 'Synoptic'

class BessyTopupBrick(BaseComponents.BlissWidget):
    def __init__(self, *args):
        BaseComponents.BlissWidget.__init__(self, *args)

        self.topupMode=None
        self.lastValue=None

        self.addProperty('mnemonic','string','')

        self.containerBox=QVGroupBox("Synchrotron status",self)
        self.containerBox.setInsideMargin(4)
        self.containerBox.setInsideSpacing(0)
        self.containerBox.setAlignment(QLabel.AlignLeft)

        self.mode=QLabel(self.containerBox)
        self.mode.setAlignment(QLabel.AlignCenter)
        self.mode.setPaletteBackgroundColor(widget_colors.LIGHT_BLUE)

        QVBoxLayout(self)
        self.layout().addWidget(self.containerBox)

        QToolTip.add(self.mode,"Storage-ring information")

    def setValue(self,value=None):
        if value is None:
            value=self.lastValue
        else:
            self.lastValue=value

        self.mode.setText("")
        if value is None or value == "":
            self.mode.setText("n/a")
        else:
            self.mode.setText("<i>%s</i>" % value)

    def propertyChanged(self,propertyName,oldValue,newValue):
        if propertyName=='mnemonic':
            if self.topupMode is not None:
                self.disconnect(self.topupMode,PYSIGNAL('valueChanged'),self.setValue)
                self.disconnect(self.topupMode,PYSIGNAL('timeout'),self.setValue)

            self.setValue()

            self.topupMode=self.getHardwareObject(newValue)
            if self.topupMode is not None:
                self.containerBox.setEnabled(True)
                self.connect(self.topupMode,PYSIGNAL('valueChanged'),self.setValue)
                self.connect(self.topupMode,PYSIGNAL('timeout'),self.setValue)
            else:
                self.containerBox.setEnabled(False)
        else:
            BaseComponents.BlissWidget.propertyChanged(self,propertyName,oldValue,newValue)
