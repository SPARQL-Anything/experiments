import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
import os

input_sizes = [1, 10, 100, 1000]
# input_sizes = [ 1000]
strategies = ["strategy0", "strategy1"]
slice_options = ["no_slice", "slice"]
# memory_limits = [256, 512, 1024, 4096]
memory_limits = [256, 512, 1024, 4096]
formats = ["csv", "json"]
summary_file = "/Users/lgu/Desktop/GTFS_summary - Foglio1.tsv"
out_folder = "/Users/lgu/Desktop/charts"

if not os.path.exists(out_folder):
    os.mkdir(out_folder)

summary_df = pd.read_csv(summary_file, sep='\t', decimal=",")
fig = plt.subplots(figsize=(12, 8))



# set height of bar
# s0_ns = [10, 20, 30]
# s1_ns = [12, 22, 32]
# s0_s = [14, 24, 34]
# s1_s = [16, 26, 36]
#
# s0_ns_e = [5, 10, 15]
# s1_ns_e = [6, 11, 16]
# s0_s_e = [7, 12, 17]
# s1_s_e = [9, 13, 18]
#
# # Set position of bar on X axis
# br1 = np.arange(len(s0_ns))
# br2 = [x + barWidth for x in br1]
# br3 = [x + barWidth for x in br2]
# br4 = [x + barWidth for x in br3]
#
# # Make the plot
# plt.bar(br1, s0_ns, yerr=s0_ns_e, color='r', width=barWidth, edgecolor='grey', label='s0_ns')
# plt.bar(br2, s1_ns, yerr=s1_ns_e, color='g', width=barWidth, edgecolor='grey', label='s1_ns')
# plt.bar(br3, s0_s, yerr=s0_s_e, color='b', width=barWidth, edgecolor='grey', label='s0_s')
# plt.bar(br4, s1_s, yerr=s1_s_e, color='y', width=barWidth, edgecolor='grey', label='s1_s')
#
# # Adding Xticks
# plt.ylabel('Time (ms)')
# plt.xticks([r + barWidth for r in range(len(s0_ns))], ['2015', '2016', '2017'])
#
# plt.legend()
# # plt.show()
#
# plt.savefig("/Users/lgu/Desktop/a.png")
# plt.clf()


def generate_chart(f, i, m):
    barWidth = 0.2
    times = {
        strategies[0] + slice_options[0]: [],
        strategies[1] + slice_options[0]: [],
        strategies[0] + slice_options[1]: [],
        strategies[1] + slice_options[1]: []
    }
    stds = {
        strategies[0] + slice_options[0]: [],
        strategies[1] + slice_options[0]: [],
        strategies[0] + slice_options[1]: [],
        strategies[1] + slice_options[1]: []
    }
    for strategy in strategies:
        for slice_option in slice_options:
            for q in range(1, 19):

                run = summary_df[
                    (summary_df["Format"] == f) &
                    (summary_df["Size"] == i) &
                    (summary_df["Strategy"] == strategy) &
                    (summary_df["Slice"] == slice_option) &
                    (summary_df["Memory"] == m) &
                    (summary_df["Query"] == f"q{q}") &
                    (summary_df["Status-1"] == "OK")
                    ]

                if len(run) > 0:
                    times[strategy + slice_option].append(float(run["Mean"]))
                    stds[strategy + slice_option].append(float(run["Std"]))
                else:
                    times[strategy + slice_option].append(0.0)
                    stds[strategy + slice_option].append(0.0)
    print(times)
    # set height of bar
    s0_ns = times[strategies[0] + slice_options[0]]
    s1_ns = times[strategies[1] + slice_options[0]]
    s0_s = times[strategies[0] + slice_options[1]]
    s1_s = times[strategies[1] + slice_options[1]]
    s0_ns_e = stds[strategies[0] + slice_options[0]]
    s1_ns_e = stds[strategies[1] + slice_options[0]]
    s0_s_e = stds[strategies[0] + slice_options[1]]
    s1_s_e = stds[strategies[1] + slice_options[1]]
    # Set position of bar on X axis
    br1 = np.arange(len(s0_ns))
    br2 = [x + barWidth for x in br1]
    br3 = [x + barWidth for x in br2]
    br4 = [x + barWidth for x in br3]
    # Make the plot
    plt.bar(br1, s0_ns, yerr=s0_ns_e, color='r', width=barWidth, edgecolor='grey', label='Strategy 0 w/o slicing',
            capsize=2, ecolor='grey')
    plt.bar(br2, s1_ns, yerr=s1_ns_e, color='g', width=barWidth, edgecolor='grey', label='Strategy 1 w/o slicing',
            capsize=2, ecolor='grey')
    plt.bar(br3, s0_s, yerr=s0_s_e, color='b', width=barWidth, edgecolor='grey', label='Strategy 0 with slicing',
            capsize=2, ecolor='grey')
    plt.bar(br4, s1_s, yerr=s1_s_e, color='y', width=barWidth, edgecolor='grey', label='Strategy 1 with slicing',
            capsize=2, ecolor='grey')
    # Adding Xticks
    plt.ylabel('Time (ms)')
    plt.xticks([r + barWidth for r in range(len(s0_ns))], [f"q{q}" for q in range(1, 19)])
    plt.legend()
    # plt.show()
    plt.savefig(f"{out_folder}/{f}_{i}_{m}.png")
    plt.clf()


