import os

import numpy as np
import pandas as pd


def get_status_string(status_list):
    result = ""
    for s in status_list:
        if "OutOfMemoryError" in s:
            result += "OOM"
        elif "Timeout" in s:
            result += "T"
        elif "Exception" in s:
            result += "E"
        else:
            result += "OK"
        result += " "
    return result


def get_status_list(status_list):
    result = []
    for s in status_list:
        if "OutOfMemoryError" in s:
            result.append("OOM")
        elif "Timeout" in s:
            result.append("T")
        elif "Exception" in s:
            result.append("E")
        else:
            result.append("OK")
    return result


input_sizes = [1, 10, 100, 1000]

configurations = [
    {"slice": "no_slice", "strategy": "strategy0", "ondisk": False},
    {"slice": "no_slice", "strategy": "strategy1", "ondisk": False},
    {"slice": "slice", "strategy": "strategy1", "ondisk": False},
    {"slice": "no_slice", "strategy": "strategy1", "ondisk": True}
]
memory_limits = [256, 512, 1024, 4096, 8192, 16384, 32768]
format = "json"
experiment_folder = "/Users/lgu/workspace/SPARQLAnything/CogComplexityAndPerformaceEvaluation/gtfs/swj_experiments/202210014-experiment_json_1_10_100_1000/"
out_folder = f"{experiment_folder}summary_{format}"

if not os.path.exists(out_folder):
    os.mkdir(out_folder)

records_summary_time = [
    [f"Format", "Query", "Strategy", "Slice", "Size", "Ondisk", "Memory", "Mean", "Std", "Status-1", "Status-2",
     "Status-3"]]

for input_size in input_sizes:

    records_time_per_size = []

    for q in range(1, 19):

        time_df = pd.read_csv(f"{experiment_folder}time_q{q}_{format}.tsv", sep='\t')

        time_headers = [f"Q{q}"]
        for memory_limit in memory_limits:
            time_headers.append(f"M{memory_limit}-MEAN")
            time_headers.append(f"M{memory_limit}-STD")
            time_headers.append(f"M{memory_limit}-Status")
        records_time_per_size.append(time_headers)

        for configuration in configurations:
            s = configuration["slice"]
            strategy = configuration["strategy"]
            ondisk = configuration["ondisk"]

            record_per_size = [f"{strategy}-{s}-ondisk:{ondisk}"]

            for memory_limit in memory_limits:
                r = time_df[(time_df["InputSize"] == input_size) &
                            (time_df["Strategy"] == strategy) &
                            (time_df["Slice"] == s) &
                            (time_df["MemoryLimit"] == memory_limit) &
                            (time_df["Ondisk"] == ondisk) &
                            (time_df["Run"] != "AVERAGE")
                            ]

                record_summary_time = [format, f"q{q}", strategy, s, input_size, ondisk, memory_limit]

                times = np.array(r["Time"])

                if len(times) > 0:
                    record_per_size.append(f"{times.mean():.1f}".replace(".", ","))
                    record_per_size.append(f"{times.std():.1f}".replace(".", ","))

                    record_summary_time.append(f"{times.mean():.1f}".replace(".", ","))
                    record_summary_time.append(f"{times.std():.1f}".replace(".", ","))
                else:
                    record_per_size.append("NA")
                    record_per_size.append("NA")

                    record_summary_time.append("NA")
                    record_summary_time.append("NA")

                record_per_size.append(get_status_string(list(r[r["STDErr"].notna()]["STDErr"])))

                record_summary_time.extend(get_status_list(list(r[r["STDErr"].notna()]["STDErr"]))[:3])
                records_summary_time.append(record_summary_time)

            records_time_per_size.append(record_per_size)

    pd.DataFrame(records_time_per_size).to_csv(f"{out_folder}/aggr_time_{input_size}_{format}.tsv", sep='\t',
                                               index=False,
                                               header=False)

pd.DataFrame(records_summary_time).to_csv(f"{out_folder}/summary_{format}.tsv", sep='\t', index=False, header=False)
