import pandas as pd
import csv
import numpy as np
import os

projects = ['commons-bcel', 'commons-csv', 'commons-dbcp', 'commons-text', 'java-faker', 'jedis', 'jsoup', 'jsprit', 'maxwell', 'nfe', 'spring-data-redis']
start_cycle_num = [129, 205, 156, 165, 96, 77, 115, 42, 104, 20, 53]
total_cycle_num = [177, 270, 324, 224, 217, 446, 378, 75, 231, 185, 177]

files = os.listdir(os.getcwd())
file_list = []
for file in files:
    if file.startswith("training_time_"):
        file_list.append(file)
# del file_list[6:12]
print(file_list)
# file_list = ['commons_imaging_failure_detail.csv']
for file in file_list:
    with open(file, 'r') as f:
        time = f.read()
        time = float(time)/1000000000 * 1000
        print(time)

files = os.listdir(os.getcwd())
file_list = []
for file in files:
    if file.startswith("test_time_"):
        file_list.append(file)
# del file_list[6:12]
print(file_list)
# file_list = ['commons_imaging_failure_detail.csv']
for file in file_list:
    with open(file, 'r') as f:
        time = f.read()
        time = float(time)/1000000000 * 1000
        print(time)