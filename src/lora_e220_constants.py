class UARTParity:
    MODE_00_8N1 = 0b00
    MODE_01_8O1 = 0b01
    MODE_10_8E1 = 0b10
    MODE_11_8N1 = 0b11

    @staticmethod
    def get_description(uart_parity):
        if uart_parity == UARTParity.MODE_00_8N1:
            return "8N1 (Default)"
        elif uart_parity == UARTParity.MODE_01_8O1:
            return "8O1"
        elif uart_parity == UARTParity.MODE_10_8E1:
            return "8E1"
        elif uart_parity == UARTParity.MODE_11_8N1:
            return "8N1"
        else:
            return "Invalid UART Parity!"

    @staticmethod
    def get_uart_value(uart_parity):
        if uart_parity == UARTParity.MODE_00_8N1:
            return None
        elif uart_parity == UARTParity.MODE_01_8O1:
            return 0
        elif uart_parity == UARTParity.MODE_10_8E1:
            return 1
        elif uart_parity == UARTParity.MODE_11_8N1:
            return None
        else:
            return ValueError("Invalid UART Parity!")


class UARTBaudRate:
    BPS_1200 = 0b000
    BPS_2400 = 0b001
    BPS_4800 = 0b010
    BPS_9600 = 0b011
    BPS_19200 = 0b100
    BPS_38400 = 0b101
    BPS_57600 = 0b110
    BPS_115200 = 0b111

    @staticmethod
    def get_description(uart_baud_rate):
        if uart_baud_rate == UARTBaudRate.BPS_1200:
            return "1200bps"
        elif uart_baud_rate == UARTBaudRate.BPS_2400:
            return "2400bps"
        elif uart_baud_rate == UARTBaudRate.BPS_4800:
            return "4800bps"
        elif uart_baud_rate == UARTBaudRate.BPS_9600:
            return "9600bps (default)"
        elif uart_baud_rate == UARTBaudRate.BPS_19200:
            return "19200bps"
        elif uart_baud_rate == UARTBaudRate.BPS_38400:
            return "38400bps"
        elif uart_baud_rate == UARTBaudRate.BPS_57600:
            return "57600bps"
        elif uart_baud_rate == UARTBaudRate.BPS_115200:
            return "115200bps"
        else:
            return "Invalid UART Baud Rate!"


class AirDataRate:
    AIR_DATA_RATE_000_24 = 0b000
    AIR_DATA_RATE_001_24 = 0b001
    AIR_DATA_RATE_010_24 = 0b010
    AIR_DATA_RATE_011_48 = 0b011
    AIR_DATA_RATE_100_96 = 0b100
    AIR_DATA_RATE_101_192 = 0b101
    AIR_DATA_RATE_110_384 = 0b110
    AIR_DATA_RATE_111_625 = 0b111

    @staticmethod
    def get_description(air_data_rate):
        if air_data_rate == AirDataRate.AIR_DATA_RATE_000_24:
            return "2.4kbps"
        elif air_data_rate == AirDataRate.AIR_DATA_RATE_001_24:
            return "2.4kbps"
        elif air_data_rate == AirDataRate.AIR_DATA_RATE_010_24:
            return "2.4kbps (default)"
        elif air_data_rate == AirDataRate.AIR_DATA_RATE_011_48:
            return "4.8kbps"
        elif air_data_rate == AirDataRate.AIR_DATA_RATE_100_96:
            return "9.6kbps"
        elif air_data_rate == AirDataRate.AIR_DATA_RATE_101_192:
            return "19.2kbps"
        elif air_data_rate == AirDataRate.AIR_DATA_RATE_110_384:
            return "38.4kbps"
        elif air_data_rate == AirDataRate.AIR_DATA_RATE_111_625:
            return "62.5kbps"
        else:
            return "Invalid Air Data Rate!"


class SubPacketSetting:
    SPS_200_00 = 0b00
    SPS_128_01 = 0b01
    SPS_064_10 = 0b10
    SPS_032_11 = 0b11

    @staticmethod
    def get_description(sub_packet_setting):
        if sub_packet_setting == SubPacketSetting.SPS_200_00:
            return "200bytes (default)"
        elif sub_packet_setting == SubPacketSetting.SPS_128_01:
            return "128bytes"
        elif sub_packet_setting == SubPacketSetting.SPS_064_10:
            return "64bytes"
        elif sub_packet_setting == SubPacketSetting.SPS_032_11:
            return "32bytes"
        else:
            return "Invalid Sub Packet Setting!"


class RssiAmbientNoiseEnable:
    RSSI_AMBIENT_NOISE_ENABLED = 0b1
    RSSI_AMBIENT_NOISE_DISABLED = 0b0

    @staticmethod
    def get_description(rssi_ambient_noise_enabled):
        if rssi_ambient_noise_enabled == RssiAmbientNoiseEnable.RSSI_AMBIENT_NOISE_ENABLED:
            return "Enabled"
        elif rssi_ambient_noise_enabled == RssiAmbientNoiseEnable.RSSI_AMBIENT_NOISE_DISABLED:
            return "Disabled (default)"
        else:
            return "Invalid RSSI Ambient Noise enabled!"


