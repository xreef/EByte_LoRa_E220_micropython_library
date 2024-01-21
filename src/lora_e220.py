#############################################################################################
# EBYTE LoRa E220 Series for MicroPython
#
# AUTHOR:  Renzo Mischianti
# VERSION: 0.0.4
#
# This library is based on the work of:
# https://www.mischianti.org/category/my-libraries/lora-e220-devices/
#
# This library implements the EBYTE LoRa E220 Series for MicroPython.
#
# The MIT License (MIT)
#
# Copyright (c) 2019 Renzo Mischianti www.mischianti.org All right reserved.
#
# You may copy, alter and reuse this code in any way you like, but please leave
# reference to www.mischianti.org in your comments if you redistribute this code.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#############################################################################################

from lora_e220_constants import UARTParity, UARTBaudRate, TransmissionPower, FixedTransmission, AirDataRate, \
    OperatingFrequency, LbtEnableByte, WorPeriod, RssiEnableByte, RssiAmbientNoiseEnable, SubPacketSetting
from lora_e220_operation_constant import ResponseStatusCode, ModeType, ProgramCommand, SerialUARTBaudRate, \
    PacketLength, RegisterAddress

import machine
import ure
import utime
import ujson


class Logger:
    def __init__(self, enable_debug):
        self.enable_debug = enable_debug
        self.name = ''

    def debug(self, msg, *args):
        if self.enable_debug:
            print(self.name, ' DEBUG ', msg, *args)

    def info(self, msg, *args):
        if self.enable_debug:
            print(self.name, ' INFO ', msg, *args)

    def error(self, msg, *args):
        if self.enable_debug:
            print(self.name, ' ERROR ', msg, *args)

    def getLogger(self, name):
        self.name = name
        return Logger(self.enable_debug)


logging = Logger(False)

logger = logging.getLogger(__name__)

BROADCAST_ADDRESS = 0xFF


class Speed:
    def __init__(self, model):
        self.model = model

        self.airDataRate = AirDataRate.AIR_DATA_RATE_010_24
        self.uartBaudRate = UARTBaudRate.BPS_9600
        self.uartParity = UARTParity.MODE_00_8N1

    def get_air_data_rate(self):
        return AirDataRate.get_description(self.airDataRate)

    def get_UART_baud_rate(self):
        return UARTBaudRate.get_description(self.uartBaudRate)

    def get_UART_parity_description(self):
        return UARTParity.get_description(self.uartParity)


class TransmissionMode:
    def __init__(self, model):
        self.model = model

        self.WORPeriod = WorPeriod.WOR_2000_011
        self.reserved2 = 0
        self.enableLBT = LbtEnableByte.LBT_DISABLED
        self.reserved = 0
        self.fixedTransmission = FixedTransmission.TRANSPARENT_TRANSMISSION
        self.enableRSSI = RssiEnableByte.RSSI_DISABLED

    def get_WOR_period_description(self):
        return WorPeriod.get_description(self.WORPeriod)

    def get_LBT_enable_byte_description(self):
        return LbtEnableByte.get_description(self.enableLBT)

    def get_fixed_transmission_description(self):
        return FixedTransmission.get_description(self.fixedTransmission)

    def get_RSSI_enable_byte_description(self):
        return RssiEnableByte.get_description(self.enableRSSI)


class Option:
    def __init__(self, model):
        self.model = model

        self.transmissionPower = TransmissionPower(self.model).get_transmission_power().get_default_value()
        self.reserved = 0
        self.RSSIAmbientNoise = RssiAmbientNoiseEnable.RSSI_AMBIENT_NOISE_DISABLED
        self.subPacketSetting = SubPacketSetting.SPS_200_00

    def get_transmission_power_description(self):
        return TransmissionPower(self.model).get_transmission_power_description(self.transmissionPower)

    def get_RSSI_ambient_noise_enable(self):
        return RssiAmbientNoiseEnable.get_description(self.RSSIAmbientNoise)

    def get_sub_packet_setting(self):
        return SubPacketSetting.get_description(self.subPacketSetting)


