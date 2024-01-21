# Author: Renzo Mischianti
# Website: www.mischianti.org
#
# Description:
# This script demonstrates how to use the E220 LoRa module with MicroPython.
# It initializes the module, retrieves the current configuration,
# sets a new configuration, and restores the default configuration.
# It also includes examples of sending and receiving data using the module.
#
# Note: This code was written and tested using MicroPython on a ESP32 board.
#       It works with other boards, but you may need to change the UART pins.

from lora_e220 import LoRaE220, print_configuration, Configuration
from lora_e220_constants import OperatingFrequency, FixedTransmission, TransmissionPower, \
    AirDataRate, UARTParity, UARTBaudRate, RssiAmbientNoiseEnable, SubPacketSetting, WorPeriod, \
    LbtEnableByte, RssiEnableByte, TransmissionPower22
from lora_e220_operation_constant import ResponseStatusCode
from machine import UART

# Create a UART object to communicate with the LoRa module with ESP32
uart2 = UART(2)
# Create a LoRaE220 object, passing the UART object and pin configurations
lora = LoRaE220('433T20D', uart2, aux_pin=15, m0_pin=21, m1_pin=19)

# Create a UART object to communicate with the LoRa module with Raspberry Pi Pico
# uart2 = UART(1)
# Use the Serial1 pins of Arduino env on the Raspberry Pi Pico
# uart2 = UART(1, rx=Pin(9), tx=Pin(8))
# lora = LoRaE220('433T20D', uart2, aux_pin=2, m0_pin=10, m1_pin=11)
# STM32F411CEU6 Shield
# uart2 = UART(2)
# lora = LoRaE220('400T22D', uart2, aux_pin='PA0', m0_pin='PB0', m1_pin='PB2')

# Initialize the LoRa module and print the initialization status code
code = lora.begin()
print("Initialization: {}", ResponseStatusCode.get_description(code))

##########################################################################################
# GET CONFIGURATION
##########################################################################################

# Retrieve the current configuration of the LoRa module and print it to the console
code, configuration = lora.get_configuration()
print("Retrieve configuration: {}", ResponseStatusCode.get_description(code))
print("------------- CONFIGURATION BEFORE CHANGE -------------")
print_configuration(configuration)

##########################################################################################
# SET CONFIGURATION
# To set the configuration, you must set the configuration with the new values
##########################################################################################

# Create a new Configuration object with the desired settings
configuration_to_set = Configuration('400T22D')
configuration_to_set.ADDL = 0x02
configuration_to_set.ADDH = 0x01
configuration_to_set.CHAN = 23

configuration_to_set.SPED.airDataRate = AirDataRate.AIR_DATA_RATE_100_96
configuration_to_set.SPED.uartParity = UARTParity.MODE_00_8N1
configuration_to_set.SPED.uartBaudRate = UARTBaudRate.BPS_9600

configuration_to_set.OPTION.transmissionPower = TransmissionPower('400T22D').\
                                                    get_transmission_power().POWER_10
# or
# configuration_to_set.OPTION.transmissionPower = TransmissionPower22.POWER_10

configuration_to_set.OPTION.RSSIAmbientNoise = RssiAmbientNoiseEnable.RSSI_AMBIENT_NOISE_ENABLED
configuration_to_set.OPTION.subPacketSetting = SubPacketSetting.SPS_064_10

configuration_to_set.TRANSMISSION_MODE.fixedTransmission = FixedTransmission.FIXED_TRANSMISSION
configuration_to_set.TRANSMISSION_MODE.WORPeriod = WorPeriod.WOR_1500_010
configuration_to_set.TRANSMISSION_MODE.enableLBT = LbtEnableByte.LBT_DISABLED
configuration_to_set.TRANSMISSION_MODE.enableRSSI = RssiEnableByte.RSSI_ENABLED

configuration_to_set.CRYPT.CRYPT_H = 1
configuration_to_set.CRYPT.CRYPT_L = 1


# Set the new configuration on the LoRa module and print the updated configuration to the console
code, confSetted = lora.set_configuration(configuration_to_set)
print("------------- CONFIGURATION AFTER CHANGE -------------")
print(ResponseStatusCode.get_description(code))
print_configuration(confSetted)

##########################################################################################
# RESTORE DEFAULT CONFIGURATION
# To restore the default configuration, you must set the configuration with the default values
##########################################################################################

# Set the configuration to default values and print the updated configuration to the console
print("------------- RESTORE ALL DEFAULT -------------")
configuration_to_set = Configuration('400T22D')
code, confSetted = lora.set_configuration(configuration_to_set)
print(ResponseStatusCode.get_description(code))
print_configuration(confSetted)


# Initialization: {} Success
# Retrieve configuration: {} Success
# ------------- CONFIGURATION BEFORE CHANGE -------------
# ----------------------------------------
# HEAD :  0xc1   0x0   0x8
#
# AddH :  0x0
# AddL :  0x0
#
# Chan :  0  ->  410
#
# SpeedParityBit :  0b0  ->  8N1 (Default)
# SpeedUARTDatte :  0b11  ->  9600bps (default)
# SpeedAirDataRate :  0b10  ->  2.4kbps (default)
#
# OptionSubPacketSett:  0b0  ->  200bytes (default)
# OptionTranPower :  0b0  ->  22dBm (Default)
# OptionRSSIAmbientNo:  0b0  ->  Disabled (default)
#
# TransModeWORPeriod :  0b11  ->  2000ms (default)
# TransModeEnableLBT :  0b0  ->  Disabled (default)
# TransModeEnableRSSI:  0b0  ->  Disabled (default)
# TransModeFixedTrans:  0b0  ->  Transparent transmission (default)
# ----------------------------------------
# ------------- CONFIGURATION AFTER CHANGE -------------
# Success
# ----------------------------------------
# HEAD :  0xc1   0x0   0x8
#
# AddH :  0x1
# AddL :  0x2
#
# Chan :  23  ->  433
#
# SpeedParityBit :  0b0  ->  8N1 (Default)
# SpeedUARTDatte :  0b11  ->  9600bps (default)
# SpeedAirDataRate :  0b100  ->  9.6kbps
#
# OptionSubPacketSett:  0b10  ->  64bytes
# OptionTranPower :  0b11  ->  10dBm
# OptionRSSIAmbientNo:  0b1  ->  Enabled
#
# TransModeWORPeriod :  0b10  ->  1500ms
# TransModeEnableLBT :  0b0  ->  Disabled (default)
# TransModeEnableRSSI:  0b1  ->  Enabled
# TransModeFixedTrans:  0b1  ->  Fixed transmission (first three bytes can be used
#  as high/low address and channel)
# ----------------------------------------
# ------------- RESTORE ALL DEFAULT -------------
# Success
# ----------------------------------------
# HEAD :  0xc1   0x0   0x8
#
# AddH :  0x0
# AddL :  0x0
#
# Chan :  0  ->  410
#
# SpeedParityBit :  0b0  ->  8N1 (Default)
# SpeedUARTDatte :  0b11  ->  9600bps (default)
# SpeedAirDataRate :  0b10  ->  2.4kbps (default)
#
# OptionSubPacketSett:  0b0  ->  200bytes (default)
# OptionTranPower :  0b0  ->  22dBm (Default)
# OptionRSSIAmbientNo:  0b0  ->  Disabled (default)
#
# TransModeWORPeriod :  0b11  ->  2000ms (default)
# TransModeEnableLBT :  0b0  ->  Disabled (default)
# TransModeEnableRSSI:  0b0  ->  Disabled (default)
# TransModeFixedTrans:  0b0  ->  Transparent transmission (default)
# ----------------------------------------
