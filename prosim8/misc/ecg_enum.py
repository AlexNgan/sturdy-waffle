from enum import Enum


class ECGEART(Enum):
    OFF = 'OFF'
    FIFTY = '50'
    SIXTY = '60'
    MSC = 'MSC'
    WAND = 'WAND'
    RESP = 'RESP'


class ECGEARTLD(Enum):
    ALL = 'ALL'
    RA = 'RA'
    LL = 'LL'
    LA = 'LA'
    V1 = 'V1'
    V2 = 'V2'
    V3 = 'V3'
    V4 = 'V4'
    V5 = 'V5'
    V6 = 'V6'


class GRANULARITY(Enum):
    COARSE = 'COARSE'
    FINE = 'FINE'


class ECGNSRAX(Enum):
    INTERMEDIATE = 'INT'
    HORIZONTAL = 'HOR'
    VERTICAL = 'VER'


class CHAMBER(Enum):
    A = 'A'
    V = 'V'

