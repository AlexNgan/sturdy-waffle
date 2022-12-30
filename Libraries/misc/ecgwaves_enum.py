from enum import Enum


class ECGSPVWAVE(Enum):
    AFL = 'AFL'
    SNA = 'SNA'
    MB80 = 'MB80'
    MB120 = 'MB120'
    ATC = 'ATC'
    PAT = 'PAT'
    NOD = 'NOD'
    SVT = 'SVT'


class ECGPREWAVE(Enum):
    PAC = 'PAC'
    PNC = 'PNC'
    PVC1 = 'PVC1'
    PVC1E = 'PVC1E'
    PVC1R = 'PVC1R'
    PVC2 = 'PVC2'
    PVC2E = 'PVC2E'
    PVC2R = 'PVC2R'
    MF = 'MR'


class ECGVNTWAVE(Enum):
    PVC6M = 'PVC6M '
    PVC12M = 'PVC12M'
    PVC24M = 'PVC24M'
    FMF = 'FMF'
    TRIG = 'TRIG'
    BIG = 'BIG'
    PAIR = 'PAIR'
    RUN5 = 'RUN5'
    RUN11 = 'RUN11'
    ASYS = 'ASYS'


class ECGCNDWAVE(Enum):
    ONEDB = '1DB '
    TWODB1 = '2DB1'
    TWODB2 = '2DB2'
    THREEDB = '3DB '
    RBBB = 'RBBB'
    LBBB = 'LBBB'


class ECGTVPWAVE(Enum):
    ATR = 'ATR'
    ASY = 'ASY'
    DFS = 'DFS'
    DOS = 'DOS'
    AVS = 'AVS'
    NCP = 'NCP'
    NFN = 'NFN'


class ECGACLSWAVE(Enum):
    SBC = 'SBC'
    PTU = 'PTU'
    MTU = 'MTU'
    NSI = 'NSI'
    NSV = 'NSV'
    WSI = 'WSI'
    WSV = 'WSV'
    TDP = 'TDP'



