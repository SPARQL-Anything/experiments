import pandas as pd
import numpy as np
import os


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


input_sizes = [1, 10, 100, 1000]
strategies = ["strategy0", "strategy1"]
slice = ["no_slice", "slice"]
memory_limits = [256, 512, 1024, 4096]
format = "json"
measures_folder = "/Users/lgu/workspace/spice/CogComplexityAndPerformaceEvaluation/gtfs/measures/"
#out_folder = "aggregated_measures_json_1_10_100_1000_2"
out_folder = "aggregated_measures_xml_1_10_100_1000"

if not os.path.exists(out_folder):
    os.mkdir(out_folder)

for input_size in input_sizes:

    records_time = []
    records_mem = []

    for q in range(1, 19):

        time_df = pd.read_csv(f"{measures_folder}time_q{q}_{format}.tsv", sep='\t')
        mem_df = pd.read_csv(f"{measures_folder}mem_q{q}_{format}.tsv", sep='\t')

        records_time.append([f"Q{q}", "M256-MEAN", "M256-STD", "M256-Status",
                        "M512-MEAN", "M512-STD", "M512-Status",
                        "M1024-MEAN", "M1024-STD", "M1024-Status",
                        "M4096-MEAN", "M4096-STD", "M4096-Status"])

        records_mem.append([f"Q{q}", "M256-CPU-MEAN", "M256-CPU-STD", "M256-RSS-MEAN", "M256-RSS-STD", "M256-Status",
                         "M512-CPU-MEAN", "M512-CPU-STD", "M512-RSS-MEAN", "M512-RSS-STD", "M512-Status",
                         "M1024-CPU-MEAN", "M1024-CPU-STD", "M1024-RSS-MEAN", "M1024-RSS-STD", "M1024-Status",
                         "M4096-CPU-MEAN", "M4096-CPU-STD", "M4096-RSS-MEAN", "M4096-RSS-STD", "M4096-Status"])

        for s in slice:
            for strategy in strategies:
                record = [f"{strategy}-{s}"]
                record_mem = [f"{strategy}-{s}"]

                for memory_limit in memory_limits:
                    r = time_df[(time_df["InputSize"] == input_size) &
                            (time_df["Strategy"] == strategy) &
                            (time_df["Slice"] == s) &
                            (time_df["MemoryLimit"] == memory_limit) &
                            (time_df["Run"] != "AVERAGE")
                           ]

                    mem_runs = mem_df[(mem_df["InputSize"] == input_size) &
                                (mem_df["Strategy"] == strategy) &
                                (mem_df["Slice"] == s) &
                                (mem_df["MemoryLimit"] == memory_limit)
                                ]

                    times = np.array(r["Time"])

                    # cpus_1 = np.array(mem_runs[mem_runs["Run"] == "RUN1"]["%cpu"])
                    # cpus_2 = np.array(mem_runs[mem_runs["Run"] == "RUN2"]["%cpu"])
                    # cpus_3 = np.array(mem_runs[mem_runs["Run"] == "RUN3"]["%cpu"])
                    cpu = np.array(mem_runs["%cpu"])

                    # rss_1 = np.array(mem_runs[mem_runs["Run"] == "RUN1"]["%rss"])
                    # rss_2 = np.array(mem_runs[mem_runs["Run"] == "RUN2"]["%rss"])
                    # rss_3 = np.array(mem_runs[mem_runs["Run"] == "RUN3"]["%rss"])
                    rss = np.array(mem_runs["rss"])

                    if len(times) > 0:
                        record.append(f"{times.mean():.1f}".replace(".", ","))
                        record.append(f"{times.std():.1f}".replace(".", ","))
                    else:
                        record.append("NA")
                        record.append("NA")

                    if len(cpu) > 0:
                        record_mem.append(f"{cpu.mean():.1f}".replace(".", ","))
                        record_mem.append(f"{cpu.std():.1f}".replace(".", ","))
                    else:
                        record_mem.append("NA")
                        record_mem.append("NA")

                    if len(rss) > 0:
                        record_mem.append(f"{rss.mean():.1f}".replace(".", ","))
                        record_mem.append(f"{rss.std():.1f}".replace(".", ","))
                    else:
                        record_mem.append("NA")
                        record_mem.append("NA")

                    record.append(get_status_string(list(r[r["STDErr"].notna()]["STDErr"])))
                    record_mem.append(get_status_string(list(r[r["STDErr"].notna()]["STDErr"])))

                records_time.append(record)
                records_mem.append(record_mem)


    pd.DataFrame(records_time).to_csv(f"{out_folder}/aggr_time_{input_size}_{format}.tsv", sep='\t', index=False, header=False)
    pd.DataFrame(records_mem).to_csv(f"{out_folder}/aggr_mem_{input_size}_{format}.tsv", sep='\t', index=False, header=False)



