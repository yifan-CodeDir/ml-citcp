import pandas as pd
import csv
import numpy as np
import os
import matplotlib.pyplot as plt
import math
import json

# filename_list = ['bcel','commons-csv','dbcp','text','java-faker','jedis','jsoup','maxwell','nfe']
# interval = 5
# only plot jedis, nfe, spring-data-redis
#             214, 86, 91
filename = 'nfe'
# training_size = 2000

# def rolling(value):
#     result = []
#     for i in range(interval, len(value)):
#         result.append(np.mean(value[i-interval:i]))
#     return result

files = os.listdir(os.getcwd())
file_list = []


for file in files:
    if (file.endswith(".csv")) and (file.find(filename) != -1) and not (file.startswith("ranker")):
        file_list.append(file)

# calculate the number of testing cycles
ref_file = "ranker0_" + filename + "_failure_detail.csv"
ref_f = open(ref_file)
ref_reader = csv.reader(ref_f)
counter = 0
for row in ref_reader:
    if row[-1] == "DDP":
        counter += 1
    else:
        continue

# print(counter)

with open("max_apfd.json", "r") as f:
    max_apfd_dict = json.load(f)

max_apfd_list = max_apfd_dict[filename]

### RL techniques ###

def dup_remover(id_list):
    prev = ""
    res_list = []
    for i in range(len(id_list)):
        cur = id_list.iloc[i]
        if cur == prev or cur == "cycle_id":
            continue
        else:
            res_list.append(cur)
            prev = cur
    return res_list


apfd_dict = {}

for file in file_list:
    # print(file)

    apfd_list = []

    if file.split('_')[0] == "pairwise" or file.split('_')[0] == "listwise" or file.split('_')[0] == "pointwise":
        df = pd.read_csv(file)
        cycle_ids = dup_remover(df["cycle_id"])
        cycle_id_list = cycle_ids[-counter:]
        for cycle_id in cycle_id_list:
            f = df.loc[df["cycle_id"] == cycle_id]
            f['verdict'] = f['verdict'].astype(float)
            n = len(f)
            m = len(f.loc[f['verdict'] > 0])
            acc_rank = 0
            for i in range(len(f)):
                if f.iloc[i]['verdict'] > 0:
                    acc_rank += i + 1
            apfd_list.append(1 - acc_rank / (n * m) + 1 / (2 * n))

    elif file.split('_')[0] == "rl":
        df = pd.read_csv(file)
        cycle_ids = dup_remover(df["cycle_id"])
        cycle_id_list = cycle_ids[-counter:]
        for cycle_id in cycle_id_list:
            f = df.loc[df["cycle_id"] == cycle_id]
            f['failures'] = f['failures'].astype(float)
            n = len(f)
            m = len(f.loc[f['failures'] > 0])
            acc_rank = 0
            for i in range(len(f)):
                if f.iloc[i]['failures'] > 0:
                    acc_rank += i + 1
            apfd_list.append(1 - acc_rank / (n * m) + 1 / (2 * n))

    elif file.split('_')[0] == "deeporder":
        # fail_test_df = test_df.loc[test_df['DDP'] >= 0.0]
        # print("111111")
        df = pd.read_csv(file, sep=';')
        df['DDP'] = df['DDP'].astype(float)
        df['NAPFD/APFD'] = df['NAPFD/APFD'].astype(float)
        fail_df = df.loc[df['DDP'] >= 0.0]
        apfd_list = fail_df['NAPFD/APFD'].values

    elif file.split('_')[0] == "coleman":
        df = pd.read_csv(file, sep=';')
        df['ddp'] = df['ddp'].astype(float)
        df['napfd/apfd'] = df['napfd/apfd'].astype(float)
        fail_df = df.loc[df['ddp'] >= 0.0]
        apfd_list = fail_df['napfd/apfd'].values
        # print(nrpa_list)

    # print(fft_list)
    apfd_dict[file.split('_')[0]] = apfd_list


