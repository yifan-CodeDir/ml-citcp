import os
import pandas as pd
import numpy as np

folders = ['commons-bcel', 'commons-csv', 'commons-dbcp', 'commons-text', 'java-faker', 'jedis', 'jsoup', 'jsprit', 'maxwell', 'nfe', 'spring-data-redis']  
# folders = ['commons-bcel']  

for folder in folders:
    # for each project get the result
    print(folder)

    files = ['_summary_ranker0.csv', '_summary_ranker1.csv', '_summary_ranker2.csv', '_summary_ranker4.csv','_summary_ranker6.csv']
    for file in files:
        # print(file)

        file_path = "./" + folder + "/2000/" + file
        data = pd.read_csv(file_path)
        failure_data = data.loc[data['ddp'] != -1]
        print(np.mean(failure_data['ddp']))
    print("Test start cycle for finetune:" + str(data.iloc[0]['cycle_id']))
    for i in range(len(data)):
        if data.iloc[i]['total_failures_in_cycle'] > 0:
            print("Test start failing cycle for finetune:" + str(data.iloc[i]['cycle_id']))
            break
