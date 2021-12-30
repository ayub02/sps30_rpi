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


def read_values(_raw_data):
    values = []
    for i in range(0, 37, 4):
        val = bytearray(_raw_data[i:i + 4])
        values.append((struct.unpack('>f', val))[0])
        print(values[-1])
    return values[1]


def exec_mode(mode):
    config = config_all[mode]
    print('Trying to {}'.format(mode))
    try:
        raw_response = device.execute(ShdlcCommand(
            id=config['command'],
            data=config['data'],
            max_response_time=10,
        ))
    except:
        print('Failed to {}'.format(mode))
    if mode == 'Read' and raw_response:
        return raw_response


try:
    with ShdlcSerialPort(port='/dev/ttyS0', baudrate=115200) as port:
        device = ShdlcDevice(ShdlcConnection(port), slave_address=0)

        exec_mode('Start')
        time.sleep(4)

        pm2p5_all = []
        for k in range(10):
            raw_data = exec_mode('Read')
            pm2p5_all.append(read_values(raw_data))
            time.sleep(2)
        pm2p5 = sum(pm2p5_all) / len(pm2p5_all)

        exec_mode('Stop')
        time.sleep(2)

    params = {"api_key": write_key, "field1": round(pm2p5)}
    response = requests.post(write_url, params=params)
    print(response.status_code)

except:
    pass
