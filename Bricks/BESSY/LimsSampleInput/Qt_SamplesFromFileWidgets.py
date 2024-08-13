#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__  = "Thomas Hauss"
__email__ = "hauss@helmholtz-berlin.de"
__date__ = "2023-05-24 21:00 CEST"
__version__ = "0.8"

"""
Description: read a csv or Excel xlsl file with sample information.
Will put samples as list of classes into the IPSyB pipeline.

This file uses SamplesFromFile_hwobj.py

"""

try:
    from PyQt5 import QtWidgets
    from PyQt5 import QtCore
    qt = 5
except ImportError:
    from PyQt4 import QtGui as QtWidgets
    from PyQt4 import QtCore
    qt = 4

import os
import SamplesFromFile_hwobj

class FileBrowser(QtWidgets.QWidget):
    def __init__(self,parent):
        QtWidgets.QWidget.__init__(self,parent=parent)
        self.parent = parent

    def getOpenFilesAndDirs(self, caption='', directory='', 
                            filter=filter, initialFilter='', options=None):
#                            filter=("*.csv"), initialFilter='', options=None):
#                            filter=("*.csv  *.xlsx"), initialFilter='', options=None):
        """https://stackoverflow.com/questions/64336575/select-a-file-or-a-folder-in-qfiledialog-pyqt5"""
        def update_text():
            # update the contents of the line edit widget with the selected files
            selected = []
            for index in view.selectionModel().selectedRows():
                selected.append('"{}"'.format(index.data()))
            lineEdit.setText(' '.join(selected))


        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(dialog.ExistingFiles)
        if options:
            dialog.setOptions(options)
        dialog.setOption(dialog.DontUseNativeDialog, True)
        if directory:
            dialog.setDirectory(directory)
        if filter:
            dialog.setNameFilter(filter)
            if initialFilter:
                dialog.selectNameFilter(initialFilter)

        # by default, if a directory is opened in file listing mode, 
        # QFileDialog.accept() shows the contents of that directory, but we 
        # need to be able to "open" directories as we can do with files, so we 
        # just override accept() with the default QDialog implementation which 
        # will just return exec_()
        dialog.accept = lambda: QtWidgets.QDialog.accept(dialog)

        # there are many item views in a non-native dialog, but the ones displaying 
        # the actual contents are created inside a QStackedWidget; they are a 
        # QTreeView and a QListView, and the tree is only used when the 
        # viewMode is set to QFileDialog.Details, which is not this case
        stackedWidget = dialog.findChild(QtWidgets.QStackedWidget)
        view = stackedWidget.findChild(QtWidgets.QListView)
        view.selectionModel().selectionChanged.connect(update_text)

        lineEdit = dialog.findChild(QtWidgets.QLineEdit)
        # clear the line edit contents whenever the current directory changes
        dialog.directoryEntered.connect(lambda: lineEdit.setText(''))

        if dialog.exec_():
            sample_file = str(dialog.selectedFiles()[0])
            self.parent.read_file(sample_file)
        else:
            pass
#            parent.sample_file = ""



class SortWindow(QtWidgets.QDialog):
    """ put the puck into the selected position"""
    open_file_signal = QtCore.pyqtSignal()
    
    def __init__(self, parent = None):
        QtWidgets.QDialog.__init__(self,parent)

        self.open_file_signal.connect(self.show_file_browser)

        self.max_pucks = SamplesFromFile_hwobj.MAX_PUCKS
        self.dewar_pucks = SamplesFromFile_hwobj.DEWAR_PUCKS
        self.read = SamplesFromFile_hwobj.ReadSamples(self)
   
        self.sample_file = ""
        
        self.puckname, self.number_of_pucks = self.read.sort_pucks("")
        self.sort_list = self.set_sort_list(self.puckname)            
        self.temp_list = self.sort_list.copy()
        self.setupUI()
        self.recover = False
        self.recover_file = os.path.expanduser("~/mxcubesortlist")
        if os.path.exists(self.recover_file):
            self.sample_file, sort_list, samples_list = self.read_recover_file(self.recover_file)
