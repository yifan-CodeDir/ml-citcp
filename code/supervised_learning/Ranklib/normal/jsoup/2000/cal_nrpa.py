import pandas as pd
import csv
import numpy as np
import os


files = os.listdir(os.getcwd())
file_list = []
for file in files:
    if file.startswith("_summary"):
        file_list.append(file)
# del file_list[6:12]
print(file_list)
# file_list = ['commons_imaging_failure_detail.csv']
for file in file_list:
    f = pd.read_csv(file, header=0)
    print(np.mean(f['NORMALIZED_RPA'].values))