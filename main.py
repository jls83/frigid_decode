import math
from collections import Counter
from functools import reduce
from itertools import chain

import matplotlib.pyplot as plt

FRIGID = '/Users/jls83/Downloads/Frigid Test.ir'
TERMPS = '/Users/jls83/Downloads/Termps.ir'
ALL_SAME = '/Users/jls83/Downloads/AllSame.ir'

FIRST_BURST = 8963
SECOND_BURST = 4511
HIGH = 625
LOW = 525
SPACE = 575
WRAPPED_LOW = (SPACE + LOW + SPACE)
SHORT_SPLIT = 20010
LONG_SPLIT = 40020
PREAMBLE = [FIRST_BURST, SECOND_BURST, HIGH, (SPACE + LOW + SPACE)]

CYCLE_LENGTH = 1200
HIGH_CYCLE = (625, 575)
LOW_CYCLE = (625, 575)

class IRSpec:
    def __init__(self, name, capture_type, frequency, duty_cycle, data):
        self.name = name
        self.capture_type = capture_type
        self.frequency = frequency
        self.duty_cycle = duty_cycle
        self.data = data

        # temp, mode, fan_speed, power = name.split('_')
        # self.config = {
        #     "temp": int(temp),
        #     "mode": mode,
        #     "fan_speed": fan_speed,
        #     "power": power,
        # }

        self.data_int = [int(n) for n in data.split(' ')]
        self.normalized_data = [self.normalize_value(n) for n in self.data_int]
        self.chunks = self.get_chunks(self.normalized_data)

    @staticmethod
    def normalize_value(n):
        if n <= 582: return SPACE
        elif n <= 656: return HIGH
        elif n <= 1683: return (SPACE + LOW + SPACE)
        elif n <= 4516: return SECOND_BURST
        elif n <= 8994: return FIRST_BURST
        elif n <= 20016: return SHORT_SPLIT
        else: return LONG_SPLIT

    @staticmethod
    def get_chunks(ns, boundaries={SHORT_SPLIT, LONG_SPLIT}):
        res = [[]]
        for n in ns:
            if n in boundaries:
                res.append([])
            else:
                res[-1].append(n)

        return res

    def get_ir_file_def(self, button_name=None):
        if button_name is None:
            button_name = self.name
        data_str = " ".join(str(n) for n in self.normalized_data)
        return f"name: {button_name}\ntype: raw\nfrequency: 38000\nduty_cycle: 0.330000\ndata: {data_str}\n"

def parse_chunk(chunk) -> IRSpec:
    name, capture_type, frequency, duty_cycle, data = (l.split(': ')[-1] for l in chunk.split('\n'))
    return IRSpec(name, capture_type, int(frequency), float(duty_cycle), data)


def split_file(file_name: str) -> "list[str]":
    with open(file_name, 'r') as f:
        content = f.read()

    _, *chunks = content.strip().split('\n# \n')
    return chunks


def bucketize(ns, threshold=5):
    buckets = []
    curr = 0
    curr_bucket = []
    for k in sorted(ns):
        if k == curr:
            continue
        elif (k - curr) > threshold:
            buckets.append(curr_bucket)
            curr_bucket = []

        curr_bucket.append(k)
        curr = k

    if curr_bucket:
        buckets.append(curr_bucket)

    return buckets


def get_specs_from_file(file_name):
    chunks = split_file(file_name)
    return [parse_chunk(chunk) for chunk in chunks]

specs_frigid = get_specs_from_file(FRIGID)
specs_termps = get_specs_from_file(TERMPS)
specs_allsame = get_specs_from_file(ALL_SAME)

datas_frigid = reduce(lambda a, c: a + c, (s.data_int for s in specs_frigid))
datas_termps = reduce(lambda a, c: a + c, (s.data_int for s in specs_termps))
datas_allsame = reduce(lambda a, c: a + c, (s.data_int for s in specs_allsame))

c_frigid = Counter(datas_frigid)
c_termps = Counter(datas_termps)
c_allsame = Counter(datas_allsame)

vals = chain(c_frigid.keys(), c_termps.keys(), c_allsame.keys())

buckets = bucketize(vals)

bucket_map = {0: 0}
for bucket in buckets:
    if not bucket:
        continue
    v = min(bucket)
    for k in bucket:
        bucket_map[k] = v

def construct_times(data_ints):
    res = [0]
    for n in data_ints:
        t_next = res[-1] + n
        res.append(t_next)
    return res



#####
def plot_specs(specs):
    # figure = plt.figure()
    # figure.subplots_adjust(left=0.3)
    _, axs = plt.subplots(len(specs), sharex=True)

    for i, spec in enumerate(specs):
        ts = construct_times(spec.normalized_data)
        axs[i].set_title(spec.name, x=0.0, y=1.0, pad=-8, fontsize=8, horizontalalignment='left')
        axs[i].step(ts, [i & 1 for i in range(len(ts))])
        axs[i].yaxis.set_ticks([])


    plt.show()

def plot_chunks(specs, chunk_idx):
    # figure = plt.figure()
    # figure.subplots_adjust(left=0.3)
    _, axs = plt.subplots(len(specs), sharex=True)

    for i, spec in enumerate(specs):
        ts = construct_times(spec.chunks[chunk_idx])
        axs[i].set_title(spec.name, x=0.0, y=1.0, pad=-8, fontsize=8, horizontalalignment='left')
        axs[i].step(ts, [i & 1 for i in range(len(ts))])
        axs[i].yaxis.set_ticks([])


    plt.show()

# plot_chunks(list(chain(specs_allsame, specs_frigid, specs_termps)), 0)

#####

def dump_specs_to_file(specs, file_name):
    button_defs = (spec.get_ir_file_def() for spec in specs)
    file_header = ["Filetype: IR signals file", "Version: 1"]
    file_text = "\n".join(file_header) + "\n" + "# \n".join(button_defs)

    with open(file_name, "w") as f:
        f.write(file_text)

dump_specs_to_file(chain(specs_allsame, specs_frigid, specs_termps), "/Users/jls83/NormalizedRemote.ir")

def to_digit_array(chunk):
    m = {
        HIGH: 1,
        LOW: 0,
        WRAPPED_LOW: 0,
        SPACE: None
    }

    return [m[n] for n in chunk if m.get(n) is not None]

def from_little_endian_digit_array(arr):
    def f(acc, cur):
        i, n = cur
        return acc + n << i

    return reduce(f, enumerate(arr), 0)