#            self.recover = True
#            with open(self.recover_file, "r") as input_file:
#                self.sample_file = input_file.readline().strip()
#                self.recover_sort_list = eval(input_file.readline())
            self.recover_previous(self.sample_file, sort_list)
        
    def setupUI(self):
        self.buttonBox = QtWidgets.QDialogButtonBox(
                               QtWidgets.QDialogButtonBox.Ok
                             | QtWidgets.QDialogButtonBox.Cancel)

        fileButton = self.buttonBox.addButton('Open File', QtWidgets.QDialogButtonBox.ActionRole)
        fileButton.clicked.connect(self.open_file_signal.emit)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.cancel)
        self.puck = []
        for i in range(self.max_pucks):
            self.puck.append(QtWidgets.QLineEdit())
            self.puck[i].setReadOnly(True)
            self.puck[i].setText("")
        # List items to select puck position
        self.combobox = []
        for i in range(self.max_pucks):
            self.combobox_item = QtWidgets.QComboBox()
            self.combobox_item.setObjectName("Combobox_" + str(i))
            self.combobox_item.activated.connect(lambda position, i=i: self.position_changed(position, i))

            for j in range(self.dewar_pucks + 1): 
                self.combobox_item.addItem(str(j))

            self.combobox.append(self.combobox_item) 
            pucki = self.temp_list[i]
            self.combobox[i].setCurrentIndex(pucki[self.puckname[i]])
            self.combobox[i].setEnabled(False)
        # Layout of selection window
        dewar_name = SamplesFromFile_hwobj.dewar_name
        self.layoutFrame = []
        self.columnLayout = []
        max_columns = 3
        self.mainLayout = QtWidgets.QGridLayout()
        self.mainLayout.addWidget(QtWidgets.QLabel(dewar_name + " dewar positions"), 0, 0)
        self.mainLayout.addWidget(self.buttonBox, self.max_pucks + 2, 0)
        self.mainLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint(QtWidgets.QLayout.SetFixedSize))
        for i in range(max_columns):
            self.columnLayout.append(QtWidgets.QGridLayout())
            self.columnLayout[i].addWidget(QtWidgets.QLabel("Puck #"), 1, 0)
            self.columnLayout[i].addWidget(QtWidgets.QLabel("Puck Name"), 1, 1)
            self.columnLayout[i].addWidget(QtWidgets.QLabel("Position"), 1, 2)
            column_min = i * 10
            column_max = column_min + 10
            for j in range(column_min, column_max):
                self.label = QtWidgets.QLabel()
                self.label.setText(str(j+1))
                self.label.setAlignment(QtCore.Qt.AlignRight)
                self.columnLayout[i].addWidget(self.label, j+2, 0) 
                self.columnLayout[i].addWidget(self.puck[j], j+2, 1)
                self.columnLayout[i].addWidget(self.combobox[j], 2+j, 2)
            self.layoutFrame.append(QtWidgets.QFrame())
            self.layoutFrame[i].setLayout(self.columnLayout[i])
            self.mainLayout.addWidget(self.layoutFrame[i], 1, i)
        self.layoutFrame[0].show()
        self.layoutFrame[1].hide()
        self.layoutFrame[2].hide()
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)

        self.setLayout(self.mainLayout)

    def updateUI(self):
        max_columns = self.number_of_pucks/10.0
        if max_columns > 0:
            self.layoutFrame[1].hide()
            self.layoutFrame[2].hide()
        if max_columns > 1.0:
            self.layoutFrame[1].show()
            self.layoutFrame[2].hide()
        if max_columns > 2.0:
            self.layoutFrame[1].show()
            self.layoutFrame[2].show()

        for i in range(self.max_pucks):
            self.puck[i].setText("")
            self.combobox[i].setEnabled(False)
        for i in range(self.number_of_pucks):
            self.puck[i].setText(self.puckname[i])
            self.combobox[i].setEnabled(True)
            
        if self.number_of_pucks > 0:
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)
                    
    def select_and_sort(self):
        """Entry from MXCube"""
        return_code = self.exec_()
        if return_code == 0:
            print("cancel")
            if os.path.exists(self.recover_file):
                sample_file, sort_list, samples_list = self.read_recover_file(self.recover_file)
