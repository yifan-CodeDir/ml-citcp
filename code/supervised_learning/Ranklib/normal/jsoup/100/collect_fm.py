import pandas as pd
import csv
import numpy as np
import os

files = os.listdir(os.getcwd())
file_list = []
for file in files:
    if file.startswith("_summary"):
        file_list.append(file)


# file_list = ['aviatorscript_failure_detail.csv', 'commons-bcel_failure_detail.csv', 'commons-configuration_failure_detail.csv', 'commons-csv_failure_detail.csv', 'commons-dbcp_failure_detail.csv', 'commons-text_failure_detail.csv','java-faker_failure_detail.csv', 'jedis_failure_detail.csv', 'maxwell_failure_detail.csv', 'nfe_failure_detail.csv']
print(file_list)
for file in file_list:
    reader = pd.read_csv(file)
    print(reader.iloc[0][-1])

