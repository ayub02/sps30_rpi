import struct
from sensirion_shdlc_driver import ShdlcSerialPort, ShdlcConnection, ShdlcDevice
from sensirion_shdlc_driver.command import ShdlcCommand
import logging
# import numpy as np

logging.basicConfig(level=logging.DEBUG)  # <- logging level set here

mode = 'Read'
config_all = {
            'Start': {
                'command': 0x00,
                'data': b"\x01\x03"
            },
            'Stop': {
                'command': 0x01,
                'data': b""
            },
            'Read': {
                'command': 0x03,
                'data': b""
            },
            'Clean': {
              'command': 0x56,
              'data': b""
            },
            'Reset': {
              'command': 0xD3,
              'data': b""
            }
        }

with ShdlcSerialPort(port='/dev/ttyS0', baudrate=115200) as port:
    device = ShdlcDevice(ShdlcConnection(port), slave_address=0)

    config = config_all[mode]
    raw_response = device.execute(ShdlcCommand(
        id=config['command'],  # The command ID as specified in the device documentation
        data=config['data'],  # The payload data to send
        max_response_time=10,  # Maximum response time in Seconds
    ))

msgs = ['PM1.0 Value in µg/m3: ',
        'PM2.5 Value in µg/m3: ',
        'PM4.0 Value in µg/m3: ',
        'PM10.0 Value in µg/m3: ',
        'NC0.5 Value in 1/cm3: ',
        'NC1.0 Value in 1/cm3: ',
        'NC2.5 Value in 1/cm3: ',
        'NC10.0 Value in 1/cm3: ',
        'NC4.0 Value in 1/cm3: ',
        'Typical Particle Size in µm: ']

if mode == 'Read':
    print("Raw Response: {}".format(list(raw_response)))
    count = 0
    print(' ')
    for i in range(0, 37, 4):
        val = bytearray(raw_response[i:i+4])
        print(msgs[count], (struct.unpack('>f', val))[0])
        count += 1
