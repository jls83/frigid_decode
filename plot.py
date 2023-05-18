import matplotlib.pyplot as plt

def plot_times(tss):
    _, axs = plt.subplots(len(tss))

    for i, ts in enumerate(tss):
        axs[i].step(ts, [i & 1 for i in range(len(ts))])

    plt.show()
