import pandas as pd
import csv
import numpy as np
import os


# files = os.listdir(os.getcwd())
# file_list = []
# for file in files:
#     if file.startswith("listwise_"):
#         file_list.append(file)

# the start index of testing cycles 
projects = ['commons-bcel', 'commons-csv', 'commons-dbcp', 'commons-text', 'java-faker', 'jedis', 'jsoup', 'jsprit', 'maxwell', 'nfe', 'spring-data-redis']
start_cycle_num = [129, 205, 156, 165, 96, 77, 115, 42, 104, 20, 53]
training_dict = {}
testing_dict = {}

for project in projects:
    # print(project)
    f = pd.read_csv('coleman_' + project + '.csv', sep=';')
    start_cycle = start_cycle_num[projects.index(project)]

    training_dict[project] = (np.mean(f['prioritization_time'].values)/1000)
    testing_dict[project] = (np.mean(f.iloc[start_cycle:]['prioritization_time'].values)/1000)

    # print(np.sum(f.iloc[start_cycle:]['testing_time'].values))
    # print(np.sum(f['training_time'].values))

print(training_dict['commons-bcel'])
print(training_dict['jedis'])
print(training_dict['jsprit'])
print(training_dict['nfe'])
print(training_dict['spring-data-redis'])
print(training_dict['commons-csv'])
print(training_dict['commons-dbcp'])
print(training_dict['commons-text'])
print(training_dict['java-faker'])
print(training_dict['jsoup'])
print(training_dict['maxwell'])
print("##################")

print(testing_dict['commons-bcel'])
print(testing_dict['jedis'])
print(testing_dict['jsprit'])
print(testing_dict['nfe'])
print(testing_dict['spring-data-redis'])
print(testing_dict['commons-csv'])
print(testing_dict['commons-dbcp'])
print(testing_dict['commons-text'])
print(testing_dict['java-faker'])
print(testing_dict['jsoup'])
print(testing_dict['maxwell'])
print("##################")

# print('Training time interval:')
# print(np.min(training_time_list))
# print(np.max(training_time_list))
#
# print('Testing time interval:')
# print(np.min(testing_time_list))
# print(np.max(testing_time_list))




