import math
from collections import Counter
from functools import reduce
from itertools import chain

import matplotlib.pyplot as plt

FRIGID = '/Users/jls83/Downloads/Frigid Test.ir'
TERMPS = '/Users/jls83/Downloads/Termps.ir'
ALL_SAME = '/Users/jls83/Downloads/AllSame.ir'

def bin_length(n):
    return math.floor(math.log2(n)) + 1


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

def construct_times(data_ints, bucket_map):
    res = [0]
    for n in data_ints:
        actual_n = bucket_map[n]
        t_next = res[-1] + actual_n
        res.append(t_next)
    return res

#####

# def plot_times(tss):
#     _, axs = plt.subplots(len(tss))

#     for i, ts in enumerate(tss):
#         axs[i].step(ts, [i & 1 for i in range(len(ts))])

#     plt.show()

def plot_specs(specs):
    # figure = plt.figure()
    # figure.subplots_adjust(left=0.3)
    _, axs = plt.subplots(len(specs), sharex=True)

    for i, spec in enumerate(specs):
        ts = construct_times(spec.data_int, bucket_map)
        axs[i].set_title(spec.name, x=0.0, y=1.0, pad=-8, fontsize=8, horizontalalignment='left')
        axs[i].step(ts, [i & 1 for i in range(len(ts))])
        axs[i].yaxis.set_ticks([])


    plt.show()

# plot_times([construct_times(s.data_int, bucket_map) for s in chain(specs_allsame, specs_frigid, specs_termps)])
plot_specs(list(chain(specs_allsame, specs_frigid, specs_termps)))

# range_defs = [
#     [550 + (25 * i) for i in range(5)],
#     [1650 + (25 * i) for i in range(2)],
#     [4510],
#     [8960 + (25 * i) for i in range(2)],
#     [20010],
#     [40020],
# ]

# ranges = reduce(lambda a, c: a + c, range_defs)

# x = [110, 115, 120, 125, 130, 330, 335, 900, 1790, 1795, 4000, 8000]
