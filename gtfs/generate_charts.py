import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

input_sizes = [1, 10, 100, 1000]
# input_sizes = [ 1000]

configurations = [
    {"slice": "no_slice", "strategy": "strategy0", "ondisk": False,
     "description": "in-memory w/o triple filtering w/o slicing"},
    {"slice": "no_slice", "strategy": "strategy1", "ondisk": False,
     "description": "in-memory with triple filtering w/o slicing"},
    {"slice": "slice", "strategy": "strategy1", "ondisk": False,
     "description": "in-memory with triple filtering with slicing"},
    {"slice": "no_slice", "strategy": "strategy1", "ondisk": True,
     "description": "on-disk with triple filtering w/o slicing"}
]

memory_limits = [256, 512, 1024, 4096, 8192, 16384, 32768]
formats = ["csv", "json"]
summary_file = "/Users/lgu/workspace/SPARQLAnything/CogComplexityAndPerformaceEvaluation/gtfs/swj_experiments/summary.tsv"
out_folder = "/Users/lgu/Desktop/charts"

if not os.path.exists(out_folder):
    os.mkdir(out_folder)

summary_df = pd.read_csv(summary_file, sep='\t', decimal=",")
fig = plt.subplots(figsize=(12, 8))


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
    plt.bar(br1, s0_ns, yerr=s0_ns_e, color='r', width=barWidth, edgecolor='grey',
            label='without triple filtering - w/o slicing',
            capsize=2, ecolor='grey')
    plt.bar(br2, s1_ns, yerr=s1_ns_e, color='g', width=barWidth, edgecolor='grey',
            label='with triple filtering - w/o slicing',
            capsize=2, ecolor='grey')
    plt.bar(br3, s0_s, yerr=s0_s_e, color='b', width=barWidth, edgecolor='grey',
            label='without triple filtering - with slicing',
            capsize=2, ecolor='grey')
    plt.bar(br4, s1_s, yerr=s1_s_e, color='y', width=barWidth, edgecolor='grey',
            label='with triple filtering - with slicing',
            capsize=2, ecolor='grey')
    # Adding Xticks
    plt.ylabel('Average Execution Time (ms)')
    plt.xticks([r + barWidth for r in range(len(s0_ns))], [f"q{q}" for q in range(1, 19)])
    plt.legend(loc='upper left')
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
    plt.bar(br1, s0_ns_0, yerr=s0_ns_e_0, color='r', width=barWidth, edgecolor='grey',
            label='w/o triple filtering - w/o slicing - CSV',
            capsize=2, ecolor='grey')
    plt.bar(br11, s0_ns_1, yerr=s0_ns_e_1, color='r', width=barWidth, edgecolor='grey',
            label='w/o triple filtering - w/o slicing - JSON',
            capsize=2, ecolor='grey', hatch="//")

    plt.bar(br2, s1_ns_0, yerr=s1_ns_e_0, color='g', width=barWidth, edgecolor='grey',
            label='with triple filtering - w/o slicing - CSV',
            capsize=2, ecolor='grey')
    plt.bar(br21, s1_ns_1, yerr=s1_ns_e_1, color='g', width=barWidth, edgecolor='grey',
            label='Strategy 1 w/o slicing CSV',
            capsize=2, ecolor='grey', hatch="//")

    plt.bar(br3, s0_s_0, yerr=s0_s_e_0, color='b', width=barWidth, edgecolor='grey',
            label='w/o triple filtering - with slicing - CSV',
            capsize=2, ecolor='grey')
    plt.bar(br31, s0_s_1, yerr=s0_s_e_1, color='b', width=barWidth, edgecolor='grey',
            label='w/o triple filtering - with slicing - JSON',
            capsize=2, ecolor='grey', hatch="//")

    plt.bar(br4, s1_s_0, yerr=s1_s_e_0, color='y', width=barWidth, edgecolor='grey',
            label='with triple filtering - with slicing - CSV',
            capsize=2, ecolor='grey')
    plt.bar(br41, s1_s_1, yerr=s1_s_e_1, color='y', width=barWidth, edgecolor='grey',
            label='with triple filtering - with slicing - JSON',
            capsize=2, ecolor='grey', hatch="//")

    # Adding Xticks
    plt.ylabel('Average Execution Time (ms)')
    plt.xticks([r + 4 * barWidth for r in range(len(s0_ns_0))], [f"q{q}" for q in range(1, 19)])
    plt.legend()

    # plt.show()
    plt.savefig(f"{out_folder}/{i}_{m}.png")
    plt.clf()


