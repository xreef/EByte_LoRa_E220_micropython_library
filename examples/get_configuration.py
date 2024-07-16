# Author: Renzo Mischianti
# Website: www.mischianti.org
#
# Description:
# This script initializes the E220 LoRa module with MicroPython,
# retrieves the current configuration, and prints it to the console.
# The code demonstrates how to use the LoRaE220 library to interact with the module and read its configuration.
#
# Note: This code was written and tested using MicroPython on an ESP32 board.
#       It works with other boards, but you may need to change the UART pins.


from machine import UART

from lora_e220 import LoRaE220, print_configuration
from lora_e220_operation_constant import ResponseStatusCode

# Create a UART object to communicate with the LoRa module with ESP32
uart2 = UART(2)
# Create a LoRaE220 object, passing the UART object and pin configurations
lora = LoRaE220('400T22D', uart2, aux_pin=15, m0_pin=21, m1_pin=19)

# Create a UART object to communicate with the LoRa module with Raspberry Pi Pico
# uart2 = UART(1)
# Use the Serial1 pins of Arduino env on the Raspberry Pi Pico
# uart2 = UART(1, rx=Pin(9), tx=Pin(8))
# lora = LoRaE220('400T22D', uart2, aux_pin=2, m0_pin=10, m1_pin=11)
# STM32F411CEU6 Shield
# uart2 = UART(2)
# lora = LoRaE220('400T22D', uart2, aux_pin='PA0', m0_pin='PB0', m1_pin='PB2')

code = lora.begin()
print("Initialization: {}", ResponseStatusCode.get_description(code))

code, configuration = lora.get_configuration()

print("Retrieve configuration: {}", ResponseStatusCode.get_description(code))

print_configuration(configuration)

#
# Initialization: {} Success
# Retrieve configuration: {} Success
# ----------------------------------------
# HEAD :  0xc1   0x0   0x8
#
# AddH :  0x0
# AddL :  0x0
#
# Chan :  23  ->  433
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
