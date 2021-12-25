import struct
from sensirion_shdlc_driver import ShdlcSerialPort, ShdlcConnection, ShdlcDevice
from sensirion_shdlc_driver.command import ShdlcCommand
import logging
import requests
import time

write_key = "IZZMMWE0GBXCN096"
channel_id = 1617989
write_url = "https://api.thingspeak.com/update"

logging.basicConfig(level=logging.DEBUG)
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

try:
    with ShdlcSerialPort(port='/dev/ttyS0', baudrate=115200) as port:
        device = ShdlcDevice(ShdlcConnection(port), slave_address=0)

        try:
            print("Stopping...")
            mode = 'Stop'
            config = config_all[mode]
            raw_response = device.execute(ShdlcCommand(
                id=config['command'],
                data=config['data'],
                max_response_time=10,
            ))
            print("{} response: {}".format(mode, list(raw_response)))
        except:
            pass

        mode = 'Start'
        config = config_all[mode]
        print("Starting...")
        raw_response = device.execute(ShdlcCommand(
            id=config['command'],
            data=config['data'],
            max_response_time=10,
        ))
        print("{} response: {}".format(mode, list(raw_response)))
        time.sleep(15)

        mode = 'Read'
        config = config_all[mode]
        print("Reading...")
        raw_measurements = device.execute(ShdlcCommand(
            id=config['command'],
            data=config['data'],
            max_response_time=10,
        ))
        print("{} response: {}".format(mode, list(raw_response)))
        time.sleep(1)

        mode = 'Stop'
        config = config_all[mode]
        print("Stopping...")
        raw_response = device.execute(ShdlcCommand(
            id=config['command'],
            data=config['data'],
            max_response_time=10,
        ))
        print("{} response: {}".format(mode, list(raw_response)))

    values = []
    for i in range(0, 37, 4):
        val = bytearray(raw_response[i:i + 4])
        values.append((struct.unpack('>f', val))[0])
        print(values[-1])

    params = {"api_key": write_key, "field1": round(values[1])}
    response = requests.post(write_url, params=params)
    print(response.status_code)
except:
    pass

