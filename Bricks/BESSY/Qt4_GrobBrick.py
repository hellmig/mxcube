import string
import logging
import sys
import sample_changer.GenericSampleChanger as SampleChanger

from PyQt4 import QtGui
from PyQt4 import QtCore

import BlissFramework
from BlissFramework.Qt4_BaseComponents import BlissWidget

from widgets.Qt4_catswidget import Ui_CatsWidget

__category__ = "Sample changer"
    

class Qt4_CatsWidget(QtGui.QWidget, Ui_CatsWidget):
    def __init__(self):
	QtGui.QWidget.__init__(self)
	self.setupUi(self)
  
    
class Qt4_GrobBrick(BlissFramework.Qt4_BaseComponents.BlissWidget):

    class MyTreeItemDelegate(QtGui.QItemDelegate):

        def paint(self, painter, option, index):
            if index.column() == 0 and (option.state & QtGui.QStyle.State_Selected):
               itemText = index.data(QtCore.Qt.DisplayRole).toString()
               myoption = option
               myoption.font.setBold(True)
               # access the QTreeWidget: myoption.widget
               super(Qt4_GrobBrick.MyTreeItemDelegate, self).paint(painter, myoption, index)
            else:
                super(Qt4_GrobBrick.MyTreeItemDelegate, self).paint(painter, option, index)


    def __init__(self, *args):
        BlissFramework.Qt4_BaseComponents.BlissWidget.__init__(self, *args)
        
        self.addProperty("hwobj", "string", "")
        
        self.widget = Qt4_CatsWidget()
        QtGui.QHBoxLayout(self)
        self.layout().addWidget(self.widget)
        
        QtCore.QObject.connect(self.widget.btLoadSample,QtCore.SIGNAL('clicked()'),self._loadSample)        
        #QtCore.QObject.connect(self.widget.btLoadSample,QtCore.SIGNAL('clicked()'),self.onMenuLoad)        
        QtCore.QObject.connect(self.widget.btUnloadSample,QtCore.SIGNAL('clicked()'),self._unloadSample)
        QtCore.QObject.connect(self.widget.btAbort,QtCore.SIGNAL('clicked()'),self._abort)                     
                
        self.device=None
        self.phase = "Unknown"
        self.state = "Unknown"
        self._loadedSample = None
        
        self.list = self.widget.lvSC   
        self.list.setItemDelegateForColumn(0, Qt4_GrobBrick.MyTreeItemDelegate())

        self.list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        #self.list.setSelectionMode(QListView::NoSelection)
        QtCore.QObject.connect(self.list,QtCore.SIGNAL('itemSelectionChanged()'),self.onListSelected)
        #QtCore.QObject.connect(self.list,QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'), self.onListPopupMenu)
        self.list.customContextMenuRequested.connect(self.onListPopupMenu)
        
        self.widget.ckShowEmptySlots.setChecked(False)
        QtCore.QObject.connect(self.widget.ckShowEmptySlots,QtCore.SIGNAL('clicked()'),self.onShowEmptySlots)

        self._clearTable()
        
    def propertyChanged(self, property, oldValue, newValue):
        logging.getLogger("user_level_log").info("Property Changed: " + str(property) + " = " + str(newValue))
        if property == 'hwobj':
            if self.device is not None:
                self.disconnect(self.device, self.device.STATE_CHANGED_EVENT, self.onStateChanged)
                self.disconnect(self.device, self.device.STATUS_CHANGED_EVENT, self.onSatusChanged)
                self.disconnect(self.device, self.device.INFO_CHANGED_EVENT, self.onInfoChanged)
                self.disconnect(self.device, self.device.LOADED_SAMPLE_CHANGED_EVENT, self.onLoadedSampleChanged)
                self.disconnect(self.device, self.device.SELECTION_CHANGED_EVENT, self.onSelectionChanged)
                self.disconnect(self.device, self.device.TASK_FINISHED_EVENT, self.onTaskFinished)
                
            self.device = self.getHardwareObject(newValue)                                    

            if self.device is not None:
                self.connect(self.device, self.device.STATE_CHANGED_EVENT, self.onStateChanged)
                self.connect(self.device, self.device.STATUS_CHANGED_EVENT, self.onStatusChanged)
                self.connect(self.device, self.device.INFO_CHANGED_EVENT, self.onInfoChanged)
                self.connect(self.device, self.device.LOADED_SAMPLE_CHANGED_EVENT, self.onLoadedSampleChanged)
                self.connect(self.device, self.device.SELECTION_CHANGED_EVENT, self.onSelectionChanged)
                self.connect(self.device, self.device.TASK_FINISHED_EVENT, self.onTaskFinished)
                self.onStateChanged(self.device.getState(),None)
                self.onStatusChanged(self.device.getStatus())
                self._createTable()       
            else:
                self.onStateChanged(SampleChanger.SampleChangerState.Unknown,None)
                self.onStatusChanged("")
                self._clearTable()
   
    def onStateChanged(self, state,former):
        former_state=self.state
        self.state=string.lower(str(state))
        logging.getLogger("user_level_log").info( "State = " + str(state) )
        self._updateButtons()        
        self.emit(QtCore.SIGNAL("stateChanged"), (state, ))
        
    def onStatusChanged(self, status):
        self.widget.txtState.setText(str(status))
        
    def onInfoChanged(self):
        if self._changedStructure(self.root):
            self._createTable()
        else:                        
            self._updateTable()
        self._updateButtons() 

    def onLoadedSampleChanged(self,sample):
        self._loadedSample = sample
        self._updateButtons()

    def onSelectionChanged(self):
        self._updateButtons()        
        self.list.repaint()

    def onTaskFinished(self,task,ret,exception):
        pass

    def onShowEmptySlots(self):        
        #self._createTable()
        if self.root is not None:
            self._checkVisibility(self.root,self.widget.ckShowEmptySlots.isChecked())            
            
    def onListSelected(self):
        #import pdb; pdb.set_trace()
        item = self.list.currentItem()
        
        if item is None:
            pass 
        elif item==self.root:
            pass            
        else:
            element = self.device.getComponentByAddress(item.text(0))
            self.onMenuSelect()

    def onListPopupMenu(self, point):
        component = self._getSelectedComponent()
        ready = (self.device.getState() == SampleChanger.SampleChangerState.Ready)
        if component is not None:
            menu = QtGui.QMenu("Popup Menu", self.list)
            font = menu.font()
            font.setPointSize(11)
            menu.setFont(font)            
            if component == self.device:
                menu.addAction("Set ID", self.onMenuSetID).setEnabled(component.isTransient())
            menu.addAction("Scan", self.onMenuScan).setEnabled(component.isScannable())
            menu.popup(self.list.viewport().mapToGlobal(point)) 
            #menu.exec_(self.view.mapToGlobal(point))
             
    def onMenuSetID(self):
        try:  
            (text,ok) = QtGui.QInputDialog.getText("ID", "Enter new  ID:", QtGui.QLineEdit.Normal,self._getElementID(self.device).strip(),  self )
            if ok:
                self.device.setToken(str(text).strip())
                self._updateTable()
        except:
            QtGui.QMessageBox.warning ( self, "Error",str(sys.exc_info()[1]))
        
        
    def onMenuScan(self):
        #import pdb; pdb.set_trace()
        try:
            component = self._getSelectedComponent()
            if component is not None:
                if component.isScannable():
                    self.device.scan(component,recursive=True,wait=False)
                else:
                    QtGui.QMessageBox.information( self, "Scan","Component is not scannable")
        except:
            QtGui.QMessageBox.warning( self, "Error",str(sys.exc_info()[1]))
                
    def onMenuLoad(self):
        try:
            component = self._getSelectedSample()
            if component is not None:
                self.device.load(component,wait=False)
        except:
            QtGui.QMessageBox.warning( self, "Error",str(sys.exc_info()[1]))

    def onMenuUnload(self):
        try:
            component = self._getSelectedSample()
            if component is not None:
                self.device.unload(component,wait=False)
        except:
            QtGui.QMessageBox.warning( self, "Error",str(sys.exc_info()[1]))
    
    def onMenuSelect(self):
        try:
            component = self._getSelectedComponent()
            if component is not None:
                self.device.select(component,wait=False)
        except:
            QtGui.QMessageBox.warning( self, "Error",str(sys.exc_info()[1]))

    def _getSelectedComponent(self):
        item = self.list.currentItem()
        if (item is not None):
            if item==self.root:
                return self.device
            element = self.device.getComponentByAddress(item.text(0))
            return element
        
    def _getSelectedSample(self):
        c=self._getSelectedComponent()
        if (c is not None) and (c != self.device) and (c.isLeaf()):
            return c

    def _updateButtons(self):
        selected_sample = self._getSelectedSample()
        if self.device is None or not self.device.isReady():
            self.widget.btLoadSample.setEnabled(False) 
            self.widget.btUnloadSample.setEnabled(False)
            self.widget.btAbort.setEnabled(False)
            self.widget.lvSC.setEnabled(False)
        else:
            charging = (self.device.getState() == SampleChanger.SampleChangerState.Charging)
            ready = (self.device.getState() == SampleChanger.SampleChangerState.Ready)
            standby = (self.device.getState() == SampleChanger.SampleChangerState.StandBy)
            moving = (self.device.getState() in [SampleChanger.SampleChangerState.Moving, SampleChanger.SampleChangerState.Loading, SampleChanger.SampleChangerState.Unloading])
            self.widget.btLoadSample.setEnabled(ready and not charging and (selected_sample is not None) and selected_sample.isPresent() and (selected_sample != self._loadedSample))
            self.widget.btUnloadSample.setEnabled(ready and not charging and self.device.hasLoadedSample())
            self.widget.lvSC.setEnabled(ready or standby or charging)
        self.widget.btAbort.setEnabled(self.device is not None and not self.device.isReady())

    def _abort(self):
        logging.getLogger("user_level_log").info("Abort")
        if self.device is not None:
            self.device.abort()
            
    def _loadSample(self):
        try:
            if self.device is not None:
                self.device.load(wait=False)
        except:
            QtGui.QMessageBox.warning(self, "Error",str(sys.exc_info()[1]))
            
    def _unloadSample(self):
        try:
            if self.device is not None:
                self.device.unload(wait=False)
        except:
            QtGui.QMessageBox.warning(self, "Error",str(sys.exc_info()[1]))

    def _clearTable(self):
        self.root=None
        while (self.list.topLevelItemCount() > 0):
            self.list.takeTopLevelItem(0);

    def _addElement(self,parent,element):  
        s = QtCore.QStringList()
        s << element.getAddress() << self._getElementStatus(element) << self._getElementID(element)
        args = self._getElementProperties(element)
        for arg in args:
            s << arg
        item = QtGui.QTreeWidgetItem(parent, s)
        if  not element.isLeaf():
            #for e in reversed(element.getComponents()):
            for e in element.getComponents():
                self._addElement(item,e)
    
    def _getElementProperties(self,e):
        args = []
        if e.isLeaf():
            for prop_name in self.device.getSampleProperties():
                prop = e.getProperty(str(prop_name))
                if prop is None: 
                    prop = ""
                args.append(str(prop)) 
        return args
        
    def _getElementStatus(self,e):
        if e.isLeaf():
            if e.isLoaded():
                return "Loaded"
            if e.hasBeenLoaded():
                return "Used"
        #if e.isScanned():
        #    return "Scanned"
        if e.isPresent():
            return "Present"            
        return ""
                
    def _getElementID(self,e):
        if e == self.device:
            if self.device.getToken() is not None:
                return self.device.getToken() 
        else:
            if e.getID() is not None:
                return  e.getID()
        return ""
    
    def _getRootID(self):
        if self.device.getToken() is not None:
            return self.device.getToken()
        return ""           
        
    def _createTable(self):
        self._clearTable()        
        if  self.device is not None:            
            #self._show_empty_slots = self.widget.ckShowEmptySlots.isChecked()
            self.list.setRootIsDecorated(True) 
            self.list.setSortingEnabled(False)
            
            header = ["Element", "Status", "Barcode/ID"]
            for prop in self.device.getSampleProperties():
                header.append(str(prop))
            self.list.setHeaderLabels(header)

            self.list.setColumnWidth(0, 150)
            self.list.setColumnWidth(1, 60)
            self.list.setColumnWidth(2, 120)
            for i in range(3, self.list.columnCount()):
                self.list.setColumnWidth(i, 60)

            root_name = self.device.getAddress()
            s = QtCore.QStringList()
            s << root_name << "" << self._getRootID()
            self.root = QtGui.QTreeWidgetItem(self.list, s)
            #for element in reversed(self.device.getComponents()):
            for element in self.device.getComponents():
                self._addElement(self.root,element)
                                
            #self.root.setOpen(True)
            self.root.setExpanded(True)
            self._checkVisibility(self.root,self.widget.ckShowEmptySlots.isChecked())

    def _checkVisibility(self, item, show_empty_slots):    
        if item != self.root:
            element = self.device.getComponentByAddress(item.text(0))
            if element is not None:           
                if element.isLeaf():
                    # item.setVisible(show_empty_slots or element.isPresent())
                    item.setHidden(not(show_empty_slots or element.isPresent()))
                else:
                    #item.setVisible( show_empty_slots or not element.isEmpty())
                    item.setHidden(not(show_empty_slots or not element.isEmpty()))
        childIndex = 0
        child = item.child(childIndex)
        while child is not None:
            self._checkVisibility(child,show_empty_slots)
            childIndex += 1
            child = item.child(childIndex)             
        
            #for c in element.getComponents():
            #    self._checkVisibility(element,show_empty_slots)
                    
    def _updateItem(self,item):    
        if item is not None:
            if item==self.root:
                item.setText(2,self._getRootID())                
            else:
                element = self.device.getComponentByAddress(item.text(0))
                if element is not None:               
                    item.setText(1,self._getElementStatus(element))
                    item.setText(2,self._getElementID(element))      
                    props = self._getElementProperties(element)
                    i=3
                    for p in props:
                        item.setText(i,p)
                        i=i+1
            childIndex = 0
            child = item.child(childIndex)
            while child is not None:
                self._updateItem(child)
                childIndex += 1
                child = item.child(childIndex)
    
    def _getChildItem(self, item, address):
        childIndex = 0
        child = item.child(childIndex)
        while child is not None:
            if child.text(0)==address:
                return True
            childIndex += 1
            child = item.child(childIndex)

    def _changedStructure(self,item):    
        if item is not None:
            if item==self.root:
                item.setText(2,self._getRootID())
            else:                
                element = self.device.getComponentByAddress(item.text(0))
                if element is None:
                    return True
                if not element.isLeaf():
                    for c in element.getComponents():
                        if self._getChildItem(item,c.getAddress()) is None:
                            return True 
            childIndex = 0
            child = item.child(childIndex)
            while child is not None:
                if self._changedStructure(child):
                    return True
                childIndex += 1
                child = item.child(childIndex)
            
    def _updateTable(self):
        if self.root is not None:                                                      
            self._updateItem(self.root)            
            self._checkVisibility(self.root,self.widget.ckShowEmptySlots.isChecked())

