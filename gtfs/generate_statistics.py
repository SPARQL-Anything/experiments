import pandas as pd

summary_file = "/Users/lgu/workspace/SPARQLAnything/CogComplexityAndPerformaceEvaluation/gtfs/swj_experiments/summary.tsv"
summary_df = pd.read_csv(summary_file, sep='\t', decimal=",")

input_sizes = [1, 10, 100, 1000]

configurations = [
    {"slice": "no_slice", "strategy": "strategy0", "ondisk": False,
     "description": "in-memory execution over a complete materialised view", "OOMEs": 0, "T": 0, "OK": 0, "NE": 0,
     "UCs": 0},
    {"slice": "no_slice", "strategy": "strategy1", "ondisk": False,
     "description": "in-memory execution optimised by a triple-filtering approach", "OOMEs": 0, "T": 0, "OK": 0,
     "NE": 0, "UCs": 0},
    {"slice": "slice", "strategy": "strategy1", "ondisk": False,
     "description": "in-memory execution over a sliced materialised view and optimised by triple-filtering", "OOMEs": 0,
     "T": 0, "OK": 0, "NE": 0, "UCs": 0},
    {"slice": "no_slice", "strategy": "strategy1", "ondisk": True,
     "description": "on-disk execution optimised by triple-filtering", "OOMEs": 0, "T": 0, "OK": 0, "NE": 0, "UCs": 0}
]
memory_limits = [256, 512, 1024, 4096, 8192, 16384, 32768]

formats = ["csv", "json"]

for configuration in configurations:
    strategy = configuration["strategy"]
    slice_option = configuration["slice"]
    ondisk = configuration["ondisk"]

    for memory_limit in memory_limits:
        for format in formats:
            for input_size in input_sizes:
                runs = summary_df[
                    (summary_df["Format"] == format) &
                    (summary_df["Size"] == input_size) &
                    (summary_df["Strategy"] == strategy) &
                    (summary_df["Slice"] == slice_option) &
                    (summary_df["Ondisk"] == ondisk) &
                    (summary_df["Memory"] == memory_limit)
                    ]

                ok = len(runs[runs['Status-1'] == 'OK'])
                t = len(runs[runs['Status-1'] == 'T'])
                oom = len(runs[runs['Status-1'] == 'OOM'])
                not_exec = len(runs[runs['Status-1'].isna()])

                configuration["OOMEs"] += oom
                configuration["T"] += t
                configuration["OK"] += ok
                configuration["NE"] += not_exec
                configuration["UCs"] += oom + t + ok + not_exec

UCs_in_memory = configurations[0]['OOMEs'] + configurations[0]['T'] + configurations[0]['OK'] + configurations[0][
    'NE'] + configurations[1]['OOMEs'] + configurations[1]['T'] + configurations[1]['OK'] + configurations[1]['NE']
om_inmemory_no_slice = summary_df[
    (summary_df["Slice"] == "no_slice") & (summary_df["Ondisk"] == False) & (summary_df["Status-1"] == 'OOM')]
sliced_or_disk_ok = summary_df[
    ((summary_df["Slice"] == "slice") | (summary_df["Ondisk"] == True)) & (summary_df["Status-1"] == 'OK')]
ok_in_memory = summary_df[
    ((summary_df["Slice"] == "no_slice") | (summary_df["Ondisk"] == False)) & (summary_df["Status-1"] == 'OK')]

print(
    f"Number of OOEMs over the number of use case in memory (with/without TF) {len(om_inmemory_no_slice)}/{UCs_in_memory} :: "
    f"{len(om_inmemory_no_slice) / UCs_in_memory}")

print(f"Number of OOEMs with slicing {configurations[2]['OOMEs']}")
print(f"Number of OOEMs with on-disk {configurations[3]['OOMEs']}/{configurations[3]['UCs']} "
      f"::: {configurations[3]['OOMEs'] / configurations[3]['UCs']}")

j = pd.merge(om_inmemory_no_slice, sliced_or_disk_ok, on=["Format", "Size", "Query", "Memory"],
             suffixes=('_im', '_sod'))

