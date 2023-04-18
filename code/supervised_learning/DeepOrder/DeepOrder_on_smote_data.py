#!/usr/bin/env python
# coding: utf-8

# Importing all neccessary libraries
from netrc import NetrcParseError
import pandas as pd
import numpy as np
from statistics import mean, stdev
from matplotlib import pyplot as plt
import seaborn as sns
import os
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

import sklearn
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split as tts
from datetime import datetime
import tensorflow.keras.backend as K

import warnings


def mish(inputs):
    return inputs * tf.nn.tanh(tf.nn.softplus(inputs))


def root_mean_squared_error(y_true, y_pred):
    return K.sqrt(K.mean(K.square(y_pred - y_true))) 
 

def split_dataset(X, Y, spilt):
    X_train = X[:spilt]
    X_test = X[spilt:]
    y_train = Y[:spilt]
    y_test = Y[spilt:]

    # Scaling both training and testing input data.
    data_scaler = MinMaxScaler()
    X_train = data_scaler.fit_transform(X_train)
    X_test = data_scaler.transform(X_test)
    
    return X_train, X_test, y_train, y_test

def soft_acc(y_true, y_pred):
    return K.mean(K.equal(K.round(y_true), K.round(y_pred)))


# ### Defining function to plot correlation between loss and epochs

# def loss_function(information):
    
#     history_dict=information.history
#     loss_values = history_dict['loss']
#     val_loss_values=history_dict['val_loss']
#     plt.plot(loss_values,'b--',label='training loss') # Training data loss
#     plt.plot(val_loss_values,'r',label='training loss val') # Validation data loss
#     plt.xlabel('Epochs',fontsize=22)
#     plt.ylabel('Loss',fontsize=22)
#     plt.title('Loss Curve',fontsize=22)
#     save_figures(plt, 'loss_function_paintcontrol')
#     plt.close()

# # ###  Defining function to plot the comparision between 'Actual' and 'Predicted' value.

# def actual_vs_prediction(y_test, y_test_pred):

#     outcome = pd.DataFrame({'Actual': y_test,'Predicted': y_test_pred.flatten()})
#     df_sorted = outcome.head(40).sort_values(by="Actual")

#     df_sorted.plot(kind='bar', figsize=(12,7))
#     plt.grid(which='major', linestyle='-', linewidth = '0.5', color='green')
#     plt.grid(which='minor', linestyle=':', linewidth = '0.5', color='black')
#     plt.xlabel('Test Cases',fontsize=22)
#     plt.ylabel('Priority Values',fontsize=22)
#     plt.title("Comparision between 'Actual' and 'Predicted' values",fontsize=22)
#     save_figures(plt, 'actual_vs_prediction_paintcontrol')
#     plt.close()

#     plt.plot(df_sorted['Actual'].tolist(), label='Actual')
#     plt.plot(df_sorted['Predicted'].tolist(), label='prediction')
#     plt.xlabel('Test cases',fontsize=22)
#     plt.ylabel('Priority Values',fontsize=22)
#     plt.title("Comparision between 'Actual' and 'Predicted' values",fontsize=22)
#     plt.grid(which='major', linestyle='-', linewidth = '0.5', color='green')
#     plt.grid(which='minor', linestyle=':', linewidth = '0.5', color='black')
#     plt.legend()
#     save_figures(plt, 'actual_vs_prediction_2_paintcontrol')
#     plt.close()

# ###  Defining function to test the model

def prediction_function(X_train, X_test):

    # y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    return y_test_pred

def FPA_generator(evaluation):
    fpa = 0.0
    for m in range(1, len(evaluation) + 1):
        ranking_sum = 0.0
        for i in range(0, m):
            ranking_sum = ranking_sum + evaluation.iloc[i]['ranking']
            if i == m - 1:
                ranking_sum = ranking_sum / evaluation['ranking'].sum()
        # print(ranking_sum)
        fpa = fpa + ranking_sum
    return (fpa / len(evaluation))

