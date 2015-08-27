import logging

from qt import *
from BlissFramework.BaseComponents import BlissWidget

__category__ = 'BESSY'

class ClearMemoryBrick(BlissWidget):

    def __init__(self, *args):
        BlissWidget.__init__(self, *args)

        self.cats_ho =None

        self.addProperty('cats', 'string', '')

        self.topBox = QHGroupBox("Cats Tools",self)
        self.topBox.setInsideMargin(4)
        self.topBox.setInsideSpacing(2)

        self.catsLabel = QLabel("device",self.topBox)
        self.openButton = QPushButton("Open lid 1",self.topBox)
        self.closeButton = QPushButton("Close lid 1",self.topBox)
        
        QObject.connect(self.openButton,SIGNAL('clicked()'),self.openLid1)
        QObject.connect(self.closeButton,SIGNAL('clicked()'),self.closeLid1)

        self.topBox.layout().addWidget(self.catsLabel)
        self.topBox.layout().addWidget(self.openButton)
        self.topBox.layout().addWidget(self.closeButton)

        self.openButton.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.MinimumExpanding)
        self.closeButton.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.MinimumExpanding)

        QVBoxLayout(self)
        self.layout().addWidget(self.topBox)
        self.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Fixed)

    def propertyChanged(self, property, oldValue, newValue):
        if property == 'cats':
            if self.cats_ho is not None:
                self.disconnect(self.cats_ho,PYSIGNAL('catsReady'),self.catsReady)

            self.cats_ho = self.getHardwareObject(newValue)
            self.catsLabel.setText(newValue)

            if self.cats_ho is not None:
                self.connect(self.cats_ho,PYSIGNAL('catsReady'),self.catsReady)

    def openLid1(self):
        if self.cats_ho is not None:
           self.cats_ho.openlid1()

    def closeLid1(self):
        if self.cats_ho is not None:
           self.cats_ho.closelid1()

    def catsReady(self, ready):
        self.openButton.setEnable(ready)
        self.closeButton.setEnable(ready)

