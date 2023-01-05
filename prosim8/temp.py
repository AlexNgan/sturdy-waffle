#!/usr/bin/env python3
import re


class TEMP(object):
    defaults = {
        'Temperature'      : 98.6,
        'Unit'             : 'F'
    }

    def __init__(self, obj=None, device=None):
        self.device=device

        if obj is None:
            obj = TEMP.defaults.copy()

        for item in ['Temperature', 'Unit']:
            if item in obj:
                exec('self.%s = \'%s\''%(item, obj[item]))
        self.Temperature = float(self.Temperature)

    def convertTemp(self, Temp=None, Unit=None):
        if Temp is None:
            Temp = self.Temperature

        if Unit is None:
            Unit = self.Unit

        if re.search(r'^t', Unit, re.I):
            Temp = (Temp * 1.8) + 32.00
        if re.search(r'^c', Unit, re.I):
            Temp = (Temp - 32.00) / 1.8

        Temp = round(Temp * 2) / 2
        self.Temp = Temp
        return self.Temp

    def setTemp(self, Temp=None, Unit=None):
        if Temp is None:
            Temp = self.Temperature

        if Unit is None:
            Unit = self.Unit

        if not re.search(r'^c', Unit, re.I):
            Temp = self.convertTemp(Temp=Temp, Unit='c')

        return self.device.send('TEMP=%s'%(Temp))


# temp = TEMP({'Temp':86, 'Unit':'C'})
# temp = TEMP({'Temp':30, 'Unit':'C'})

# temp = TEMP({'Temp':107})
# temp = TEMP({'Temp':42, 'Unit':'C'})
# temp.setTemp()
