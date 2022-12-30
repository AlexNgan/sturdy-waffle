"""
This module defines custom exceptions used in other modules.
"""
class EmptyCommandError(Exception):
    """
    Exception to define a empty command error
    
    Attributes:
        None
    """
    pass

class UnknownCommandError(Exception):
    """
    Exception to define a unknown command error
    
    Attributes:
        None
    """
    pass

class IllegalCommandError(Exception):
    """
    Exception to define a illegal command error
    
    Attributes:
        None
    """
    pass

class InvalidParameterError(Exception):
    """
    Exception to define a invalid parameter error
    
    Attributes:
        None
    """
    def __init__(self):
        Exception.__init__(self, 'Parameter wrong or out of range')
    pass

class BufferOverflowError(Exception):
    """
    Exception to define a buffer overflow error
    
    Attributes:
        None
    """
    pass

class DeviceMemoryError(Exception):
    """
    Exception to define a device memory error
    
    Attributes:
        None
    """
    pass

class NotInstalledError(Exception):
    """
    Exception to define a not installed error (Aux/SpO2)
    
    Attributes:
        None
    """
    pass

class CantZeroPressureError(Exception):
    """
    Exception to define a can't zero pressure error

    Attributes:
        None
    """
    pass

