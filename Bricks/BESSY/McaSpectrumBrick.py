#$Log: McaSpectrumBrick.py,v $
#Revision 1.3  2007/06/20 09:42:59  beteva
#changed Numeric to numpy & forceUpdate() to refreshWidgets()
#
#Revision 1.2  2007/06/06 09:13:32  beteva
#added more config parameters. Forced the display on energy.
#
#Revision 1.1  2007/06/04 14:58:27  beteva
#Initial revision
#
"""
[Name] McaSpectrumBrick

[Description]
The McaSpectrumBrick allows to display Mca Spectrum obtained in SPEC.
If configured, it will take into account the energy calibration factors and
the fit configuration file well as 

[Properties]

[Signals]

[Slots]
-------------------------------------------------------------
| name     | arguments | description
-------------------------------------------------------------
| setData  | data      | numeric array (x, y)
           | calib     | dictionary with the calibration factors (a,b,c)
           | config    | dictionary with the fit parameters



[HardwareObjects]

"""

__category__ = 'Spec'


import logging
from qt import *
from BlissFramework.BaseComponents import BlissWidget
#from BlissFramework import Icons
#import Icons
#print Icons.__file__
#from PyMca import McaAdvancedFit
import MXCuBEAdvancedFit
import numpy.oldnumeric as Numeric
from PyMca import ConfigDict

class McaSpectrumBrick(BlissWidget):
    def __init__(self, *args):
        BlissWidget.__init__(self, *args)

        self.defineSlot('setData',())

        self.addProperty("disableSpectrumFit", "boolean", False)
        self.disableSpectrumFit = False
        
        self.mcafit = MXCuBEAdvancedFit.MXCuBEAdvancedFit(self)
        #self.mcafit = McaAdvancedFit.McaAdvancedFit(self)
        self.mcafit.dismissButton.hide()
        QVBoxLayout(self)        
        self.layout().addWidget(self.mcafit)

    def propertyChanged(self, propertyName, oldValue, newValue):
        if propertyName == 'disableSpectrumFit':
            self.disableSpectrumFit = bool(newValue)

    def setData(self, data,calib,config):
        try:
            if config.has_key('file') and config["file"]:
                self._configure(config)
            else:
                self._configureDefault(config)

            x = Numeric.array(data[:,0]).astype(Numeric.Float)
            y = Numeric.array(data[:,1]).astype(Numeric.Float)
            xmin = float(config["min"])
            xmax = float(config["max"])
            self.mcafit.refreshWidgets()
            calib = Numeric.ravel(calib).tolist()
            kw = {}
            kw.update(config)
            kw['xmin'] = xmin
            kw['xmax'] = xmax
            kw['calibration'] = calib
            self.mcafit.setdata(x, y, **kw)# xmin=xmin, xmax=xmax, calibration=calib)
            self.mcafit._energyAxis = False
            self.mcafit.toggleEnergyAxis()
            result = self._fit()
            if not self.disableSpectrumFit:
                #pyarch file name and directory
                pf = config["legend"].split(".")
                pd = pf[0].split("/")
                outfile = pd[-1]
                outdir = config['htmldir']
                sourcename = config['legend']
                report = McaAdvancedFit.QtMcaAdvancedFitReport.QtMcaAdvancedFitReport(None, outfile=outfile, outdir=outdir,fitresult=result, sourcename=sourcename, plotdict={'logy':False}, table=2)

                text = report.getText()
                report.writeReport(text=text)
  
        except:
            logging.getLogger().exception('McaSpectrumBrick: problem fitting %s %s %s' % (str(data),str(calib),str(config)))
            raise

    def _fit(self):
        if self.disableSpectrumFit:
            #return self.mcafit.mxcubefit()
            #return self.mcafit.fit()
            return self.mcafit.plot()
        else:
            return self.mcafit.mxcubefit()
            #return self.mcafit.fit()

    def _configure(self,config):
        d = ConfigDict.ConfigDict()
        d.read(config["file"])

        if not d.has_key('concentrations'):
            d['concentrations']= {}
        if not d.has_key('attenuators'):
            d['attenuators']= {}
            d['attenuators']['Matrix'] = [1, 'Water', 1.0, 0.01, 45.0, 45.0]
        if config.has_key('flux'):
            d['concentrations']['flux'] = float(config['flux'])
        if config.has_key('time'):
            d['concentrations']['time'] = float(config['time'])
        self.mcafit.mcafit.configure(d)
        
    def _configureDefault(self,config):
        d = ConfigDict.ConfigDict()

        d['fit'] = {}
        d['fit']['energy'] = config["energy"]
        d["fit"]["fitfunction"] = 0;
        d["fit"]["hypermetflag"] = 1;
        d["fit"]["continuum"] = 0;
        d["fit"]["escapeflag"] = 1;
        d["fit"]["sumflag"] = 0;
        d["fit"]["maxiter"] = 10;
        d["fit"]["stripflag"] = 0;
        d["fit"]["xmin"] = config["min"]
        d["fit"]["xmax"] = config["max"]
        d["fit"]["use_limit"] = 0;
        d["fit"]["deltachi"] = 0.001;
        d["peaks"] = {}

        self.mcafit.mcafit.configure(d)
        
