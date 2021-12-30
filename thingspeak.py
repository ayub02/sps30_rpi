import struct
from sensirion_shdlc_driver import ShdlcSerialPort, ShdlcConnection, ShdlcDevice
from sensirion_shdlc_driver.command import ShdlcCommand
import logging
import requests
import time
from config import constants, modes

write_key = "IZZMMWE0GBXCN096"
channel_id = 1617989
write_url = "https://api.thingspeak.com/update"

logging.basicConfig(level=logging.DEBUG)


def read_values(_raw_data):
    values = []
    for i in range(0, 37, 4):
        val = bytearray(_raw_data[i:i + 4])
        values.append((struct.unpack('>f', val))[0])
        print(values[-1])
    return values[1]


def exec_mode(mode):
    config = modes[mode]
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


with ShdlcSerialPort(port='/dev/ttyS0', baudrate=115200) as port:
    device = ShdlcDevice(ShdlcConnection(port), slave_address=0)

    exec_mode('Start')
    time.sleep(constants["delay_after_start"])

    pm2p5_all = []
    for k in range(int(constants["num_of_read"])):
        pm2p5_all.append(read_values(exec_mode('Read')))
        time.sleep(constants["delay_between_read"])
    pm2p5 = sum(pm2p5_all) / len(pm2p5_all)

    exec_mode('Stop')
    time.sleep(constants["delay_after_stop"])

params = {"api_key": write_key, "field1": round(pm2p5)}
response = requests.post(write_url, params=params)
print(response.status_code)

