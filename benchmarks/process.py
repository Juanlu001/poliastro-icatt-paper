import json
import pandas as pd
import glob
import os.path


RESULTS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                           "benchmark_nounits")


def aggregate_data():
    data = []
    for fname in glob.glob(os.path.join(RESULTS_DIR, "*.json")):
        with open(fname, 'r') as fh:
            name, _ = os.path.splitext(fname)
            _, run, warmup, jit = os.path.basename(name).split("-")
            benchmark = json.load(fh)
            for bb in benchmark["benchmarks"]:
                for val in bb["stats"]["data"]:
                    data.append({
                        "time": val * 1e6,  # us
                        "run": int(run),
                        "warmup": {"on": True, "off": False}[warmup],
                        "test": bb["name"],
                        "jit": {0: True, 1: False}[int(jit)],
                    })
    return pd.DataFrame(data)


def plot_benchmark(df, **fig_kwargs):
    fig, (ax1, ax2) = plt.subplots(2, **fig_kwargs)
    for ax, jit in ((ax1, False), (ax2, True)):
        title = {False: "Benchmark, JIT disabled",
                 True: "Benchmark, JIT enabled"}[jit]

        sns.boxplot(x="time", y="test", hue="warmup", data=df[df["jit"] == jit],
                    orient="h", showfliers=False, palette="PuBuGn_d",
                    ax=ax)

        ax.set(xlabel='Time ($\mu s$)', ylabel='Test',
               title=title)

    ax1.legend_.remove()

    return fig, (ax1, ax2)


def plot_benchmark_vallado(df, **fig_kwargs):
    fig, ax1 = plt.subplots(1, **fig_kwargs)

    sns.boxplot(x="time", y="test", hue="warmup", data=df[df["jit"] == True],
                orient="h", showfliers=False, palette="YlOrRd_d",
                ax=ax1)
    ax1.set(xlabel='Time, JIT enabled ($\mu s$)')
    ax1.set_xlim(6.0, 20.0)
    ax1.legend(loc='center left', title="warmup")

    ax2 = ax1.twiny()

    sns.boxplot(x="time", y="test", hue="warmup", data=df[df["jit"] == False],
                orient="h", showfliers=False, palette="PuBuGn_d",
                ax=ax2)
    ax2.set(xlabel='Time, JIT disabled ($\mu s$)', ylabel='Test')
    ax2.set_xlim(880.0, 1020.0)
    ax2.legend(loc='center right', title="warmup")

    return fig, (ax1, ax2)


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import seaborn as sns

    df = aggregate_data()

    sns.set(style="whitegrid")
    plt.rc("font", family="serif")

    fig, axes = plot_benchmark_vallado(
        df[df["test"] == "test_lambert_single_rev_vallado"],
        figsize=(12, 2)
    )
    fig.tight_layout()
    fig.savefig("benchmark_vallado.pdf")

    fig, axes = plot_benchmark(df[(
        (df["test"] == "test_lambert_single_rev_izzo") |
        (df["test"] == "test_lambert_multi_rev_izzo")
    )], sharex=True, figsize=(12, 4))
    fig.tight_layout()
    fig.savefig("benchmark_izzo.pdf")
