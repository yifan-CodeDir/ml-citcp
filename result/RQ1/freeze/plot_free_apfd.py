import pandas as pd
import csv
import numpy as np
import os
import matplotlib.pyplot as plt
import json


# filename_list = ['commons-bcel','commons-csv','commons-dbcp','commons-text','java-faker','jedis','jsoup','maxwell','nfe','jsprit','spring-data-redis']
filename_list = ['jedis','nfe','spring-data-redis']
training_size = 2000

# y1_list = np.array([])
# y4_list = np.array([])
# y10_list = np.array([])
# y11_list = np.array([])

y1_list_later = np.array([])
y4_list_later = np.array([])
y10_list_later = np.array([])
y11_list_later = np.array([])

y1_list_earlier = np.array([])
y4_list_earlier = np.array([])
y10_list_earlier = np.array([])
y11_list_earlier = np.array([])

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

# collect normal result
# for filename in filename_list:
#     files = os.listdir('../')
#     file_list = []
#     for file in files:
#         if (file.endswith(".csv")) and (file.find(filename) != -1) and not (file.startswith("ranker")):
#             file_list.append(file)
#
#     # calculate the number of testing cycles
#     ref_file = "ranker0_" + filename + "_failure_detail.csv"
#     ref_f = open(ref_file)
#     ref_reader = csv.reader(ref_f)
#     counter = 0
#     for row in ref_reader:
#         if row[-1] == "DDP":
#             counter += 1
#         else:
#             continue
#
#     ### RL techniques ###
#
#     ddp_dict = {}
#     for file in file_list:
#         # print(file)
#
#         ddp_list = []
#
#         if file.split('_')[0] == "pairwise" or file.split('_')[0] == "listwise" or file.split('_')[0] == "pointwise":
#             df = pd.read_csv(file)
#             cycle_ids = dup_remover(df["cycle_id"])
#             cycle_id_list = cycle_ids[-counter:]
#             for cycle_id in cycle_id_list:
#                 f = df.loc[df["cycle_id"]==cycle_id]
#                 f['verdict'] = f['verdict'].astype(float)
#                 # calculate number of test cases and number of failures, initialize distance
#                 total_len = len(f)
#                 f_len = len(f.loc[f["verdict"] > 0])
#                 dis = 0
#                 for i in range(total_len-1):
#                     for j in range(i+1, total_len):
#                         if int(f.iloc[j]["verdict"]) == 0:
#                             continue
#                         elif int(f.iloc[i]["verdict"]) == 0 and int(f.iloc[j]["verdict"]) > 0:
#                             dis += 1
#                         elif int(f.iloc[i]["verdict"]) > 0 and int(f.iloc[j]["verdict"]) > 0 and float(f.iloc[i]["last_exec_time"]) > float(f.iloc[j]["last_exec_time"]):
#                             dis += 1 / (f_len * (f_len - 1) / 2)
#                         else:
#                             continue
#                 dis = dis/((total_len-f_len)*f_len + 1)
#                 ddp_list.append(float(dis))
#         elif file.split('_')[0] == "rl":
#             df = pd.read_csv(file)
#             cycle_ids = dup_remover(df["cycle_id"])
#             cycle_id_list = cycle_ids[-counter:]
#             for cycle_id in cycle_id_list:
#                 f = df.loc[df["cycle_id"]==cycle_id]
#                 f['failures'] = f['failures'].astype(float)
#                 # calculate number of test cases and number of failures, initialize distance
#                 total_len = len(f)
#                 f_len = len(f.loc[f["failures"] > 0])
#                 dis = 0
#                 for i in range(total_len-1):
#                     for j in range(i+1, total_len):
#                         if int(f.iloc[j]["failures"]) == 0:
#                             continue
#                         elif int(f.iloc[i]["failures"]) == 0 and int(f.iloc[j]["failures"]) > 0:
#                             dis += 1
#                         elif int(f.iloc[i]["failures"]) > 0 and int(f.iloc[j]["failures"]) > 0 and float(f.iloc[i]["time"]) > float(f.iloc[j]["time"]):
#                             dis += 1 / (f_len * (f_len - 1) / 2)
#                         else:
#                             continue
#                 dis = dis/((total_len-f_len)*f_len + 1)
#                 ddp_list.append(float(dis))
#         # elif file.split('_')[0] == "deeporder":
#         #     # fail_test_df = test_df.loc[test_df['DDP'] >= 0.0]
#         #     # print("111111")
#         #     df = pd.read_csv(file, sep=';')
#         #     fail_df = df.loc[df['DDP'] >= 0.0]
#         #     ddp_list = fail_df['DDP'].values
#         #
#         # elif file.split('_')[0] == "coleman":
#         #     df = pd.read_csv(file, sep=';')
#         #     fail_df = df.loc[df['ddp'] >= 0.0]
#         #     ddp_list = fail_df['ddp'].values
#
#         # print(fft_list)
#         ddp_dict[file.split('_')[0]] = ddp_list
#
#     y1 = ddp_dict['rl'][-counter:]
#     # y2 = ddp_dict['rl-mlp'][-counter:]
#     y4 = ddp_dict['pairwise'][-counter:]
#     y10 = ddp_dict['listwise'][-counter:]
#     y11 = ddp_dict['pointwise'][-counter:]
#     # y12 = ddp_dict['deeporder'][-counter:]
#     # y13 = ddp_dict['coleman'][-counter:]
#
#
#     # collect FRP for each project
#     y1_list = np.hstack((y1_list, y1))
#     y4_list = np.hstack((y4_list, y4))
#     y10_list = np.hstack((y10_list, y10))
#     y11_list = np.hstack((y11_list, y11))
#     # y12_list = np.hstack((y12_list, y12))
#     # y13_list = np.hstack((y13_list, y13))

