import pandas as pd


input_sizes = [1, 10, 100, 1000]
strategies = ["strategy0", "strategy1"]
slice = ["no_slice", "slice"]
memory_limits = [256, 512, 1024, 4096]
format = "json"
measures_folder = "/Users/lgu/workspace/spice/CogComplexityAndPerformaceEvaluation/gtfs/measures/"

for input_size in input_sizes:
    records = []
    for q in range(1,19):

        input_file = f"{measures_folder}time_q{q}_{format}.tsv"
        df = pd.read_csv(input_file, sep='\t')

        records.append([f"Q{q}", "M256", "M512", "M1024", "M4096", "Status"])

        for s in slice:
            for strategy in strategies:
                record = [f"{strategy}-{s}"]
                status = ""
                for memory_limit in memory_limits:
                    r = df[(df["InputSize"] == input_size) &
                            (df["Strategy"] == strategy) &
                            (df["Slice"] == s) &
                            (df["MemoryLimit"] == memory_limit) &
                            (df["Run"] == "AVERAGE")
                           ]
                    runs = df[(df["InputSize"] == input_size) &
                           (df["Strategy"] == strategy) &
                           (df["Slice"] == s) &
                           (df["MemoryLimit"] == memory_limit)
                           ]
                    status += " ".join(list(runs[runs["Status"].notna()]["Status"]))
                    status += " / "
                    try:
                        record.append(int(r["Time"]))
                    except:
                        record.append("NOT_AVAILABLE")

                record.append(status)
                records.append(record)

        #records.extend(records)

    pd.DataFrame(records).to_csv(f"aggr_{input_size}_{format}.tsv", sep='\t', index=False, header=False)