def generate_chart_for_all_formats(i, m):
    barWidth = 0.1
    times = {
        strategies[0] + slice_options[0] + formats[0]: [],
        strategies[1] + slice_options[0] + formats[0]: [],
        strategies[0] + slice_options[1] + formats[0]: [],
        strategies[1] + slice_options[1] + formats[0]: [],
        strategies[0] + slice_options[0] + formats[1]: [],
        strategies[1] + slice_options[0] + formats[1]: [],
        strategies[0] + slice_options[1] + formats[1]: [],
        strategies[1] + slice_options[1] + formats[1]: []
    }

    stds = {
        strategies[0] + slice_options[0] + formats[0]: [],
        strategies[1] + slice_options[0] + formats[0]: [],
        strategies[0] + slice_options[1] + formats[0]: [],
        strategies[1] + slice_options[1] + formats[0]: [],
        strategies[0] + slice_options[0] + formats[1]: [],
        strategies[1] + slice_options[0] + formats[1]: [],
        strategies[0] + slice_options[1] + formats[1]: [],
        strategies[1] + slice_options[1] + formats[1]: []
    }
    for strategy in strategies:
        for slice_option in slice_options:
            for q in range(1, 19):

                run_0 = summary_df[
                    (summary_df["Format"] == formats[0]) &
                    (summary_df["Size"] == i) &
                    (summary_df["Strategy"] == strategy) &
                    (summary_df["Slice"] == slice_option) &
                    (summary_df["Memory"] == m) &
                    (summary_df["Query"] == f"q{q}") &
                    (summary_df["Status-1"] == "OK")
                    ]

                if len(run_0) > 0:
                    times[strategy + slice_option + formats[0]].append(float(run_0["Mean"]))
                    stds[strategy + slice_option + formats[0]].append(float(run_0["Std"]))
                else:
                    times[strategy + slice_option + formats[0]].append(0.0)
                    stds[strategy + slice_option + formats[0]].append(0.0)

                run_1 = summary_df[
                    (summary_df["Format"] == formats[1]) &
                    (summary_df["Size"] == i) &
                    (summary_df["Strategy"] == strategy) &
                    (summary_df["Slice"] == slice_option) &
                    (summary_df["Memory"] == m) &
                    (summary_df["Query"] == f"q{q}") &
                    (summary_df["Status-1"] == "OK")
                    ]

                if len(run_1) > 0:
                    times[strategy + slice_option + formats[1]].append(float(run_1["Mean"]))
                    stds[strategy + slice_option + formats[1]].append(float(run_1["Std"]))
                else:
                    times[strategy + slice_option + formats[1]].append(0.0)
                    stds[strategy + slice_option + formats[1]].append(0.0)
    print(times)
    # set height of bar

    s0_ns_0 = times[strategies[0] + slice_options[0] + formats[0]]
    s1_ns_0 = times[strategies[1] + slice_options[0] + formats[0]]
    s0_s_0 = times[strategies[0] + slice_options[1] + formats[0]]
    s1_s_0 = times[strategies[1] + slice_options[1] + formats[0]]

    s0_ns_1 = times[strategies[0] + slice_options[0] + formats[1]]
    s1_ns_1 = times[strategies[1] + slice_options[0] + formats[1]]
    s0_s_1 = times[strategies[0] + slice_options[1] + formats[1]]
    s1_s_1 = times[strategies[1] + slice_options[1] + formats[1]]

    s0_ns_e_0 = stds[strategies[0] + slice_options[0] + formats[0]]
    s1_ns_e_0 = stds[strategies[1] + slice_options[0] + formats[0]]
    s0_s_e_0 = stds[strategies[0] + slice_options[1] + formats[0]]
    s1_s_e_0 = stds[strategies[1] + slice_options[1] + formats[0]]

    s0_ns_e_1 = stds[strategies[0] + slice_options[0] + formats[1]]
    s1_ns_e_1 = stds[strategies[1] + slice_options[0] + formats[1]]
    s0_s_e_1 = stds[strategies[0] + slice_options[1] + formats[1]]
    s1_s_e_1 = stds[strategies[1] + slice_options[1] + formats[1]]


    # Set position of bar on X axis
    br1 = np.arange(len(s0_ns_0))
    br11 = [x + barWidth for x in br1]
    br2 = [x + barWidth for x in br11]
    br21 = [x + barWidth for x in br2]
    br3 = [x + barWidth for x in br21]
    br31 = [x + barWidth for x in br3]
    br4 = [x + barWidth for x in br31]
    br41 = [x + barWidth for x in br4]



    # Make the plot
    plt.bar(br1, s0_ns_0, yerr=s0_ns_e_0, color='r', width=barWidth, edgecolor='grey', label='Strategy 0 w/o slicing CSV',
            capsize=2, ecolor='grey')
    plt.bar(br11, s0_ns_1, yerr=s0_ns_e_1, color='r', width=barWidth, edgecolor='grey', label='Strategy 0 w/o slicing JSON',
            capsize=2, ecolor='grey', hatch="//")

    plt.bar(br2, s1_ns_0, yerr=s1_ns_e_0, color='g', width=barWidth, edgecolor='grey', label='Strategy 1 w/o slicing CSV',
            capsize=2, ecolor='grey')
    plt.bar(br21, s1_ns_1, yerr=s1_ns_e_1, color='g', width=barWidth, edgecolor='grey',
            label='Strategy 1 w/o slicing CSV',
            capsize=2, ecolor='grey', hatch="//")

    plt.bar(br3, s0_s_0, yerr=s0_s_e_0, color='b', width=barWidth, edgecolor='grey', label='Strategy 0 with slicing CSV',
            capsize=2, ecolor='grey')
    plt.bar(br31, s0_s_1, yerr=s0_s_e_1, color='b', width=barWidth, edgecolor='grey', label='Strategy 0 with slicing JSON',
            capsize=2, ecolor='grey', hatch="//")

    plt.bar(br4, s1_s_0, yerr=s1_s_e_0, color='y', width=barWidth, edgecolor='grey', label='Strategy 1 with slicing CSV',
            capsize=2, ecolor='grey')
    plt.bar(br41, s1_s_1, yerr=s1_s_e_1, color='y', width=barWidth, edgecolor='grey', label='Strategy 1 with slicing JSON',
            capsize=2, ecolor='grey', hatch="//")

    # Adding Xticks
    plt.ylabel('Time (ms)')
    plt.xticks([r + 4 * barWidth for r in range(len(s0_ns_0))], [f"q{q}" for q in range(1, 19)])
    plt.legend()

    # plt.show()
    plt.savefig(f"{out_folder}/{i}_{m}.png")
    plt.clf()