with open("max_apfd.json", "r") as f:
    max_apfd_dict = json.load(f)

# collect freeze result
for filename in filename_list:
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

    apfd_dict_freeze = {}
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
        # elif file.split('_')[0] == "deeporder":
        #     # fail_test_df = test_df.loc[test_df['DDP'] >= 0.0]
        #     # print("111111")
        #     df = pd.read_csv(file, sep=';')
        #     fail_df = df.loc[df['DDP'] >= 0.0]
        #     ddp_list = fail_df['DDP'].values
        #
        # elif file.split('_')[0] == "coleman":
        #     df = pd.read_csv(file, sep=';')
        #     fail_df = df.loc[df['ddp'] >= 0.0]
        #     ddp_list = fail_df['ddp'].values

        # print(fft_list)
        apfd_dict_freeze[file.split('_')[0]] = apfd_list


    y1 = [(a-(1-b))/(b-(1-b)) for a,b in zip(apfd_dict_freeze['rl'][-counter:], max_apfd_list[-counter:])]
    y4 = [(a-(1-b))/(b-(1-b)) for a,b in zip(apfd_dict_freeze['pairwise'][-counter:], max_apfd_list[-counter:])]
    y10 = [(a-(1-b))/(b-(1-b)) for a,b in zip(apfd_dict_freeze['listwise'][-counter:], max_apfd_list[-counter:])]
    y11 = [(a-(1-b))/(b-(1-b)) for a,b in zip(apfd_dict_freeze['pointwise'][-counter:], max_apfd_list[-counter:])]

    # y12 = ddp_dict_freeze['deeporder'][-counter:]
    # y13 = ddp_dict_freeze['coleman'][-counter:]

    # y1 = ddp_dict_freeze['rl']
    # y4 = ddp_dict_freeze['pairwise']
    # y10 = ddp_dict_freeze['listwise']
    # y11 = ddp_dict_freeze['pointwise']

    y1_list_earlier = np.hstack((y1_list_earlier, y1[:30]))
    y4_list_earlier = np.hstack((y4_list_earlier, y4[:30]))
    y10_list_earlier = np.hstack((y10_list_earlier, y10[:30]))
    y11_list_earlier = np.hstack((y11_list_earlier, y11[:30]))

    # collect FRP for each project
    y1_list_later = np.hstack((y1_list_later, y1[-30:]))
    y4_list_later = np.hstack((y4_list_later, y4[-30:]))
    y10_list_later = np.hstack((y10_list_later, y10[-30:]))
    y11_list_later = np.hstack((y11_list_later, y11[-30:]))
    # y12_list = np.hstack((y12_list, y12))
    # y13_list = np.hstack((y13_list, y13))

# record_dict = {'rl_earlier':y1_list_earlier,'rl_later':y1_list_later,'ppo2-po_earlier':y11_list_earlier,'ppo2-po_later':y11_list_later,
#                'acer-pa_earlier':y4_list_earlier,'acer-pa_later':y4_list_later,'ppo1-li_earlier':y10_list_earlier,'ppo1-li_later':y10_list_later}
# record_df = pd.DataFrame(record_dict)
# record_df.to_csv('freeze_record.csv', header=True, index=False)



labels_1 = ['RL', 'PPO2-PO', 'ACER-PA', 'PPO1-LI']
plt.rcParams['boxplot.flierprops.markersize'] = 2
plt.rcParams['figure.figsize'] = (6, 3)

