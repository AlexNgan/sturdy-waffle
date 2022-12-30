"""
This module provides serial connections to devices, such as a Impulse Device.
"""

import time
import re
import serial


# from prosim8.custom_exceptions import EmptyCommandError
from prosim8.custom_exceptions import UnknownCommandError
from prosim8.custom_exceptions import IllegalCommandError
from prosim8.custom_exceptions import InvalidParameterError
from prosim8.custom_exceptions import BufferOverflowError
from prosim8.custom_exceptions import DeviceMemoryError
from prosim8.custom_exceptions import NotInstalledError
from prosim8.custom_exceptions import CantZeroPressureError


class Connection(object):
    """
    Class to to control the communication with the serial devices

    Attributes:
        device_id: device name or None
        baudrate: baud rate
        bytesize: number of data bits
        parity: enable parity checking
        stopbits: number of stop bits
        timeout(float): Set a read timeout value
        write_timeout(float): Set a write timeout value
        xonxoff(bool): enable software flow control
        rtscts(bool): enable hardware (RTS/CTS) flow control
        dsrdtr(bool): Enable hardware (DSR/DTR) flow control
    """

    #GoodCommand           = {'name' : 'OK'                   , 'search' : r'^\*$'},
    RESPONSES = [
        {'Exception' : UnknownCommandError   , 'name' : 'Empty Command'        , 'search' : r'^!$'},
        {'Exception' : IllegalCommandError   , 'name' : 'Unknown Command'      , 'search' : r'^!01 Unknown command$'},
        {'Exception' : IllegalCommandError   , 'name' : 'Illegal Command'      , 'search' : r'^!02 Illegal command$'},
        {'Exception' : InvalidParameterError , 'name' : 'Illegal Parameter'    , 'search' : r'^!03 Illegal parameter$'},
        {'Exception' : BufferOverflowError   , 'name' : 'Buffer Overflow'      , 'search' : r'^!04 Buffer overflow$'},
        {'Exception' : DeviceMemoryError     , 'name' : 'Memory Error'         , 'search' : r'^!21 Memory error$'},
        {'Exception' : CantZeroPressureError , 'name' : 'Failed Zero Pressure' , 'search' : r'^!22 Can\'t zero pressure$'},
        {'Exception' : NotInstalledError     , 'name' : 'Communication Failure', 'search' : r'^!27 Aux/SpO2 Communication Error$'},
    ]

    def __init__(self,
                 device_id=0,
                 baudrate=115200,
                 bytesize=serial.EIGHTBITS,
                 parity=serial.PARITY_NONE,
                 stopbits=serial.STOPBITS_ONE,
                 timeout=None,
                 write_timeout=None,
                 xonxoff=False,
                 rtscts=True,
                 dsrdtr=False,
                 response_timeout=1.0, debug=False):

        """
        The initialization creates the defined connection

        Args:
            device_id: device name or None
            baudrate: baud rate
            bytesize: number of data bits
            parity: enable parity checking
            stopbits: number of stop bits
            timeout(float): Set a read timeout value
            write_timeout(float): Set a write timeout value
            xonxoff(bool): enable software flow control
            rtscts(bool): enable hardware (RTS/CTS) flow control
            dsrdtr(bool): Enable hardware (DSR/DTR) flow control

        Returns:
            none

        Raises:
            Propagates the following to the calling method:
            ValueError: Will be raised when parameter are out of range,
                e.g. baud rate, data bits.
            SerialException:  In case the device can not be found or can
                not be configured
        """

        # Add variables to control testing loop and message validation.

        self._current_input_size = 0
        self._current_output_size = 0
        self._current_response = ''
        self.response_timeout = response_timeout

        self._ser = serial.Serial(port=device_id,
                                  baudrate=baudrate,
                                  bytesize=bytesize,
                                  parity=parity,
                                  stopbits=stopbits,
                                  timeout=timeout,
                                  write_timeout=write_timeout,
                                  xonxoff=xonxoff,
                                  rtscts=rtscts,
                                  dsrdtr=dsrdtr)
        self.DEBUG = debug
    @property
    def current_input_size(self):
        """
        Define a class property to store the input size.
        """
        return self._current_input_size

    @current_input_size.setter
    def current_input_size(self, new_value):
        self._current_input_size = int(new_value)

    @property
    def current_output_size(self):
        """
        Define a class property to store the canned output size.
        """
        return self._current_output_size

    @current_output_size.setter
    def current_output_size(self, new_value):
        self._current_output_size = int(new_value)

    @property
    def current_response(self):
        """
        Define a class property to store the current response.
        """
        return self._current_response

    @current_response.setter
    def current_response(self, new_value):
        self._current_response = new_value

    def open(self):

        """
        Opens up the connection.  The settings are retained from
        when the object was initialized.

        Args:
            none

        Returns:
            none

        Raises:
            Propagates the following to the calling method:
            ValueError: Will be raised when parameter are out of range, e.g.
                baud rate, data bits.
            SerialException: In case the device can not be found or can not be
                configured.
        """
        self._ser.open()

    def close(self):
        """
        Closes the connection

        Args:
            none

        Returns:
            none

        Raises:
            propagates any unhandled exceptions to the calling method
        """
        self._ser.close()

    def is_open(self):
        """
        Checks if the connection is open

        Args:
            none

        Returns:
            is_open: True if connection is open, otherwise False

        Raises:
            propagates any unhandled exceptions to the calling method
        """
        return self._ser.is_open

    def flush_input_buffer(self):
        """
        Clears the input buffer

        Args:
            none

        Returns:
            none

        Raises:
            propagates any unhandled exceptions to the calling method
        """
        self._ser.reset_input_buffer()

    def flush_output_buffer(self):
        """
        Clears the output buffer

        Args:
            none

        Returns:
            none

        Raises:
            propagates any unhandled exceptions to the calling method
        """
        self._ser.reset_output_buffer()

    def get_input_byte_size(self):
        """
        Retrieves the size of data in bytes in the input buffer

        Args:
            none

        Outputs:
            size - the size of data in bytes in the input buffer

        Raises:
            propagates any exceptions to the calling method
        """
        size = self._ser.in_waiting
        return size

    def get_output_byte_size(self):
        """
        Retrieves the size of data in bytes in the output buffer

        Returns:
            size - the size of data in bytes in the output buffer

        Raises:
            propagates any unhandled exceptions to the calling method
        """
        size = self._ser.out_waiting
        return size

    def send_msg(self, data):
        """
        Sends a command to the device

        Args:
            data - the message that is sent.

        Returns:
            none

        Raises:
            SerialException: In case the device can not be found
                or can not be configured
            Propagates the following to the calling method:
            SerialTimeoutException: In case a write timeout is configured
                for the port and the time is exceeded.
        """
        try:
            data = data + "\r"
            self._ser.write(data.encode())

        except serial.SerialException:
            # write() can get a SerialException if the connection is closed.
            # open the connection and try again.

            self._ser.open()
            self._ser.write(data.encode())

    def get_response(self, size):
        """
        Retrieves the contents from the input buffer

        Args:
            size - the size in bytes to read

        Returns:
            response - the retrieved response

        Raises:
            SerialException: In case the device can not be found
                or can not be configured
            Propagates the following to the calling method:
            SerialTimeoutException: In case a read timeout is configured
                for the port and the time is exceeded.
        """
        try:
            response = self._ser.read(size).decode().strip()
            for R in Connection.RESPONSES:
                if re.search(R['search'], response):
                    raise R['Exception']
            return response

        except serial.SerialException:
            # read() can get a SerialException if the connection is closed.
            # open the connection and try again.

            self._ser.open()
            response = self._ser.read(size).decode()
            return response
      
    def send(self, mesg):
        if self.DEBUG:
            print('Sending: %s'%mesg)
        self.send_msg(mesg)
        time.sleep(self.response_timeout)
        response = self.get_response(self.get_input_byte_size()).rstrip()
        if self.DEBUG:
            print('Received: %s'%response)
        return response