class WorPeriod:
    WOR_500_000 = 0b000
    WOR_1000_001 = 0b001
    WOR_1500_010 = 0b010
    WOR_2000_011 = 0b011
    WOR_2500_100 = 0b100
    WOR_3000_101 = 0b101
    WOR_3500_110 = 0b110
    WOR_4000_111 = 0b111

    @staticmethod
    def get_description(wor_period):
        if wor_period == WorPeriod.WOR_500_000:
            return "500ms"
        elif wor_period == WorPeriod.WOR_1000_001:
            return "1000ms"
        elif wor_period == WorPeriod.WOR_1500_010:
            return "1500ms"
        elif wor_period == WorPeriod.WOR_2000_011:
            return "2000ms (default)"
        elif wor_period == WorPeriod.WOR_2500_100:
            return "2500ms"
        elif wor_period == WorPeriod.WOR_3000_101:
            return "3000ms"
        elif wor_period == WorPeriod.WOR_3500_110:
            return "3500ms"
        elif wor_period == WorPeriod.WOR_4000_111:
            return "4000ms"
        else:
            return "Invalid WOR period!"


class LbtEnableByte:
    LBT_ENABLED = 0b1
    LBT_DISABLED = 0b0

    @staticmethod
    def get_description(lbt_enable_byte):
        if lbt_enable_byte == LbtEnableByte.LBT_ENABLED:
            return "Enabled"
        elif lbt_enable_byte == LbtEnableByte.LBT_DISABLED:
            return "Disabled (default)"
        else:
            return "Invalid LBT enable byte!"



class RssiEnableByte:
    RSSI_ENABLED = 0b1
    RSSI_DISABLED = 0b0

    @staticmethod
    def get_description(rssi_enable_byte):
        if rssi_enable_byte == RssiEnableByte.RSSI_ENABLED:
            return "Enabled"
        elif rssi_enable_byte == RssiEnableByte.RSSI_DISABLED:
            return "Disabled (default)"
        else:
            return "Invalid RSSI enable byte!"


class FixedTransmission:
    TRANSPARENT_TRANSMISSION = 0b0
    FIXED_TRANSMISSION = 0b1

    @staticmethod
    def get_description(fixed_transmission):
        if fixed_transmission == FixedTransmission.TRANSPARENT_TRANSMISSION:
            return "Transparent transmission (default)"
        elif fixed_transmission == FixedTransmission.FIXED_TRANSMISSION:
            return "Fixed transmission (first three bytes can be used as high/low address and channel)"
        else:
            return "Invalid fixed transmission param!"


class TransmissionPower22:
    POWER_22 = 0b00
    POWER_17 = 0b01
    POWER_13 = 0b10
    POWER_10 = 0b11

    @staticmethod
    def get_description(transmission_power):
        if transmission_power == TransmissionPower22.POWER_22:
            return "22dBm (Default)"
        elif transmission_power == TransmissionPower22.POWER_17:
            return "17dBm"
        elif transmission_power == TransmissionPower22.POWER_13:
            return "13dBm"
        elif transmission_power == TransmissionPower22.POWER_10:
            return "10dBm"
        else:
            return "Invalid transmission power param"

    @staticmethod
    def get_default_value():
        return TransmissionPower22.POWER_22


class TransmissionPower30:
    POWER_30 = 0b00
    POWER_27 = 0b01
    POWER_24 = 0b10
    POWER_21 = 0b11

    @staticmethod
    def get_description(transmission_power):
        if transmission_power == TransmissionPower30.POWER_30:
            return "30dBm (Default)"
        elif transmission_power == TransmissionPower30.POWER_27:
            return "27dBm"
        elif transmission_power == TransmissionPower30.POWER_24:
            return "24dBm"
        elif transmission_power == TransmissionPower30.POWER_21:
            return "21dBm"
        else:
            return "Invalid transmission power param"

    @staticmethod
    def get_default_value():
        return TransmissionPower30.POWER_30


# here a class that contains the starting frequency of the different devices
# the device 433 start with 410 frequency and so on
class OperatingFrequency:
    FREQUENCY_433 = 410
    FREQUENCY_400 = 410
    FREQUENCY_170 = 130
    FREQUENCY_230 = 220
    FREQUENCY_470 = 370
    FREQUENCY_868 = 850
    FREQUENCY_900 = 850
    FREQUENCY_915 = 900

    @staticmethod
    def get_value_from_frequency(frequency):
        if not isinstance(frequency, str):
            frequency = str(frequency)

        freq_attr_name = 'FREQUENCY_' + frequency
        freq_value = getattr(OperatingFrequency, freq_attr_name)
        return freq_value

    @staticmethod
    def get_frequency_dict():
        frequency_dict = {name.split("_")[1]: value for name, value in vars(OperatingFrequency).items() if name.startswith('FREQUENCY_')}
        return frequency_dict

    # the frequency is the base element plus the channel
    @staticmethod
    def get_freq_from_channel(device_frequency, channel):
        return OperatingFrequency.get_value_from_frequency(device_frequency) + channel


# model is like 433T20D or 433T27D or 433T30D or 868T20S or 868T27S or 868T30S
# the part before T is the frequency (example 433)
# the part after T is the transmission power (example 20)
# the last letter is the package type, D is for discrete S is for SMD  (example D)
class TransmissionPower:
    def __init__(self, model):
        self.model = model
        self.package_type = None
        self.frequency = None
        self.transmission_power = None

        if model is not None:
            self.package_type = model[6]
            self.frequency = int(model[0:3])
            self.transmission_power = int(model[4:6])

    def get_transmission_power(self):
        if self.transmission_power == self.transmission_power:
            return TransmissionPower22
        elif self.transmission_power == self.transmission_power:
            return TransmissionPower30
        else:
            return "Invalid transmission power param"

    def get_transmission_power_description(self, transmission_power):
        return self.get_transmission_power().get_description(transmission_power)
