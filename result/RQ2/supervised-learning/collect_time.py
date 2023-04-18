import pandas as pd
import csv
import numpy as np
import os

projects = ['bcel', 'csv', 'dbcp', 'text', 'java-faker', 'jedis', 'jsoup', 'jsprit', 'maxwell', 'nfe', 'spring-data-redis']
start_cycle_num = [129, 205, 156, 165, 96, 77, 115, 42, 104, 20, 53]
total_cycle_num = [177, 270, 324, 224, 217, 446, 378, 75, 231, 185, 177]

for project in projects:
    print("-------------" + project + "-------------")
    files = os.listdir("./" + project + '/')
    file_list = []
    for file in files:
        if file.startswith("training_time_"):
            file_list.append(file)
    # del file_list[6:12]
    # print(file_list)
    # file_list = ['commons_imaging_failure_detail.csv']
    start_cycle = start_cycle_num[projects.index(project)]
    total_cycle = total_cycle_num[projects.index(project)]
    training_dict = {}
    for file in file_list:
        with open("./" + project + '/' + file, 'r') as f:
            time = f.read()
            time = float(time)/1000000000   # (in seconds)
            training_dict[file.split('_')[-1][:-4]] = time / start_cycle

    files = os.listdir("./" + project + '/')
    file_list = []
    for file in files:
        if file.startswith("test_time_"):
            file_list.append(file)
    # del file_list[6:12]
    # print(file_list)
    # file_list = ['commons_imaging_failure_detail.csv']
    testing_dict = {}
    for file in file_list:
        with open("./" + project + '/' + file, 'r') as f:
            time = f.read()
            time = float(time)/1000000000  # (in seconds)
            testing_dict[file.split('_')[-1][:-4]] = time / (total_cycle - start_cycle)

    print(training_dict['ranker0'])
    print(training_dict['ranker1'])
    print(training_dict['ranker2'])
    print(training_dict['ranker4'])
    print(training_dict['ranker6'])
    print('#################')

    print(testing_dict['ranker0'])
    print(testing_dict['ranker1'])
    print(testing_dict['ranker2'])
    print(testing_dict['ranker4'])
    print(testing_dict['ranker6'])
    print('#################')