class Crypt:
    def __init__(self):
        self.CRYPT_H = 0
        self.CRYPT_L = 0


class Configuration:
    def __init__(self, model):
        self.model = model

        self.package_type = None
        self.frequency = None
        self.transmission_power = None

        if model is not None:
            self.package_type = model[6]
            self.frequency = int(model[0:3])
            self.transmission_power = int(model[4:6])

        self._COMMAND = 0
        self._STARTING_ADDRESS = 0
        self._LENGTH = 0
        self.ADDH = 0
        self.ADDL = 0
        self.SPED = Speed(self.model)
        self.OPTION = Option(self.model)
        self.CHAN = 23
        self.TRANSMISSION_MODE = TransmissionMode(self.model)
        self.CRYPT = Crypt()

    def get_model(self):
        return self.model

    def get_package_type(self):
        return self.package_type

    def get_channel(self):
        return self.CHAN

    def get_frequency(self):
        return OperatingFrequency.get_freq_from_channel(self.frequency, self.CHAN)

    def get_model(self):
        return self.model

    def to_hex_string(self):
        return ''.join(['0x{:02X} '.format(x) for x in self.to_hex_array()])

    def to_bytes(self):
        hexarray = self.to_hex_array()
        # Convert values to valid byte values
        for i in range(len(hexarray)):
            if hexarray[i] > 255:
                hexarray[i] = hexarray[i] % 256

        return bytes(hexarray)

    def from_hex_array(self, hex_array):
        self._COMMAND = hex_array[0]
        self._STARTING_ADDRESS = hex_array[1]
        self._LENGTH = hex_array[2]
        self.ADDH = hex_array[3]
        self.ADDL = hex_array[4]

        self.SPED.airDataRate = hex_array[5] & 0b00000111
        self.SPED.uartParity = (hex_array[5] & 0b00011000) >> 3
        self.SPED.uartBaudRate = (hex_array[5] & 0b11100000) >> 5

        self.OPTION.transmissionPower = hex_array[6] & 0b00000011
        self.OPTION.RSSIAmbientNoise = (hex_array[6] & 0b00100000) >> 5
        self.OPTION.subPacketSetting = (hex_array[6] & 0b11000000) >> 6

        self.CHAN = hex_array[7]

        self.TRANSMISSION_MODE.WORPeriod = hex_array[8] & 0b00000111
        self.TRANSMISSION_MODE.enableLBT = (hex_array[8] & 0b00010000) >> 4
        self.TRANSMISSION_MODE.fixedTransmission = (hex_array[8] & 0b01000000) >> 6
        self.TRANSMISSION_MODE.enableRSSI = (hex_array[8] & 0b10000000) >> 7

        self.CRYPT.CRYPT_H = hex_array[9]
        self.CRYPT.CRYPT_L = hex_array[10]

    def to_hex_array(self):
        return [self._COMMAND,
                self._STARTING_ADDRESS,
                self._LENGTH,
                self.ADDH,
                self.ADDL,
                self.SPED.airDataRate | (self.SPED.uartParity << 3) | (self.SPED.uartBaudRate << 5),
                self.OPTION.transmissionPower | (self.OPTION.RSSIAmbientNoise << 5) | (
                            self.OPTION.subPacketSetting << 6),
                self.CHAN,
                self.TRANSMISSION_MODE.WORPeriod | (self.TRANSMISSION_MODE.enableLBT << 4) | (
                        self.TRANSMISSION_MODE.fixedTransmission << 6) | (self.TRANSMISSION_MODE.enableRSSI << 7),
                self.CRYPT.CRYPT_H,
                self.CRYPT.CRYPT_L]

    def from_hex_string(self, hex_string):
        self.from_hex_array([int(hex_string[i:i + 2], 16) for i in range(0, len(hex_string), 2)])

    def from_bytes(self, bytes):
        self.from_hex_array([x for x in bytes])