def generate_chart_for_all_formats_all_memories(i):
    barWidth = 0.1
    times = {
        strategies[0] + slice_options[0] + formats[0]: [],
        strategies[1] + slice_options[0] + formats[0]: [],
        strategies[0] + slice_options[1] + formats[0]: [],
        strategies[1] + slice_options[1] + formats[0]: [],
        strategies[0] + slice_options[0] + formats[1]: [],
        strategies[1] + slice_options[0] + formats[1]: [],
        strategies[0] + slice_options[1] + formats[1]: [],
        strategies[1] + slice_options[1] + formats[1]: []
    }

    stds = {
        strategies[0] + slice_options[0] + formats[0]: [],
        strategies[1] + slice_options[0] + formats[0]: [],
        strategies[0] + slice_options[1] + formats[0]: [],
        strategies[1] + slice_options[1] + formats[0]: [],
        strategies[0] + slice_options[0] + formats[1]: [],
        strategies[1] + slice_options[0] + formats[1]: [],
        strategies[0] + slice_options[1] + formats[1]: [],
        strategies[1] + slice_options[1] + formats[1]: []
    }
    for strategy in strategies:
        for slice_option in slice_options:
            for q in range(1, 19):

                run_0 = summary_df[
                    (summary_df["Format"] == formats[0]) &
                    (summary_df["Size"] == i) &
                    (summary_df["Strategy"] == strategy) &
                    (summary_df["Slice"] == slice_option) &
                    #(summary_df["Memory"] == m) &
                    (summary_df["Query"] == f"q{q}") &
                    (summary_df["Status-1"] == "OK")
                    ]

                if len(run_0) > 0:
                    times[strategy + slice_option + formats[0]].append(np.array(run_0["Mean"]).mean())
                    stds[strategy + slice_option + formats[0]].append(np.array(run_0["Mean"]).std())
                else:
                    times[strategy + slice_option + formats[0]].append(0.0)
                    stds[strategy + slice_option + formats[0]].append(0.0)

                run_1 = summary_df[
                    (summary_df["Format"] == formats[1]) &
                    (summary_df["Size"] == i) &
                    (summary_df["Strategy"] == strategy) &
                    (summary_df["Slice"] == slice_option) &
                    #(summary_df["Memory"] == m) &
                    (summary_df["Query"] == f"q{q}") &
                    (summary_df["Status-1"] == "OK")
                    ]

                if len(run_1) > 0:
                    times[strategy + slice_option + formats[1]].append(np.array(run_1["Mean"]).mean())
                    stds[strategy + slice_option + formats[1]].append(np.array(run_1["Mean"]).std())
                else:
                    times[strategy + slice_option + formats[1]].append(0.0)
                    stds[strategy + slice_option + formats[1]].append(0.0)
    print(times)
    # set height of bar

    s0_ns_0 = times[strategies[0] + slice_options[0] + formats[0]]
    s1_ns_0 = times[strategies[1] + slice_options[0] + formats[0]]
    s0_s_0 = times[strategies[0] + slice_options[1] + formats[0]]
    s1_s_0 = times[strategies[1] + slice_options[1] + formats[0]]

    s0_ns_1 = times[strategies[0] + slice_options[0] + formats[1]]
    s1_ns_1 = times[strategies[1] + slice_options[0] + formats[1]]
    s0_s_1 = times[strategies[0] + slice_options[1] + formats[1]]
    s1_s_1 = times[strategies[1] + slice_options[1] + formats[1]]

    s0_ns_e_0 = stds[strategies[0] + slice_options[0] + formats[0]]
    s1_ns_e_0 = stds[strategies[1] + slice_options[0] + formats[0]]
    s0_s_e_0 = stds[strategies[0] + slice_options[1] + formats[0]]
    s1_s_e_0 = stds[strategies[1] + slice_options[1] + formats[0]]

    s0_ns_e_1 = stds[strategies[0] + slice_options[0] + formats[1]]
    s1_ns_e_1 = stds[strategies[1] + slice_options[0] + formats[1]]
    s0_s_e_1 = stds[strategies[0] + slice_options[1] + formats[1]]
    s1_s_e_1 = stds[strategies[1] + slice_options[1] + formats[1]]


    # Set position of bar on X axis
    br1 = np.arange(len(s0_ns_0))
    br11 = [x + barWidth for x in br1]
    br2 = [x + barWidth for x in br11]
    br21 = [x + barWidth for x in br2]
    br3 = [x + barWidth for x in br21]
    br31 = [x + barWidth for x in br3]
    br4 = [x + barWidth for x in br31]
    br41 = [x + barWidth for x in br4]



    # Make the plot
    plt.bar(br1, s0_ns_0, yerr=s0_ns_e_0, color='r', width=barWidth, edgecolor='grey', label='Strategy 0 w/o slicing CSV',
            capsize=2, ecolor='grey')
    plt.bar(br11, s0_ns_1, yerr=s0_ns_e_1, color='r', width=barWidth, edgecolor='grey', label='Strategy 0 w/o slicing JSON',
            capsize=2, ecolor='grey', hatch="//")

    plt.bar(br2, s1_ns_0, yerr=s1_ns_e_0, color='g', width=barWidth, edgecolor='grey', label='Strategy 1 w/o slicing CSV',
            capsize=2, ecolor='grey')
    plt.bar(br21, s1_ns_1, yerr=s1_ns_e_1, color='g', width=barWidth, edgecolor='grey',
            label='Strategy 1 w/o slicing CSV',
            capsize=2, ecolor='grey', hatch="//")

    plt.bar(br3, s0_s_0, yerr=s0_s_e_0, color='b', width=barWidth, edgecolor='grey', label='Strategy 0 with slicing CSV',
            capsize=2, ecolor='grey')
    plt.bar(br31, s0_s_1, yerr=s0_s_e_1, color='b', width=barWidth, edgecolor='grey', label='Strategy 0 with slicing JSON',
            capsize=2, ecolor='grey', hatch="//")

    plt.bar(br4, s1_s_0, yerr=s1_s_e_0, color='y', width=barWidth, edgecolor='grey', label='Strategy 1 with slicing CSV',
            capsize=2, ecolor='grey')
    plt.bar(br41, s1_s_1, yerr=s1_s_e_1, color='y', width=barWidth, edgecolor='grey', label='Strategy 1 with slicing JSON',
            capsize=2, ecolor='grey', hatch="//")

    # Adding Xticks
    plt.ylabel('Time (ms)')
    plt.xticks([r + 4 * barWidth for r in range(len(s0_ns_0))], [f"q{q}" for q in range(1, 19)])
    plt.legend()

    # plt.show()
    plt.savefig(f"{out_folder}/{i}.png")
    plt.clf()


for input_size in input_sizes:
    generate_chart_for_all_formats_all_memories(input_size)
    for memory_limit in memory_limits:
        generate_chart_for_all_formats(input_size, memory_limit)
        for f in formats:
            generate_chart(f, input_size, memory_limit)


#generate_chart("json", 1, 256)
#generate_chart_for_all_formats(1, 256)
#generate_chart_for_all_formats(100, 256)
#generate_chart_for_all_formats(100, 512)



