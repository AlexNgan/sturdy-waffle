import re

from prosim8.misc.ibp_wave_enum import IBPWAVE


class IBP(object):
    defaults = {
        'ibps_chan'   : 1,
        'ibps_pres'   : 200,
        'ibpw_chan'   : 1,
        'ibpw_wave'   : 'ART',
        'ibpp_chan'   : 1,
        'ibpp_sys'    : 120,
        'ibpp_diast'  : 80,
        'ibpartp_chan': 1,
        'ibpartp_art' : 5,
        'ibpartm_chan': 1,
        'ibpartm_art' : 5,
        'ibpsns_chan' : 1,
        'ibpsns_sens' : 5
    }

    def __init__(self, obj=None, device=None):
        self.device = device
        self.values = IBP.defaults.copy()

        if obj is not None:
            for item in obj:
                self.values[item] = obj[item]

        self.set_ibp_dynamic_pressure(1, 120, 80, IBPWAVE.ARTERIAL.value)

    ########################################################
    #   Class Variables
    ########################################################

    '''
        Type: Class Variable
        Set an IBP channel to a static pressure.
        value: ibp channel 1 or 2 
    '''

    def set_ibps_chan(self, channel):
        self.values['ibps_chan'] = channel

    '''
        Type: Class Variable
        Set an IBP channel to a static pressure.
        value: ibp pressure - 3 digits: -010 to + 300  
    '''

    def set_ibps_pres(self, pressure):
        self.values['ibps_pres'] = pressure

    '''
        Type: Class Variable
        Set an IBP channel to a dynamic wave.        
        value: ibpw channel 1 or 2 
    '''

    def set_ibpw_chan(self, channel):
        self.values['ibpw_chan'] = channel

    '''
        Type: Class Variable
        Set an IBP channel to a dynamic wave.        
        value: ibp wave:  ART, RART, LV, LA, RV, PA, PAW, RA   
    '''

    def set_ibpw_wave(self, wave):
        self.values['ibpw_wave'] = wave

    '''
        Type: Class Variable
        Set an IBP channel to a dynamic pressure.        
        value: ibpp channel:  1 or 2   
    '''

    def set_ibpp_chan(self, channel):
        self.values['ibpp_chan'] = channel

    '''
        Type: Class Variable
        Set an IBP channel to a dynamic pressure.        
        value: ibpp syst:  000 to 300
    '''

    def set_ibpp_syst(self, syst):
        self.values['ibpp_sys'] = syst

    '''
        Type: Class Variable
        Set an IBP channel to a dynamic pressure.        
        value: ibpp_diast:  000 to 300
    '''

    def set_ibpp_diast(self, diast):
        self.values['ibpp_diast'] = diast

    '''
        Type: Class Variable
        Set an IBP channel’s artifact by percent. Valid for Arterial, Radial Artery and Left Ventricle.        
        value: ibpartp_chan: 1 or 2
    '''

    def set_ibpartp_chan(self, channel):
        self.values['ibpartp_chan'] = channel

    '''
        Type: Class Variable
        Set an IBP channel’s artifact by percent. Valid for Arterial, Radial Artery and Left Ventricle.        
        value: ibpartp_art: 0, 5, 10
    '''

    def set_ibpartp_art(self, artifact):
        self.values['ibpartp_art'] = artifact

    '''
        Type: Class Variable
        Set an IBP channel’s artifact by mmHg. Valid for Left Atrium, Right Ventricle, Pulmonary Artery, PA Wedge, Right Atrium (CVP).
        value: ibpartm_chan: 1 or 2
    '''

    def set_ibpartm_chan(self, channel):
        self.values['ibpartp_chan'] = channel

    '''
        Type: Class Variable
        Set an IBP channel’s artifact by mmHg. Valid for Left Atrium, Right Ventricle, Pulmonary Artery, PA Wedge, Right Atrium (CVP).
        value: ibpartm_art: 0, 5, 10
    '''

    def set_ibpartm_art(self, artifact):
        self.values['ibpartp_art'] = artifact

    '''
        Type: Class Variable
        Set an IBP channel’s artifact by percent. Valid for Arterial, Radial Artery and Left Ventricle.        
        value: ibpsns_chan: 1 or 2
    '''

    def set_ibpsns_chan(self, channel):
        self.values['ibpsns_chan'] = channel

    '''
        Type: Class Variable
        Set an IBP channel’s artifact by percent. Valid for Arterial, Radial Artery and Left Ventricle.        
        value: 40 or 5
    '''

    def set_ibpsns_sens(self, sensitivity):
        self.values['ibpsns_sens'] = sensitivity


    ########################################################
    #   Commands
    ########################################################

    '''
        Type: Command
        Method to set the static pressure
    '''

    def ibps(self):
        ibps_chan = self.values['ibps_chan']
        ibps_pres = self.values['ibps_pres']

        regex = r'-'
        if -10 < int(ibps_pres) < 0:
            re_pos = re.sub(regex, '-00', str(ibps_pres))
            ibps_pres = '%s' % re_pos

        if 0 < int(ibps_pres) < 10:
            ibps_pres = '+00%s' % ibps_pres
        elif 11 < int(ibps_pres) < 100:
            ibps_pres = '+0%s' % ibps_pres

        ibps_chan = str(ibps_chan)
        ibps_pres = str(ibps_pres)
        return self.device.send('IBPS=%s,%s' % (ibps_chan, ibps_pres))

    '''
        Type: Command
        Method to set the dynamic wave
    '''

    def ibpw(self):
        ibpw_chan = self.values['ibpw_chan']
        ibpw_wave = self.values['ibpw_wave']
        if ibpw_chan == 1:
            ibpw_chan = ibpw_chan
        else:
            ibpw_chan = ibpw_chan

        if ibpw_wave == 'ARTERIAL':
            ibpw_wave = str(IBPWAVE.ARTERIAL)
        elif ibpw_wave == 'RADIAL_ARTERY':
            ibpw_wave = str(IBPWAVE.RADIAL_ARTERY)
        elif ibpw_wave == 'LEFT_VENTRICLE':
            ibpw_wave = str(IBPWAVE.LEFT_VENTRICLE)
        elif ibpw_wave == 'LEFT_ATRIUM':
            ibpw_wave = str(IBPWAVE.LEFT_ATRIUM)
        elif ibpw_wave == 'RIGHT_VENTRICLE':
            ibpw_wave = str(IBPWAVE.RIGHT_VENTRICLE)
        elif ibpw_wave == 'PULMONARY_ARTERY':
            ibpw_wave = str(IBPWAVE.PULMONARY_ARTERY)
        elif ibpw_wave == 'PA_WEDGE':
            ibpw_wave = str(IBPWAVE.PA_WEDGE)
        elif ibpw_wave == 'RIGHT_ATRIUM':
            ibpw_wave = str(IBPWAVE.RIGHT_ATRIUM)

        ibpw_chan = str(ibpw_chan)
        ibpw_wave = str(ibpw_wave)
        return self.device.send('IBPW=%s,%s' % (ibpw_chan, ibpw_wave))

    '''
        Type: Command
        Method to set the dynamic pressure
    '''

    def ibpp(self):
        ibpp_chan = self.values['ibpp_chan']
        ibpp_syst = self.values['ibpp_sys']
        ibpp_diast = self.values['ibpp_diast']

        if ibpp_chan == 1:
            ibpp_chan = ibpp_chan
        else:
            ibpp_chan = ibpp_chan

        if int(ibpp_syst) < 10:
            ibpp_syst = '00%s' % ibpp_syst
        elif int(ibpp_syst) < 100:
            ibpp_syst = '0%s' % ibpp_syst

        if int(ibpp_diast) < 10:
            ibpp_diast = '00%s' % ibpp_diast
        elif int(ibpp_diast) < 100:
            ibpp_diast = '0%s' % ibpp_diast

        ibpp_chan = str(ibpp_chan)
        ibpp_syst = str(ibpp_syst)
        ibpp_diast = str(ibpp_diast)
        return self.device.send('IBPP=%s,%s,%s' % (ibpp_chan, ibpp_syst, ibpp_diast))

    '''
        Type: Command
        Method to set channel’s artifact by percent
    '''

    def ibpartp(self):
        ibpartp_chan = self.values['ibpartp_chan']
        ibpartp_art = self.values['ibpartp_art']

        if ibpartp_chan == 1:
            ibpartp_chan = ibpartp_chan
        else:
            ibpartp_chan = ibpartp_chan

        if ibpartp_art == 0:
            ibpartp_art = ibpartp_art
        elif ibpartp_art == 5:
            ibpartp_art = ibpartp_art
        elif ibpartp_art == 10:
            ibpartp_art = ibpartp_art

        ibpartp_chan = str(ibpartp_chan)
        ibpartp_art = str(ibpartp_art)
        return self.device.send('IBPARTP=%s,%s' % (ibpartp_chan, ibpartp_art))

    '''
        Type: Command
        Method to set channel’s artifact by mmHg
    '''

    def ibpartm(self):
        ibpartm_chan = self.values['ibpartm_chan']
        ibpartm_art = self.values['ibpartm_art']

        if ibpartm_chan == 1:
            ibpartm_chan = ibpartm_chan
        else:
            ibpartm_chan = ibpartm_chan

        if ibpartm_art == 0:
            ibpartm_art = ibpartm_art
        elif ibpartm_art == 5:
            ibpartm_art = ibpartm_art
        elif ibpartm_art == 10:
            ibpartm_art = ibpartm_art

        ibpartm_chan = str(ibpartm_chan)
        ibpartm_art = str(ibpartm_art)
        return self.device.send('IBPARTM=%s,%s' % (ibpartm_chan, ibpartm_art))

    '''
        Type: Command
        Method to set circuit sensitivity in μV/V/mmHg.
    '''

    def ibpsns(self):
        ibpsns_chan = self.values['ibpsns_chan']
        ibpsns_sens = self.values['ibpsns_sens']

        if ibpsns_chan == 1:
            ibpsns_chan = ibpsns_chan
        else:
            ibpsns_chan = ibpsns_chan

        if ibpsns_sens == 40:
            ibpsns_sens = ibpsns_sens
        else:
            ibpsns_sens = ibpsns_sens

        ibpsns_chan = str(ibpsns_chan)
        ibpsns_sens = str(ibpsns_sens)
        return self.device.send('IBPSNS=%s,%s' % (ibpsns_chan, ibpsns_sens))


    ########################################################
    #   Actions
    ########################################################

    '''
        Type: Action
        Method to set the ibps for the PROSIM8
    '''

    def set_ibps_reading(self):
        return self.ibps()

    '''
        Type: Action
        Method to set the ibpw for the PROSIM8
    '''

    def set_ibpw_reading(self):
        return self.ibpw()

    '''
        Type: Action
        Method to set the ibpp for the PROSIM8
    '''

    def set_ibpp_reading(self):
        return self.ibpp()

    '''
        Type: Action
        Method to set the ibpartp for the PROSIM8
    '''

    def set_ibpartp_reading(self):
        return self.ibpartp()

    '''
        Type: Action
        Method to set the ibpartm for the PROSIM8
    '''

    def set_ibpartm_reading(self):
        return self.ibpartm()

    '''
        Type: Action
        Method to set the ibpsns for the PROSIM8
    '''

    def set_ibpsns_reading(self):
        return self.ibpsns()


    ########################################################
    #   Model
    ########################################################
    '''
    Model for sending ibp reading
    channel: 1 or 2
    sys: Systolic Pressure
    dia: Diastolic Pressure
    '''
    def set_ibp_dynamic_pressure(self, channel, sys, dia, wave):
        self.set_ibpp_chan(channel)
        self.set_ibpp_syst(sys)
        self.set_ibpp_diast(dia)
        self.set_ibpw_wave(wave)
        self.ibpp()