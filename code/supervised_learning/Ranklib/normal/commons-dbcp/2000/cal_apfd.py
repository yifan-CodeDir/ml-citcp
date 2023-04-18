import pandas as pd
import csv
import numpy as np
import os

training_size = 2000

files = os.listdir(os.getcwd())
file_list = []
for file in files:
    if file.endswith("failure_detail.csv"):
        file_list.append(file)
# file_list = ['commons-bcel_failure_detail.csv', 'commons-configuration_failure_detail.csv', 'commons-csv_failure_detail.csv', 'commons-dbcp_failure_detail.csv', 'commons-text_failure_detail.csv','java-faker_failure_detail.csv', 'jedis_failure_detail.csv', 'maxwell_failure_detail.csv', 'nfe_failure_detail.csv', 'jsoup_failure_detail.csv']
# file_list = ['commons-dbcp_failure_detail.csv']
print(file_list)

dataset = "commons-dbcp"
ref_file = "C:\\Users\\insane\\Desktop\\RT-CI-master-ICSE\\code\\TestPrioritization\\Ranklib\\normal\\" + dataset + "\\" \
           + str(training_size) + "\\" + "ranker0_failure_detail.csv"
if os.path.exists(ref_file):
    ref_f = open(ref_file)
    ref_reader = csv.reader(ref_f)
    counter = 0
    for row in ref_reader:
        if row[-1] == "failure_metric":
            counter += 1
        else:
            continue
else:
    counter = 0

dataset_file = "C:\\Users\\insane\\Desktop\\RT-CI-master-ICSE\\code\\TestPrioritization\\Ranklib\\dataset_sources\\normal\\" + dataset + "_result.csv"
df = pd.read_csv(dataset_file)
df = df.loc[df['current_failures'] > 0]
commit_id_list = list(df['cycle_id'])
commit_id_list_ = list(set(commit_id_list))
commit_id_list_.sort(key=commit_id_list.index)
length_list = []
rdf = pd.read_csv(dataset_file)
for commit_id in commit_id_list_:
    length_list.append(len(rdf.loc[rdf['cycle_id']==commit_id]))

length_list = length_list[-counter:]
# print(length_list)
for file in file_list:
    f = open(file)
    apfd_list = []
    reader = csv.reader(f)
    df = pd.read_csv(file)
    flag = 0
    count = -1
    for row in reader:
        if row[-1] == "failure_metric":
            flag = 1
            fft = 0
            count += 1
        elif flag == 1:
            apfd_list.append(1-float(row[-1])+1/(2*length_list[count]))
            flag = 0
        else:
            continue
    # print(fft_list)
    print(np.mean(apfd_list))





