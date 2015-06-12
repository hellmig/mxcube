import qt
import sys
import time
import gevent
from PyMca import McaAdvancedFit
import logging

class MXCuBEAdvancedFit(McaAdvancedFit.McaAdvancedFit):

    def mxcubefit(self):

        self.mcatable.setRowCount(0)

        if self.concentrationsWidget is not None:
            self.concentrationsWidget.concentrationsTable.setRowCount(0)

        fitconfig = {}
        fitconfig.update(self.mcafit.configure())

        if fitconfig['peaks'] == {}:
            msg = qt.QMessageBox(self)
            msg.setIcon(qt.QMessageBox.Information)
            msg.setText("No peaks defined.\nPlease configure peaks")
            msg.show()
            return

        self.mxcubefit_start()

        self.fitmsg_dialog = qt.QDialog(self)
        self.fitmsg_dialog.setModal(0)
        #self.fitmsg_dialog.setWindowTitle("Please Wait")
        layout = qt.QHBoxLayout(self.fitmsg_dialog)
        self.fitmsg_l1 = qt.QLabel(self.fitmsg_dialog)
        layout.addWidget(self.fitmsg_l1)
        self.fitmsg_l1.setFixedWidth(self.fitmsg_l1.fontMetrics().width('##'))
        self.fitmsg_l2 = qt.QLabel(self.fitmsg_dialog)
        layout.addWidget(self.fitmsg_l2)
        #self.fitmsg_l2.setText("%s" % message)
        self.fitmsg_l2.setText("Calculating fit")
        self.fitmsg_l3 = qt.QLabel(self.fitmsg_dialog)
        layout.addWidget(self.fitmsg_l3)
        self.fitmsg_l3.setFixedWidth(self.fitmsg_l3.fontMetrics().width('##'))
        self.fitmsg_dialog.show()

    def mxcubefit_start(self):

        # start a timer to update gevent       

        # self.mxcube_timer.start()
        self.mxcubefit_timer = qt.QTimer(self)
        self.mxcubefit_timer.start(100)
        qt.QObject.connect(self.mxcubefit_timer,qt.SIGNAL("timeout()"), self.mxcubefit_loop)
          

        self.mxcubefit_started = time.time()
        self.mcafit.estimate()
        gevent.spawn( self.mxcubefit_task )
        self.mxcubefit_done = False
        self.mxcubefit_exception = None
        
    def mxcubefit_loop(self):
        gevent.wait(timeout=0.1)
        logging.info("updating fit task")

        if self.mxcubefit_done:
           self.mxcubefit_wrapup()
        else:
           self.elapsed = time.time() - self.mxcubefit_started
           self.tick = int(self.elapsed/10.0)
           ticks = ['-','\\', "|", "/","-","\\",'|','/']
           i = (self.tick+1) % 8
           self.fitmsg_l1.setText(ticks[i])
           self.fitmsg_l3.setText(" "+ticks[i])
        
    def mxcubefit_task(self):

        try:
            #self.mxcubefit_result = self.mcafit.startfit({'digest':1},"Calculating Fit")
            logging.info( str(self.mcafit.xdata))
            logging.info( str(self.mcafit.ydata))
            logging.info( "max y value to fit is %s" % self.mcafit.ydata.max())
            self.mxcubefit_result = self.mcafit.startfit(digest=1)
        except:
            import traceback
            self.mxcubefit_exception = traceback.format_exc()
            self.mxcubefit_result = ("Exception",self.mxcubefit_exception)
            logging.info("We got an exception" + traceback.format_exc())
        self.mxcubefit_done = True

    def mxcubefit_wrapup(self):
        logging.info("wraping up  mxcube fit")
        # self.mxcube_timer.stop()

        self.mxcubefit_timer.stop()
        self.fitmsg_dialog.close()

        if self.mxcubefit_exception is not None:
            print "  - mcafit exception occurs"
            time.sleep(0.5)
            self.errmsg_dialog = qt.QMessageBox(self)
            self.errmsg_dialog.setIcon(qt.QMessageBox.Critical)
            self.errmsg_dialog.setText("Error on fit:" + self.mxcubefit_exception)
            self.errmsg_dialog.show()
            #fitresult = None
            #result = None
            return None


        threadResult = self.mxcubefit_result

        try:
            if type(threadResult) == type((1,)):
               if len(threadResult):
                   if threadResult[0] == "Exception":
                      raise Exception(threadResult[1], threadResult[2])

            fitresult = threadResult[0]
            result = threadResult[1]
        except:
            print "  - mcafit exception occurs"
            self.errmsg_dialog = qt.QMessageBox(self)
            self.errmsg_dialog.setIcon(qt.QMessageBox.Critical)
            self.errmsg_dialog.setText("Error on fit:" + str(sys.exc_info()[1]))
            #self.errmsg_dialog.setDetailedText(traceback.format_exc())
            self.errmsg_dialog.show()
            fitresult = None
            result = None
            return None


        #logging.info("wraping up  mxcube fit 1")
        #try:
            #self.mcatable.fillfrommca(result)
        #except:
            #self.fitmsg_dialog = qt.QMessageBox(self)
            #self.fitmsg_dialog.setIcon(qt.QMessageBox.Critical)
            #self.fitmsg_dialog.setText("Error filling Table: %s" % (sys.exc_info()[1]))
            #self.fitmsg_dialog.show()
            #return

        logging.info("wraping up  mxcube fit 2")
        dict={}
        dict['event']     = "McaAdvancedFitFinished"
        #dict['fitresult'] = fitresult
        dict['result']    = result

        #I should make a copy but ...
        self.dict = {}
        self.dict['info'] = {}
        self.dict['info'] = self.info.copy()
        self.dict['result'] = dict['result']

        # add the matrix spectrum
        logging.info("wraping up  mxcube fit matrix")
        if self.matrixSpectrumButton.isChecked():
            self.matrixSpectrum()
        else:
            if "Matrix" in self.graph.curves.keys():
                self.graph.delcurve("Matrix")

        # clear the Monte Carlo spectra (if any)
        self._xrfmcMatrixSpectra = None

        logging.info("wraping up  mxcube fit peaks")
        # add the peaks spectrum
        if self.peaksSpectrumButton.isChecked():
            self.peaksSpectrum()
        else:
            self._clearPeaksSpectrum()
        logging.info("wraping up  mxcube fit plotting")
        self.plot()
        logging.info("wraping up  mxcube fit plot done")

        if self.concentrationsWidget is not None:
            if (str(self.mainTab.tabText(self.mainTab.currentIndex())).upper() == 'CONCENTRATIONS') or \
                (self.concentrationsWidget.parent() is None):
                if not self.concentrationsWidget.isHidden():
                     try:
                         self.concentrations()
                     except:
                         msg = qt.QMessageBox(self)
                         msg.setIcon(qt.QMessageBox.Critical)
                         msg.setText("Concentrations Error: %s" % (sys.exc_info()[1]))
                         msg.show()
                         return

        logging.info("wraping up  mxcube fit 3")
        if str(self.mainTab.tabText(self.mainTab.currentIndex())).upper() == 'DIAGNOSTICS':
            try:
                self.diagnostics()
            except:
                msg = qt.QMessageBox(self)
                msg.setIcon(qt.QMessageBox.Critical)
                msg.setText("Diagnostics Error: %s" % (sys.exc_info()[1]))
                msg.show()
                return
        logging.info("wraping up  mxcube fit 4")

        return self._anasignal(dict)