print(f"Number of UCs not supported by the complete approach and successfully executed "
      f"with slicing or on-disk {len(j[['Format', 'Size', 'Query', 'Memory']].drop_duplicates())}/ {len(om_inmemory_no_slice)} "
      f"::: {len(j[['Format', 'Size', 'Query', 'Memory']].drop_duplicates()) / len(om_inmemory_no_slice)} ")

print(f"Number of  supported  UCs over number of UCs "
      f"{len(summary_df[summary_df['Status-1'] == 'OK'][['Format', 'Size', 'Query', 'Memory']].drop_duplicates())}/"
      f"{len(summary_df[['Format', 'Size', 'Query', 'Memory']].drop_duplicates())} ::: "
      f"{len(summary_df[summary_df['Status-1'] == 'OK'][['Format', 'Size', 'Query', 'Memory']].drop_duplicates()) / len(summary_df[['Format', 'Size', 'Query', 'Memory']].drop_duplicates())}")

avg_time_strategy0 = summary_df[
    (summary_df["Strategy"] == "strategy0") & (summary_df["Slice"] == "no_slice") & (summary_df["Ondisk"] == False)][
    "Mean"].std()
avg_time_strategy1 = summary_df[
    (summary_df["Strategy"] == "strategy1") & (summary_df["Slice"] == "no_slice") & (summary_df["Ondisk"] == False)][
    "Mean"].std()

print(f"Strategy0 avg time / strategy1 avg time ::: {avg_time_strategy0}ms/{avg_time_strategy1}ms "
      f"::: {avg_time_strategy0 / avg_time_strategy1}")

ok_strategy0_inmemory_no_slice = summary_df[
    (summary_df["Slice"] == "no_slice") & (summary_df["Ondisk"] == False) & (summary_df["Strategy"] == "strategy0") & (
            summary_df["Status-1"] == 'OK')]
ok_strategy1_inmemory_no_slice = summary_df[
    (summary_df["Slice"] == "no_slice") & (summary_df["Ondisk"] == False) & (summary_df["Strategy"] == "strategy1") & (
            summary_df["Status-1"] == 'OK')]

ok_strategy0_stratety1_in_memory_no_slice = pd.merge(ok_strategy0_inmemory_no_slice, ok_strategy1_inmemory_no_slice,
                                                     on=["Format", "Size", "Query", "Memory", "Slice", "Ondisk"],
                                                     suffixes=('_s0', '_s1'))
avg_s0_by_query = ok_strategy0_stratety1_in_memory_no_slice[["Query", "Mean_s0"]].groupby("Query").mean()
avg_s1_by_query = ok_strategy0_stratety1_in_memory_no_slice[["Query", "Mean_s1"]].groupby("Query").mean()
avgtime_by_query = pd.DataFrame(data=avg_s0_by_query["Mean_s0"] / avg_s1_by_query["Mean_s1"], columns=["Mean"])

print("Avg time by query executed under in memory regimes without slicing")
print(avgtime_by_query[avgtime_by_query["Mean"] > 2].sort_values(by=["Mean"]))

ok_im_sld = pd.merge(ok_in_memory, sliced_or_disk_ok, on=["Format", "Size", "Query", "Memory"],
                     suffixes=('_im', '_sld'))
print(f"Avg time in-memory vs. avg time slice or disk {ok_im_sld['Mean_sld'].std()}/{ok_im_sld['Mean_im'].std()} "
      f":: {ok_im_sld['Mean_sld'].std() / ok_im_sld['Mean_im'].std()}")

experiment_folder = "/Users/lgu/workspace/SPARQLAnything/CogComplexityAndPerformaceEvaluation/gtfs/swj_experiments/json_and_csv"
mem_df = pd.DataFrame()
for q in range(1, 19):
    for f in formats:
        mem_df = pd.concat([mem_df, pd.read_csv(f"{experiment_folder}/mem_q{q}_{f}.tsv", sep='\t', decimal=",")])

    # .rename({"MemoryLimit": "Run_", "%cpu": "%CPU"}).rename({"Ondisk": "MemoryLimit", "PID": "%cpu", })

mem_df[(mem_df["InputSize"] == 1000) & ((mem_df["Strategy"] == "strategy0") | (mem_df["Strategy"] == "strategy1")) & (
        mem_df["Slice"] == "no_slice")][
    "PID"].std()
