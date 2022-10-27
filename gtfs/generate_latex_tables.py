import pandas as pd

input_sizes = [1, 10, 100, 1000]

configurations = [
    {"slice": "no_slice", "strategy": "strategy0", "ondisk": False, "description": "in-memory execution over a complete materialised view"},
    {"slice": "no_slice", "strategy": "strategy1", "ondisk": False, "description": "in-memory execution optimised by a triple-filtering approach"},
    {"slice": "slice", "strategy": "strategy1", "ondisk": False, "description": "in-memory execution over a sliced materialised view and optimised by triple-filtering"},
    {"slice": "no_slice", "strategy": "strategy1", "ondisk": True, "description": "on-disk execution optimised by triple-filtering"}
]
memory_limits = [256, 512, 1024, 4096, 8192, 16384, 32768]

formats = ["csv", "json"]
summary_file = "/Users/lgu/workspace/SPARQLAnything/CogComplexityAndPerformaceEvaluation/gtfs/swj_experiments/summary.tsv"

summary_df = pd.read_csv(summary_file, sep='\t')

for configuration in configurations:
    strategy = configuration["strategy"]
    slice_option = configuration["slice"]
    ondisk = configuration["ondisk"]

    table_string_latex = "\\begin{table}[h]\n\t\centering\n\t\\begin{tabular}{c|c|c|c|c|c|c|c|c}\n\t\hline & " \
                         "\multicolumn{4}{c|}{CSV}  & \multicolumn{4}{c}{JSON}  " \
                         "\\\\ \n\t & 1 & 10 & 100 & 1000 & 1 & 10 & 100 & 1000 \\\\\\hline\n"
    for memory_limit in memory_limits:
        row_string = f"\n\t{memory_limit}"
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

                row_string += f" & \\ok{{{ok}}}-\\ti{{{t}}}-\\oom{{{oom}}}-\\nex{{{not_exec}}} % {strategy}-{slice_option}-{memory_limit}-{format}-{input_size} \n\t "

        row_string += "\n \\\\"
        table_string_latex += row_string

    table_string_latex += f"\n\t\hline\n\t\end{{tabular}} \n\t\caption{{ Results of the execution of the queries under the regime  {configuration['description']}. Each cell reports the number of queries successfully executed (green), those exceeding the timeout (orange) or the memory limit (red), and those not executed (black). }} \n\t\label{{tab:{strategy}_{slice_option}_{ondisk}}}\n\end{{table}}"

    print(table_string_latex)
    print("\n\n\n")