def print_configuration(configuration):
    print("----------------------------------------")
    print("HEAD : ", hex(configuration._COMMAND), " ", hex(configuration._STARTING_ADDRESS), " ",
          hex(configuration._LENGTH))
    print("")
    print("AddH : ", hex(configuration.ADDH))
    print("AddL : ", hex(configuration.ADDL))
    print("")
    print("Chan : ", str(configuration.CHAN), " -> ", configuration.get_frequency())
    print("")
    print("SpeedParityBit : ", bin(configuration.SPED.uartParity), " -> ",
          configuration.SPED.get_UART_parity_description())
    print("SpeedUARTDatte : ", bin(configuration.SPED.uartBaudRate), " -> ", configuration.SPED.get_UART_baud_rate())
    print("SpeedAirDataRate : ", bin(configuration.SPED.airDataRate), " -> ", configuration.SPED.get_air_data_rate())
    print("")
    print("OptionSubPacketSett: ", bin(configuration.OPTION.subPacketSetting), " -> ",
          configuration.OPTION.get_sub_packet_setting())
    print("OptionTranPower : ", bin(configuration.OPTION.transmissionPower), " -> ",
          configuration.OPTION.get_transmission_power_description())
    print("OptionRSSIAmbientNo: ", bin(configuration.OPTION.RSSIAmbientNoise), " -> ",
          configuration.OPTION.get_RSSI_ambient_noise_enable())
    print("")
    print("TransModeWORPeriod : ", bin(configuration.TRANSMISSION_MODE.WORPeriod), " -> ",
          configuration.TRANSMISSION_MODE.get_WOR_period_description())
    print("TransModeEnableLBT : ", bin(configuration.TRANSMISSION_MODE.enableLBT), " -> ",
          configuration.TRANSMISSION_MODE.get_LBT_enable_byte_description())
    print("TransModeEnableRSSI: ", bin(configuration.TRANSMISSION_MODE.enableRSSI), " -> ",
          configuration.TRANSMISSION_MODE.get_RSSI_enable_byte_description())
    print("TransModeFixedTrans: ", bin(configuration.TRANSMISSION_MODE.fixedTransmission), " -> ",
          configuration.TRANSMISSION_MODE.get_fixed_transmission_description())
    print("----------------------------------------")


MAX_SIZE_TX_PACKET = 200


class ModuleInformation:
    def __init__(self):
        self._COMMAND = 0
        self._STARTING_ADDRESS = 0
        self._LENGTH = 0
        self.model = 0
        self.version = 0
        self.features = 0

    def to_hex_array(self):
        hex_array = bytearray()
        hex_array.append(self._COMMAND)
        hex_array.append(self._STARTING_ADDRESS)
        hex_array.append(self._LENGTH)
        hex_array.append(self.model)
        hex_array.append(self.version)
        hex_array.append(self.features)
        return hex_array

    def from_hex_array(self, hex_array):
        self._COMMAND = hex_array[0]
        self._STARTING_ADDRESS = hex_array[1]
        self._LENGTH = hex_array[2]
        self.model = hex_array[3]
        self.version = hex_array[4]
        self.features = hex_array[5]

    def to_hex_string(self):
        return ''.join(['{:02X}'.format(x) for x in self.to_hex_array()])

    def to_bytes(self):
        return bytes(self.to_hex_array())

    def from_hex_string(self, hex_string):
        self.from_hex_array([int(hex_string[i:i + 2], 16) for i in range(0, len(hex_string), 2)])

    def from_bytes(self, bytes):
        self.from_hex_array([x for x in bytes])


