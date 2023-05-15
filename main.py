import re

FILE_NAME = '/Users/josephsanders/Downloads/Frigid Test.ir'

class IRSpec:
    def __init__(self, name, capture_type, frequency, duty_cycle, data):
        self.name = name
        self.capture_type = capture_type
        self.frequency = frequency
        self.duty_cycle = duty_cycle
        self.data = data

        temp, mode, fan_speed, power = name.split('_')
        self.config = {
            "temp": int(temp),
            "mode": mode,
            "fan_speed": fan_speed,
            "power": power,
        }

        self.data_int = [int(n) for n in data.split(' ')]

def parse_chunk(chunk) -> IRSpec:
    name, capture_type, frequency, duty_cycle, data = (l.split(': ')[-1] for l in chunk.split('\n'))
    return IRSpec(name, capture_type, int(frequency), float(duty_cycle), data)


def split_file(file_name: str) -> "list[str]":
    with open(file_name, 'r') as f:
        content = f.read()

    _, *chunks = content.strip().split('\n# \n')
    return chunks


chunks = split_file(FILE_NAME)

specs = [parse_chunk(chunk) for chunk in chunks]

rig = [spec for spec in specs if re.match(r'6._.*_.*_off', spec.name)]

rig_data = [r.data_int for r in rig]

z = list(zip(*rig_data))

import math

def bin_length(n):
    return math.floor(math.log2(n)) + 1

