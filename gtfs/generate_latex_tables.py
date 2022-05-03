import pandas as pd
import numpy as np
import os


input_sizes = [1, 10, 100, 1000]
#input_sizes = [ 1000]
strategies = ["strategy0", "strategy1"]
slice_options = ["no_slice", "slice"]
#memory_limits = [256, 512, 1024, 4096]
memory_limits = [256, 512, 1024, 4096]
formats = ["csv", "json"]
summary_file = "/Users/lgu/Desktop/GTFS_summary - Foglio1.tsv"

summary_df = pd.read_csv(summary_file, sep='\t')


for strategy in strategies:
    for slice_option in slice_options:
        table_string_latex="\\begin{table}[h]\n\t\centering\n\t\\begin{tabular}{c|c|c|c|c|c|c|c|c}\n\t\hline & " \
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
                                    (summary_df["Memory"] == memory_limit)
                                ]

                    #print(runs)
                    #print(f"{format} {input_size} {strategy} {slice_option} {memory_limit}")
                    #print(f"OK: {len(runs[runs['Status-1'] == 'OK'])}")
                    #print(f"T: {len(runs[runs['Status-1'] == 'T'])}")
                    #print(f"OOM: {len(runs[runs['Status-1'] == 'OOM'])}")
                    #print(f"Nan: {len(runs[runs['Status-1'].isna()])}")

                    ok = len(runs[runs['Status-1'] == 'OK'])
                    t = len(runs[runs['Status-1'] == 'T'])
                    oom = len(runs[runs['Status-1'] == 'OOM'])
                    not_exec = len(runs[runs['Status-1'].isna()])

                    row_string += f" & \\ok{{{ok}}}-\\ti{{{t}}}-\\oom{{{oom}}}-\\nex{{{not_exec}}} % {strategy}-{slice_option}-{memory_limit}-{format}-{input_size} \n\t "

            row_string += "\n \\\\"
            table_string_latex += row_string

        table_string_latex += f"\n\t\hline\n\t\end{{tabular}} \n\t\caption{{{strategy} {slice_option.replace('_',' ')}}} \n\t\label{{tab:{strategy}_{slice_option}}}\n\end{{table}}"

        print(table_string_latex)
        print("\n\n\n")