# def save_figures(fig, filename):

#     FIGURE_DIR = os.path.abspath(os.getcwd())
#     fig.savefig(os.path.join(FIGURE_DIR+'/Paintcontrol', filename + '.pdf'), bbox_inches='tight')


# ###  Defining function to plot the regression line for the model

# def regression_line(y_test, y_test_pred):
    
#     fig, ax = plt.subplots()
#     ax.scatter(y_test, y_test_pred)
#     ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
#     ax.set_xlabel('Calculated by DeepOrder algorithm',fontsize=22)
#     ax.set_ylabel('Predicted by Neural Network',fontsize=22)
#     plt.title("Neural Network Regression Line",fontsize=22)
#     plt.grid(which='major', linestyle='-', linewidth = '0.5', color='green')
#     plt.grid(which='minor', linestyle=':', linewidth = '0.5', color='black')
#     save_figures(plt, 'regression_line_paintcontrol')
#     plt.close()


if __name__ == '__main__':
    # start 
    warnings.simplefilter(action='ignore')
    config = tf.compat.v1.ConfigProto()
    config.gpu_options.allow_growth = True
    session = tf.compat.v1.Session(config=config)

    # hardcode the number of training sample
    projects = ['commons-bcel', 'commons-csv', 'commons-dbcp', 'commons-text', 'java-faker', 'jedis', 'jsoup', 'jsprit', 'maxwell', 'nfe', 'spring-data-redis']  
    # projects = ['commons-bcel']  
    training_sample_list = [3888, 4016, 3982, 4002, 5994, 6008, 3982, 3748, 4024, 3328, 3942]


    for project in projects:

        startTime = datetime.now()

        # Reading the dataset
        df = pd.read_csv('Datasets/smote/proc_' + project + '_result.csv') ##############
        df.head()
        # values = pd.DataFrame()
        # values['Id'] =  range(0, 1)
        # values['env'] = 'bcel'  ################

        X = df[['DurationFeature', 'E1','E2','E3', 'LastRunFeature','DIST','CHANGE_IN_STATUS']] # Defining feature variable
        Y = df['PRIORITY_VALUE'] # Defining label variable
        MSE_list=[] # mean square error list
        R2_list=[] 

        # ### Deep Neural Network 
        spilt = training_sample_list[projects.index(project)]
        X_train, X_test, y_train, y_test = split_dataset(X, Y, spilt)

        
        model = Sequential()
        model.add(Dense(10, input_shape=(7,), activation=mish))
        model.add(Dense(20, activation=mish))
        model.add(Dense(15, activation=mish))
        model.add(Dense(1,))
        model.compile(Adam(lr=0.001), loss='mean_squared_error', metrics=[soft_acc])    

        # train the model
        trainStartTime = datetime.now()
        information = model.fit(X_train, y_train, validation_data= (X_test, y_test), epochs = 2,
                                shuffle = True, verbose = 1)
        trainEndTime = datetime.now()
        trainingTime = trainEndTime - trainStartTime

        y_test_pred = prediction_function(X_train, X_test)    

        MSE_list.append(mean_squared_error(y_test, y_test_pred))
        R2_list.append(r2_score(y_test, y_test_pred))


        outcome = pd.DataFrame({'Actual': y_test, 'Predicted': y_test_pred.flatten()})
        outcome.head(10)

        '''
        # serialize model to JSON
        model_json = model.to_json()
        with open("paintcontrol_model.json", "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        model.save_weights("paintcontrol_model.h5")
        print("Saved model to disk")
        
        # load json and create model
        json_file = open('paintcontrol_model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights("paintcontrol_model.h5")
        print("Loaded model from disk")
        '''

        #---------------------#
        # values['MSE_list'] = mean(MSE_list)
        print('Average Mean Squared Error: %.6f'% mean(MSE_list))
        if (len(MSE_list) >1):
            
            print('Standard Deviation of MSE: %.6f'% stdev(MSE_list))

        # values['R2_list'] = mean(R2_list)

        print('Average R2 Score: %.6f'% mean(R2_list))
        if (len(R2_list) >1):

            print('Standard Deviation of R2 Score: %.6f'% stdev(R2_list))
        preparation_time = datetime.now() - startTime


        # loss_function(information) # displaying performance based on loss

        # actual_vs_prediction(y_test, y_test_pred)

        # regression_line(y_test, y_test_pred)
        # # m is number of fault in dataset
        # _,m=df['Verdict'].value_counts()
        # n=df.shape[0]

        # values['Number of Failed Tests'] = m
        # values['Total Test Cases'] = n
        # start_prio_time = datetime.now()

        # XX = data_scaler.fit_transform(df[['DurationFeature', 'E1','E2','E3', 'LastRunFeature','DIST','CHANGE_IN_STATUS']])
        # A = model.predict(XX)
        # df['CalcPrio'] = A
        # final_df = df.sort_values(by=['CalcPrio'], ascending=False)
        # final_df['ranking'] = range(1, 1+len(df))
        # available_time = sum(final_df['Duration'])
        # prioritization_time = datetime.now() - start_prio_time


        # scheduled_time = 0
        # detection_ranks = []
        # undetected_failures = 0
        # rank_counter = 1

        # for index, row in final_df.iterrows():
        #     if scheduled_time + row['Duration'] <= available_time:
        #         if row['Verdict'] == 1:
        #             #print (rank_counter)

        #             detection_ranks.append(rank_counter)
        #         scheduled_time += row['Duration']
        #         rank_counter += 1
        #     else:
        #         undetected_failures += row['Id']

        # detected_failures = len(detection_ranks)


        # p = 0
        # if undetected_failures > 0:
        #     p = (detected_failures / m)
        # else:
        #     p = 1
        # print ("recall: ",p)        


        # if p==1:
        #     apfd = p - sum(detection_ranks) / (m * n) + p / (2 * n)
        #     print ("apfd: ",apfd)
        #     print ("napfd equals apfd")
        # else:
        #     napfd = p - sum(detection_ranks) / (m * n) + p / (2 * n)
        #     print ("napfd: ",napfd)
        # values['APFD'] = apfd

        # ## Calculating NAPFD per cycle
        data_scaler = MinMaxScaler()
        missing = []
        Last_cycle = df['Cycle'].iloc[-1]
        print (Last_cycle, " will be last cycle")

        cycle_num = 1
        NAPFD = []
        NRPA = []
        DDP = []
        prev_cycle = 0
        predict_time_list = []

        # prioritize for each cycle
        for index in range (1, Last_cycle+1):
            
            if (cycle_num <= Last_cycle and cycle_num in df['Cycle']):
                # print ("Cycle :",cycle_num)
                df_temp = df.loc[df['Cycle'] == cycle_num]
                cycle_num = cycle_num + 1
                if (df_temp.empty):
                    missing.append(i-1) 
                    continue
                
                predictStartTime = datetime.now()
                XX = data_scaler.fit_transform(df_temp[['DurationFeature', 'E1','E2','E3', 'LastRunFeature','DIST','CHANGE_IN_STATUS']])
                A = model.predict(XX)
                predictEndTime = datetime.now()
                # record prediction time
                predict_time_list.append((predictEndTime - predictStartTime).microseconds)
                
                df_temp['CalcPrio'] = A
                
                # get the optimal prioritization result, to calculate NRPA
                df_temp = df_temp.sort_values(by=['Verdict', 'Duration'], ascending=[False, True])
                rank = [i for i in range(len(df_temp), 0, -1)]
                df_temp.insert(len(df_temp.columns), 'ranking', rank, allow_duplicates=True)
                optimal_fpa = FPA_generator(df_temp)

                ##### get the final prioritization result
                final_df_temp = df_temp.sort_values(by=['CalcPrio'], ascending=False)
                final_df_temp.reset_index(drop=True, inplace=True)

                available_time = sum(final_df_temp['Duration'])
                
                counts = final_df_temp['Verdict'].value_counts().to_dict()
                # number of failing test 
                if 1 in counts:
                    m=counts[1]
                    #print ("count 1: ",counts[1])
                else:
                    m=0
                    #print ("count 0: ",0)

                # record the prioritized data
                final_df_temp.to_csv('./result/smote/' + project + '_detail.csv',
                                    header=True, mode='a',
                                    index=False)  ################


                #----------- calculate metric-------------------

                n=final_df_temp.shape[0]  
                scheduled_time = 0
                detection_ranks = []
                undetected_failures = 0
                rank_counter = 1
                
                # calculate NAPFD
                for index, row in final_df_temp.iterrows():
                    if scheduled_time + row['Duration'] <= available_time:    
                        if row['Verdict'] == 1:
                            #print (rank_counter)

                            detection_ranks.append(rank_counter)
                        scheduled_time += row['Duration']
                        #scheduled_testcases.append(row[:])
                        rank_counter += 1
                    else:
                        undetected_failures = undetected_failures +1
                detected_failures = len(detection_ranks)
                #print ("Detected: ",detected_failures, " Total: ",m)

                # if there is no failing test, then NAPFD = 0
                if m > 0:
                    p = 0
                    if undetected_failures > 0:
                        p = (detected_failures / m)
                    else:
                        p = 1
                    #print ("recall: ",p)

                    # if execute all test cases, then NAPFD equals to APFD
                    if p==1:
                        apfd = p - sum(detection_ranks) / (m * n) + p / (2 * n)
                        #print ("apfd: ",apfd)
                        NAPFD.append(apfd)
                        #print ("napfd equals apfd")
                    else:
                        napfd = p - sum(detection_ranks) / (m * n) + p / (2 * n)
                        NAPFD.append(napfd)
                        #print ("napfd: ",napfd)
                else:
                    NAPFD.append(0)
                
                # calculate NRPA
                estimated_fpa = FPA_generator(final_df_temp)
                NRPA.append(estimated_fpa / optimal_fpa)

                # calculate DDP
                f = final_df_temp
                # calculate number of test cases and number of failures, initialize distance
                total_len = len(f)
                f['Verdict'] = f['Verdict'].apply(pd.to_numeric)
                f_len = len(f.loc[f["Verdict"] > 0])
                if f_len == 0:
                    dis = -1
                else:
                    dis = 0
                    for i in range(total_len - 1):
                        for j in range(i + 1, total_len):
                            if f.iloc[j]["Verdict"] == 0:
                                continue
                            elif f.iloc[i]["Verdict"] == 0 and f.iloc[j]["Verdict"] > 0:
                                dis += 1
                            elif f.iloc[i]["Verdict"] > 0 and f.iloc[j]["Verdict"] > 0 and float(
                                    f.iloc[i]["Duration"]) > float(f.iloc[j]["Duration"]):
                                dis += 1 / (f_len * (f_len - 1) / 2)
                            else:
                                continue

                    dis = dis / ((total_len - f_len) * f_len + 1)
                DDP.append(dis)
                #print ("-----------------------------------------------------------------------------------")


        Cycle = df['Cycle'].unique()
        
        # plt.plot(Cycle[1:], NAPFD, color='red', marker='o')
        # plt.title('NAPFD over cycles bcel', fontsize=14)
        # plt.xlabel('Cycles', fontsize=24)
        # plt.ylabel('NAPFD', fontsize=24)
        # plt.grid(True)
        # plt.gcf().set_size_inches(25, 10)
        # save_figures(plt, 'NAPFD_per_cycle_bcel')
        # plt.close()

        # values['Avg NAPFD per cycle'] = mean(NAPFD)

        # ## Saving results to output.csv for visualizations
        output = pd.DataFrame()
        output['step'] =  df['Cycle'][1:].unique()
        output['env'] = 'bcel'  #################
        output['model'] = 'DeepOrder'
        output['NAPFD/APFD'] = NAPFD
        output['NRPA'] = NRPA
        output['DDP'] = DDP
        output['training_time(seconds)'] = trainingTime.seconds
        output['prediction_time(microseconds)'] = predict_time_list
        output.to_csv('./result/smote/'+ project +'.csv', mode='a', sep=";",header=True, index = False) ############


    # ## Calculating Time related metrics

    # # Plotting Prioritized test cases class distribution
    # sns.FacetGrid(final_df, hue="Verdict", height=6) \
    #    .map(sns.kdeplot, "ranking") 
    # plt.legend(title='Verdict', loc='upper right', labels=['Passed', 'Failed'])
    # save_figures(plt, 'Prioritized_test_cases_class_distribution_paintcontrol')
    # plt.close()
    # # Plotting Non-Prioritized test cases class distribution
    # sns.FacetGrid(df, hue="Verdict", height=6) \
    #    .map(sns.kdeplot, "Id") 
    # plt.legend(title='Verdict', loc='upper right', labels=['Passed', 'Failed'])
    # save_figures(plt, 'Non_Prioritized_test_cases_class_distribution_paintcontrol')
    # plt.close()

    # # For ['Verdict'] based binary visualization
    # plt.plot(df['Verdict'].tolist(), label='Actual')
    # plt.plot(final_df['Verdict'].tolist(), label='Prediction')
    # plt.xlabel('Test cases')
    # plt.ylabel('Time')
    # plt.title("Comparision between 'Actual' and 'Predicted' values")
    # plt.grid(which='major', linestyle='-', linewidth = '0.5', color='green')
    # plt.grid(which='minor', linestyle=':', linewidth = '0.5', color='black')
    # plt.legend(fontsize=16,loc = 'upper right')
    # plt.gcf().set_size_inches(20, 10)
    # save_figures(plt, 'binary_visualization_verdict_paintcontrol')
    # plt.close()

    # # For ['Duration'] based visualization
    # plt.plot(df['Duration'].tolist(), label='Actual')
    # plt.plot(final_df['Duration'].tolist(), label='Prediction')
    # plt.xlabel('Test cases', fontsize=22)
    # plt.ylabel('Time', fontsize=22)
    # plt.title("Comparision between 'Actual' and 'Predicted' values w.r.t Execution time", fontsize=22)
    # plt.grid(which='major', linestyle='-', linewidth = '0.5', color='green')
    # plt.grid(which='minor', linestyle=':', linewidth = '0.5', color='black')
    # plt.legend(fontsize=16)
    # plt.gcf().set_size_inches(20, 10)
    # save_figures(plt, 'Test_execution_time_overall_paintcontrol')
    # plt.close()

    # #For pririotized  
    # chunk1,chunk2,chunk3,chunk4,chunk5,chunk6,chunk7,chunk8,chunk9,chunk10 = np.array_split(final_df['Duration'],10)
    # mean_chunk=[mean(chunk1),mean(chunk2),mean(chunk3),mean(chunk4),mean(chunk5),mean(chunk6),mean(chunk7),mean(chunk8),mean(chunk9),mean(chunk10)]
    # add_chunk=[sum(chunk1),sum(chunk2),sum(chunk3),sum(chunk4),sum(chunk5),sum(chunk6),sum(chunk7),sum(chunk8),sum(chunk9),sum(chunk10)]

    # #For non-pririotized
    # chunk1_non,chunk2_non,chunk3_non,chunk4_non,chunk5_non,chunk6_non,chunk7_non,chunk8_non,chunk9_non,chunk10_non = np.array_split(df['Duration'],10)
    # mean_chunk_non=[mean(chunk1_non),mean(chunk2_non),mean(chunk3_non),mean(chunk4_non),mean(chunk5_non),mean(chunk6_non),mean(chunk7_non),mean(chunk8_non),mean(chunk9_non),mean(chunk10_non)]
    # add_chunk_non=[sum(chunk1_non),sum(chunk2_non),sum(chunk3_non),sum(chunk4_non),sum(chunk5_non),sum(chunk6_non),sum(chunk7_non),sum(chunk8_non),sum(chunk9_non),sum(chunk10_non)]

    # #For pririotized 
    # sum_chunk = []    
    # chunk1,chunk2,chunk3,chunk4,chunk5,chunk6,chunk7,chunk8,chunk9,chunk10 = np.array_split(final_df['Verdict'],10)

    # counts = chunk1.value_counts().to_dict()
    # if 1 in counts: 
    #     sum_chunk.append(counts[1])
    # else:
    #     sum_chunk.append(0)

    # counts = chunk2.value_counts().to_dict()
    # if 1 in counts: 
    #     sum_chunk.append(counts[1])
    # else:
    #     sum_chunk.append(0)

    # counts = chunk3.value_counts().to_dict()
    # if 1 in counts: 
    #     sum_chunk.append(counts[1])
    # else:
    #     sum_chunk.append(0)

    # counts = chunk4.value_counts().to_dict()
    # if 1 in counts: 
    #     sum_chunk.append(counts[1])
    # else:
    #     sum_chunk.append(0)

    # counts = chunk5.value_counts().to_dict()
    # if 1 in counts: 
    #     sum_chunk.append(counts[1])
    # else:
    #     sum_chunk.append(0)
        
    # counts = chunk6.value_counts().to_dict()
    # if 1 in counts: 
    #     sum_chunk.append(counts[1])
    # else:
    #     sum_chunk.append(0)

    # counts = chunk7.value_counts().to_dict()
    # if 1 in counts: 
    #     sum_chunk.append(counts[1])
    # else:
    #     sum_chunk.append(0)
        
    # counts = chunk8.value_counts().to_dict()
    # if 1 in counts: 
    #     sum_chunk.append(counts[1])
    # else:
    #     sum_chunk.append(0)
        
    # counts = chunk9.value_counts().to_dict()
    # if 1 in counts: 
    #     sum_chunk.append(counts[1])
    # else:
    #     sum_chunk.append(0)
        
    # counts = chunk10.value_counts().to_dict()
    # if 1 in counts: 
    #     sum_chunk.append(counts[1])
    # else:
    #     sum_chunk.append(0)    
        
    # print (sum_chunk)    

    # #For non-pririotized 
    # sum_chunk_non = []    
    # chunk1_non,chunk2_non,chunk3_non,chunk4_non,chunk5_non,chunk6_non,chunk7_non,chunk8_non,chunk9_non,chunk10_non = np.array_split(df['Verdict'],10)

    # counts = chunk1_non.value_counts().to_dict()
    # if 1 in counts: 
    #     sum_chunk_non.append(counts[1])
    # else:
    #     sum_chunk_non.append(0)

    # counts = chunk2_non.value_counts().to_dict()
    # if 1 in counts: 
    #     sum_chunk_non.append(counts[1])
    # else:
    #     sum_chunk_non.append(0)

    # counts = chunk3_non.value_counts().to_dict()
    # if 1 in counts: 
    #     sum_chunk_non.append(counts[1])
    # else:
    #     sum_chunk_non.append(0)

    # counts = chunk4_non.value_counts().to_dict()
    # if 1 in counts: 
    #     sum_chunk_non.append(counts[1])
    # else:
    #     sum_chunk_non.append(0)

    # counts = chunk5_non.value_counts().to_dict()
    # if 1 in counts: 
    #     sum_chunk_non.append(counts[1])
    # else:
    #     sum_chunk_non.append(0)
        
    # counts = chunk6_non.value_counts().to_dict()
    # if 1 in counts: 
    #     sum_chunk_non.append(counts[1])
    # else:
    #     sum_chunk_non.append(0)

    # counts = chunk7_non.value_counts().to_dict()
    # if 1 in counts: 
    #     sum_chunk_non.append(counts[1])
    # else:
    #     sum_chunk_non.append(0)
        
    # counts = chunk8_non.value_counts().to_dict()
    # if 1 in counts: 
    #     sum_chunk_non.append(counts[1])
    # else:
    #     sum_chunk_non.append(0)
        
    # counts = chunk9_non.value_counts().to_dict()
    # if 1 in counts: 
    #     sum_chunk_non.append(counts[1])
    # else:
    #     sum_chunk_non.append(0)
        
    # counts = chunk10_non.value_counts().to_dict()
    # if 1 in counts: 
    #     sum_chunk_non.append(counts[1])
    # else:
    #     sum_chunk_non.append(0)    
        
    # print (sum_chunk_non)    

    # # Visualizing frequency of fault detection cases per 10 intervals
    # length = np.array([0.1,0.2,0.3, 0.4,0.5, 0.6,0.7,0.8,0.9,1.0])
    # #Year =  range(0, length)
    # newList = [x / max(sum_chunk) for x in sum_chunk]
    # newList
    # newList2 = [x / max(sum_chunk_non) for x in sum_chunk_non]  
    # plt.plot(length, sum_chunk, color='green', marker='o', label='Prioritized')
    # plt.plot(length, sum_chunk_non, color='red', marker='o', label='Actual')

    # plt.title('Frequency of Failed test cases in paintcontrol', fontsize=14)
    # plt.xlabel('Fault test cases', fontsize=18)
    # plt.ylabel('Verdict Frequency', fontsize=18)
    # plt.grid(True)
    # plt.legend(fontsize=16)

    # plt.gcf().set_size_inches(15, 8)
    # save_figures(plt, 'frequency_of_fault_detection_per_interval_paintcontrol')
    # plt.close()


    # # Visualizing average time of all test cases per 10 intervals
    # length = np.array([0.1,0.2,0.3, 0.4,0.5, 0.6,0.7,0.8,0.9,1.0])
    # #Year =  range(0, length)
    # newList = [x / max(mean_chunk) for x in mean_chunk]
    # newList
    # newList2 = [x / max(mean_chunk_non) for x in mean_chunk_non]  
    # plt.plot(length, mean_chunk, color='green', marker='o',label='Prioritized')
    # plt.plot(length, mean_chunk_non, color='red', marker='o',label='Non-Prioritized')
    # plt.legend()
    # plt.title('time over test cases paintcontrol', fontsize=14)
    # plt.xlabel('test cases', fontsize=18)
    # plt.ylabel('time (average per interval))', fontsize=18)
    # plt.grid(True)
    # plt.legend(fontsize=16)
    # save_figures(plt, 'average_time_of_all_tests_per_interval_paintcontrol')
    # plt.close()


    # # Visualizing summed time of all test cases per 10 intervals
    # length = np.array([0.1,0.2,0.3, 0.4,0.5, 0.6,0.7,0.8,0.9,1.0])
    # #Year =  range(0, length)
    # newList = [x / max(add_chunk) for x in add_chunk]
    # newList
    # newList2 = [x / max(add_chunk_non) for x in add_chunk_non]  
    # plt.plot(length, add_chunk, color='green', marker='o', label='Prioritized')
    # plt.plot(length, add_chunk_non, color='red', marker='o',label='Non-Prioritized')

    # plt.title('time over test cases paintcontrol', fontsize=14)
    # plt.xlabel('test cases', fontsize=18)
    # plt.ylabel('time (sum per interval))', fontsize=18)
    # plt.grid(True)
    # plt.legend(fontsize=16)

    # plt.gcf().set_size_inches(15, 8)
    # save_figures(plt, 'total_time_of_all_tests_per_interval_paintcontrol')
    # plt.close()



    # ---------------------------------------------------------------------------- 


    # # For pririotized test cases
    # start = datetime.now() 

    # Rank = final_df.ranking[final_df['Verdict'] == 1].tolist()
    # rank_counter = 1
    # first_rank = False
    # for index, row in final_df.iterrows():
        
    #     if row['Verdict'] == 1 and first_rank == False:
    #         FT = datetime.now()-start
            
    #         print (rank_counter)
    #         first_rank = True
            
    #     if row['Verdict'] == 1 and  Rank[-1]  == rank_counter:
    #         LT = datetime.now()-start

    #         print (rank_counter)
    #     rank_counter += 1

    # AT = (FT+LT)/2

    # print("AT ",AT, " seconds", ":", "FT ",FT, " seconds",":", "LT ",LT, " seconds")

    # '''
    # FT_milliseconds = FT.microsecond
    # FT_seconds = FT.second
    # LT_milliseconds = LT.microsecond
    # LT_seconds = LT.second
    # AT_milliseconds   = (FT_milliseconds+LT_milliseconds)/2
    # AT_seconds = (FT_seconds+LT_seconds)/2
    # print("AT ",AT_milliseconds, " milliseconds", ":", "FT ",FT_milliseconds, " milliseconds",":", "LT ",LT_milliseconds, " milliseconds")
    # print("AT ",AT_seconds, " seconds", ":", "FT ",FT_seconds, " seconds",":", "LT ",LT_seconds, " seconds")
    # '''

    # # For non-pririotized test cases
    # start = datetime.now() 

    # Rank = df.Id[final_df['Verdict'] == 1].tolist()
    # rank_counter = 1
    # first_rank = False
    # for index, row in df.iterrows():
        
    #     if row['Verdict'] == 1 and first_rank == False:
    #         FT_non = datetime.now()-start
            
    #         print (rank_counter)
    #         first_rank = True
            
    #     if row['Verdict'] == 1 and  Rank[-1]  == rank_counter:
    #         LT_non = datetime.now()-start

    #         print (rank_counter)
    #     rank_counter += 1

    # AT_non = (FT_non+LT_non)/2

    # print("AT ",AT_non, " seconds", ":", "FT ",FT_non, " seconds",":", "LT ",LT_non, " seconds")


    # '''
    # FT_milliseconds_non = FT_non.microsecond
    # FT_seconds_non = FT_non.second
    # LT_milliseconds_non = LT_non.microsecond
    # LT_seconds_non = LT_non.second
    # AT_milliseconds_non   = (FT_milliseconds_non+LT_milliseconds_non)/2
    # AT_seconds_non = (FT_seconds_non+LT_seconds_non)/2
    # print("AT ",AT_milliseconds_non, " milliseconds", ":", "FT ",FT_milliseconds_non, " milliseconds",":", "LT ",LT_milliseconds_non, " milliseconds")
    # print("AT ",AT_seconds_non, " seconds", ":", "FT ",FT_seconds_non, " seconds",":", "LT ",LT_seconds_non, " seconds")
    # '''



    # time = pd.DataFrame()
    # time['Id'] =  range(0, 1)
    # time['env'] = 'Paintcontrol'
    # time['FT'] = FT
    # time['LT'] = LT
    # time['AT'] = AT
    # time['FT non-prio'] = FT_non
    # time['LT non-prio'] = LT_non
    # time['AT non-prio'] = AT_non
    # time.to_csv('./Paintcontrol/time.csv', sep=";",index = False)

    # time 

    # total_time = datetime.now() - startTime


    # print ("Preparation Time : ",preparation_time)
    # print ("Pririotization Time : ",prioritization_time)
    # print ("Total Algorithm Time : ",total_time)
    # values['Preparation Time'] = preparation_time
    # values['Pririotization Time'] = prioritization_time
    # values['Total Algorithm Time'] = total_time


    # values.to_csv('./result/test/values.csv', sep=";", index = False)



