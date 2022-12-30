from enum import Enum


class AMBF(Enum):
    DC = 'DC'
    FIFTY = '50Hz'
    SIXTY = '60Hz'
    ONE = '1KHz'
    TWO = '2KHz'
    THREE = '3KHz'
    FOUR = '4KHz'
    FIVE = '5KHz'
    SIX = '6KHz'
    SEVEN = '7KHz'
    EIGHT = '8KHz'
    NINE = '9KHz'
    TEN = '10KHz'


class SPO2TYPE(Enum):
    NELCR = 'NELCR'
    MASIM = 'MASIM'
    MASIMR = 'MASIMR'
    NONIN = 'NONIN'
    OHMED = 'OHMED'
    PHIL = 'PHIL'
    NIHON = 'NIHON'
    MINDR = 'MINDR'
    BCI = 'BCI'