import pandas as pd
import sys
import os
import numpy as np

#FAILURE PERCENTILE ACCURACY (FPA) GENERATOR
def FPA_generator(evaluation):
    fpa = 0.0
    for m in range(1, len(evaluation)+1):
        ranking_sum = 0.0
        for i in range(0, m):
            ranking_sum = ranking_sum + evaluation.iloc[i]['ranking']
            if i == m - 1:
                ranking_sum = ranking_sum / evaluation['ranking'].sum()
        #print(ranking_sum)
        fpa = fpa + ranking_sum
    return(fpa / len(evaluation))
    

if __name__ == '__main__':
    args = sys.argv[1]
    rank_arg = sys.argv[2]

    data = pd.read_csv(args, header = 0)
    ranking = pd.read_csv(rank_arg, sep="\t", header=None)
    ranking.columns = ['a', 'b', 'rank_index']

    ranking.drop(columns=['a','b'])

    #dropping the training set
    print(len(data)-len(ranking))
    n = len(data)-len(ranking)
    data.drop(data.index[:n], inplace=True)
    data=data.reset_index(drop=True)

    #appending rank indexes
    data.insert(len(data.columns),'rank_index', ranking['rank_index'], allow_duplicates = True)

    commit_id_list = list(data['cycle_id'])
    commit_id_list = list(dict.fromkeys(commit_id_list))
    ddp_list = []
    output_data = pd.DataFrame()
    for commit_id in commit_id_list:
         #print(commit_id)
         data_subset = data.loc[data['cycle_id'] == commit_id]

         evaluation = pd.DataFrame()

         rank_index_array = []
         time_array = []
         class_array = []
         failures_array = []
         for j in range(0, len(data_subset)):
             rank_index_array.append(data_subset.iloc[j]['rank_index'])
             time_array.append(data_subset.iloc[j]['time'])
             class_array.append(data_subset.iloc[j]['A_priority_with_time'])
             failures_array.append(data_subset.iloc[j]['current_failures'])
        
         evaluation.insert(len(evaluation.columns), 'rank_index', rank_index_array, allow_duplicates = True)
         evaluation.insert(len(evaluation.columns), 'time', time_array, allow_duplicates = True)
         evaluation.insert(len(evaluation.columns), 'class', class_array, allow_duplicates = True)
         evaluation.insert(len(evaluation.columns), 'failures', failures_array, allow_duplicates = True)
         #inserisco la colonna RANKING
         evaluation = evaluation.sort_values(by = ['class', 'time'], ascending = [False, True])
         rank = [i for i in range(len(evaluation), 0, -1)]
         evaluation.insert(len(evaluation.columns),'ranking', rank, allow_duplicates = True)

         #OPTIMAL FAILURE PERCENTILE ACCURACY (FPA) BEFORE RANKING
         #print('OPTIMAL_RPA')
         optimal_fpa = FPA_generator(evaluation)
         #print(optimal_fpa)
         #Calcolo tempo di esecuzione prima dell'ordinamento
         optimal_exec_time_25 = evaluation['time'].head(max(int(len(data_subset)/4), 1)).sum()
         optimal_exec_time_50 = evaluation['time'].head(max(int((len(data_subset)/4)*2), 1)).sum()
         optimal_exec_time_75 = evaluation['time'].head(max(int((len(data_subset)/4)*3), 1)).sum()
         optimal_failures_25 = evaluation['failures'].head(max(int(len(data_subset)/4), 1)).sum()
         optimal_failures_50 = evaluation['failures'].head(max(int((len(data_subset)/4)*2), 1)).sum()
         optimal_failures_75 = evaluation['failures'].head(max(int((len(data_subset)/4)*3), 1)).sum()
            
         #ordino su priority_p e priority
         evaluation = evaluation.sort_values(by = ['rank_index'], ascending = [False])
         evaluation.reset_index(drop=True, inplace=True)
            
         #ESTIMATED FAILURE PERCENTILE ACCURACY (FPA) AFTER RANKING 
         #print('ESTIMATED_RPA')   
         estimated_fpa = FPA_generator(evaluation)
         evaluation.insert(len(evaluation.columns), 'nfpa', [estimated_fpa / optimal_fpa] * len(evaluation),
                           allow_duplicates=True)

         if len(evaluation[(evaluation['failures'] > 0)]) == 0:
            evaluation.insert(len(evaluation.columns), 'DDP', [-1] * len(evaluation),
                               allow_duplicates=True)
            dis = -1
         else:
             # calculate DDP
            f = evaluation
            # calculate number of test cases and number of failures, initialize distance
            total_len = len(f)
            f_len = len(f.loc[f["failures"] > 0])
            dis = 0
            for i in range(total_len - 1):
                for j in range(i + 1, total_len):
                    if f.iloc[j]["failures"] == 0:
                        continue
                    elif f.iloc[i]["failures"] == 0 and f.iloc[j]["failures"] > 0:
                        dis += 1
                    elif f.iloc[i]["failures"] > 0 and f.iloc[j]["failures"] > 0 and float(
                            f.iloc[i]["time"]) > float(f.iloc[j]["time"]):
                        dis += 1 / (f_len * (f_len - 1) / 2)
                    else:
                        continue

            dis = dis / ((total_len - f_len) * f_len + 1)
            evaluation.insert(len(evaluation.columns), 'DDP', [dis] * len(evaluation),
                            allow_duplicates=True)
            evaluation.to_csv('ranker'+sys.argv[3]+'_failure_detail.csv',
                               header=True, mode='a',
                               index=False)  ################

         evaluation.to_csv('ranker'+sys.argv[3]+'_whole_detail.csv',
                           header=True, mode='a',
                           index=False)  ################
         print(estimated_fpa)
         #print(estimated_fpa)

         #metriche per ciclo
         output_data_temp = pd.DataFrame({"cycle_id":[commit_id], "num_testsuite":[len(data_subset)], "NORMALIZED_RPA":[estimated_fpa / optimal_fpa], "total_failures_in_cycle":[evaluation['failures'].sum()], "exec_time":[evaluation['time'].sum()], "optimal_failures_25%":[optimal_failures_25], "failures_in_25%_ordered":[evaluation['failures'].head(max(int(len(data_subset)/4), 1)).sum()], "optimal_exec_time_25%":[optimal_exec_time_25], "exec_time_25%":[evaluation['time'].head(max(int(len(data_subset)/4), 1)).sum()], "optimal_failures_50%":[optimal_failures_50], "failures_in_50%_ordered":[evaluation['failures'].head(max(int((len(data_subset)/4)*2), 1)).sum()], "optimal_exec_time_50%":[optimal_exec_time_50],"exec_time_50%":[evaluation['time'].head(max(int((len(data_subset)/4)*2), 1)).sum()], "optimal_failures_75%":[optimal_failures_75], "failures_in_75%_ordered":[evaluation['failures'].head(max(int((len(data_subset)/4)*3), 1)).sum()], "optimal_exec_time_75%":[optimal_exec_time_75], "exec_time_75%":[evaluation['time'].head(max(int((len(data_subset)/4)*3), 1)).sum()], "ddp":[dis]})
         output_data = output_data.append(output_data_temp)

    # fm = np.mean(failure_metric_list)
    # output_data.insert(len(output_data.columns), 'failure_metric',[fm] * len(output_data))
    if not os.path.isfile('_summary_ranker'+sys.argv[3]+'.csv'):
        output_data.to_csv('_summary_ranker'+sys.argv[3]+'.csv', index = False, header = True)
    else: # else it exists so append without writing the header
        output_data.to_csv('_summary_ranker'+sys.argv[3]+'.csv',index = False, mode = 'a', header = False)