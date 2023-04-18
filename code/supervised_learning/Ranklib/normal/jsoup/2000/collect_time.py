import pandas as pd
import csv
import numpy as np
import os


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