medianprops = {'linestyle':'-','color':'black'} # 设置中位数线的属性，线的类型和颜色
# plt.vlines(6.5, 0, 1, colors="g", linestyles="dashed")
plt.xticks(rotation=10, fontsize=9)
colors = [(202/255.,96/255.,17/255.), (255/255.,217/255.,102/255.),(202/255.,96/255.,17/255.), (255/255.,217/255.,102/255.),(202/255.,96/255.,17/255.), (255/255.,217/255.,102/255.)]

bplot1 = plt.boxplot([y1_list_earlier,y1_list_later],patch_artist=True, labels=["earlier", "later"],positions=(1,1.4),widths=0.3,medianprops=medianprops)
for patch, color in zip(bplot1['boxes'], colors):
    patch.set_facecolor(color)

bplot2 = plt.boxplot([y11_list_earlier,y11_list_later],patch_artist=True,labels=["earlier", "later"],positions=(2,2.4),widths=0.3,medianprops=medianprops)
for patch, color in zip(bplot2['boxes'], colors):
    patch.set_facecolor(color)

bplot3 = plt.boxplot([y4_list_earlier,y4_list_later],patch_artist=True,labels=["earlier", "later"],positions=(3,3.4),widths=0.3,medianprops=medianprops)
for patch, color in zip(bplot3['boxes'], colors):
    patch.set_facecolor(color)

bplot4 = plt.boxplot([y10_list_earlier,y10_list_later],patch_artist=True,labels=["earlier", "later"],positions=(4,4.4),widths=0.3,medianprops=medianprops)
for patch, color in zip(bplot4['boxes'], colors):
    patch.set_facecolor(color)

# bplot1 = plt.boxplot([y1_list_earlier[:30],y1_list_later[:30],y1_list_earlier[30:60],y1_list_later[30:60],y1_list_earlier[60:],y1_list_later[60:]],patch_artist=True, labels=["earlier", "later"],positions=(1,1.4),widths=0.3,medianprops=medianprops)
# for patch, color in zip(bplot1['boxes'], colors):
#     patch.set_facecolor(color)
#
# bplot2 = plt.boxplot([y11_list_earlier[:30],y11_list_later[:30],y11_list_earlier[30:60],y11_list_later[30:60],y11_list_earlier[60:],y11_list_later[60:]],patch_artist=True,labels=["earlier", "later"],positions=(2,2.4),widths=0.3,medianprops=medianprops)
# for patch, color in zip(bplot2['boxes'], colors):
#     patch.set_facecolor(color)
#
# bplot3 = plt.boxplot([y4_list_earlier[:30],y4_list_later[:30],y4_list_earlier[30:60],y4_list_later[30:60],y4_list_earlier[60:],y4_list_later[60:]],patch_artist=True,labels=["earlier", "later"],positions=(3,3.4),widths=0.3,medianprops=medianprops)
# for patch, color in zip(bplot3['boxes'], colors):
#     patch.set_facecolor(color)
#
# bplot4 = plt.boxplot([y10_list_earlier[:30],y10_list_later[:30],y10_list_earlier[30:60],y10_list_later[30:60],y10_list_earlier[60:],y10_list_later[60:]],patch_artist=True,labels=["earlier", "later"],positions=(4,4.4),widths=0.3,medianprops=medianprops)
# for patch, color in zip(bplot4['boxes'], colors):
#     patch.set_facecolor(color)
# plt.boxplot([[y1_list,y1_list_freeze], [y11_list,y11_list_freeze], [y4_list,y4_list_freeze], [y10_list,y10_list_freeze]], labels=labels_1)
x_position = [1, 2, 3, 4]
x_position_fmt = ['RL', 'PPO2-PO', 'ACER-PA', 'PPO1-LI']
plt.xticks([i + 0.4 / 2 for i in x_position], x_position_fmt)

plt.ylim([-0.1, 1.1])
plt.ylabel("rAPFD")
plt.legend(bplot1['boxes'], ["earlier cycles", "later cycles"], loc=8, bbox_to_anchor=(0.5, -0.25), borderaxespad=0, fontsize=8, ncol=2)  #绘制表示框，右下角绘制
plt.savefig("../figure/RQ1.2/plot_freeze_new_apfd.pdf", bbox_inches='tight')
plt.show()

# print(np.mean(y5_list))
# print(np.mean(y6_list))
# print(np.mean(y7_list))
# print(np.mean(y8_list))
# print(np.mean(y9_list))
# print(np.mean(y1_list))
# print(np.mean(y2_list))
# print(np.mean(y4_list))

# plt.vlines(6.5, 0, 1, colors="g", linestyles="dashed")
# plt.xticks(rotation=20, fontsize=9)
# plt.boxplot([y1_list_freeze,], labels=labels_1)



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
