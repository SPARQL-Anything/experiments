import pandas as pd
import numpy as np


def get_status_string(status_list):
    result = ""
    for s in status_list:
        if "OutOfMemoryError" in s:
            result += "OOM"
        elif "Timeout" in s:
            result += "T"
        else:
            result += "OK"
        result += " "
    return result


input_sizes = [1, 10, 100, 1000]
strategies = ["strategy0", "strategy1"]
slice = ["no_slice", "slice"]
memory_limits = [256, 512, 1024, 4096]
format = "csv"
measures_folder = "/Users/lgu/workspace/spice/CogComplexityAndPerformaceEvaluation/gtfs/measures2/"

for input_size in input_sizes:
    records = []
    for q in range(1, 19):

        input_file = f"{measures_folder}time_q{q}_{format}.tsv"
        df = pd.read_csv(input_file, sep='\t')

        records.append([f"Q{q}", "M256-MEAN", "M256-STD", "M256-Status",
                        "M512-MEAN", "M512-STD", "M512-Status",
                        "M1024-MEAN", "M1024-STD", "M1024-Status",
                        "M4096-MEAN", "M4096-STD", "M4096-Status"])

        for s in slice:
            for strategy in strategies:
                record = [f"{strategy}-{s}"]

                for memory_limit in memory_limits:
                    r = df[(df["InputSize"] == input_size) &
                            (df["Strategy"] == strategy) &
                            (df["Slice"] == s) &
                            (df["MemoryLimit"] == memory_limit) &
                            (df["Run"] != "AVERAGE")
                           ]

                    runs = df[(df["InputSize"] == input_size) &
                           (df["Strategy"] == strategy) &
                           (df["Slice"] == s) &
                           (df["MemoryLimit"] == memory_limit)
                           ]

                    times = np.array(r["Time"])

                    if len(times) > 0:
                        record.append(f"{times.mean():.1f}".replace(".", ","))
                        record.append(f"{times.std():.1f}".replace(".", ","))
                    else:
                        record.append("NA")
                        record.append("NA")

                    record.append(get_status_string(list(runs[runs["STDErr"].notna()]["STDErr"])))



                #record.append(status)
                records.append(record)


    pd.DataFrame(records).to_csv(f"aggr_{input_size}_{format}.tsv", sep='\t', index=False, header=False)