#            self.recover = True
#                with open(self.recover_file, "r") as input_file:
#                    self.sample_file = input_file.readline().strip()
#                    self.recover_sort_list = eval(input_file.readline())

                return samples_list
            else:
                return [SamplesFromFile_hwobj.LimsSample()]
        if return_code == 1:
            sort_list = self.get_list()
            samples_list = self.read.resort_puck_position(self.samples,sort_list)
            self.write_recover_file(self.sample_file, sort_list, samples_list)
            return samples_list  # Samples returned to MXCube
        else:
            return [SamplesFromFile_hwobj.LimsSample()]

    def write_recover_file(self, sample_file, sort_list, samples_list):
        import pickle
        with open(self.recover_file, "wb") as outfile:
            pickle.dump([sample_file, sort_list, samples_list], outfile)

    def read_recover_file(self, recover_file):
        import pickle
        with open(recover_file, "rb") as input_file:
            sample_file, sort_list, samples_list = pickle.load(input_file)
        return sample_file, sort_list, samples_list
        
    def show_file_browser(self):
        file_browser = FileBrowser(self)
        filter = "*.csv"       
        if SamplesFromFile_hwobj.xlsx:
            filter = "*.csv *.xlsx"       

        file_browser.getOpenFilesAndDirs(self, filter=filter)

    def pucknames(self, unipuck):
        puckname = []
        number_of_pucks = 0
        for i in range(self.max_pucks):
            try:
                puckname.append(unipuck[i+1][1][1])
                number_of_pucks += 1
            except KeyError:
                puckname.append("")
        return puckname, number_of_pucks
        
    def set_sort_list(self,puckname):
        sort_list = {}
        for i in range(self.max_pucks):
            puck = {}
            puck.setdefault(puckname[i], 0)
            sort_list.setdefault(i,puck)
        return sort_list

    def read_file(self, sample_file):
        self.sample_file = sample_file
        self.csv_worksheet = self.read.read_samples(sample_file)        
        self.puckname, self.number_of_pucks = self.read.sort_pucks(self.csv_worksheet)
        self.samples = self.read.csv_worksheet_to_samples(self.csv_worksheet)
        self.temp_list = self.set_sort_list(self.puckname)            
        for i in range(self.max_pucks):
            self.combobox[i].setCurrentIndex(0)
        self.updateUI()       

    def recover_previous(self, sample_file,sort_list):
        self.sample_file = sample_file
        self.csv_worksheet = self.read.read_samples(sample_file)        
        self.puckname, self.number_of_pucks = self.read.sort_pucks(self.csv_worksheet)
        self.samples = self.read.csv_worksheet_to_samples(self.csv_worksheet)
        self.temp_list = sort_list
        for i in range(self.max_pucks):
            self.combobox[i].setCurrentIndex(0)
        for i in range(self.number_of_pucks):
            value = sort_list[i][self.puckname[i]]
            self.combobox[i].setCurrentIndex(value)            
        self.updateUI()       

    def get_list(self):
        return self.final_list

    def accept(self):
        self.final_list = self.temp_list.copy()
        self.done(1)
    def cancel(self):
        self.final_list = self.sort_list
        self.done(0)
                    
    def show_message(self,text):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setText("Error: position "+ str(text) + " already used. \n Set to position 0.")
        msgBox.setWindowTitle("Information")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        retVal = msgBox.exec_()

    def position_changed(self, position, ii):
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)
        pucki = self.temp_list[ii]
         
        pucki[self.puckname[ii]] = int(position)
        i = 0
        for key, value in self.temp_list.items():
            if key == ii or value[self.puckname[i]] == 0:
                i += 1
                continue
            else:
                if value[self.puckname[i]] == int(position):
                    self.show_message(position)
                    self.combobox[ii].setCurrentIndex(0)
                    pucki[self.puckname[ii]] = 0
                i += 1 
