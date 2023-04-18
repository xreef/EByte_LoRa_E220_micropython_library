<div>
<a href="https://www.mischianti.org/forums/forum/mischiantis-libraries/ebyte-lora-e220-uart-devices-llcc68/"><img
  src="https://github.com/xreef/LoRa_E32_Series_Library/raw/master/resources/buttonSupportForumEnglish.png" alt="Support forum EByte e220 English"
   align="right"></a>
</div>
<div>
<a href="https://www.mischianti.org/it/forums/forum/le-librerie-di-mischianti/ebyte-e220-dispositivi-lora-uart-llcc68/"><img
  src="https://github.com/xreef/LoRa_E32_Series_Library/raw/master/resources/buttonSupportForumItaliano.png" alt="Forum supporto EByte e220 italiano"
  align="right"></a>
</div>


</br></br>

# EBYTE LoRa E220 devices micropython library (LLCC68)   


### Changelog
 - 2023-04-18 0.0.3 Fix regular expression models
 - 2023-04-18 0.0.2 Distinct frequency from 900MHz and 915Mhz devices [Forum](https://www.mischianti.org/forums/topic/e32-915t-and-e32-900t-modules/)
 - 2023-03-21 0.0.1 Fully functional library

### Installation
To install the library execute the following command:

```bash
pip install ebyte-lora-e220
```

### Library usage
Here an example of constructor, you must pass the UART interface and (if you want, but It's reccomended)
the AUX pin, M0 and M1.

#### Initialization

```python
from lora_e220 import LoRaE220
from machine import UART

uart2 = UART(2)
lora = LoRaE220('400T22D', uart2, aux_pin=15, m0_pin=21, m1_pin=19)
```
#### Start the module transmission

```python
code = lora.begin()
print("Initialization: {}", ResponseStatusCode.get_description(code))
```

#### Get Configuration

```python
from lora_e220 import LoRaE220, print_configuration
from lora_e220_operation_constant import ResponseStatusCode

code, configuration = lora.get_configuration()

print("Retrieve configuration: {}", ResponseStatusCode.get_description(code))

print_configuration(configuration)
```

The result

```
----------------------------------------
Initialization: {} Success
Retrieve configuration: {} Success
----------------------------------------
HEAD :  0xc1   0x0   0x8
AddH :  0x0
AddL :  0x0
Chan :  23  ->  433
SpeedParityBit :  0b0  ->  8N1 (Default)
SpeedUARTDatte :  0b11  ->  9600bps (default)
SpeedAirDataRate :  0b10  ->  2.4kbps (default)
OptionSubPacketSett:  0b0  ->  200bytes (default)
OptionTranPower :  0b0  ->  22dBm (Default)
OptionRSSIAmbientNo:  0b0  ->  Disabled (default)
TransModeWORPeriod :  0b11  ->  2000ms (default)
TransModeEnableLBT :  0b0  ->  Disabled (default)
TransModeEnableRSSI:  0b0  ->  Disabled (default)
TransModeFixedTrans:  0b0  ->  Transparent transmission (default)
----------------------------------------
```

#### Set Configuration

You can set only the desidered parameter, the other will be set to default value.
```python
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
```

I create a CONSTANTS class for each parameter, here a list:
AirDataRate, UARTBaudRate, UARTParity, TransmissionPower, ForwardErrorCorrectionSwitch, WirelessWakeUpTime, IODriveMode, FixedTransmission

#### Send string message

Here an example of send data, you can pass a string 
```python
lora.send_transparent_message('pippo')
```

```python
lora.send_fixed_message(0, 2, 23, 'pippo')
```
Here the receiver code
```python
while True:
    if lora.available() > 0:
        code, value = lora.receive_message()
        print(ResponseStatusCode.get_description(code))

        print(value)
        utime.sleep_ms(2000)
```

If you want receive RSSI also you must enable it in the configuration
```python
configuration_to_set.TRANSMISSION_MODE.enableRSSI = RssiEnableByte.RSSI_ENABLED
```

and set the flag to True in the receive_message method
```python
code, value, rssi = lora.receive_message(True)
```



Result

```
Success!
pippo
```

#### Send dictionary message

Here an example of send data, you can pass a dictionary
```python
lora.send_transparent_dict({'pippo': 'fixed', 'pippo2': 'fixed2'})
```

```python
lora.send_fixed_dict(0, 0x01, 23, {'pippo': 'fixed', 'pippo2': 'fixed2'})
```

Here the receiver code
```python
while True:
    if lora.available() > 0:
        code, value = lora.receive_dict()
        print(ResponseStatusCode.get_description(code))
        print(value)
        print(value['pippo'])
        utime.sleep_ms(2000)
```

if you want receive RSSI also you must enable it in the configuration
```python
configuration_to_set.TRANSMISSION_MODE.enableRSSI = RssiEnableByte.RSSI_ENABLED
```

and set the flag to True in the receive_dict method
```python
code, value, rssi = lora.receive_dict(True)
```


Result

```
Success!
{'pippo': 'fixed', 'pippo2': 'fixed2'}
fixed
```


# This is a porting of the Arduino library for EBYTE LoRa E220 devices to Micropython

## Tutorial of the original library  

- [Ebyte LoRa E220 device for Arduino, esp32 or esp8266: settings and basic usage](https://www.mischianti.org/2022/03/11/ebyte-lora-e220-llcc68-device-for-arduino-esp32-or-esp8266-specs-and-basic-use-1/)
- [Ebyte LoRa E220 device for Arduino, esp32 or esp8266: library](https://www.mischianti.org/2022/03/17/ebyte-lora-e220-llcc68-device-for-arduino-esp32-or-esp8266-library-2/)
- [Ebyte LoRa E220 device for Arduino, esp32 or esp8266: configuration](https://www.mischianti.org/2022/04/19/ebyte-lora-e220-llcc68-device-for-arduino-esp32-or-esp8266-configuration-3/)
- [Ebyte LoRa E220 device for Arduino, esp32 or esp8266: fixed transmission, broadcast, monitor, and RSSI](https://www.mischianti.org/2022/04/27/ebyte-lora-e220-device-for-arduino-esp32-or-esp8266-fixed-transmission-broadcast-monitor-and-rssi-4/)
- [Ebyte LoRa E220 device for Arduino, esp32 or esp8266: power saving and sending structured data](https://www.mischianti.org/2022/05/06/ebyte-lora-e220-device-for-arduino-esp32-or-esp8266-manage-wake-on-radio-and-sends-structured-data-5/)
- Ebyte LoRa E220 device for Arduino, esp32 or esp8266: WOR microcontroller and Arduino shield
- Ebyte LoRa E220 device for Arduino, esp32 or esp8266: WOR microcontroller and WeMos D1 shield
- Ebyte LoRa E220 device for Arduino, esp32 or esp8266: WOR microcontroller and esp32 dev v1 shield



<h2>LLCC68 </h2>



<p>LoRa Smart Home (LLCC68) is a sub-GHz LoRa® RF Transceiver for medium-range indoor and indoor to outdoor wireless applications. SPI interface. Pin-to-pin is compatible with SX1262. SX1261, SX1262, SX1268, and LLCC68 are designed for long battery life with just 4.2 mA of active receive current consumption. The SX1261 can transmit up to +15 dBm, and the SX1262, SX1268, and LLCC68 can transmit up to +22 dBm with highly efficient integrated power&nbsp;amplifiers.</p>



<div class="wp-block-image">
<img src="https://www.mischianti.org/wp-content/uploads/2021/12/EByte-LoRa-E220-LLCC68-photo-3-devices-red-520x331.jpg"/>
</div>



<p>These devices support LoRa modulation for LPWAN use cases and (G)FSK modulation for legacy use cases. The devices are highly configurable to meet different application requirements for consumer use. The device provides LoRa modulation compatible with Semtech transceivers used by the LoRaWAN® specification released by the LoRa Alliance®. The radio is suitable for systems targeting compliance with radio regulations, including but not limited to ETSI EN 300 220, FCC CFR 47 Part 15, China regulatory requirements, and the Japanese ARIB T-108. Continuous frequency coverage from 150MHz to 960MHz allows the support of all major sub-GHz ISM bands around the world.</p>



<h2>Features</h2>



<ul><li>The new LoRa spread spectrum modulation technology developed based on LLCC68, it brings a more extended communication distance and stronger anti-interference ability;</li><li>Support users to set the communication key by themselves, and it cannot be read, which significantly improves the confidentiality of user data;</li><li>Support LBT function, monitor the channel environment noise before sending, which significantly improves the communication success rate of the module in harsh environments;</li><li>Support RSSI signal strength indicator function for evaluating signal quality, improving communication network, and ranging;</li><li>Support air wakeup, that is ultra-low power consumption, suitable for battery-powered applications;</li><li>Support point to point transmission, broadcast transmission, channel sense;</li><li>Support deep sleep, the power consumption of the whole machine is about 5uA in this mode;</li><li>The module has built-in PA+LNA, and the communication distance can reach 5km under ideal conditions;</li><li>The parameters are saved after power-off, and the module will work according to the set parameters after power-on;</li><li>Efficient watchdog design, once an exception occurs, the module will automatically restart and continue to work according to the previous parameter settings;</li><li>Support the bit rate of2.4k～62.5kbps;</li><li>Support 3.0～5.5V power supply, power supply greater than 5V can guarantee the best performance;</li><li>Industrial standard design, supporting long-term use at -40～+85℃;</li></ul>



<h2>Comparison</h2>



<figure class="wp-block-table mischianti-table-left"><table class="has-pale-ocean-gradient-background has-background"><thead><tr><th></th><th>LLCC68</th><th>SX1278-SX1276</th></tr></thead><tbody><tr><td>Distance</td><td>&gt; 11Km</td><td>8Km</td></tr><tr><td>Rate (LoRa)</td><td>1.76Kbps – 62.5Kbps </td><td>0.3Kbps – 19.2Kbps</td></tr><tr><td>Sleep power consumption</td><td>2µA </td><td>5µA</td></tr></tbody></table></figure>



<h1>Library</h1>



<p>Library for Ebyte LoRa E220 LLCC68 device for Arduino, esp32 or esp8266. </p>



<h2>Pinout</h2>



<div class="wp-block-image">
<img src="https://www.mischianti.org/wp-content/uploads/2019/09/sx1278-sx1276-wireless-lora-uart-module-serial-3000m-arduino-433-rf-robotedu-1705-13-robotedu@101.jpg"/>
</div>



<figure class="wp-block-table mischianti-table-left"><table class="has-very-light-gray-to-cyan-bluish-gray-gradient-background has-background"><thead><tr><th>Pin No.</th><th>Pin item</th><th>Pin direction</th><th>Pin application</th></tr></thead><tbody><tr><td>1</td><td>M0</td><td>Input（weak pull-up）</td><td>Work with M1 &amp; decide the four operating modes. Floating is not allowed; it can be ground.</td></tr><tr><td>2</td><td>M1</td><td>Input（weak pull-up）</td><td>Work with M0 &amp; decide the four operating modes. Floating is not allowed; it can be ground.</td></tr><tr><td>3</td><td>RXD</td><td>Input</td><td>TTL UART inputs connect to external (MCU, PC) TXD output pin. It can be configured as open-drain or pull-up input.</td></tr><tr><td>4</td><td>TXD</td><td>Output</td><td>TTL UART outputs connect to external RXD (MCU, PC) input pin. Can be configured as open-drain or push-pull output</td></tr><tr><td><br>5</td><td><br>AUX</td><td><br>Output</td><td>To indicate the module’s working status &amp; wake up the external MCU. During the procedure of self-check initialization, the pin outputs a low level. It can be configured as open-drain or push-pull output (floating is allowed).</td></tr><tr><td>6</td><td>VCC</td><td></td><td>Power supply 3V~5.5V DC</td></tr><tr><td>7</td><td>GND</td><td></td><td>Ground</td></tr></tbody></table></figure>



<p>As you can see, you can set various modes via M0 and M1 pins.</p>



<figure class="wp-block-table is-style-stripes mischianti-table-left"><table class="has-very-light-gray-to-cyan-bluish-gray-gradient-background has-background"><thead><tr><th><strong>Mode</strong></th><th><strong>M1</strong></th><th><strong>M0</strong></th><th><strong>Explanation</strong></th></tr></thead><tbody><tr><td>Normal</td><td>0</td><td>0</td><td>UART and wireless channels are open, and transparent transmission is on</td></tr><tr><td>WOR Transmitter</td><td>0</td><td>1</td><td>WOR Transmitter</td></tr><tr><td>WOR Receiver</td><td>1</td><td>0</td><td>WOR Receiver (Supports wake up over air)</td></tr><tr><td>Deep sleep mode</td><td>1</td><td>1</td><td>The module goes to sleep (automatically wake up when configuring parameters)</td></tr></tbody></table></figure>



<p> Some pins can be used statically, but If you connect them to the microcontroller and configure them in the library, you gain in performance and can control all modes via software. Still, we are going to explain better next.</p>



<h1>Fully connected schema</h1>



<p>As I already said, It’s not essential to connect all pins to the microcontroller’s output; you can put M0 and M1 pins to HIGH or LOW to get the desired configuration. If<strong> you don’t connect AUX, the library set a reasonable delay to ensure that the operation is complete</strong> (<strong>If you have trouble</strong> with the <strong>device <strong>freezing</strong>, </strong> <strong>you must put a pull-up 4.7k resistor or better connect to the device.</strong> ).</p>



<h2>AUX pin</h2>



<p>When transmitting data can be used to wake up external MCU and return HIGH on data transfer finish.</p>



<div class="wp-block-image">
<img src="https://www.mischianti.org/wp-content/uploads/2019/10/e32auxPinOnTransmission-1024x269.jpg"/>
</div>



<p>When receiving, AUX goes LOW and returns HIGH when the buffer is empty.</p>



<div class="wp-block-image"><img src="https://www.mischianti.org/wp-content/uploads/2019/10/e32auxPinOnReception-1024x342.jpg"/></div>



<p>It’s also used for self-checking to restore regular operation (on power-on and sleep/program mode).</p>



<div class="wp-block-image">
<img src="https://www.mischianti.org/wp-content/uploads/2019/10/e32auxPinOnSelfCheck-1024x312.jpg"/>
</div>



<h2> esp8266 </h2>



<p>esp8266 connection schema is more straightforward because it works at the same voltage of logical communications (3.3v).</p>



<div class="wp-block-image">
<img src="https://www.mischianti.org/wp-content/uploads/2019/10/LoRa_E32-TTL-100_WemosD1_VD_PU_FullyConnected_bb-e1570517387323.jpg"/>
</div>



<p>It’s essential to add a pull-up resistor (4,7Kohm) to get good stability.</p>



<figure class="wp-block-table mischianti-table-left"><table><thead><tr><th>E22</th><th>esp8266</th></tr></thead><tbody><tr><td>M0</td><td>D7</td></tr><tr><td>M1</td><td>D6</td></tr><tr><td>TX</td><td>PIN D2 (PullUP 4,7KΩ)</td></tr><tr><td>RX</td><td>PIN D3 (PullUP 4,7KΩ)</td></tr><tr><td>AUX</td><td>PIN D5 (PullUP 4,7KΩ)</td></tr><tr><td>VCC</td><td>5V (but work with less power in 3.3v)</td></tr><tr><td>GND</td><td>GND</td></tr><tr><td></td><td></td></tr></tbody></table></figure>



<h2>esp32</h2>



<p>Similar connection schema for esp32, but for RX and TX, we use RX2 and TX2 because, by default, esp32 doesn’t have SoftwareSerial but has 3 Serial.</p>



<div class="wp-block-image">
<img src="https://www.mischianti.org/wp-content/uploads/2020/08/Ebyte-LoRa-E22-device-esp32-dev-kit-v1-breadboard-full-connection-768x668.jpg"/>
</div>



<figure class="wp-block-table mischianti-table-left"><table><thead><tr><th>E22</th><th>esp32</th></tr></thead><tbody><tr><td>M0</td><td>D21</td></tr><tr><td>M1</td><td>D19</td></tr><tr><td>TX</td><td>PIN RX2 (PullUP 4,7KΩ)</td></tr><tr><td>RX</td><td>PIN TX3 (PullUP 4,7KΩ)</td></tr><tr><td>AUX</td><td>PIN D18 (PullUP 4,7KΩ) (D15 to wake up)</td></tr><tr><td>VCC</td><td>5V (but work with less power in 3.3v)</td></tr><tr><td>GND</td><td>GND</td></tr><tr><td></td><td></td></tr></tbody></table></figure>



<h2>Arduino MKR WiFi 1010 </h2>



<div class="wp-block-image"><img src="https://www.mischianti.org/wp-content/uploads/2021/12/Ebyte_LoRa_Exx_Arduino_MKR_WiFi_1010_Fully_connected_breadboard-520x450.jpg"/></div>



<figure class="wp-block-table mischianti-table-left"><table><tbody><tr><td>M0</td><td>2 (voltage divider)</td></tr><tr><td>M1</td><td>3 (voltage divider)</td></tr><tr><td>TX</td><td>PIN 14 Tx (PullUP 4,7KΩ)</td></tr><tr><td>RX</td><td>PIN 13 Rx (PullUP 4,7KΩ)</td></tr><tr><td>AUX</td><td>PIN 1 (PullUP 4,7KΩ)</td></tr><tr><td>VCC</td><td>5V</td></tr><tr><td>GND</td><td>GND</td></tr></tbody></table></figure>





# An Arduino UNO shield to simplify the use
![Arduino UNO shield](https://www.mischianti.org/wp-content/uploads/2019/12/ArduinoShieldMountedE32LoRa_min.jpg)

You can order the PCB  [here](https://www.pcbway.com/project/shareproject/LoRa_E32_Series_device_Arduino_shield.html) 

Instruction and assembly video on 6 part of the guide

# An WeMos D1 shield to simplify the use
![Arduino UNO shield](https://www.mischianti.org/wp-content/uploads/2020/01/WeMosD1ShieldMountedE32LoRa_min.jpg)

You can order the PCB  [here](https://www.pcbway.com/project/shareproject/LoRa_E32_Series_device_WeMos_D1_mini_shield_RF_8km_range.html) 

Instruction and assembly video on 6 part of the guide



# Ebyte LoRa E220 LLCC68 device for Arduino, esp32 or esp8266: library



<div class="amp-wp-article-content">
		<br>
<p><strong><strong>LoRa or Long Range wireless data telemetry</strong> </strong>is a technology pioneered by Semtech that operates at a lower frequency than NRF24L01 (433 MHz, 868 MHz, or 916 MHz against 2.4 GHz for the NRF24L01) but at thrice the distance (from 5000m to 11000m).  </p>


      

<div class="mischianti-forum-button-container">
  	<a class="mischianti-forum-button" href="https://www.mischianti.org/forums/forum/mischiantis-libraries/ebyte-lora-e220-uart-devices-llcc68/" target="_blank">Support Forum</a>
</div>



<div class="wp-block-image">
<img src="https://www.mischianti.org/wp-content/uploads/2021/12/Ebyte-LoRa-E220-LLCC68-device-for-Arduino-esp32-or-esp8266-library-520x280.jpg"/>
</div>


<h2>Basic configuration option</h2>



<figure class="wp-block-table mischianti-table-left"><table class="has-electric-grass-gradient-background has-background"><thead><tr><th>Name</th><th>Description</th><th>Address</th></tr></thead><tbody><tr><td>ADDH</td><td>High address byte of the module (the default 00H)</td><td>00H</td></tr><tr><td>ADDL</td><td>Low address byte of the module (the default 00H)</td><td>01H</td></tr><tr><td>SPED</td><td>Information about data rate parity bit and Air data rate</td><td>02H</td></tr><tr><td>OPTION</td><td> Type of transmission, packet size, allow the special message </td><td>03H </td></tr><tr><td>CHAN</td><td>Communication channel（410M + CHAN*1M）, default 17H (433MHz),&nbsp;<strong>valid only for 433MHz device</strong>&nbsp;check below to check the correct frequency of your device</td><td>04H</td></tr><tr><td>OPTION</td><td>Type of transmission, packet size, allow the special message</td><td>05H</td></tr><tr><td>TRANSMISSION_MODE</td><td>A lot of parameters that specify the transmission modality</td><td>06H</td></tr><tr><td>CRYPT</td><td>Encryption to avoid interception</td><td>07H</td></tr></tbody></table></figure>



<h3>SPED detail</h3>



<p>UART Parity bit: <em>UART mode can be different between communication parties</em></p>



<figure class="wp-block-table mischianti-table-left"><table class="has-electric-grass-gradient-background has-background"><thead><tr><th>UART parity bit</th><th>Constant value</th></tr></thead><tbody><tr><td>8N1 (default)</td><td>MODE_00_8N1</td></tr><tr><td>8O1</td><td>MODE_01_8O1</td></tr><tr><td>8E1</td><td>MODE_10_8E1</td></tr><tr><td>8N1 (equal to 00)</td><td>MODE_11_8N1</td></tr></tbody></table></figure>



<p>UART baud rate: UART baud rate can be different between communication parties (but not reccomended). The UART baud rate has nothing to do with wireless transmission parameters &amp; won’t affect the wireless transmit/receive features.</p><div class="code-block code-block-10 ai-viewport-2 ai-viewport-3 amp-wp-a750a3a" data-amp-original-style="margin: 8px auto; text-align: center; clear: both;">
</div>
<div class="code-block code-block-9 ai-viewport-1 amp-wp-a750a3a" data-amp-original-style="margin: 8px auto; text-align: center; clear: both;">
</div>




<figure class="wp-block-table mischianti-table-left"><table class="has-electric-grass-gradient-background has-background"><thead><tr><th>TTL UART baud rate（bps）</th><th>Constant value</th></tr></thead><tbody><tr><td>1200</td><td>UART_BPS_1200</td></tr><tr><td>2400</td><td>UART_BPS_2400</td></tr><tr><td>4800</td><td>UART_BPS_4800</td></tr><tr><td>9600 (default)</td><td>UART_BPS_9600</td></tr><tr><td>19200</td><td>UART_BPS_19200</td></tr><tr><td>38400</td><td>UART_BPS_38400</td></tr><tr><td>57600</td><td>UART_BPS_57600</td></tr><tr><td>115200</td><td>UART_BPS_115200</td></tr></tbody></table></figure>



<p>Air data rate: The lower the air data rate, the longer the transmitting distance,      better anti-interference performance, and longer transmitting time; the air data rate must be constant for both communication parties.</p>



<figure class="wp-block-table mischianti-table-left"><table class="has-electric-grass-gradient-background has-background"><thead><tr><th> Air data rate（bps） </th><th> Constant value </th></tr></thead><tbody><tr><td>2.4k </td><td>AIR_DATA_RATE_000_24 </td></tr><tr><td>2.4k </td><td>AIR_DATA_RATE_001_24 </td></tr><tr><td>2.4k (default)</td><td>AIR_DATA_RATE_010_24</td></tr><tr><td>4.8k</td><td>AIR_DATA_RATE_011_48</td></tr><tr><td>9.6k</td><td>AIR_DATA_RATE_100_96</td></tr><tr><td>19.2k</td><td>AIR_DATA_RATE_101_192</td></tr><tr><td>38.4k</td><td>AIR_DATA_RATE_110_384</td></tr><tr><td>62.5k</td><td>AIR_DATA_RATE_111_625</td></tr></tbody></table></figure>



<h3>OPTION detail</h3>



<h4>Sub packet setting</h4>



<p>This is the max length of the packet.</p>



<p>When the data is smaller than the subpacket length, the serial output of the receiving end is an uninterrupted continuous output. The receiving end serial port will output the subpacket when the data is larger than the subpacket length.</p>



<figure class="wp-block-table mischianti-table-left"><table class="has-pale-ocean-gradient-background has-background"><thead><tr><th>Packet size</th><th> Constant value </th></tr></thead><tbody><tr><td>200bytes (default)</td><td>SPS_200_00</td></tr><tr><td>128bytes</td><td>SPS_128_01</td></tr><tr><td>64bytes</td><td>SPS_064_10</td></tr><tr><td>32bytes</td><td>SPS_032_11</td></tr></tbody></table></figure>



<h4>RSSI Ambient noise enable</h4>



<p>This command can enable/disable the management type of RSSI, and It’s essential to manage the remote configuration. Pay attention isn’t the RSSI parameter in the message.</p>



<p>When enabled, the C0, C1, C2, C3 commands can be sent in the transmitting mode or WOR transmitting mode to read the register. Register 0x00: Current ambient noise RSSI Register 0X01: RSSI when the data was received last time.</p>



<figure class="wp-block-table mischianti-table-left"><table class="has-pale-ocean-gradient-background has-background"><thead><tr><th>RSSI Ambient noise enable</th><th> Constant value </th></tr></thead><tbody><tr><td>Enable</td><td>RSSI_AMBIENT_NOISE_ENABLED</td></tr><tr><td>Disable (default)</td><td>RSSI_AMBIENT_NOISE_DISABLED</td></tr></tbody></table></figure>



<h4>Transmission power</h4>



<p>You can change this set of constants by applying a define like so:</p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: cpp; title: ; notranslate" title="">#define E220_22 // default value without set 
</pre></div>


<p>Applicable for <strong>E220 with 22dBm as max power.</strong><br>Low power transmission is not recommended due to its low power supply efficiency.</p>



<figure class="wp-block-table mischianti-table-left"><table class="has-pale-ocean-gradient-background has-background"><thead><tr><th> Transmission power (approximation) </th><th> Constant value </th></tr></thead><tbody><tr><td>22dBm (default)</td><td>POWER_22</td></tr><tr><td>17dBm</td><td>POWER_17</td></tr><tr><td>13dBm</td><td>POWER_13</td></tr><tr><td>10dBm</td><td>POWER_10</td></tr></tbody></table></figure>



<p>Applicable for <strong>E220 with 30dBm as max power.</strong><br>Low power transmission is not recommended due to its low power supply efficiency.</p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: cpp; title: ; notranslate" title="">#define E220_30
</pre></div>


<figure class="wp-block-table mischianti-table-left"><table class="has-pale-ocean-gradient-background has-background"><thead><tr><th> Transmission power (approximation) </th><th> Constant value </th></tr></thead><tbody><tr><td>30dBm (default)</td><td>POWER_30</td></tr><tr><td>27dBm</td><td>POWER_27</td></tr><tr><td>24dBm</td><td>POWER_24</td></tr><tr><td>21dBm</td><td>POWER_21</td></tr></tbody></table></figure>



<p>You can configure Channel frequency also with this define:</p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: cpp; title: ; notranslate" title="">// One of 
#define FREQUENCY_433 
#define FREQUENCY_170
#define FREQUENCY_470
#define FREQUENCY_868
#define FREQUENCY_915
</pre></div>


<h3>TRANSMISSION_MODE Detail</h3>



<h4>Enable RSSI</h4>



<p>When enabled, the module receives wireless data, and it will follow an RSSI strength byte after output via the serial port TXD</p>



<figure class="wp-block-table mischianti-table-left"><table class="has-blush-light-purple-gradient-background has-background"><thead><tr><th> Enable RSSI </th><th> Constant value </th></tr></thead><tbody><tr><td>Enable</td><td>RSSI_ENABLED</td></tr><tr><td>Disable (default)</td><td>RSSI_DISABLED</td></tr></tbody></table></figure>



<h4>Transmission type</h4>



<p>Transmission mode: The first three bytes of each user’s data frame can be used as high/low address and channel in fixed transmission mode.   The module changes its address and channel when transmitted. And it will revert to the original setting after completing the process.</p>



<figure class="wp-block-table mischianti-table-left"><table class="has-blush-light-purple-gradient-background has-background"><thead><tr><th>Fixed transmission enabling bit</th><th> Constant value </th></tr></thead><tbody><tr><td>Fixed transmission mode</td><td>FT_FIXED_TRANSMISSION</td></tr><tr><td>Transparent transmission mode (default)</td><td>FT_TRANSPARENT_TRANSMISSION</td></tr></tbody></table></figure>



<h4>Monitor data before transmission</h4>



<p>When enabled, wireless data will be monitored before it is transmitted, avoiding interference to a certain extent, but may cause data delay.</p>



<figure class="wp-block-table mischianti-table-left"><table class="has-blush-light-purple-gradient-background has-background"><thead><tr><th> LBT enable byte </th><th> Constant value </th></tr></thead><tbody><tr><td>Enable</td><td>LBT_ENABLED</td></tr><tr><td>Disable (default)</td><td>LBT_DISABLED</td></tr></tbody></table></figure>



<div class="wp-block-image"><img src="https://www.mischianti.org/wp-content/uploads/2020/07/Ebyte-LoRa-E22-device-for-Arduino-esp32-or-esp8266-carrier-sense.jpg"/></div>



<h4>WOR cycle</h4>



<p>If WOR is transmitting: after the WOR receiver receives the wireless data and outputs it through the serial port, it will wait for 1000ms before entering the WOR again. Users can input the serial port data and return it via wireless during this period. Each serial byte will be refreshed for 1000ms. Users must transmit the first byte within 1000ms.</p>



<ul><li>Period T = (1 + WOR) * 500ms, maximum 4000ms, minimum 500ms</li><li>The longer the WOR monitoring interval period, the lower the average power consumption, but the greater the data delay</li><li><strong>Both the transmitter and the receiver must be the same (very important).</strong></li></ul>



<figure class="wp-block-table mischianti-table-left"><table class="has-blush-light-purple-gradient-background has-background"><thead><tr><th>Wireless wake-up time</th><th> Constant value </th></tr></thead><tbody><tr><td>500ms</td><td>WAKE_UP_500</td></tr><tr><td>1000ms</td><td>WAKE_UP_1000</td></tr><tr><td>1500ms</td><td>WAKE_UP_1500</td></tr><tr><td>2000ms (default)</td><td>WAKE_UP_2000</td></tr><tr><td>2500ms</td><td>WAKE_UP_2500</td></tr><tr><td>3000ms</td><td>WAKE_UP_3000</td></tr><tr><td>3500ms</td><td>WAKE_UP_3500</td></tr><tr><td>4000ms</td><td>WAKE_UP_4000</td></tr></tbody></table></figure>



<h1>Check buffer</h1>



<p>First, we must introduce a simple but practical method to check if something is in the receiving buffer.</p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: arduino; title: ; notranslate" title="">int available();
</pre></div>


<p>It’s simple to return how many bytes you have in the current stream.</p><div class="code-block code-block-2 amp-wp-d1954fa" data-amp-original-style="margin: 8px 0; clear: both;">
</div>




<h1>Send receive messages</h1>



<h2>Normal transmission mode</h2>



<p>Normal/Transparent transmission mode sends messages to all devices with the same address and channel.</p>



<div class="wp-block-image"><img src="https://www.mischianti.org/wp-content/uploads/2019/10/LoRa_E32_transmittingScenarios.jpg"/></div>





<h3>Fixed transmission</h3>


<p>Fixed transmission have more scenarios</p>



<div class="wp-block-image"><img src="https://www.mischianti.org/wp-content/uploads/2019/10/LoRa_E32_transmittingScenarios.jpg"/></div>






<h1>Thanks</h1>



<p>Now you have all information to do your work, but I think It’s important to show some real examples to understand better all the possibilities.</p>



<ol><li>Ebyte LoRa E220 device for Arduino, esp32 or esp8266: settings and basic usage</li><li>Ebyte LoRa E220 device for Arduino, esp32 or esp8266: library</li><li>Ebyte LoRa E220 device for Arduino, esp32 or esp8266: configuration</li><li>Ebyte LoRa E220 device for Arduino, esp32 or esp8266: fixed transmission, broadcast, monitor, and RSSI</li><li>Ebyte LoRa E220 device for Arduino, esp32 or esp8266: power saving and sending structured data</li><li><span data-amp-original-style="color: initial;" class="amp-wp-2ca27fe">Ebyte LoRa E220 device for Arduino, esp32 or esp8266: WOR microcontroller and Arduino shield</span></li><li>Ebyte LoRa E220 device for Arduino, esp32 or esp8266: WOR microcontroller and WeMos D1 shield</li><li>Ebyte LoRa E220 device for Arduino, esp32 or esp8266: WOR microcontroller and esp32 dev v1 shield</li></ol>



<p><a href="https://github.com/xreef/EByte_LoRa_E220_Series_Library" data-type="URL" data-id="https://github.com/xreef/EByte_LoRa_E220_Series_Library" target="_blank" rel="noreferrer noopener">Github library</a></p>



<ul><li><a href="https://www.pcbway.com/project/shareproject/LoRa_E32_Series_device_Arduino_shield.html">Mischianti Arduino LoRa shield (Open source)</a></li><li><a href="https://www.pcbway.com/project/shareproject/LoRa_E32_Series_device_WeMos_D1_mini_shield_RF_8km_range.html">Mischianti WeMos LoRa shield (Open source)</a></li><li><a rel="noreferrer noopener" href="https://www.pcbway.com/project/shareproject/LoRa_ESP32_DEV_KIT_v1_shield_for_EByte_E32_E22__RF_8km_12km_range.html?from=mischianti05" target="_blank">Mischianti ESP32 DOIT DEV KIT v1 shield (Open source)</a></li></ul>


      

<div class="mischianti-forum-button-container">
  	<a class="mischianti-forum-button" href="https://www.mischianti.org/forums/forum/mischiantis-libraries/ebyte-lora-e220-uart-devices-llcc68/" target="_blank">Support Forum</a>
</div>
	</div>