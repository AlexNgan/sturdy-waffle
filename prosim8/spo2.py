'''
SPO2 Commands, Actions and Class Variables
'''
import re

import numpy as np

from .misc.spo2_enum import AMBF, SPO2TYPE

#These default values are what the patient is at the start of the protocol.
class SPO2(object):
    defaults = {
        'saturation': 88,
        'perfusion': '10.0',
        'ppm': 100.00,
        'ambs': 2.0,
        'ambf': 4,
        'size': 5,
        'type': 'MASIM',
        'index': 10,
        'qur_index': 10,
        'ratio': 20000,
        'test': 10
    }

    def __init__(self, obj=None, device=None, qspo2type=2,
                 qurcurves=4, qurcurve=4, rcurveload=4,
                 spo2ident=None, qstat=None, spo2slftst=None,
                 spo2sngltst=None):
        self.device = device
        self.values = SPO2.defaults.copy()

        self.qspo2type = qspo2type
        self.qurcurves = qurcurves
        self.qurcurve = qurcurve
        self.rcurveload = rcurveload
        self.spo2ident = spo2ident
        self.qstat = qstat
        self.spo2slftst = spo2slftst
        self.spo2sngltst = spo2sngltst

        if obj is not None:
            for item in obj:
                self.values[item] = obj[item]


    ########################################################
    #   Class Variables
    ########################################################

    '''
        Type: Class Variable
        Sets SpO2 saturation percentage.
        Value: 000 to 100.
    '''
    def set_spo2_sat(self, saturation):
        self.values['saturation'] = saturation

    '''
        Type: Class Variable
        Sets SpO2 perfusion, the pulse amplitude in percent.
        Value: 00.01 to 20.00 [by 0.01].
    '''

    def set_spo2_perf(self, perfusion):
        self.values['perfusion'] = perfusion

    '''
        Type: Class Variable
        Sets SpO2 transmission in PPM.
        Value: 000.01 to 300.00 [by 0.01].
    '''

    def set_spo2_trans(self, ppm):
        self.values['ppm'] = ppm

    '''
        Type: Class Variable
        Sets SpO2 ambient size, the relative amplitude of ambient light.
        Value: 0.0 to 4.0 [by 0.1].
    '''

    def set_spo2_ambs(self, size):
        self.values['ambs'] = size

    '''
        Type: Class Variable
        Sets SpO2 ambient frequency
        Value: DC 50Hz 60Hz 1KHz 2KHz 3KHz 4KHz 5KHz 6KHz 7KHz 
               8KHz 9KHz 10KHz
    '''

    def set_spo2_ambf(self, size):
        self.values['ambf'] = size

    '''
        Type: Class Variable
        Sets SpO2 respiration size.
        Value: 0 to 5. (%)
    '''

    def set_spo2_resps(self, size):
        self.values['size'] = size

    '''
        Type: Class Variable
        Sets SpO2 Type (R-Curve) to a built-in type.
        Value: NELCR MASIM MASIMR NONIN OHMED PHIL NIHON MINDR BCI
    '''

    def set_spo2_spo2type(self, type):
        self.values['type'] = type

    '''
        Type: Class Variable
        Sets SpO2 Type (R-Curve) to a user loaded type.
        Value: 00 to 19
    '''

    def set_spo2_spo2utype(self, index):
        self.values['index'] = index

    '''
        Type: Class Variable
        Queries the name of a user loaded R-Curve.
        Value: 00 to 20
    '''

    def set_spo2_qurcurve(self, index):
        self.values['qur_index'] = index

    '''
        Type: Class Variable
        Sets SpO2 ratio directly instead of having it set based on saturation percentage and R-Curve. 
        This is a diagnostic not normally used for a simulation.
        Value: 00000 to 65535.
    '''

    def set_spo2_ratio(self, ratio):
        self.values['ratio'] = ratio

    '''
        Type: Class Variable
        Runs SpO2 a single self test. Includes a 10 second delay to 
        allow the test to finish before re-enabling communication
        Value: unsigned test number
    '''

    def set_spo2_spo2sngltst_test(self, test):
        self.values['test'] = test

    '''
    The following are getters for the SPO2 methods
    '''

    def get_spo2type(self):
        return self.qspo2type

    def get_qurcurves(self):
        return self.qurcurves

    def get_qurcuve(self):
        return self.qurcurve

    def get_rcurveload(self):
        return self.rcurveload

    def get_qstat(self):
        return self.qstat

    def get_spo2slftst(self):
        return self.spo2slftst

    def get_spo2sngltst(self):
        return self.spo2sngltst

    ########################################################
    #   Commands
    ########################################################

    '''
       Type: Command
       Method to set saturation percentage
    '''
    def sat(self):
        sat = self.values['saturation']

        if sat < 10:
            sat = '00%s' % sat
        elif sat < 100:
            sat = '0%s' % sat
        else:
            sat = sat

        sat = str(sat)
        return self.device.send('SAT=%s' % sat)

    '''
        Type: Command
        Method to set pulse amplitude in percent
    '''
    def perf(self):
        perf = self.values['perfusion']

        if len(str(perf)) <= 4:
            perf = '%s0' % perf
        else:
            perf = perf

        perf = str(perf)
        return self.device.send('PERF=%s' % perf)

    '''
        Type: Command
        Method to set transmission in PPM
    '''
    def trans(self):
        trans = self.values['ppm']

        dot = r'.'
        if re.search(dot, str(trans)):
            if len(str(trans)) <= 3:
                trans =  '0%s0' % trans
                trans = '0%s' % trans
            if len(str(trans)) <= 4:
                trans = '0%s0' % trans
            if len(str(trans)) <= 5:
                trans = '%s0' % trans
        else:
            trans = trans

        trans = str(trans)
        return self.device.send('TRANS=%s' % trans)

    '''
        Type: Command
        Methods to the ambient mode
    '''
    def ambm(self, on='ON'):
        on = str(on)
        return self.device.send('AMBM=%s' % on)

    '''
        Type: Command
        Methods to the ambient size, indicated by relative amplitude
    '''
    def ambs(self):
        size = self.values['ambs']

        if len(str(size)) <= 2:
            size = '%s.0' % size

        size = str(size)
        return self.device.send('AMBS=%s' % size)

    '''
        Type: Command
        Methods to set the ambient frequency
    '''
    def ambf(self):
        size = self.values['ambf']

        if size == 'DC':
            size = AMBF.DC
        elif size == 'FIFTY':
            size = AMBF.FIFTY
        elif size == 'SIXTY':
            size = AMBF.SIXTY
        elif size == 'ONE':
            size = AMBF.ONE
        elif size == 'TWO':
            size = AMBF.TWO
        elif size == 'THREE':
            size = AMBF.THREE
        elif size == 'FOUR':
            size = AMBF.FOUR
        elif size == 'FIVE':
            size = AMBF.FIVE
        elif size == 'SIX':
            size = AMBF.SIX
        elif size == 'SEVEN':
            size = AMBF.SEVEN
        elif size == 'EIGHT':
            size = AMBF.EIGHT
        elif size == 'NINE':
            size = AMBF.NINE
        elif size == 'TEN':
            size = AMBF.TEN

        size = str(size)
        return self.device.send('AMBF=%s' % size)

    '''
        Type: Command
        Methods to set the respiration mode
    '''
    def respm(self, on='ON'):
        on = bool(on)
        return self.device.send('RESPM=%s' % on)

    '''
        Type: Command
        Methods to set the respiration size
    '''
    def resps(self):
        size = self.values['size']

        size_range = range(0, 5, 1)
        if size in size_range:
            size = size

        size = str(size)
        return self.device.send('RESPS=%s' % size)

    '''
        Type: Command
        Methods to set the type
    '''

    def spo2type(self):
        type = self.values['type']

        if type == 'NELCR':
            type = SPO2TYPE.NELCR
        elif type == 'MASIM':
            type = SPO2TYPE.MASIM
        elif type == 'MASIMR':
            type = SPO2TYPE.MASIMR
        elif type == 'NONIN':
            type = SPO2TYPE.NONIN
        elif type == 'OHMED':
            type = SPO2TYPE.OHMED
        elif type == 'PHIL':
            type = SPO2TYPE.PHIL
        elif type == 'NIHON':
            type = SPO2TYPE.NIHON
        elif type == 'MINDR':
            type = SPO2TYPE.MINDR
        elif type == 'BCI':
            type = SPO2TYPE.BCI

        type = str(type)
        return self.device.send('SPO2TYPE=%s' % type)

    '''
        Type: Command
        Method to set the type (R-Curve)
    '''

    def spo2utype(self):
        index = self.values['index']

        if index < 10:
            index = '0%s' % index

        index = str(index)
        return self.device.send('SPO2UTYPE=%s' % index)

    '''
        Type: Command
        Method to automatically adjust SpO2 in relation to FiO2 change
    '''
    def FiO2_adjust(self,fio2):
        oxygen = int(85 + (100-85)/(100-21)*(fio2-21)) #Where minSpO2 and maxSpO2 is the range of SpO2s you want to simulate and FIO2 is in %.
        #self.spo2.set_spo2_sat(oxygen) 
        return oxygen
            
        
    '''
        Type: Command
        Method to query the name of the user loaded
    '''
    def send_qurcurve(self):
        index = self.values['qur_index']

        if index < 10:
            index = '0%s' % index

        index = str(index)
        return self.device.send('QURCURVE=%s' % index)


    '''
        Type: Command
        Deletes all user loaded R-Curves.
    '''
    def rcurvedelall(self):
        return self.device.send('RCURVEDELALL')


    '''
        Type: Command
        Queries the currently selected SpO2 Type
    '''
    def qspo2type(self):
        return self.device.send('QSPO2TYPE')

    '''
        Type: Command
        Queries the number of user R-Curves loaded
    '''
    def qurcurves(self):
        return self.device.send('QURCURVES')

    '''
        Type: Command
        Queries the number of user R-Curves loaded
    '''
    def qurcurve(self):
        return self.device.send('QURCURVE')

    '''
        Type: Command
        Queries the number of user R-Curves loaded
    '''
    def spo2ident(self):
        return self.device.send('SPO2IDENT')

    '''
        Type: Command
        SpO2 status information.
    '''
    def qstat(self):
        return self.device.send('QSTAT')

    '''
        Type: Command
        set the saturation percentage and R-curve
    '''
    def ratio(self):
        ratio = self.values['ratio']

        if ratio < 10:
            ratio = '0000%s' % ratio
        elif ratio < 100:
            ratio = '000%s' % ratio
        elif ratio < 1000:
            ratio = '00%s' % ratio
        elif ratio < 10000:
            ratio = '0%s' % ratio

        ratio = str(ratio)
        return self.device.send('RATIO=%s' % ratio)

    '''
        Type: Command
        Run the self test for Sp02
    '''
    def spo2slftst(self):
        return self.device.send('SPO2SLFTST')

    '''
        Type: Command
        Run the self test for Sp02
    '''

    def send_spo2sngltst(self, on='ON'):
        test = self.values['test']
        on = str(on)

        test = str(test)
        return self.device.send('SPO2SNGLTST=%s,%s' % (test, on))

    '''
        Type: Command
        Run the single self test for Sp02
    '''

    def spo2sngltst(self):
        return self.device.send('SPO2SNGLTST')

    ########################################################
    #   Actions
    ########################################################

    '''
        Type: Action
        Send the Saturation to the PROSIM8
    '''

    def set_sat_reading(self):
        self.sat()

    '''
        Type: Action
        Send the perfusion to the PROSIM8
    '''

    def set_perf_reading(self):
        self.perf()

    '''
        Type: Action
        Send the transmission to the PROSIM8
    '''

    def set_trans_reading(self):
        self.trans()

    '''
        Type: Action
        Send the Ambient mode command to the PROSIM8
    '''

    def set_ambs_reading(self):
        self.ambs()

    '''
        Type: Action
        Send the ambient size command to the PROSIM8
    '''

    def set_ambf_reading(self):
        self.ambf()

    '''
        Type: Action
        Send the respiration size command to the PROSIM8
    '''

    def set_resps_reading(self):
        self.resps()

    '''
        Type: Action
        Send the respiration mode command to the PROSIM8
    '''

    def set_respm_reading(self):
        self.respm()

    '''
        Type: Action
        Send the SPO2 type (built-in) command to the PROSIM8
    '''

    def set_spo2type_reading(self):
        self.spo2type()

    '''
        Type: Action
        Send the SPO2 type (user loaded) command to the PROSIM8
    '''

    def set_spo2utype_reading(self):
        self.spo2utype()

    '''
        Type: Action
        Send the user loaded R-curve command to the PROSIM8
    '''

    def set_qurcurve_reading(self):
        self.send_qurcurve()

    '''
        Type: Action
        Send the ratio command to the PROSIM8
    '''

    def set_ratio_reading(self):
        self.ratio()

    '''
        Type: Action
        Send the single self test command to the PROSIM8
    '''

    def set_spo2sngltst_reading(self):
        self.send_spo2sngltst()

    '''
        Type: Action
        Turn on and off ambient mode
    '''

    def turn_ambm_on(self):
        self.ambm(on='ON')

    def turn_ambm_off(self):
        self.ambm(on='OFF')

    '''
        Type: Action
        Turn on and off respiration mode
    '''

    def turn_respm_on(self):
        self.respm(on='ON')

    def turn_respm_off(self):
        self.respm(on='OFF')

    '''
            Type: Action
            Turn on and off test repeats
    '''

    def turn_spo2sngltst_on(self):
        self.send_spo2sngltst(on=True)

    def turn_spo2sngltst_off(self):
        self.send_spo2sngltst(on=False)

