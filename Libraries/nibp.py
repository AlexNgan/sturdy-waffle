#!/usr/bin/env python3

import re

'''
Class that describes NIBP commands, actions and class variables
'''

class NIBP(object):
    defaults = {
        'patient_type': 'Pediatric',
        'nibp_systolic': 120,
        'nibp_diastolic': 80,
        'nibp_heart_rate': 72,
        'nibp_pressure': 150,
        'nibp_volume': 1.00,
        'nibp_shift': 1,
        'nibp_nibpleak_target': 150,
        'nibp_nibpleak_time': 150,
        'nibp_pop_target': 150,
        'nibp_pst_pressure': 150,
        'nibp_stgo_pos': 10,
        'nibp_nibptp_pressure': 100,
        'stfind_pressure': 0
    }

    '''
        self.device = Serial Connection to ProSim8
        self.values = Contains any data to set/push to the ProSim8 for NIBP
        self.pulse_function = Pulse Function to use (NSRA:Adult|NSRP:Pediatric)
    '''

    def __init__(self, obj=None, device=None, lkstat=None, popstat=None):
        self.device = device
        self.values = NIBP.defaults.copy()
        self.pulse_function = 'NSRP'

        self.lkstat = lkstat
        self.popstat = popstat

        if obj is not None:
            for item in obj:
                self.values[item] = obj[item]

        # # Set Patient Type Adult/Pediatric
        self.set_patient_type(self.pulse_function)

    ########################################################
    #   Class Variables
    ########################################################

    '''
        Type: Class Variable
        This determines which pulse function to use NSRA (Adult) or NSRP (Pediatric)
        value: Adult|Pediatric    
    '''

    def set_patient_type(self, value):
        if value == 'Adult':
            self.pulse_function = 'NSRA'
        else:
            self.pulse_function = 'NSRP'

    '''
        Type: Class Variable
        Method to set the class variable systolic for use on the ProSim8
        Value: int
    '''

    def set_systolic(self, sys):
        self.values['nibp_systolic'] = sys

    '''
        Type: Class Variable
        Method to set the class variable diastolic for use on the ProSim8
        value: int 
    '''

    def set_diastolic(self, dia):
        self.values['nibp_diastolic'] = dia

    '''
        Type: Class Variable
        Method to set the class variable target for use on the ProSim8
        value: int 
    '''

    def set_target(self, target):
        self.values['nibp_nibpleak_target'] = target

    '''
        Type: Class Variable
        Method to set the class variable time for use on the ProSim8
        value: int 
    '''

    def set_time(self, time):
        self.values['nibp_nibpleak_time'] = time

    '''
        Type: Class Variable
        Method to set the class variable heart_rate for use on the ProSim8
        value: int 
    '''

    def set_heart_rate(self, hr):
        self.values['nibp_heart_rate'] = hr

    '''
        Type: Class Variable
        Method to set the class variable volume for use on the ProSim8
        value: int 
    '''

    def set_vol(self, vol):
        self.values['nibp_volume'] = vol

    '''
        Type: Class Variable
        Method to set the class variable nibpes for use on the ProSim8
        value: int 
    '''

    def set_nibpes(self, shift):
        self.values['nibp_shift'] = shift

    '''
        Type: Class Variable
        Method to set the class variable nibppop for use on the ProSim8
        value: int 
    '''

    def set_nibppop(self, pop_target):
        self.values['nibp_pop_target'] = pop_target

    '''
        Type: Class Variable
        Method to set the class variable pst for use on the ProSim8
        value: int 
    '''

    def set_pst(self, pst):
        self.values['nibp_pst_pressure'] = pst

    '''
            Type: Class Variable
            Method to set the class variable stgo for use on the ProSim8
            value: int 
    '''

    def set_stgo(self, stg):
        self.values['nibp_stgo_pos'] = stg


    '''
        Get methods for NIBP
    '''
    def get_lkstat(self):
       return self.lkstat()

    def get_popstat(self):
        return self.popstat()

    ########################################################
    #    Actions
    ########################################################

    '''
        Type: Action
        Method to turn the nibp module on the ProSim8 on
    '''

    def turn_on_nibp(self):
        return self.nibprun(on=True)

    '''
        Type: Action
        Method to turn the nibp module on the ProSim8 Off
    '''

    def turn_off_nibp(self):
        return self.nibprun(on=False)

    '''
        Type: Action
        Method to turn the lkoff module on the ProSim8 Off
    '''

    def turn_off_leak(self):
        return self.lkoff(off=True)

    '''
        Type: Action
        Method to turn the lkoff module on the ProSim8 Off
    '''

    def turn_off_pressure_relief(self):
        return self.popoff(off=True)

    '''
        Type: Action
        Method to turn the ps module on the ProSim8 on
    '''

    def turn_on_ps(self):
        return self.ps(on=True)

    '''
        Type: Action
        Method to turn the ps module on the ProSim8 off
    '''

    def turn_off_ps(self):
        return self.ps(on=False)

    '''
        Type: Action
        Action method to cause ProSim8 to use the NIBPP command to set the systolic and diastolic 
        Base on the class variables  
    '''

    def set_nibp_reading(self):
        return self.nibpp()

    '''
        Type: Action
        Action method to cause ProSim8 to use the NIBPLEAK command to set the target and time 
        Base on the class variables  
    '''

    def set_nibpleak_reading(self):
        return self.nibpleak()

    '''
        Type: Action
        Action method to cause ProSim8 to use the NIBPV command to set nibpv value
        Base on the class variables  
    '''

    def set_nibp_volume_reading(self):
        return self.nibpv()

    '''
        Type: Action
        Action method to cause ProSim8 to use the NIBPV command to set nibpv value
        Base on the class variables  
    '''

    def set_nibptp_pressure_reading(self):
        return self.nibptp()

    '''
        Type: Action
        Method to Zero NIBP Module
    '''

    def zero_nibp_reading(self):
        return self.zpress()

    '''
        Type: Action
        Method to clear pressure Zero factor NIBP Module
    '''

    def clear_pressure_zero_factor_reading(self):
        return self.czpress()

    '''
        Type: Action
        Method to ask for Zpressure Zero factor NIBP Module
    '''

    def get_pressure_factor_reading(self):
        return self.uzpress()

    '''
        Type: Action
        Method to ask for LKSTAT NIBP Module
    '''

    def get_lkstat_reading(self):
        return self.lkstat()

    '''
        Type: Action
        Method to ask for POPSTAT NIBP Module
    '''

    def get_popstat_reading(self):
        return self.popstat()

    '''
        Type: Action
        Action method to cause ProSim8 to use the NIBPES command
    '''

    def set_nibpes_reading(self):
        return self.nibpes()

    '''
        Type: Action
        Action method to cause ProSim8 to use the NIBPPOP command 
    '''

    def set_nibppop_reading(self):
        return self.nibppop()

    '''
        Type: Action
        Action method to cause ProSim8 to use the NIBPPOP command 
    '''

    def set_pst_reading(self):
        return self.pst()

    ''' 
        Type: Action
        Action method to cause ProSim8 to use the STFIND command 
    '''

    def set_stfind_reading(self):
        return self.stfind()

    ''' 
       Type: Action
       Action method to cause ProSim8 to use the STHOME command 
    '''

    def set_sthome_reading(self):
        return self.sthome()

    ''' 
       Type: Action
       Action method to cause ProSim8 to use the STGO command 
    '''

    def set_stgo_reading(self):
        return self.stgo()

    ########################################################
    #    Commands
    ########################################################

    '''
        Type: Command
        Method to set turn on the pressure source
    '''

    def ps(self, on=True):
        on = bool(on)
        return self.device.send('PS=%s' % on)

    '''
        Type: Command
        Method to set the target for pressure source
    '''

    def pst(self):
        pressure = self.values['nibp_pst_pressure']
        if int(pressure) < 100:
            pressure = '0%s' % pressure

        pressure = str(pressure)
        return self.device.send('PST=%s' % pressure)

    '''
        Type: Command
        Method to turn off LKOFF module
    '''

    def popoff(self, off=True):
        off = bool(off)
        return self.device.send('POPOFF=%s' % off)

    '''
        Type: Command
        method to send NIBPPOP command
    '''

    def nibppop(self):
        target = self.values['nibp_pressure']
        target = str(target)
        return self.device.send('NIBPPOP=%s' % target)

    '''
        Type: Command
        method to send NIBPLEAK command
    '''

    def nibpleak(self):
        target = self.values['nibp_target']
        time = self.values['nibp_time']
        if int(target) < 100:
            target = '0%s' % target

        if int(time) < 10:
            time = '00%s' % time
        elif int(time) < 100:
            time = '0%s' % time

        target = str(target)
        time = str(time)
        return self.device.send('NIBPLEAK=%s,%s' % (target, time))

    '''
        Type: Command
        Method to turn off LKOFF module
    '''

    def lkoff(self, off=True):
        off = bool(off)
        return self.device.send('LKOFF=%s' % off)

    '''
        Type: Command
        Method to send NIBPP command
    '''

    def nibpes(self):
        shift = self.values['nibp_shift']
        if 0 < int(shift) < 10:
            shift = '+0%s' % shift

        if -10 < int(shift) < 0:
            regex = r'-'
            re_shift = re.sub(regex, '-0', str(shift))
            shift = '%s' % re_shift

        shift = str(shift)
        return self.device.send('NIBPES=%s' % shift)

    '''
        Type: Command
        Method to send NIBPTP command
    '''

    def nibptp(self):
        pressure = self.values['nibp_nibptp_pressure']

        if int(pressure) < 10:
            pressure = '00%s' % pressure
        elif int(pressure) < 100:
            pressure = '0%s' % pressure

        pressure = str(pressure)
        return self.device.send('NIBPTP=%s' % pressure)

    '''
        Type: Command
        Method to zero NIBP module on ProSim8
    '''

    def zpress(self):
        return self.device.send('ZPRESS')

    '''
        Type: Command
        Method to clear the pressure zero factor NIBP module on ProSim8
    '''

    def czpress(self):
        return self.device.send('CZPRESS')

    '''
       Type: Command
       Method to clear the pressure zero factor NIBP module on ProSim8
    '''

    def uzpress(self):
        return self.device.send('UZPRESS')

    '''
        Type: Command
        Method to turn on/off NIBP module
    '''

    def nibprun(self, on=True):
        on = bool(on)
        return self.device.send('NIBPRUN=%s' % on)

    '''
        Type: Command
        Method to send NIBPVP command
    '''

    def nibpv(self):
        volume = self.values['nibp_volume']

        if len(str(volume)) <= 3:
            volume = '%s0' % volume

        volume = str(volume)
        return self.device.send('NIBPV=%s' % volume)

    '''
        Type: Command
        Method to send NIBPP command
    '''

    def nibpp(self):
        systolic = self.values['nibp_systolic']
        diastolic = self.values['nibp_diastolic']
        if int(systolic) < 10:
            systolic = '00%s' % systolic
        elif int(systolic) < 100:
            systolic = '0%s' % systolic

        if int(diastolic) < 10:
            diastolic = '00%s' % diastolic
        elif int(diastolic) < 100:
            diastolic = '0%s' % diastolic

        systolic = str(systolic)
        diastolic = str(diastolic)
        return self.device.send('NIBPP=%s,%s' % (systolic, diastolic))

    ''' TODO: Need to massage more
        Type: COMMAND
        Method to get LKSTAT
    '''

    def lkstat(self):
        return self.device.send('LKSTAT')

    ''' TODO: Need to massage more
        Type: COMMAND
        Method to get POPSTAT
    '''

    def popstat(self):
        return self.device.send('POPSTAT')

    '''
        Type: COMMAND
        Method to set the motor position to close end position
    '''

    def stfind(self):
        position = self.values['stfind_pressure']
        position = str(position)
        return self.device.send('STFIND=%s' % position)

    '''
       Type: COMMAND
       Method to set the stepper motor to home position
    '''

    def sthome(self, home='0'):
        return self.device.send('STHOME=%s' % home)

    '''
        Type: COMMAND
        Method to move the stepper motor
    '''

    def stgo(self):
        position = self.values['nibp_stgo_pos']
        if 0 < int(position) < 10:
            position = '+00%s' % position
        elif 11 < int(position) < 100:
            position = '+0%s' % position

        regex = r'-'
        if -10 < int(position) < 0:
            re_pos = re.sub(regex,'-00', str(position))
            position = '%s' % re_pos
        elif -99 < int(position) < -11:
            re_pos = re.sub(regex, '-0', str(position))
            position = '%s' % re_pos

        position = str(position)
        return self.device.send('STGO=%s' % position)

    '''
        Type: COMMAND
        Method to set the motor position to close end position
    '''

    def stclose(self, position='105'):
        plus = '+'
        position = str(plus + position)
        return self.device.send('STFIND=%s' % position)

    '''
        Type: COMMAND
        Method to set the heart rate reading
    '''

    def heart_rate(self):
        hr = self.values['nibp_heart_rate']

        if int(hr) < 10:
            hr = '00%s' % hr
        elif int(hr) < 100:
            hr = '0%s' % hr

        return self.device.send('%s=%s' % (self.pulse_function, hr))

    '''
        Ask for the Pressure measurement: PRESS
    '''

    def get_press(self):
        return self.device.send('PRESS')

    '''
        Ask for the Pressure measurement: PRESSX
    '''

    def get_pressx(self):
        return self.device.send('PRESSX')

# Sample Usage
# nibp = NIBP()
# nibp.set_systolic('120')
# nibp.set_diastolic('80')
# nibp.set_nibp_reading()
