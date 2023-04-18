import pandas as pd
import csv
import numpy as np
import os
import matplotlib.pyplot as plt

files = os.listdir(os.getcwd())
file_list = []
for file in files:
    if file.endswith("failure_detail.csv"):
        file_list.append(file)

fm_dict = {}
for file in file_list:
    print(file)
    f = open(file)
    fm_list = []
    reader = csv.reader(f)

    flag = 0
    for row in reader:
        if row[6] == "failure_metric":
            flag = 1
        elif flag == 1:
            fm_list.append(float(row[6]))
            flag = 0
        else:
            continue
    # print(fft_list)
    # print(fm_list)
    fm_dict[file.split('_')[0]] = fm_list

x = range(len(fm_dict['ranker0']))
y1 = fm_dict['ranker0']
y2 = fm_dict['ranker1']
y3 = fm_dict['ranker2']
y4 = fm_dict['ranker4']
y5 = fm_dict['ranker6']

plt.plot(x, y1, label="MART")
plt.plot(x, y2, label="RankNet")
plt.plot(x, y3, label="Rankboost")
plt.plot(x, y4, label="CA")
plt.plot(x, y5, label="L-MART")

plt.legend()
plt.xlabel("CI cycle")
plt.ylabel("Failure metric")
plt.title("commons-dbcp")
plt.show()




