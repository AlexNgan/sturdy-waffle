from enum import Enum

'''
Enum for ibp channel to a dynamic wave 
'''


class IBPWAVE(Enum):
    ARTERIAL = 'ART'
    RADIAL_ARTERY = 'RART'
    LEFT_VENTRICLE = 'LV'
    LEFT_ATRIUM = 'LA'
    RIGHT_VENTRICLE = 'RV'
    PULMONARY_ARTERY = 'PA'
    PA_WEDGE = 'PAW'
    RIGHT_ATRIUM = 'RA'
