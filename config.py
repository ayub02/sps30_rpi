constants = {
    "delay_after_start": 3,
    "delay_between_read": 3,
    "num_of_read": 10,
    "delay_after_stop": 0}

modes = {
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

