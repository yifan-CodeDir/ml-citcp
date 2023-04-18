import pandas as pd
import csv
import numpy as np
import os
import json



projects = ['commons-bcel', 'commons-csv', 'commons-dbcp', 'commons-text', 'java-faker', 'jedis', 'jsoup', 'jsprit', 'maxwell', 'nfe', 'spring-data-redis']

max_apfd_dict = {}
for p in projects:
    data = pd.read_csv(f"{p}_result.csv", header=0, sep=",")

    commit_id_list = list(data['cycle_id'])
    commit_id_list = list(dict.fromkeys(commit_id_list))

    max_apfd_list = []
    for commit_id in commit_id_list:
        data_subset = data.loc[data['cycle_id'] == commit_id]
        n = len(data_subset)
        m = len(data_subset.loc[data_subset['current_failures'] > 0])
        if m > 0:   # only record failing cycle
            max_apfd_list.append(1 - m/(2*n))

    max_apfd_dict[p] = max_apfd_list

with open("max_apfd.json", "w") as f:
    json.dump(max_apfd_dict, f, indent=4)

