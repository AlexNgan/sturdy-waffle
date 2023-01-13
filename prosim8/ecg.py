#!/usr/bin/env python3
import re

import numpy as np

from prosim8.misc.ecg_enum import ECGEART, ECGEARTLD, CHAMBER, GRANULARITY
from prosim8.misc.ecgwaves_enum import ECGSPVWAVE, ECGPREWAVE, ECGVNTWAVE, ECGCNDWAVE, ECGTVPWAVE, ECGACLSWAVE

from prosim8.misc.ecg_enum import ECGNSRAX


class ECG(object):
    defaults = {
        'Patient'   : 'Adult',
        'nsra_rate' : 100,
        'nsrp_rate': 100,
        'nsrax_axis': 'INT',
        'stdev': +.50,
        'ecgampl': 1.0,
        'artifact': 50,
        'size': 50,
        'lead': 'RA',
        'spvwave': 'AFL',
        'prewave': 'PAC',
        'vntwave': 'PVC6M',
        'cndwave': '1DB',
        'tvppol_chamber':'A',
        'polarity':'P',
        'tvpampl_chamber': 'A',
        'ampl': '20',
        'tvpwid_chamber':'A',
        'width': 1.0,
        'tvpwave': 'ATR',
        'aclswave': 'SBC',
        'afib_granularity': 'FINE',
        'afib2_granularity': 'FINE',
        'vfib_granularity': 'FINE',
        'vfib1_granularity': 'FINE',
        'vfib2_granularity': 'FINE',
        'monovtach_rate': 150,
        'polyvtach_rate': 3,
        'pulse_rate': 72,
        'square_freq': 2.0,
        'sine_freq': 5,
        'tri_freq': 2.0,
        'rdet_width': 100,
        'rdet_rate': 120,
        'qrs_width': 150,
        'qrs_rate': 120,
        'percent': 100
    }

    def __init__(self, obj=None, device=None):
        self.values = ECG.defaults.copy()
        self.device = device

        if obj is not None:
            for item in obj:
                self.values[item] = obj[item]

        # for item in ECG_Commands:
        #     if item['Command'] in obj:
        #         exec('self.%s = \'%s\''%(item['Command'], obj[item]))
        #     else:
        #         try:
        #             exec('temp = self.%s'%item)
        #         except Exception as e:
        #             exec('self.%s = item[\'Default\']'%item['Command'])

     #   self.setECG(100, ECGEART.SIXTY.value, ECGEARTLD.LL.value, 1)

    '''
    Model for ECG Commands
    rate: Normal Sinus Rate
    art: ECG Artifact
    lead: ECG Artifcact lead
    siWaveFreq: Sine Wave Frequency
    '''
    def setECG(self, rate, art, lead, siWaveFreq):
        self.turn_on_ecg()
        self.set_ecg_nsra(rate)
        self.set_ecg_eart(art)
        self.set_ecg_eartld(lead)
        self.set_ecg_sine(siWaveFreq)
        self.nsra()
        self.eart()
        self.eartld()
        self.sine()

    ########################################################
    #   Class Variables
    ########################################################

    '''
        Type: Class Variable
        Set Ecg wave to Normal Sinus Rhythm Adult, at a rate.
        value: 3 digits: 010 to 360.
    '''

    def set_ecg_nsra(self, rate):
        self.values['nsra_rate'] = rate

    '''
        Type: Class Variable
        Set Ecg wave to Normal Sinus Rhythm Pediatric, at a rate.
        value: 3 digits: 010 to 360.
    '''

    def set_ecg_nsrp(self, rate):
        self.values['nsrp_rate'] = rate

    '''
        Type: Class Variable
        Set Ecg axis for Normal Sinus Rhythm.
        value: INT, HOR, VER 
    '''

    def set_ecg_nsrax(self, axis):
        self.values['nsrax_axis'] = axis

    '''
        Type: Class Variable
        Set ST Deviation for Normal Sinus Rhythm, adult only.
        value: Signed 2 digits w/dp:
            ±0.00
            ±0.05
            ±0.10 to ±0.80 [by .10]
    '''

    def set_ecg_stdev(self, dev):
        self.values['stdev'] = dev


    '''
        Type: Class Variable
        Set Ecg amplitude.        
        value: 3 digits w/dp:
            0.05 to 0.45 [by 0.05]
            0.50 to 5.00 [by 0.25]
    '''

    def set_ecg_ecgampl(self, ampl):
        self.values['ecgampl'] = ampl

    '''
        Type: Class Variable
        Set Ecg artifact.        
        value: OFF 
               50  
               60  
               MSC 
               WAND
               RESP
    '''

    def set_ecg_eart(self, artifact):
        self.values['artifact'] = artifact

    '''
        Type: Class Variable
        Set Ecg artifact size in percent.
        value: 025, 050, 100
    '''

    def set_ecg_eartsz(self, size):
        self.values['size'] = size

    '''
        Type: Class Variable
        Set Ecg artifact lead.
        value: ALL, RA, LL, LA, V1, V2, V3, V4, V5, or V6.
    '''

    def set_ecg_eartld(self, lead):
        self.values['lead'] = lead

    '''
        Type: Class Variable
        Set Ecg wave to a Supraventricular arrhythmia.
        value: AFL  
               SNA  
               MB80 
               MB120
               ATC  
               PAT  
               NOD  
               SVT  
    '''

    def set_ecg_spvwave(self, wave):
        self.values['spvwave'] = wave

    '''
        Type: Class Variable
        Set Ecg wave to a Premature arrhythmia.
        value: PAC 
              PNC  
              PVC1 
              PVC1E
              PVC1R
              PVC2 
              PVC2E
              PVC2R PVC 2, Right, R on T
    '''

    def set_ecg_prewave(self, wave):
        self.values['prewave'] = wave

    '''
        Type: Class Variable
        Set Ecg wave to a Premature arrhythmia.
        value:PVC6M  
              PVC12M 
              PVC24M 
              FMF    
              TRIG   
              BIG    
              PAIR   
              RUN5   
              RUN11  
              ASYS   
    '''

    def set_ecg_vntwave(self, wave):
        self.values['vntwave'] = wave

    '''
        Type: Class Variable
        Set Ecg wave to a Conduction arrhythmia.       
        value:1DB 
              2DB1
              2DB2
              3DB 
              RBBB
              LBBB
    '''

    def set_ecg_cndwave(self, wave):
        self.values['cndwave'] = wave

    '''
        Type: Class Variable
        Set the Pacer pulse polarity for TV Paced waves.
        value: Chamber: A and V
    '''

    def set_ecg_tvppol_chamber(self, chamber):
        self.values['tvppol_chamber'] = chamber

    '''
        Type: Class Variable
        Set the Pacer pulse polarity for TV Paced waves.
        value: polarity: P and N
    '''

    def set_ecg_tvppol_polarity(self, polarity):
        self.values['polarity'] = polarity

    '''
        Type: Class Variable
        Set the Pacer pulse polarity for TV Paced waves.
        value: Chamber: A and V
    '''

    def set_ecg_tvpampl_chamber(self, chamber):
        self.values['tvpampl_chamber'] = chamber

    '''
        Type: Class Variable
        Set the Pacer pulse polarity for TV Paced waves.
        value: Ampl: 000, 002, 004, 006, 008, 010, 012, 014, 016, 018, 020, 050, 100, 200, 500, or 700.
    '''

    def set_ecg_tvpampl_ampl(self, ampl):
        self.values['ampl'] = ampl

    '''
        Type: Class Variable
        Set the Pacer pulse width for TV Paced waves.
        value: Chamber: A and V
    '''

    def set_ecg_tvpwid_chamber(self, chamber):
        self.values['tvpwid_chamber'] = chamber

    '''
        Type: Class Variable
        Set the Pacer pulse width for TV Paced waves.
        value: width: 0.1, 0.2, 0.5, 1.0, or 2.0.
    '''

    def set_ecg_tvpwid_width(self, width):
        self.values['width'] = width

    '''
        Type: Class Variable
        Set Ecg wave to a TV Paced arrhythmia.
        value: ATR 
               ASY 
               DFS 
               DOS 
               AVS 
               NCP 
               NFN 
    '''

    def set_ecg_tvpwave(self, wave):
        self.values['tvpwave'] = wave

    '''
        Type: Class Variable
        Set Ecg wave to an ACLS arrhythmia.
        value: SBC 
               PTU 
               MTU 
               NSI 
               NSV 
               WSI 
               WSV 
               TDP 
    '''

    def set_ecg_aclswave(self, wave):
        self.values['aclswave'] = wave

    '''
        Type: Class Variable
        Set Ecg wave to Atrial Fibrillation 1. This is the new afib with increased randomness.
        value: COARSE or FINE
    '''

    def set_ecg_afib(self, granularity):
        self.values['afib_granularity'] = granularity

    '''
        Type: Class Variable
        Set Ecg wave to Atrial Fibrillation 2. This is the original afib that is not as random as the new one.
        value: COARSE or FINE
    '''

    def set_ecg_afib2(self, granularity):
        self.values['afib2_granularity'] = granularity

    '''
        Type: Class Variable
        Set Ecg wave to Ventricular Fibrillation. This is the original vfib, same as VFIB1.
        value: COARSE or FINE
    '''

    def set_ecg_vfib(self, granularity):
        self.values['vfib_granularity'] = granularity

    '''
        Type: Class Variable
        Set Ecg wave to Ventricular Fibrillation. This is also the original vfib, same as VFIB.
        value: COARSE or FINE
    '''

    def set_ecg_vfib1(self, granularity):
        self.values['vfib1_granularity'] = granularity

    '''
        Type: Class Variable
        Set Ecg wave to Ventricular Fibrillation. This is the new vfib that is 50% faster.
        value: COARSE or FINE
    '''

    def set_ecg_vfib2(self, granularity):
        self.values['vfib2_granularity'] = granularity

    '''
        Type: Class Variable
        Set Ecg wave to Monophase Ventricular Tachycardia at rate.
        value: 3 digits: 120 to 300.
    '''

    def set_ecg_monovtach(self, rate):
        self.values['monovtach_rate'] = rate

    '''
        Type: Class Variable
        Set Ecg wave to Polyphasic Ventricular Tachycardia
        value: 1 digit: 1 to 5.
    '''

    def set_ecg_polyvtach(self, rate):
        self.values['polyvtach_rate'] = rate

    '''
        Type: Class Variable
        Set Ecg wave to Pulse
        value: 30, 60, or 80.
    '''

    def set_ecg_pulse(self, rate):
        self.values['pulse_rate'] = rate

    '''
        Type: Class Variable
        Set Ecg wave to Square
        value: 0.125, 2.0, or 2.5
    '''

    def set_ecg_square(self, freq):
        self.values['square_freq'] = freq

    '''
        Type: Class Variable
        Set Ecg wave to Sine.
        value: 0.05, 0.5, 1, 2, 5, 10, 25, 30, 40, 50, 60, 100, or 150.
    '''

    def set_ecg_sine(self, freq):
        self.values['sine_freq'] = freq

    '''
        Type: Class Variable
        Set Ecg wave to Triangle.
        value: 0.125, 2.0, or 2.5.
    '''

    def set_ecg_tri(self, freq):
        self.values['tri_freq'] = freq

    '''
        Type: Class Variable
        Set Ecg wave to R Wave Detection at width and rate.
        value: 3 digits: 008 to 200.
    '''

    def set_ecg_rdet_width(self, width):
        self.values['rdet_width'] = width

    '''
        Type: Class Variable
        Set Ecg wave to R Wave Detection at width and rate.
        value: 30, 60, 80, 120, 200, or 250.
    '''

    def set_ecg_rdet_rate(self, rate):
        self.values['rdet_rate'] = rate

    '''
        Type: Class Variable
        Set Ecg wave to QRS Detection at width and rate.
        value: 3 digits: 008 to 200.
    '''

    def set_ecg_qrs_width(self, width):
        self.values['qrs_width'] = width

    '''
       Type: Class Variable
       Set Ecg wave to QRS Detection at width and rate.
       value: 3 digits: 30, 60, 80, 120, 200, or 250.
    '''

    def set_ecg_qrs_rate(self, rate):
        self.values['qrs_rate'] = rate

    '''
        Type: Class Variable
        Set Ecg wave to Tall T Rejection.
        value: 3 digits: 000 to 150 [by 010].
    '''


    def set_ecg_tallt(self, percent):
        self.values['percent'] = percent

    ########################################################
    #   Commands
    #######################################################

    '''
        Type: Command
        Method to set turn on the ecg wave
    '''

    def ecgrun(self, on=True):
        on = bool(on)
        return self.device.send('ECGRUN=%s' % on)

    '''
        Type: Command
        Method to set turn on the ecg wave to normal sinus rhythm
    '''

    def nsra(self):
        rate = self.values['nsra_rate']

        if rate < 10:
            rate = '00%s' % rate
        elif rate < 100:
            rate = '0%s' % rate

        rate = str(rate)
        return self.device.send('NSRA=%s' % rate)

    '''
        Type: Command
        Method to set turn on the ecg wave to normal sinus rhythm: pediatric
    '''

    def nsrp(self):
        rate = self.values['nsrp_rate']

        if rate < 10:
            rate = '00%s' % rate
        elif rate < 100:
            rate = '0%s' % rate

        rate = str(rate)
        return self.device.send('NSRP=%s' % rate)

    '''
       Type: Command
       Method to set ecg axis to normal sinus rhythm
    '''

    def nsrax(self):
        nsrax = self.values['nsrax_axis']

        if nsrax == 'INTERMEDIATE':
            nsrax = ECGNSRAX.INTERMEDIATE.value
        elif nsrax == 'HORIZONTAL':
            nsrax = ECGNSRAX.HORIZONTAL.value
        elif nsrax == 'VERTICAL':
            nsrax = ECGNSRAX.VERTICAL.value

        nsrax = str(nsrax)
        return self.device.send('NSRAX=%s' % nsrax)

    '''
        Type: Command
        Set the ST Deviation for normal sinus rhythm
    '''

    def stdev(self):
        dev = self.values['stdev']
        regex = r'-'
        if -.80 < float(dev) < -.10:
            re_pos = re.sub(regex, '-', str(dev))
            dev = '%s' % re_pos

        if .10 < float(dev) < .80:
            dev = '+0%s' % dev

        if .00 or -.00:
            dev = str(dev)
        elif .05 or -.05:
            dev = str(dev)


        dev = str(dev)
        return self.device.send('STDEV=%s' % dev)

    '''
        Type: Command
        Set the ecg amplitude
    '''

    def ecgampl(self):
        ampl = self.values['ecgampl']
        range1 = np.arange(0.05, 0.45, 0.10)
        range2 = np.arange(0.50, 5.00, 0.25)

        if ampl in range1:
            ampl = '%s0' % ampl
        if ampl in range2:
            ampl = '%s0' % ampl

        ampl = str(ampl)
        return self.device.send('ECGAMPL=%s' % ampl)

    '''
        Type: Command
        Set the ecg artifact
    '''

    def eart(self):
        art = self.values['artifact']

        if art == 'OFF':
            art = ECGEART.OFF.value
        elif art == 50:
            art = ECGEART.FIFTY.value
        elif art == 60:
            art = ECGEART.SIXTY.value
        elif art == 'MSC':
            art = ECGEART.MSC.value
        elif art == 'WAND':
            art = ECGEART.WAND.value
        elif art == 'RESP':
            art = ECGEART.RESP.value

        art = str(art)
        return self.device.send('EART=%s' % art)

    '''
        Type: Command
        Set the ecg artifact in percent
    '''

    def eartsz(self):
        eartsz = self.values['size']

        if eartsz == 25:
            eartsz = '0%s' % eartsz
        elif eartsz == 50:
            eartsz = '0%s' % eartsz
        elif eartsz == 100:
            eartsz = eartsz

        eartsz = str(eartsz)
        return self.device.send('EARTSZ=%s' % eartsz)

    '''
        Type: Command
        Set the ecg artifact lead
    '''

    def eartld(self):
        eartld = self.values['lead']

        if eartld == 'ALL':
            eartld = ECGEARTLD.ALL.value
        elif eartld == 'RA':
            eartld = ECGEARTLD.RA.value
        elif eartld == 'LL':
            eartld = ECGEARTLD.LL.value
        elif eartld == 'LA':
            eartld = ECGEARTLD.LA.value
        elif eartld == 'V1':
            eartld = ECGEARTLD.V1.value
        elif eartld == 'V2':
            eartld = ECGEARTLD.V2.value
        elif eartld == 'V3':
            eartld = ECGEARTLD.V3.value
        elif eartld == 'V4':
            eartld = ECGEARTLD.V4.value
        elif eartld == 'V5':
            eartld = ECGEARTLD.V5.value
        elif eartld == 'V6':
            eartld = ECGEARTLD.V6.value

        eartld = str(eartld)
        return self.device.send('EARTLD=%s' % eartld)

    '''
        Type: Command
        Set the ecg wave
    '''

    def spvwave(self):
        spvwave = self.values['spvwave']

        if spvwave == 'AFL':
            spvwave = ECGSPVWAVE.AFL.value
        elif spvwave == 'SNA':
            spvwave = ECGSPVWAVE.SNA.value
        elif spvwave == 'MB80':
            spvwave = ECGSPVWAVE.MB80.value
        elif spvwave == 'MB120':
            spvwave = ECGSPVWAVE.MB120.value
        elif spvwave == 'ATC':
            spvwave = ECGSPVWAVE.ATC.value
        elif spvwave == 'PAT':
            spvwave = ECGSPVWAVE.PAT.value
        elif spvwave == 'NOD':
            spvwave = ECGSPVWAVE.NOD.value
        elif spvwave == 'SVT':
            spvwave = ECGSPVWAVE.SVT.value

        spvwave = str(spvwave)
        return self.device.send('SPVWAVE=%s' % spvwave)

    '''
        Type: Command
        Set the ecg wave
    '''

    def prewave(self):
        prewave = self.values['prewave']

        if prewave == 'PAC':
            prewave = ECGPREWAVE.PAC.value
        elif prewave == 'PNC':
            prewave = ECGPREWAVE.PNC.value
        elif prewave == 'PVC1':
            prewave = ECGPREWAVE.PVC1.value
        elif prewave == 'PVC1E':
            prewave = ECGPREWAVE.PVC1E.value
        elif prewave == 'PVC1R':
            prewave = ECGPREWAVE.PVC1R.value
        elif prewave == 'PVC2':
            prewave = ECGPREWAVE.PVC2.value
        elif prewave == 'PVC2E':
            prewave = ECGPREWAVE.PVC2E.value
        elif prewave == 'PVC2R':
            prewave = ECGPREWAVE.PVC2R.value
        elif prewave == 'MF':
            prewave = ECGPREWAVE.MF.value

        prewave = str(prewave)
        return self.device.send('PREWAVE=%s' % prewave)

    '''
        Type: Command
        Set the ecg wave
    '''

    def vntwave(self):
        vntwave = self.values['vntwave']

        if vntwave == 'PVC6M':
            vntwave = ECGVNTWAVE.PVC6M.value
        elif vntwave == 'PVC12M':
            vntwave = ECGVNTWAVE.PVC12M.value
        elif vntwave == 'PVC24M':
            vntwave = ECGVNTWAVE.PVC24M.value
        elif vntwave == 'FMF':
            vntwave = ECGVNTWAVE.FMF.value
        elif vntwave == 'TRIG':
            vntwave = ECGVNTWAVE.TRIG.value
        elif vntwave == 'BIG':
            vntwave = ECGVNTWAVE.BIG.value
        elif vntwave == 'PAIR':
            vntwave = ECGVNTWAVE.PAIR.value
        elif vntwave == 'RUN5':
            vntwave = ECGVNTWAVE.RUN5.value
        elif vntwave == 'RUN11':
            vntwave = ECGVNTWAVE.RUN11.value
        elif vntwave == 'ASYS':
            vntwave = ECGVNTWAVE.ASYS.value

        vntwave = str(vntwave)
        return self.device.send('VNTWAVE=%s' % vntwave)

    '''
        Type: Command
        Set the ecg wave
    '''

    def cndwave(self):
        cndwave = self.values['cndwave']

        if cndwave == '1DB':
            cndwave = ECGCNDWAVE.ONEDB.value
        if cndwave == '2DB1':
            cndwave = ECGCNDWAVE.TWODB1.value
        if cndwave == '2DB2':
            cndwave = ECGCNDWAVE.TWODB2.value
        if cndwave == '3DB':
            cndwave = ECGCNDWAVE.THREEDB.value
        if cndwave == 'RBBB':
            cndwave = ECGCNDWAVE.RBBB.value
        if cndwave == 'LBBB':
            cndwave = ECGCNDWAVE.LBBB.value

        cndwave = str(cndwave)
        return self.device.send('CNDWAVE=%s' % cndwave)

    '''
        Type: Command
        Set the pacer pulse polarity
    '''

    def tvppol(self):
        tvppol_chamber = self.values['tvppol_chamber']
        tvppol_polarity = self.values['polarity']

        if tvppol_chamber == 'V':
            tvppol_chamber = CHAMBER.V.value
        elif tvppol_chamber == 'A':
            tvppol_chamber = CHAMBER.A.value

        if tvppol_polarity == 'P':
            tvppol_polarity = 'P'
        elif tvppol_polarity == 'N':
            tvppol_polarity = 'N'

        tvppol_polarity = str(tvppol_polarity)
        tvppol_chamber = str(tvppol_chamber)
        return self.device.send('TVPPOl=%s,%s' % (tvppol_chamber, tvppol_polarity))

    '''
        Type: Command
        Set the pacer pulse amplitude
    '''

    def tvpampl(self):
        tvpampl_chamber = self.values['tvppol_chamber']
        ampl = self.values['ampl']

        if tvpampl_chamber == 'V':
            tvpampl_chamber = CHAMBER.V.value
        elif tvpampl_chamber == 'A':
            tvpampl_chamber = CHAMBER.A.value

        ampl_range = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 50, 100, 200, 500, 700]
        if ampl in ampl_range:
            if ampl < 10:
                ampl = '00%s' % ampl
            elif ampl < 100:
                ampl = '0%s' % ampl
            else:
                ampl = ampl

        ampl = str(ampl)
        return self.device.send('TVPAMPL=%s,%s' % (tvpampl_chamber,ampl))

    '''
        Type: Command
        Set the pacer pulse width
    '''

    def tvpwid(self):
        tvpwid_chamber = self.values['tvpwid_chamber']
        width = self.values['width']

        if tvpwid_chamber == 'V':
            tvpwid_chamber = CHAMBER.V.value
        elif tvpwid_chamber == 'A':
            tvpwid_chamber = CHAMBER.A.value

        width_range = [0.1, 0.2, 0.5, 1.0, 2.0]
        if width in width_range:
            width = width

        width = str(width)
        return self.device.send('TVPWID=%s,%s' % (tvpwid_chamber, width))

    '''
        Type: Command
        Set the TV Paced arrhythmia
    '''

    def tvpwave(self):
        tvpwave = self.values['tvpwave']

        if tvpwave == 'ATR':
            tvpwave = ECGTVPWAVE.ATR.value
        elif tvpwave == 'ASY':
            tvpwave = ECGTVPWAVE.ASY.value
        elif tvpwave == 'DFS':
            tvpwave = ECGTVPWAVE.DFS.value
        elif tvpwave == 'DOS':
            tvpwave = ECGTVPWAVE.DOS.value
        elif tvpwave == 'AVS':
            tvpwave = ECGTVPWAVE.AVS.value
        elif tvpwave == 'NCP':
            tvpwave = ECGTVPWAVE.NCP.value
        elif tvpwave == 'NFN':
            tvpwave = ECGTVPWAVE.NFN.value

        tvpwave = str(tvpwave)
        return self.device.send('TVPWAVE=%s' % tvpwave)

    '''
        Type: Command
        Set the ACLS arrhythmia.
    '''

    def aclswave(self):
        aclswave = self.values['aclswave']

        if aclswave == 'SBC':
            aclswave = ECGACLSWAVE.SBC.value
        elif aclswave == 'PTU':
            aclswave = ECGACLSWAVE.PTU.value
        elif aclswave == 'MTU':
            aclswave = ECGACLSWAVE.MTU.value
        elif aclswave == 'NSI':
            aclswave = ECGACLSWAVE.NSI.value
        elif aclswave == 'NSV':
            aclswave = ECGACLSWAVE.NSV.value
        elif aclswave == 'WSI':
            aclswave = ECGACLSWAVE.WSI.value
        elif aclswave == 'WSV':
            aclswave = ECGACLSWAVE.WSV.value
        elif aclswave == 'TDP':
            aclswave = ECGACLSWAVE.TDP.value

        aclswave = str(aclswave)
        return self.device.send('ACLSWAVE=%s' % aclswave)

    '''
        Type: Command
        Set the Atrial Fibrillation 1.
    '''

    def afib(self):
        afib = self.values['afib_granularity']

        if afib == 'COARSE':
            afib = GRANULARITY.COARSE.value
        elif afib == 'FINE':
            afib = GRANULARITY.FINE.value

        afib = str(afib)
        return self.device.send('AFIB=%s' % afib)

    '''
        Type: Command
        Set the Atrial Fibrillation 2.
    '''

    def afib2(self):
        afib2 = self.values['afib2_granularity']

        if afib2 == 'COARSE':
            afib2 = GRANULARITY.COARSE.value
        elif afib2 == 'FINE':
            afib2 = GRANULARITY.FINE.value

        afib2 = str(afib2)
        return self.device.send('AFIB2=%s' % afib2)

    '''
       Type: Command
       Set the Ventricular Fibrillation.
    '''

    def vfib(self):
        vfib = self.values['vfib_granularity']

        if vfib == 'COARSE':
            vfib = GRANULARITY.COARSE.value
        elif vfib == 'FINE':
            vfib = GRANULARITY.FINE.value

        vfib = str(vfib)
        return self.device.send('VFIB=%s' % vfib)

    '''
        Type: Command
        Set the Ventricular Fibrillation.
    '''

    def vfib1(self):
        vfib1 = self.values['vfib1_granularity']

        if vfib1 == 'COARSE':
            vfib1 = GRANULARITY.COARSE.value
        elif vfib1 == 'FINE':
            vfib1 = GRANULARITY.FINE.value

        vfib1 = str(vfib1)
        return self.device.send('VFIB1=%s' % vfib1)

    '''
        Type: Command
        Set the Ventricular Fibrillation.
    '''

    def vfib2(self):
        vfib2 = self.values['vfib2_granularity']

        if vfib2 == 'COARSE':
            vfib2 = GRANULARITY.COARSE.value
        elif vfib2 == 'FINE':
            vfib2 = GRANULARITY.FINE.value

        vfib2 = str(vfib2)
        return self.device.send('VFIB2=%s' % vfib2)

    '''
        Type: Command
        Set the Monophase Ventricular Tachycardia
    '''

    def monovtach(self):
        monovtach = self.values['monovtach_rate']

        monovtach = str(monovtach)
        return self.device.send('MONOVTACH=%s' % monovtach)

    '''
        Type: Command
        Set the Polyphasic Ventricular Tachycardia
    '''

    def polyvtach(self):
        polyvtach = self.values['polyvtach_rate']

        polyvtach = str(polyvtach)
        return self.device.send('POLYVTACH=%s' % polyvtach)

    '''
        Type: Command
        Set the ECG Wave to pulse
    '''

    def pulse(self):
        pulse = self.values['pulse_rate']

        pulse = str(pulse)
        return self.device.send('PULSE=%s' % pulse)

    '''
        Type: Command
        Set the ECG Wave to square
    '''

    def square(self):
        square = self.values['square_freq']

        square = str(square)
        return self.device.send('SQUARE=%s' % square)

    '''
        Type: Command
        Set the ECG Wave to sine
    '''

    def sine(self):
        sine = self.values['sine_freq']

        sine = str(sine)
        return self.device.send('SINE=%s' % sine)

    '''
        Type: Command
        Set the ECG Wave to triangle
    '''

    def tri(self):
        tri = self.values['tri_freq']

        tri = str(tri)
        return self.device.send('TRI=%s' % tri)

    '''
        Type: Command
        Set the ECG Wave to R wave detection
    '''

    def rdet(self):
        rdet_width = self.values['rdet_width']
        rdet_rate = self.values['rdet_rate']

        if rdet_width < 10:
            rdet_width = '00%s' % rdet_width
        elif rdet_width < 100:
            rdet_width = '0%s' % rdet_width

        rdet_width = str(rdet_width)
        rdet_rate = str(rdet_rate)
        return self.device.send('RDET=%s,%s' % (rdet_width, rdet_rate))

    '''
        Type: Command
        Set the ECG Wave to QRS Detection
    '''

    def qrs(self):
        qrs_width = self.values['qrs_width']
        qrs_rate = self.values['qrs_rate']

        if qrs_width < 10:
            qrs_width = '00%s' % qrs_width
        elif qrs_width < 100:
            qrs_width = '0%s' % qrs_width

        qrs_width = str(qrs_width)
        qrs_rate = str(qrs_rate)
        return self.device.send('RDET=%s,%s' % (qrs_width, qrs_rate))

    '''
        Type: Command
        Set the ECG Wave to Tall T Rejection.
    '''

    def tallt(self):
        tallt = self.values['percent']

        tallt_range = np.arange(0, 150, 10)
        if tallt in tallt_range:
            if tallt < 10:
                tallt = '00%s' % tallt
            elif tallt < 100:
                tallt = '0%s' % tallt

        tallt = str(tallt)
        return self.device.send('TALLT=%s' % tallt)

    ########################################################
    #   Actions
    ########################################################

    '''
        Type: Action
        Method to turn the ecg module on the ProSim8 on
    '''

    def turn_on_ecg(self):
        return self.ecgrun(on=True)

    '''
        Type: Action
        Method to turn the ecg module on the ProSim8 off
    '''

    def turn_off_ecg(self):
        return self.ecgrun(on=False)

    '''
        Type: Action
        Method to set nsra in the PROSIM8
    '''

    def set_nsra_reading(self):
        return self.nsra()

    '''
       Type: Action
       Method to set nsrp in the PROSIM8
    '''

    def set_nsrp_reading(self):
        return self.nsrp()

    '''
       Type: Action
       Method to set nsrax in the PROSIM8
    '''

    def set_nsrax_reading(self):
        return self.nsrax()

    '''
       Type: Action
       Method to set stdev in the PROSIM8
    '''

    def set_stdev_reading(self):
        return self.stdev()

    '''
        Type: Action
        Method to set ecgampl in the PROSIM8
    '''

    def set_ecgampl_reading(self):
        return self.ecgampl()

    '''
        Type: Action
        Method to set eart in the PROSIM8
    '''

    def set_eart_reading(self):
        return self.eart()

    '''
        Type: Action
        Method to set eartsz in the PROSIM8
    '''

    def set_eartsz_reading(self):
        return self.eartsz()

    '''
        Type: Action
        Method to set eartld in the PROSIM8
    '''

    def set_eartld_reading(self):
        return self.eartld()

    '''
        Type: Action
        Method to set spvwave in the PROSIM8
    '''

    def set_spvwave_reading(self):
        return self.spvwave()

    '''
        Type: Action
        Method to set prewave in the PROSIM8
    '''

    def set_prewave_reading(self):
        return self.prewave()

    '''
        Type: Action
        Method to set vntwave in the PROSIM8
    '''

    def set_vntwave_reading(self):
        return self.vntwave()

    '''
        Type: Action
        Method to set cndwave in the PROSIM8
    '''

    def set_cndwave_reading(self):
        return self.cndwave()

    '''
        Type: Action
        Method to set tvppol in the PROSIM8
    '''

    def set_tvppol_reading(self):
        return self.tvppol()

    '''
        Type: Action
        Method to set tvpwid in the PROSIM8
    '''

    def set_tvpwid_reading(self):
        return self.tvpwid()

    '''
        Type: Action
        Method to set tvpwave in the PROSIM8
    '''

    def set_tvpwave_reading(self):
        return self.tvpwave()

    '''
        Type: Action
        Method to set aclswave in the PROSIM8
    '''

    def set_aclswave_reading(self):
        return self.aclswave()

    '''
        Type: Action
        Method to set afib in the PROSIM8
    '''

    def set_afib_reading(self):
        return self.afib()

    '''
        Type: Action
        Method to set afib2 in the PROSIM8
    '''

    def set_afib2_reading(self):
        return self.afib2()

    '''
        Type: Action
        Method to set vfib in the PROSIM8
    '''

    def set_vfib_reading(self):
        return self.vfib()

    '''
        Type: Action
        Method to set vfib1 in the PROSIM8
    '''

    def set_vfib1_reading(self):
        return self.vfib1()

    '''
       Type: Action
       Method to set vfib2 in the PROSIM8
    '''

    def set_vfib2_reading(self):
        return self.vfib2()

    '''
        Type: Action
        Method to set monovtach in the PROSIM8
    '''

    def set_monovtach_reading(self):
        return self.monovtach()

    '''
        Type: Action
        Method to set polyvtach in the PROSIM8
    '''

    def set_polyvtach_reading(self):
        return self.polyvtach()

    '''
        Type: Action
        Method to set pulse in the PROSIM8
    '''

    def set_pulse_reading(self):
        return self.pulse()

    '''
        Type: Action
        Method to set square in the PROSIM8
    '''

    def set_square_reading(self):
        return self.square()

    '''
        Type: Action
        Method to set sine in the PROSIM8
    '''

    def set_sine_reading(self):
        return self.sine()

    '''
        Type: Action
        Method to set tri in the PROSIM8
    '''

    def set_tri_reading(self):
        return self.tri()

    '''
        Type: Action
        Method to set rdet in the PROSIM8
    '''

    def set_rdet_reading(self):
        return self.rdet()

    '''
        Type: Action
        Method to set qrs in the PROSIM8
    '''

    def set_qrs_reading(self):
        return self.qrs()

    '''
        Type: Action
        Method to set tallt in the PROSIM8
    '''

    def set_tallt_reading(self):
        return self.tallt()