mem_df[(mem_df["InputSize"] == 1000) & (mem_df["Strategy"] == "strategy1") & (mem_df["Slice"] == "slice")][
    "PID"].std()

ok256 = summary_df[(summary_df["Memory"] == 256) & (summary_df["Status-1"] == "OK")]
ok512 = summary_df[(summary_df["Memory"] == 512) & (summary_df["Status-1"] == "OK")]
ok1024 = summary_df[(summary_df["Memory"] == 1024) & (summary_df["Status-1"] == "OK")]
ok4096 = summary_df[(summary_df["Memory"] == 4096) & (summary_df["Status-1"] == "OK")]
ok8192 = summary_df[(summary_df["Memory"] == 8192) & (summary_df["Status-1"] == "OK")]
ok16384 = summary_df[(summary_df["Memory"] == 16384) & (summary_df["Status-1"] == "OK")]
ok32768 = summary_df[(summary_df["Memory"] == 32768) & (summary_df["Status-1"] == "OK")]

print("Avg exec time with heap 256mb " + str(ok256["Mean"].mean()))
print("Avg exec time with heap 512mb " + str(
    pd.merge(ok256, ok512, on=["Format", "Query", "Strategy", "Slice", "Ondisk", "Size"])["Mean_y"].mean()))
print("Avg exec time with heap 1024mb " + str(
    pd.merge(ok256, ok1024, on=["Format", "Query", "Strategy", "Slice", "Ondisk", "Size"])["Mean_y"].mean()))
print("Avg exec time with heap 4096mb " + str(
    pd.merge(ok256, ok4096, on=["Format", "Query", "Strategy", "Slice", "Ondisk", "Size"])["Mean_y"].mean()))
print("Avg exec time with heap 8192mb " + str(
    pd.merge(ok256, ok8192, on=["Format", "Query", "Strategy", "Slice", "Ondisk", "Size"])["Mean_y"].mean()))
print("Avg exec time with heap 16384mb " + str(
    pd.merge(ok256, ok16384, on=["Format", "Query", "Strategy", "Slice", "Ondisk", "Size"])["Mean_y"].mean()))
print("Avg exec time with heap 32768mb " + str(
    pd.merge(ok256, ok32768, on=["Format", "Query", "Strategy", "Slice", "Ondisk", "Size"])["Mean_y"].mean()))

okjson = summary_df[(summary_df["Format"] == "json") & (summary_df["Status-1"] == "OK")]
okcsv = summary_df[(summary_df["Format"] == "csv") & (summary_df["Status-1"] == "OK")]
okjsoncsv = pd.merge(okjson, okcsv, on=["Memory", "Query", "Strategy", "Slice", "Ondisk", "Size"],
                     suffixes=("_json", "_csv"))

print(f"Avg exec time for json {okjsoncsv['Mean_json'].mean()}")
print(f"Avg exec time for csv {okjsoncsv['Mean_csv'].mean()}")

json_experiments_ooms = len(summary_df[(summary_df["Format"] == "json") & (summary_df["Status-1"] == "OOM")])
json_experiments = len(summary_df[(summary_df["Format"] == "json")])
print(f"%OOM in JSON experiments {json_experiments_ooms / json_experiments} ")

json_experiments_t = len(summary_df[(summary_df["Format"] == "json") & (summary_df["Status-1"] == "T")])
print(f"%T in JSON experiments {json_experiments_t / json_experiments} ")

csv_experiments_ooms = len(summary_df[(summary_df["Format"] == "csv") & (summary_df["Status-1"] == "OOM")])
csv_experiments = len(summary_df[(summary_df["Format"] == "csv")])
print(f"%OOM in CSV experiments {csv_experiments_ooms / csv_experiments} ")

csv_experiments_t = len(summary_df[(summary_df["Format"] == "csv") & (summary_df["Status-1"] == "T")])
print(f"%OOM in CSV experiments {csv_experiments_t / csv_experiments} ")

ondisk_run = summary_df[summary_df["Ondisk"] == True]
s1_ns_im = summary_df[
    (summary_df["Strategy"] == "strategy1") & (summary_df["Slice"] == "no_slice") & (summary_df["Ondisk"] == False)]
