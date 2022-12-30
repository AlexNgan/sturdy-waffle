#!/usr/bin/env python3
from prosim8.connection import Connection
from prosim8.ecg import ECG
from prosim8.ibp import IBP
from prosim8.nibp import NIBP
from prosim8.spo2 import SPO2
from prosim8.temp import TEMP


class PROSIM(object):

    def __init__(self, com_port='COM4', debug=False):
        #   self.device = Connection(device_id='/dev/ttyUSB0', timeout=1.0, write_timeout=1.0)
        #   self.device = Connection(device_id='/dev/ttyS3', timeout=1.0, write_timeout=1.0)
        self.device = Connection(device_id=com_port, timeout=1.0, write_timeout=1.0, debug=debug)
        self.device.send('QMODE')
        self.device.send('QUI')
        self.device.send('REMOTE')

        self.temp = TEMP(device=self.device)
        self.ecg = ECG(device=self.device)
        self.ibp = IBP(device=self.device)
        self.nibp = NIBP(device=self.device)
        self.spo2 = SPO2(device=self.device)
