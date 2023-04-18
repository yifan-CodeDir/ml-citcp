import pandas as pd
import csv
import numpy as np
import os

files = os.listdir(os.getcwd())
file_list = []
for file in files:
    if file.endswith("failure_detail.csv"):
        file_list.append(file)


# file_list = ['aviatorscript_failure_detail.csv', 'commons-bcel_failure_detail.csv', 'commons-configuration_failure_detail.csv', 'commons-csv_failure_detail.csv', 'commons-dbcp_failure_detail.csv', 'commons-text_failure_detail.csv','java-faker_failure_detail.csv', 'jedis_failure_detail.csv', 'maxwell_failure_detail.csv', 'nfe_failure_detail.csv']
# print(file_list)
print("FFT:")
for file in file_list:
    f = open(file)
    fft_list = []
    reader = csv.reader(f)

    flag = 0
    for row in reader:
        if row[6] == "failure_metric":
            flag = 1
            fft = 0
        elif flag == 1:
            if float(row[3]) == 0:
                fft += float(row[1])
            else:
                fft += float(row[1])
                fft_list.append(fft)
                flag = 0
        else:
            continue
    # print(fft_list)
    print(np.sum(fft_list)*1000)

print("LFT:")
for file in file_list:
    f = open(file)
    lft_list = []
    lft = 0
    reader = csv.reader(f)
    last_time_list = [0]
    failures = []
    flag = 0

    for row in reader:
        if row[6] == "failure_metric":
            if flag > 0:
                index = [i for i,x in enumerate(failures) if x > 0]
                lft_list.append(last_time_list[index[-1]+1])
            failures = []
            last_time_list = [0]
            flag = 1
        else:
            failures.append(float(row[3]))
            last_time_list.append(last_time_list[-1] + float(row[1]))
    # print(fft_list)

    index = [i for i, x in enumerate(failures) if x > 0]
    lft_list.append(last_time_list[index[-1]+1])

    # print(lft_list)
    print(np.sum(lft_list)*1000)

