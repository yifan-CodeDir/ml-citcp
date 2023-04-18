import pandas as pd
import csv
import numpy as np
import os
import matplotlib.pyplot as plt
import json


filename_list = ['commons-bcel', 'commons-csv', 'commons-dbcp', 'commons-text', 'java-faker', 'jedis', 'jsoup', 'jsprit', 'maxwell', 'nfe', 'spring-data-redis']
# filename_list = ['commons-bcel','jedis','nfe','jsprit','spring-data-redis']
training_size = 2000

y1_list = np.array([])
y2_list = np.array([])
y3_list = np.array([])
y4_list = np.array([])
y5_list = np.array([])
y6_list = np.array([])
y7_list = np.array([])
y8_list = np.array([])
y9_list = np.array([])
y10_list = np.array([])
y11_list = np.array([])
y12_list = np.array([])
y13_list = np.array([])


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

with open("max_apfd.json", "r") as f:
    max_apfd_dict = json.load(f)

for filename in filename_list:
    # print(filename)
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

    max_apfd_list = max_apfd_dict[filename]

    ### RL techniques ###
    apfd_dict = {}
    for file in file_list:

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

    # collect FRP for each project
    y1_list = np.hstack((y1_list, y1)) # RL
    # y2_list = np.hstack((y2_list, y2))
    y4_list = np.hstack((y4_list, y4)) # ACER-PA
    y5_list = np.hstack((y5_list, y5)) # MART
    y6_list = np.hstack((y6_list, y6)) # RankNet
    y7_list = np.hstack((y7_list, y7)) # RankBoost
    y8_list = np.hstack((y8_list, y8)) # CA
    y9_list = np.hstack((y9_list, y9)) # L-MART
    y10_list = np.hstack((y10_list, y10)) # PPO1-LI
    y11_list = np.hstack((y11_list, y11)) # PPO2-PO
    y12_list = np.hstack((y12_list, y12)) # DeepOrder
    y13_list = np.hstack((y13_list, y13)) # COLEMAN

    # print(filename)
    # print(np.mean(y7))


plt.rcParams['boxplot.flierprops.markersize'] = 2
plt.rcParams['figure.figsize'] = (6, 3)
labels_1 = ['MART', 'RankNet', 'Rankboost', 'CA', 'L-MART', 'DeepOrder', 'RL', 'COLEMAN', 'PPO2-PO', 'ACER-PA', 'PPO1-LI']

medianprops = {'linestyle':'-','color':'black'}
# plt.vlines(6.5, 0, 1, colors="g", linestyles="dashed")
plt.xticks(rotation=20, fontsize=9)
f = plt.boxplot([y5_list, y6_list, y7_list, y8_list, y9_list, y12_list, y1_list, y13_list, y11_list, y4_list, y10_list], labels=labels_1, patch_artist=True, medianprops=medianprops)

c_list = ['#84C1FF', '#84C1FF', '#84C1FF','#84C1FF','#84C1FF','#84C1FF', '#93FF93','#93FF93','#93FF93','#93FF93','#93FF93']  
for box, c in zip(f['boxes'], c_list):  # set color
    # box.set(color=c, linewidth=2)
    box.set(facecolor=c)
# plt.show()

plt.legend(f['boxes'][0:7:6], ["SL-based","RL-based"], loc=8, bbox_to_anchor=(0.5, -0.3), borderaxespad=0, fontsize=8, ncol=2)  
# plt.legend(f['boxes'][6:7], ["reinforcement"], loc=8, bbox_to_anchor=(0.6, -0.25), borderaxespad=0, fontsize=8, ncol=2)  
plt.ylim([-0.1, 1.1])
plt.ylabel("rAPFD")
plt.savefig("figure/RQ1.1/total_new_apfd.pdf", bbox_inches='tight')
plt.show()


# df = pd.DataFrame(dict)
# # df.to_csv("data_mf.csv", header=True, index=False)
# df.to_csv("ddp_record.csv", header=True, index=False)