def configuration_to_key(configuration):
    return configuration["slice"] + configuration["strategy"] + str(configuration["ondisk"])


def generate_chart_for_all_formats_all_memories(i):
    barWidth = 0.1
    times = {
        configuration_to_key(configurations[0]) + formats[0]: [],
        configuration_to_key(configurations[1]) + formats[0]: [],
        configuration_to_key(configurations[2]) + formats[0]: [],
        configuration_to_key(configurations[3]) + formats[0]: [],

        configuration_to_key(configurations[0]) + formats[1]: [],
        configuration_to_key(configurations[1]) + formats[1]: [],
        configuration_to_key(configurations[2]) + formats[1]: [],
        configuration_to_key(configurations[3]) + formats[1]: []
    }

    stds = {
        configuration_to_key(configurations[0]) + formats[0]: [],
        configuration_to_key(configurations[1]) + formats[0]: [],
        configuration_to_key(configurations[2]) + formats[0]: [],
        configuration_to_key(configurations[3]) + formats[0]: [],

        configuration_to_key(configurations[0]) + formats[1]: [],
        configuration_to_key(configurations[1]) + formats[1]: [],
        configuration_to_key(configurations[2]) + formats[1]: [],
        configuration_to_key(configurations[3]) + formats[1]: []
    }
    for configuration in configurations:

        for q in range(1, 19):

            run_0 = summary_df[
                (summary_df["Format"] == formats[0]) &
                (summary_df["Size"] == i) &
                (summary_df["Strategy"] == configuration["strategy"]) &
                (summary_df["Slice"] == configuration["slice"]) &
                (summary_df["Ondisk"] == configuration["ondisk"]) &
                (summary_df["Query"] == f"q{q}") &
                (summary_df["Status-1"] == "OK")
                ]

            if len(run_0) > 0:
                times[configuration_to_key(configuration) + formats[0]].append(np.array(run_0["Mean"]).mean())
                stds[configuration_to_key(configuration) + formats[0]].append(np.array(run_0["Mean"]).std())
            else:
                times[configuration_to_key(configuration) + formats[0]].append(0.0)
                stds[configuration_to_key(configuration) + formats[0]].append(0.0)

            run_1 = summary_df[
                (summary_df["Format"] == formats[1]) &
                (summary_df["Size"] == i) &
                (summary_df["Strategy"] == configuration["strategy"]) &
                (summary_df["Slice"] == configuration["slice"]) &
                (summary_df["Ondisk"] == configuration["ondisk"]) &
                (summary_df["Query"] == f"q{q}") &
                (summary_df["Status-1"] == "OK")
                ]

            if len(run_1) > 0:
                times[configuration_to_key(configuration) + formats[1]].append(np.array(run_1["Mean"]).mean())
                stds[configuration_to_key(configuration) + formats[1]].append(np.array(run_1["Mean"]).std())
            else:
                times[configuration_to_key(configuration) + formats[1]].append(0.0)
                stds[configuration_to_key(configuration) + formats[1]].append(0.0)
    print(times)
    # set height of bar

    c0_0 = times[configuration_to_key(configurations[0]) + formats[0]]
    c1_0 = times[configuration_to_key(configurations[1]) + formats[0]]
    c2_0 = times[configuration_to_key(configurations[2]) + formats[0]]
    c3_0 = times[configuration_to_key(configurations[3]) + formats[0]]

    c0_1 = times[configuration_to_key(configurations[0]) + formats[1]]
    c1_1 = times[configuration_to_key(configurations[1]) + formats[1]]
    c2_1 = times[configuration_to_key(configurations[2]) + formats[1]]
    c3_1 = times[configuration_to_key(configurations[3]) + formats[1]]

    ## stds
    c0_0_e = stds[configuration_to_key(configurations[0]) + formats[0]]
    c1_0_e = stds[configuration_to_key(configurations[1]) + formats[0]]
    c2_0_e = stds[configuration_to_key(configurations[2]) + formats[0]]
    c3_0_e = stds[configuration_to_key(configurations[3]) + formats[0]]

    c0_1_e = stds[configuration_to_key(configurations[0]) + formats[1]]
    c1_1_e = stds[configuration_to_key(configurations[1]) + formats[1]]
    c2_1_e = stds[configuration_to_key(configurations[2]) + formats[1]]
    c3_1_e = stds[configuration_to_key(configurations[3]) + formats[1]]

    # Set position of bar on X axis
    br1 = np.arange(len(c0_0))
    br11 = [x + barWidth for x in br1]
    br2 = [x + barWidth for x in br11]
    br21 = [x + barWidth for x in br2]
    br3 = [x + barWidth for x in br21]
    br31 = [x + barWidth for x in br3]
    br4 = [x + barWidth for x in br31]
    br41 = [x + barWidth for x in br4]

    # Make the plot"
    plt.bar(br1, c0_0, yerr=c0_0_e, color='r', width=barWidth, edgecolor='grey',
            label=(configurations[0]["description"] + " - CSV"),
            capsize=2, ecolor='grey')
    plt.bar(br11, c0_1, yerr=c0_1_e, color='r', width=barWidth, edgecolor='grey',
            label=(configurations[0]["description"] + " - JSON"),
            capsize=2, ecolor='grey', hatch="//")

    plt.bar(br2, c1_0, yerr=c1_0_e, color='g', width=barWidth, edgecolor='grey',
            label=(configurations[1]["description"] + " - CSV"),
            capsize=2, ecolor='grey')
    plt.bar(br21, c1_1, yerr=c1_1_e, color='g', width=barWidth, edgecolor='grey',
            label=(configurations[1]["description"] + " - JSON"),
            capsize=2, ecolor='grey', hatch="//")

    plt.bar(br3, c2_0, yerr=c2_0_e, color='b', width=barWidth, edgecolor='grey',
            label=(configurations[2]["description"] + " - CSV"),
            capsize=2, ecolor='grey')
    plt.bar(br31, c2_1, yerr=c2_1_e, color='b', width=barWidth, edgecolor='grey',
            label=(configurations[2]["description"] + " - JSON"),
            capsize=2, ecolor='grey', hatch="//")

    plt.bar(br4, c3_0, yerr=c3_0_e, color='y', width=barWidth, edgecolor='grey',
            label=(configurations[3]["description"] + " - CSV"),
            capsize=2, ecolor='grey')
    plt.bar(br41, c3_1, yerr=c3_1_e, color='y', width=barWidth, edgecolor='grey',
            label=(configurations[3]["description"] + " - JSON"),
            capsize=2, ecolor='grey', hatch="//")

    # Adding Xticks
    plt.ylabel('Average Execution Time (ms)')
    plt.xlim(-barWidth, len(br1) - barWidth)
    plt.xticks([r + 4 * barWidth for r in range(len(c0_0))], [f"q{q}" for q in range(1, 19)])
    plt.legend(loc='upper right')

    # plt.show()
    plt.tight_layout()
    plt.savefig(f"{out_folder}/{i}.png")
    plt.clf()


# UC: QUERY, FORMAT, MEMORY, SIZE - EXPERIMENTAL REGIME: STRATEGY, SLICE, ONDISK


for input_size in input_sizes:
    generate_chart_for_all_formats_all_memories(input_size)
    # for memory_limit in memory_limits:
    #    generate_chart_for_all_formats(input_size, memory_limit)
    #    for f in formats:
    #        generate_chart(f, input_size, memory_limit)

# generate_chart("json", 1, 256)
# generate_chart_for_all_formats(1, 256)
# generate_chart_for_all_formats(100, 256)
# generate_chart_for_all_formats(100, 512)

# generate_chart_for_all_formats_all_memories(1)