y1 = [(a-(1-b))/(b-(1-b)) for a,b in zip(apfd_dict['rl'][-counter:], max_apfd_list[-counter:])]
y4 = [(a-(1-b))/(b-(1-b)) for a,b in zip(apfd_dict['pairwise'][-counter:], max_apfd_list[-counter:])]
y10 = [(a-(1-b))/(b-(1-b)) for a,b in zip(apfd_dict['listwise'][-counter:], max_apfd_list[-counter:])]
y11 = [(a-(1-b))/(b-(1-b)) for a,b in zip(apfd_dict['pointwise'][-counter:], max_apfd_list[-counter:])]
y12 = [(a-(1-b))/(b-(1-b)) for a,b in zip(apfd_dict['deeporder'][-counter:], max_apfd_list[-counter:])]
y13 = [(a-(1-b))/(b-(1-b)) for a,b in zip(apfd_dict['coleman'][-counter:], max_apfd_list[-counter:])]

#### Supervised learning techniques ####
file_list = []
for file in files:
    if (file.endswith("failure_detail.csv")) and (file.find(filename) != -1) and (file.startswith("ranker")):
        file_list.append(file)

apfd_dict = {}
for file in file_list:
    if file.startswith('ranker'):
        df = pd.read_csv(file)
        start_index_list = list(df.loc[df['rank_index'] == 'rank_index'].index)
        start_index_list.insert(0, -1)
        start_index_list.append(len(df))
        n_list = [start_index_list[i+1] - start_index_list[i] - 1 for i in range(len(start_index_list)-1)]

        # calculate apfd for each cycle
        apfd_list = []
        start_index_list = start_index_list[:-1]
        for i in range(len(start_index_list)):
            apfd_list.append(1 - float(df.iloc[start_index_list[i]+1]['failure_metric']) + 1 / (2 * n_list[i]))

        # apfd_dict[file.split('_')[0]] = apfd_list
        apfd_dict[file.split('_')[0]] = [(a-(1-b))/(b-(1-b)) for a,b in zip(apfd_list, max_apfd_list[-counter:])]

y5 = np.array(apfd_dict['ranker0'])
y6 = np.array(apfd_dict['ranker1'])
y7 = np.array(apfd_dict['ranker2'])
y8 = np.array(apfd_dict['ranker4'])
y9 = np.array(apfd_dict['ranker6'])

# plt.rcParams['boxplot.flierprops.markersize'] = 2
# plt.rcParams['figure.figsize'] = (6, 3)
# plt.boxplot([y5, y6, y7, y8, y9, y1, y2, y4], labels=labels_1)
# plt.vlines(5.5, 0, 1, colors="g", linestyles="dashed")

# plt.xticks(rotation=10, fontsize=9)



def avg_each_five_cycle(y):
    result_list = []
    for i in range(math.floor(len(y)/5)):
        avg = np.mean(y[5*i:5*i+5])
        result_list.append(avg)
    result_list.append(np.mean(y[(i+1)*5:]))
    return result_list

#### plot trend ####
# only report result every 5 cycle
x = list(range(5, len(apfd_dict['ranker0']), 5))
x.append(len(apfd_dict['ranker0']))
# print(x)
## for supervised learning
plt.plot(x, avg_each_five_cycle(y5), label='MART')
plt.plot(x, avg_each_five_cycle(y6), label='RankNet')
plt.plot(x, avg_each_five_cycle(y7), label='Rankboost')
plt.plot(x, avg_each_five_cycle(y8), label='CA')
plt.plot(x, avg_each_five_cycle(y9), label='L-MART')
plt.plot(x, avg_each_five_cycle(y12), label='DeepOrder')
## for RL
# plt.plot(x, avg_each_five_cycle(y1), label='RL')
# plt.plot(x, avg_each_five_cycle(y13), label='COLEMAN')
# plt.plot(x, avg_each_five_cycle(y11), label='PPO2-PO')
# plt.plot(x, avg_each_five_cycle(y4), label='ACER-PA')
# plt.plot(x, avg_each_five_cycle(y10), label='PPO1-LI')

# plt.xticks(range(0,len(x)),rotation=0,fontsize=9)

plt.legend(loc=8, bbox_to_anchor=(0.5, -0.2), borderaxespad=0, fontsize=8, ncol=4)
# plt.legend()
# plt.xlabel("CI cycle")
# plt.figure(dpi=300,figsize=(24,8))
plt.ylim([-0.1, 1.1])
plt.xlim([0, len(apfd_dict['ranker0'])+1])
# plt.xlim([0, 80])
plt.ylabel("rAPFD")
plt.title(filename)
# plt.title("csv")
plt.savefig("./figure/RQ1.2/su_" + filename + "_new_apfd_after80.pdf", bbox_inches='tight')
plt.show()


