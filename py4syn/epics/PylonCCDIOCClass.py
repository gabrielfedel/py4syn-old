"""PyLoN Charge-Coupled Devices (CCD) for IOC Class

Python Class for EPICS IOC  control of Princeton Instruments
PyLoN camera.

:platform: Unix
:synopsis: Python Class for EPICS IOC  control of Princeton Instruments
PyLoN camera.

.. moduleauthor:: Gabriel de Souza Fedel <gabriel.fedel@lnls.br>
    .. note:: //2018 [gabriel.fedel]  first version released
"""

from epics import PV, ca
from py4syn.epics.StandardDevice import StandardDevice
from py4syn.epics.ICountable import ICountable

class PylonCCDIOC(StandardDevice, ICountable):
    """
    Python class to help control of Charge-Coupled Devices
    (CCD) via EPICS IOC.
    """
    # PyLoN CCD constructor 
    def __init__(self, pvName, mnemonic):
        StandardDevice.__init__(self, mnemonic)

        self._done = True

        self.pvAcquire = PV(pvName + ":Acquire")
        self.pvDone = PV(pvName + ":Done", callback = self.onDoneChange)

# not implemented yet
#        self.pvStop = PV(pvName + ":Stop")
#        self.pvFileName = PV(pvName + ":FileName")

    def getValue(self, **kwargs):
        # there is no value. Values came from spe files generated
        # by LightField
        return 0

    def setCountTime(self, t):
        # The count time must be setted by LightField
        pass

    def setPresetValue(self, channel, val):
        # The PresetValue must be setted by LightField
        pass

    def startCount(self):
        self._done = False
        self.pvAcquire.put(1, wait=True)

    def stopCount(self):
        # Not implemented yet
        pass

    def canMonitor(self):
        return True

    def canStopCount(self):
        return False

    def isCounting(self):
        return (not self._done and self._startAcquire)

    def waitFinishAcquiring(self):
        while(not self._done):
            ca.poll(0.001)

    def wait(self):
        self.waitFinishAcquiring()

    def onDoneChange(self, value, **kw):
        self._done = (value == 1)