class LoRaE220:
    # now the constructor that receive directly the UART object
    def __init__(self, model, uart, aux_pin=None, m0_pin=None, m1_pin=None,
                 uart_baudrate=SerialUARTBaudRate.BPS_RATE_9600):
        self.uart = uart
        self.model = model

        pattern = '^(230|400|900)(T|R|MM|M)(22|30)[SD]$'

        model_regex = ure.compile(pattern)
        if not model_regex.match(model):
            raise ValueError('Invalid model')

        self.aux_pin = aux_pin
        self.m0_pin = m0_pin
        self.m1_pin = m1_pin

        self.aux = None
        self.m0 = None
        self.m1 = None

        self.uart_baudrate = uart_baudrate
        self.mode = None

    # model is like 433T20D or 433T27D or 433T30D or 868T20S or 868T27S or 868T30S
    # def __init__(self, model, tx_pin, rx_pin, uart_id=0, aux_pin=None, m0_pin=None, m1_pin=None,
    #              uart_baudrate=SerialUARTBaudRate.BPS_RATE_9600):
    #     self.uart = machine.UART(uart_id, tx=tx_pin, rx=rx_pin)
    #     super().__init__(model, self.uart, aux_pin, m0_pin, m1_pin, uart_baudrate)

    def begin(self, uart_parity=UARTParity.MODE_00_8N1):
        self.uart.init(baudrate=self.uart_baudrate, bits=8, parity=UARTParity.get_uart_value(uart_parity), stop=1,
                       timeout=1000, timeout_char=1000)

        self.m0 = None
        self.m1 = None
        self.aux = None
        if self.aux_pin is not None:
            self.aux = machine.Pin(self.aux_pin, machine.Pin.IN)
        if self.m0_pin is not None and self.m1_pin is not None:
            self.m0 = machine.Pin(self.m0_pin, machine.Pin.OUT)
            self.m1 = machine.Pin(self.m1_pin, machine.Pin.OUT)
            self.m0.on()
            self.m1.on()

        # self.uart.timeout(1000)

        code = self.set_mode(ModeType.MODE_0_NORMAL)
        if code != ResponseStatusCode.SUCCESS:
            return code

        return code

    def set_mode(self, mode: ModeType) -> ResponseStatusCode:
        self.managed_delay(40)

        if self.m0 is None and self.m1 is None:
            logger.debug(
                "The M0 and M1 pins are not set, which means that you are connecting the pins directly as you need!")
        else:
            if mode == ModeType.MODE_0_NORMAL:
                # Mode 0 | normal operation
                self.m0.off()
                self.m1.off()
                logger.debug("MODE NORMAL!")
            elif mode == ModeType.MODE_1_WOR_TRANSMITTER:
                # Mode 1 | wake-up operation
                self.m0.on()
                self.m1.off()
                logger.debug("MODE WOR TRANSMITTER!")
            elif mode == ModeType.MODE_2_POWER_SAVING:
                # Mode 2 | power saving operation
                self.m0.off()
                self.m1.on()
                logger.debug("MODE WOR RECEIVER!")
            elif mode == ModeType.MODE_3_CONFIGURATION:
                # Mode 3 | Setting operation
                self.m0.on()
                self.m1.on()
                logger.debug("MODE PROGRAM!")
            else:
                return ResponseStatusCode.ERR_E220_INVALID_PARAM

        self.managed_delay(40)

        res = self.wait_complete_response(1000)
        if res == ResponseStatusCode.E220_SUCCESS:
            self.mode = mode

        return res

    @staticmethod
    def managed_delay(timeout):
        t = utime.ticks_ms()

        # make darn sure ticks_ms() is not about to reach max data type limit and start over
        if utime.ticks_add(t, timeout) == 0:
            t = 0

        while utime.ticks_diff(utime.ticks_ms(), t) < timeout:
            pass

    def wait_complete_response(self, timeout, wait_no_aux=100) -> ResponseStatusCode:
        result = ResponseStatusCode.E220_SUCCESS
        t = utime.ticks_ms()

        if utime.ticks_add(t, timeout) == 0:
            t = 0

        if self.aux is not None:
            while self.aux.value() == 0:
                if utime.ticks_diff(utime.ticks_ms(), t) > timeout:
                    result = ResponseStatusCode.ERR_E220_TIMEOUT
                    logger.debug("Timeout error!")
                    return result

            logger.debug("AUX HIGH!")
        else:
            self.managed_delay(wait_no_aux)
            logger.debug("Wait no AUX pin!")

        self.managed_delay(20)
        logger.debug("Complete!")
        return result

    def check_UART_configuration(self, mode) -> ResponseStatusCode:
        if mode == ModeType.MODE_3_PROGRAM and self.uart_baudrate != SerialUARTBaudRate.BPS_RATE_9600:
            return ResponseStatusCode.ERR_E220_WRONG_UART_CONFIG
        return ResponseStatusCode.E220_SUCCESS

    def set_configuration(self, configuration, permanentConfiguration=True) -> (ResponseStatusCode, Configuration):
        # code = ResponseStatusCode.E220_SUCCESS
        code = self.check_UART_configuration(ModeType.MODE_3_PROGRAM)
        if code != ResponseStatusCode.E220_SUCCESS:
            return code, None

        prev_mode = self.mode
        code = self.set_mode(ModeType.MODE_3_PROGRAM)
        if code != ResponseStatusCode.E220_SUCCESS:
            return code, None

        configuration._STARTING_ADDRESS = RegisterAddress.REG_ADDRESS_CFG
        configuration._LENGTH = PacketLength.PL_CONFIGURATION

        if permanentConfiguration:
            configuration._COMMAND = ProgramCommand.WRITE_CFG_PWR_DWN_SAVE
        else:
            configuration._COMMAND = ProgramCommand.WRITE_CFG_PWR_DWN_LOSE

        data = configuration.to_bytes()
        logger.debug("Writing configuration: {} size {}".format(configuration.to_hex_string(), len(data)))

        len_writed = self.uart.write(data)
        if len_writed != len(data):
            self.set_mode(prev_mode)
            return code, None

        code = self.set_mode(prev_mode)
        if code != ResponseStatusCode.E220_SUCCESS:
            return code, None

        data = self.uart.read()

        if data is None or len(data) != PacketLength.PL_CONFIGURATION+3:
            if data is not None:
                logger.debug("data: {}".format(data))
                logger.debug("data len: {}".format(len(data)))
            code = ResponseStatusCode.ERR_E220_DATA_SIZE_NOT_MATCH
            return code, None
        logger.debug("data: {}".format(data))
        logger.debug("data len: {}".format(len(data)))

        logger.debug("model: {}".format(self.model))
        configuration = Configuration(self.model)
        configuration.from_bytes(data)

        if ProgramCommand.WRONG_FORMAT == configuration._COMMAND:
            code = ResponseStatusCode.ERR_E220_WRONG_FORMAT
        if ProgramCommand.RETURNED_COMMAND != configuration._COMMAND or \
                RegisterAddress.REG_ADDRESS_CFG != configuration._STARTING_ADDRESS or \
                PacketLength.PL_CONFIGURATION != configuration._LENGTH:
            code = ResponseStatusCode.ERR_E220_HEAD_NOT_RECOGNIZED

        self.clean_UART_buffer()

        return code, configuration

    def write_program_command(self, cmd, addr, pl) -> int:
        cmd = bytearray([cmd, addr, pl])
        size = self.uart.write(cmd)

        self.managed_delay(50)  # need to check

        return size != 3

    def get_configuration(self) -> (ResponseStatusCode, Configuration):
        code = self.check_UART_configuration(ModeType.MODE_3_PROGRAM)
        logger.debug("check_UART_configuration: {}".format(code))
        if code != ResponseStatusCode.E220_SUCCESS:
            return code, None

        prev_mode = self.mode
        code = self.set_mode(ModeType.MODE_3_PROGRAM)
        if code != ResponseStatusCode.E220_SUCCESS:
            return code, None
        logger.debug("set_mode: {}".format(code))

        self.write_program_command(
            ProgramCommand.READ_CONFIGURATION,
            RegisterAddress.REG_ADDRESS_CFG,
            PacketLength.PL_CONFIGURATION)

        data = self.uart.read()
        if data is None or len(data) != PacketLength.PL_CONFIGURATION+3:
            if data is not None:
                logger.debug("data: {}".format(data))
                logger.debug("data len: {}".format(len(data)))
            code = ResponseStatusCode.ERR_E220_DATA_SIZE_NOT_MATCH
            return code, None

        logger.debug("data: {}".format(data))
        logger.debug("data len: {}".format(len(data)))

        logger.debug("model: {}".format(self.model))
        configuration = Configuration(self.model)
        configuration.from_bytes(data)
        code = self.set_mode(prev_mode)

        if ProgramCommand.WRONG_FORMAT == configuration._COMMAND:
            code = ResponseStatusCode.ERR_E220_WRONG_FORMAT

        if ProgramCommand.RETURNED_COMMAND != configuration._COMMAND or \
                RegisterAddress.REG_ADDRESS_CFG != configuration._STARTING_ADDRESS or \
                PacketLength.PL_CONFIGURATION != configuration._LENGTH:
            code = ResponseStatusCode.ERR_E220_HEAD_NOT_RECOGNIZED

        return code, configuration

    def get_module_information(self):
        code = self.check_UART_configuration(ModeType.MODE_3_PROGRAM)
        if code != ResponseStatusCode.E220_SUCCESS:
            return code, None

        prev_mode = self.mode
        code = self.set_mode(ModeType.MODE_3_PROGRAM)
        if code != ResponseStatusCode.E220_SUCCESS:
            return code, None

        self.write_program_command(
            ProgramCommand.READ_CONFIGURATION, RegisterAddress.REG_ADDRESS_PID, PacketLength.PL_PID)

        module_information = ModuleInformation()
        data = self.uart.read(4)
        if data is None or len(data) != 4:
            code = ResponseStatusCode.ERR_E220_DATA_SIZE_NOT_MATCH
            return code, None

        module_information.from_bytes(data)

        if code != ResponseStatusCode.E220_SUCCESS:
            self.set_mode(prev_mode)
            return code, None

        code = self.set_mode(prev_mode)
        if code != ResponseStatusCode.E220_SUCCESS:
            return code, None

        if ProgramCommand.WRONG_FORMAT == module_information._COMMAND:
            code = ResponseStatusCode.ERR_E220_WRONG_FORMAT
        if ProgramCommand.RETURNED_COMMAND != module_information._COMMAND or \
                RegisterAddress.REG_ADDRESS_PID != module_information._STARTING_ADDRESS or \
                PacketLength.PL_PID != module_information._LENGTH:
            code = ResponseStatusCode.ERR_E220_HEAD_NOT_RECOGNIZED

        return code, module_information

    def reset_module(self) -> ResponseStatusCode:
        code = ResponseStatusCode.ERR_E220_NOT_IMPLEMENT
        return code

    @staticmethod
    def _normalize_array(data):
        # Convert values to valid byte values
        for i in range(len(data)):
            if data[i] > 255:
                data[i] = data[i] % 256
        return data

    def receive_dict(self, rssi=False, delimiter=None, size=None) -> (ResponseStatusCode, any, int or None):
        code, msg, rssi_value = self.receive_message(rssi, delimiter, size)
        if code != ResponseStatusCode.E220_SUCCESS:
            return code, None, None

        try:
            msg = ujson.loads(msg)
        except Exception as e:
            logger.error("Error: {}".format(e))
            return ResponseStatusCode.ERR_E220_JSON_PARSE, None, None

        return code, msg, rssi_value

    def receive_message(self, rssi=False, delimiter=None, size=None):
        code = ResponseStatusCode.E220_SUCCESS
        rssi_value = None
        if delimiter is not None:
            data = self._read_until(delimiter)
            if rssi:
                rssi_value = data[-1]  # last byte is rssi
                data = data[:-1]  # remove rssi from data
        elif size is not None:
            data = self.uart.read(size)
        else:
            data = self.uart.read()
            self.clean_UART_buffer()
            if rssi:
                rssi_value = data[-1]  # last byte is rssi
                data = data[:-1]  # remove rssi from data

        if data is None or len(data) == 0:
            return (ResponseStatusCode.ERR_E220_DATA_SIZE_NOT_MATCH, None, None) \
                if rssi else (ResponseStatusCode.ERR_E220_DATA_SIZE_NOT_MATCH, None)

        data = data.decode('utf-8')
        msg = data

        return (code, msg, rssi_value) if rssi else (code, msg)

    def clean_UART_buffer(self):
        self.uart.read()

    def _read_until(self, terminator='\n') -> bytes:
        line = b''
        while True:
            c = self.uart.read(1)
            if c == terminator:
                break
            line += c
        return line

    def send_broadcast_message(self, CHAN, message) -> ResponseStatusCode:
        return self._send_message(message, BROADCAST_ADDRESS, BROADCAST_ADDRESS, CHAN)

    def send_broadcast_dict(self, CHAN, dict_message) -> ResponseStatusCode:
        message = ujson.dumps(dict_message)
        return self._send_message(message, BROADCAST_ADDRESS, BROADCAST_ADDRESS, CHAN)

    def send_transparent_message(self, message) -> ResponseStatusCode:
        return self._send_message(message)

    def send_fixed_message(self, ADDH, ADDL, CHAN, message) -> ResponseStatusCode:
        return self._send_message(message, ADDH, ADDL, CHAN)

    def send_fixed_dict(self, ADDH, ADDL, CHAN, dict_message) -> ResponseStatusCode:
        message = ujson.dumps(dict_message)
        return self._send_message(message, ADDH, ADDL, CHAN)

    def send_transparent_dict(self, dict_message) -> ResponseStatusCode:
        message = ujson.dumps(dict_message)
        return self._send_message(message)

    def _send_message(self, message, ADDH=None, ADDL=None, CHAN=None) -> ResponseStatusCode:
        result = ResponseStatusCode.E220_SUCCESS

        size_ = len(message.encode('utf-8'))
        if size_ > MAX_SIZE_TX_PACKET + 2:
            return ResponseStatusCode.ERR_E220_PACKET_TOO_BIG

        if ADDH is not None and ADDL is not None and CHAN is not None:
            if isinstance(message, str):
                message = message.encode('utf-8')
            dataarray = bytes([ADDH, ADDL, CHAN]) + message
            dataarray = LoRaE220._normalize_array(dataarray)
            lenMS = self.uart.write(bytes(dataarray))
            size_ += 3
        elif isinstance(message, str):
            lenMS = self.uart.write(message.encode('utf-8'))
        else:
            lenMS = self.uart.write(bytes(message))

        if lenMS != size_:
            logger.debug("Send... len:", lenMS, " size:", size_)
            if lenMS == 0:
                result = ResponseStatusCode.ERR_E220_NO_RESPONSE_FROM_DEVICE
            else:
                result = ResponseStatusCode.ERR_E220_DATA_SIZE_NOT_MATCH
        if result != ResponseStatusCode.E220_SUCCESS:
            return result

        result = self.wait_complete_response(1000)
        if result != ResponseStatusCode.E220_SUCCESS:
            return result
        logger.debug("Clear buffer...")
        self.clean_UART_buffer()

        logger.debug("ok!")
        return result

    def available(self) -> int:
        return self.uart.any()

    def end(self) -> ResponseStatusCode:
        try:
            if self.uart is not None:
                self.uart.deinit()
                del self.uart
            return ResponseStatusCode.E220_SUCCESS

        except Exception as E:
            logger.error("Error: {}".format(E))
            return ResponseStatusCode.ERR_E220_DEINIT_UART_FAILED
