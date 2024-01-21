import sys
sys.path.pop(0)
from setuptools import setup

setup(
    name="ebyte-lora-e220",
    package_dir={'': 'src'},
    py_modules=["lora_e220", "lora_e220_constants", "lora_e220_operation_constant"],
    version="0.0.4",
    description="LoRa EBYTE E220 device library complete and tested with Arduino, esp8266, esp32, STM32 and Raspberry Pi Pico. LLCC68",
    long_description="Ebyte E220 LoRa (Long Range) library device very cheap and very long range (from 5Km to 10Km). Arduino LoRa EBYTE E220 device library complete and tested with Arduino, esp8266, esp32, STM32 and Raspberry Pi Pico. LLCC68",
    keywords="LoRa, UART, EByte, esp32, esp8266, stm32, SAMD, Arduino, Raspberry Pi Pico, MicroPython",
    url="https://github.com/xreef/EByte_LoRa_E220_micropython_library",
    author="Renzo Mischianti",
    author_email="renzo.mischianti@gmail.com",
    maintainer="Renzo Mischianti",
    maintainer_email="renzo.mischianti@gmail.com",
    license="MIT",
    install_requires=[],
    project_urls={
        'Documentation': 'https://www.mischianti.org/category/my-libraries/lora-e220-llcc68-devices/',
        'Documentazione': 'https://www.mischianti.org/it/category/le-mie-librerie/dispositivi-lora-e220-llcc68/',
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: Implementation :: MicroPython",
        "License :: OSI Approved :: MIT License",
    ],
)