import pandas as pd
import csv
import numpy as np
import os
import matplotlib.pyplot as plt


projects = ['commons-bcel', 'commons-csv', 'commons-dbcp', 'commons-text', 'java-faker', 'jedis', 'jsoup', 'jsprit', 'maxwell', 'nfe', 'spring-data-redis']
start_cycle_num = [129, 205, 156, 165, 96, 77, 115, 42, 104, 20, 53]

filename_list = ['commons-bcel','commons-csv','commons-dbcp','commons-text','java-faker','jedis','jsoup','maxwell','nfe','jsprit','spring-data-redis']
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
            if cur == prev or cur == "cycle_id" or cur =='Cycle':
                continue
            else:
                res_list.append(cur)
                prev = cur
        return res_list

for filename in filename_list:
    print(filename)
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

    ### RL techniques ###

    ntr_dict = {}
    for file in file_list:
        # print(file)

        if file.split('_')[0] == "pairwise" or file.split('_')[0] == "listwise" or file.split('_')[0] == "pointwise":
            df = pd.read_csv(file)
            cycle_ids = dup_remover(df["cycle_id"])
            cycle_id_list = cycle_ids[-counter:]

            ttf_list = []
            duration_list = []
            # get the ttf and total duration for each cycle
            for cycle_id in cycle_id_list:
                f = df.loc[df["cycle_id"] == cycle_id]
                f['verdict'] = f['verdict'].astype(float)
                f['last_exec_time'] = f['last_exec_time'].astype(float)
                # calculate number of test cases and number of failures, initialize distance
                ttf = 0
                for i in range(len(f)):
                    if f.iloc[i]['verdict'] == 0:
                        ttf += float(f.iloc[i]['last_exec_time'])
                    else:
                        ttf += float(f.iloc[i]['last_exec_time'])
                        break
                ttf_list.append(ttf)
                duration_list.append(np.sum(f['last_exec_time'].values))
            ntr = (np.sum(duration_list) - np.sum(ttf_list)) / np.sum(duration_list)
        elif file.split('_')[0] == "rl":
            df = pd.read_csv(file)
            cycle_ids = dup_remover(df["cycle_id"])
            cycle_id_list = cycle_ids[-counter:]

            ttf_list = []
            duration_list = []
            # get the ttf and total duration for each cycle
            for cycle_id in cycle_id_list:
                f = df.loc[df["cycle_id"] == cycle_id]
                f['failures'] = f['failures'].astype(float)
                f['time'] = f['time'].astype(float)
                # calculate number of test cases and number of failures, initialize distance
                ttf = 0
                for i in range(len(f)):
                    if f.iloc[i]['failures'] == 0:
                        ttf += f.iloc[i]['time']
                    else:
                        ttf += f.iloc[i]['time']
                        break
                ttf_list.append(ttf)
                duration_list.append(np.sum(f['time'].values))
            ntr = (np.sum(duration_list) - np.sum(ttf_list)) / np.sum(duration_list)

        elif file.split('_')[0] == "deeporder":
            df = pd.read_csv(file)
            cycle_ids = dup_remover(df["Cycle"])
            start_cycle = start_cycle_num[projects.index(filename)]
            cycle_id_list = cycle_ids[start_cycle:]

            ttf_list = []
            duration_list = []
            for cycle_id in cycle_id_list:
                f = df.loc[df["Cycle"] == cycle_id]
                # print(f['Verdict'])
                f['Verdict'] = f['Verdict'].astype(float)
                f['Duration'] = f['Duration'].astype(float)

                # if do not exist failing test
                if len(f.loc[f['Verdict'] > 0]) == 0:
                    continue
                else:
                    ttf = 0
                    for i in range(len(f)):
                        if f.iloc[i]['Verdict'] == 0:
                            ttf += f.iloc[i]['Duration']
                        else:
                            ttf += f.iloc[i]['Duration']
                            break
                    ttf_list.append(ttf)
                    duration_list.append(np.sum(f['Duration'].values))
            ntr = (np.sum(duration_list) - np.sum(ttf_list)) / np.sum(duration_list)

        elif file.split('_')[0] == "coleman":
            df = pd.read_csv(file, sep=';')
            df['total_build_duration'] = df['total_build_duration'].astype(float)
            df['time_reduction'] = df['time_reduction'].astype(float)

            start_cycle = start_cycle_num[projects.index(filename)]
            test_df = df[start_cycle:]
            fail_df = test_df.loc[test_df['ddp'] > 0]
            duration_list = fail_df['total_build_duration'].values
            reduction_list = fail_df['time_reduction'].values

            ntr = np.sum(reduction_list) / np.sum(duration_list)

        # print(fft_list)
        ntr_dict[file.split('_')[0]] = ntr

    # y1 = ddp_dict['rl'][-counter:]
    # # y2 = ddp_dict['rl-mlp'][-counter:]
    # y4 = ddp_dict['pairwise'][-counter:]
    # y10 = ddp_dict['listwise'][-counter:]
    # y11 = ddp_dict['pointwise'][-counter:]
    # y12 = ddp_dict['deeporder'][-counter:]
    # y13 = ddp_dict['coleman'][-counter:]

