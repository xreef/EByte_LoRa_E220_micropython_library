# Author: Renzo Mischianti
# Website: www.mischianti.org
#
# Description:
# This script demonstrates how to use the E220 LoRa module with MicroPython.
# Sending dictionary
#
# Note: This code was written and tested using MicroPython on an ESP32 board.
#       It works with other boards, but you may need to change the UART pins.

from machine import UART

from lora_e220 import LoRaE220, Configuration
from lora_e220_constants import RssiAmbientNoiseEnable, RssiEnableByte
from lora_e220_operation_constant import ResponseStatusCode

# Initialize the LoRaE220 module
uart2 = UART(2)
lora = LoRaE220('400T22D', uart2, aux_pin=15, m0_pin=21, m1_pin=19)
code = lora.begin()
print("Initialization: {}", ResponseStatusCode.get_description(code))

# Set the configuration to default values and print the updated configuration to the console
# Not needed if already configured
configuration_to_set = Configuration('400T22D')
# To enable RSSI, you must also enable RSSI on receiver
configuration_to_set.TRANSMISSION_MODE.enableRSSI = RssiEnableByte.RSSI_ENABLED
code, confSetted = lora.set_configuration(configuration_to_set)
print("Set configuration: {}", ResponseStatusCode.get_description(code))

# Send a dictionary message (transparent)
data = {'key1': 'value1', 'key2': 'value2'}
code = lora.send_transparent_dict(data)
print("Send message: {}", ResponseStatusCode.get_description(code))
