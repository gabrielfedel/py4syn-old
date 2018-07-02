from py4syn.epics.StandardDevice import StandardDevice
from py4syn.epics.ICountable import ICountable
from time import sleep

from epics import PV

MAXIMAGES = 1000

class ExperimentControlSAXS(StandardDevice, ICountable):
    def __init__(self, pvName, mnemonic):
        self.pvStart = PV(pvName + ':Start')
        self.pvStop = PV(pvName + ':Stop')
        self.pvTriggerFrom = PV(pvName + ':TriggerFrom')
        self.pvDelayBefore = PV(pvName + ':DelayBefore')
        self.pvNumberOfPoints = PV(pvName + ':NumberOfPoints')
        self.pvStatus = PV(pvName + ':Status')
        self.pvAutoSamplerStatus = PV(pvName + ':AutoSamplerStatus')
        self.pvLastPointRead = PV(pvName + ':LastPointRead')
        self.pvLastConfigError = PV(pvName + ':LastConfigError')
        self.pvLastOperationError = PV(pvName + ':LastOperationError')
        self.pvDiode1Data = PV(pvName + ':Diode1Data')
        self.pvDiode2Data = PV(pvName + ':Diode2Data')
        self.pvDarkCurrent1V = PV(pvName + ':DarkCurrent1Volts')
        self.pvDarkCurrent2V = PV(pvName + ':DarkCurrent2Volts')
        self.pvDarkCurrent1 = PV(pvName + ':DarkCurrent1')
        self.pvDarkCurrent2 = PV(pvName + ':DarkCurrent2')
        self.pvDiode1DataMinusDark = PV(pvName + ':Diode1DataMinusDark')
        self.pvDiode2DataMinusDark = PV(pvName + ':Diode2DataMinusDark')
        self.pvCloseShutter = PV(pvName + ':FastShutter')
        self.pvCrioImageTime = PV(pvName + ':CrioImageTime')
        self.pvIgnoreShutter = PV(pvName + ':IgnoreShutter')
        self.pvDelayAfter = PV(pvName + ':DelayAfter')


    def getValue(self, **kwargs):
        return None

    def setCountTime(self, t):
        pass

    def startCount(self, wait = True):
        if not self.isCounting:
            self.pvStart.put(1, wait = wait)
        else:
            raise ValueError("Experiment Control is already counting")

    def stopCount(self, wait = True):
        if self.isRunning:
            self.pvStop.put(1, wait = wait)
        else:
            raise ValueError("Experiment Control is already stopped")

    def canMonitor(self):
        return False

    def canStopCount(self):
        return True

    def isCounting(self):
        self.pvStatus.get()

    def wait(self):
        pass


    def prepareAcquire(self, nimg, nfd, delaybefore=0, delayafter=0, crioimagetime=0.1):
        if nimg < 1 or nimg > MAXIMAGES:
            raise ValueError("Number of images is invalid")

        # TODO: is it necessary to save this values?
        self.nimg = nimg
        self.nfd = nfd
        self.delaybefore = delaybefore
        self.delayafter = delayafter
        # in ms
        self.crioimagetime = crioimagetime*1000

        self.pvDelayBefore.put(self.delaybefore)
        self.pvDelayAfter.put(self.delayafter)
        self.pvCrioImageTime.put(self.crioimagetime)
        self.pvNumberOfPoints.put(self.nimg)

#### importado


        self.errorConfig = self.pvLastConfigError.get()
        self.errorOp = self.pvLastOperationError.get()
        self.diode1 =  self.pvDiode1Data.get()
        self.diode2 =  self.pvDiode2Data.get()
        self.darkcurrent1v = self.pvDarkCurrent1V.get()
        self.darkcurrent2v = self.pvDarkCurrent2V.get()
        self.darkcurrent1 = self.pvDarkCurrent1.get()
        self.darkcurrent2 = self.pvDarkCurrent2.get()
        self.diode1dataminusdark = self.pvDiode1DataMinusDark.get()
        self.diode2dataminusdark = self.pvDiode2DataMinusDark.get()
        self.lastRead = 0
        self.pvDiode1Data.add_callback(self.getDiode1Data)
        self.pvDiode2Data.add_callback(self.getDiode2Data)
        self.pvLastPointRead.add_callback(self.lastPointRead)
        self.pvStatus.add_callback(self.statusChange)
        self.pvLastConfigError.add_callback(self.lastConfigError)
        self.pvLastOperationError.add_callback(self.lastOperationError)  
        self.pvDiode1Data.add_callback(self.getDiode1Data)  
        self.pvDiode2Data.add_callback(self.getDiode2Data)
        self.pvDarkCurrent1V.add_callback(self.getDarkCurrent1Volts)
        self.pvDarkCurrent2V.add_callback(self.getDarkCurrent2Volts)
        self.pvDarkCurrent1.add_callback(self.getDarkCurrent1)
        self.pvDarkCurrent2.add_callback(self.getDarkCurrent2)
        self.pvDiode1DataMinusDark.add_callback(self.getDiode1DataMinusDark)
        self.pvDiode2DataMinusDark.add_callback(self.getDiode2DataMinusDark)
        #self.I0Atual = 0
        #self.ITAtual = 0

       
        #self.pvDiodeInShow.add_callback(self.diodeInShowChange)
        #self.diodeInShow = 1

        
    def statusChange(self, pvname = None, value = None, char_value = None, **kw):
        self.isRunning = value




    # Função para callback da PV auxiliar
    #def diodeInShowChange(self, pvname = None, value = None, **kw):
    #    #print('inShow'+str(value))
    #    self.diodeInShow = value

    # Funcao para corrigir erro de leitura de um record do tipo vetor pelo pyepics
    # var: tamanho do vetor; value: valor do vetor              
    def fixData(self,var, value):
        if var == 0: return []
        if var > 0: 
            if var == 1: return [value]                
            if var > 1: return value               

    def getDiode1DataMinusDark(self, pvname = None, value = None, char_value = None, count = None, **kw):
        self.diode1dataminusdark = self.fixData(count,value)

    def getDiode2DataMinusDark(self, pvname = None, value = None, char_value = None, count = None, **kw):
        self.diode2dataminusdark = self.fixData(count,value)
    
    def lastPointRead(self, pvname = None, value = None, char_value = None, count = None, **kw):
        self.lastRead = int(value)

    def getDiode1Data(self, pvname = None, value = None, char_value = None, count = None, **kw):
        self.diode1 = self.fixData(count,value)

    def getDiode2Data(self, pvname = None, value = None, char_value = None, count = None, **kw):
        self.diode2 = self.fixData(count,value)
  
    def lastConfigError(self, pvname = None, value = None, char_value = None, **kw):
        self.errorConfig = value
        try:
            if self.errorConfig != "No Error":
                raise Exception

        except Exception:
            print('Config error:'+self.errorConfig)

    
    def lastOperationError(self, pvname = None, value = None, char_value = None, **kw):
        self.errorOp = value
        try:
            if self.errorOp != "No Error":
                raise Exception

        except Exception:
            print('Operation error:'+self.errorOp)
    