#### Supervised learning techniques ####
    file_list = []
    for file in files:
        if (file.endswith("failure_detail.csv")) and (file.find(filename) != -1) and (file.startswith("ranker")):
            file_list.append(file)

    # ddp_dict = {}
    for file in file_list:
        if file.startswith('ranker'):
            # calculate total duration
            df = pd.read_csv(file)
            real_df = df.loc[df['time'] != 'time']
            real_df['time'] = real_df['time'].astype(float)
            duration_list = real_df['time'].values

            f = open(file)
            reader = csv.reader(f)
            ttf_list = []
            flag = 0
            ttf = 0
            for row in reader:
                if row[-1] == "DDP" and flag == 0:
                    flag = 1
                elif flag == 1 and float(row[3]) == 0:
                    ttf += float(row[1])
                elif flag == 1 and float(row[3]) > 0:
                    ttf += float(row[1])
                    ttf_list.append(ttf)
                    ttf = 0
                    flag = 0

            ntr = (np.sum(duration_list) - np.sum(ttf_list)) / np.sum(duration_list)
            ntr_dict[file.split('_')[0]] = ntr
            f.close()

    print(ntr_dict['ranker0'])
    print(ntr_dict['ranker1'])
    print(ntr_dict['ranker2'])
    print(ntr_dict['ranker4'])
    print(ntr_dict['ranker6'])
    print(ntr_dict['deeporder'])
    print(ntr_dict['rl'])
    print(ntr_dict['coleman'])
    print(ntr_dict['pointwise'])
    print(ntr_dict['pairwise'])
    print(ntr_dict['listwise'])
    # y5 = np.array(ddp_dict['ranker0'])
    # y6 = np.array(ddp_dict['ranker1'])
    # y7 = np.array(ddp_dict['ranker2'])
    # y8 = np.array(ddp_dict['ranker4'])
    # y9 = np.array(ddp_dict['ranker6'])

    # # collect FRP for each project
    # y1_list = np.hstack((y1_list, y1))
    # # y2_list = np.hstack((y2_list, y2))
    # y4_list = np.hstack((y4_list, y4))
    # y5_list = np.hstack((y5_list, y5))
    # y6_list = np.hstack((y6_list, y6))
    # y7_list = np.hstack((y7_list, y7))
    # y8_list = np.hstack((y8_list, y8))
    # y9_list = np.hstack((y9_list, y9))
    # y10_list = np.hstack((y10_list, y10))
    # y11_list = np.hstack((y11_list, y11))
    # y12_list = np.hstack((y12_list, y12))
    # y13_list = np.hstack((y13_list, y13))



# plt.rcParams['boxplot.flierprops.markersize'] = 2
# plt.rcParams['figure.figsize'] = (6, 3)
# labels_1 = ['MART', 'RankNet', 'Rankboost', 'CA', 'L-MART', 'DeepOrder', 'RL', 'COLEMAN', 'PPO2-PO', 'ACER-PA', 'PPO1-LI']
#
# plt.vlines(6.5, 0, 1, colors="g", linestyles="dashed")
# plt.xticks(rotation=20, fontsize=9)
# plt.boxplot([y5_list, y6_list, y7_list, y8_list, y9_list, y12_list, y1_list, y13_list, y11_list, y4_list, y10_list], labels=labels_1)

# show results
# print(np.mean(y5_list))
# print(np.mean(y6_list))
# print(np.mean(y7_list))
# print(np.mean(y8_list))
# print(np.mean(y9_list))
# print(np.mean(y1_list))
# print(np.mean(y2_list))
# print(np.mean(y4_list))

# plt.ylim([-0.1, 1.1])
# plt.ylabel("DDP")
# plt.savefig("figure/RQ1.1/total_new.pdf", bbox_inches='tight')
# plt.show()

### record total DDP ###
# dict = {}
# dict['MART'] = y5_list
# dict['RankNet'] = y6_list
# dict['RankBoost'] = y7_list
# dict['CA'] = y8_list
# dict['L-MART'] = y9_list
# dict['RL'] = y1_list
# # dict['RL-MLP'] = y2_list
# dict['PPO1-LI'] = y10_list
# dict['ACER-PA'] = y4_list
# dict['PPO2-PO'] = y11_list
# dict['DeepOrder'] = y12_list
# dict['COLEMAN'] = y13_list
# df = pd.DataFrame(dict)
# df.to_csv("data_mf.csv", header=True, index=False)
