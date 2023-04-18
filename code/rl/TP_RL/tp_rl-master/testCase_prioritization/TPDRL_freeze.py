import argparse
import pandas as pd
import numpy as np
import math
import os
from datetime import datetime
from statistics import mean


from TPAgentUtil import TPAgentUtil
from PairWiseEnv import CIPairWiseEnv
from TPPairWiseDQNAgent import TPPairWiseDQNAgent
from ci_cycle import CICycleLog
from Config import Config
from TestcaseExecutionDataLoader import TestCaseExecutionDataLoader
from CustomCallback import CustomCallback
from stable_baselines.bench import Monitor
from pathlib import Path
from CIListWiseEnvMultiAction import CIListWiseEnvMultiAction
from CIListWiseEnv import CIListWiseEnv
from PointWiseEnv import CIPointWiseEnv
import sys


def train(trial, model):
    pass


def test(model):
    pass


#### record the freeze_cycle
freeze_cycle_sample = [129, 205, 156, 165, 96, 77, 115, 42, 104, 53, 20]
files = ['commons-bcel_result.csv', 'commons-csv_result.csv', 'commons-dbcp_result.csv', 'commons-text_result.csv', 'java-faker_result.csv', 'jedis_result.csv', 'jsoup_result.csv', 'jsprit_result.csv', 'maxwell_result.csv', 'spring-data-redis_result.csv', 'nfe_result.csv']  
# freeze_cycle_sample = [3]
# files = ['commons-bcel_result.csv']
# , 'commons-csv_result.csv', 'commons-dbcp_result.csv', 'commons-text_result.csv', 'java-faker_result.csv', 'jedis_result.csv', 'jsoup_result.csv', 'jsprit_result.csv', 'maxwell_result.csv', 'spring-data-redis_result.csv', 'nfe_result.csv']  

freeze_cycle = 0

def millis_interval(start, end):
    """start and end are datetime instances"""
    diff = end - start
    millis = diff.days * 24 * 60 * 60 * 1000
    millis += diff.seconds * 1000
    millis += diff.microseconds / 1000
    return millis


# find the cycle with maximum number of test cases
def get_max_test_cases_count(cycle_logs:[]):
    max_test_cases_count = 0
    for cycle_log in cycle_logs:
        if cycle_log.get_test_cases_count() > max_test_cases_count:
            max_test_cases_count = cycle_log.get_test_cases_count()
    return max_test_cases_count


def experiment(mode, algo, test_case_data, start_cycle, end_cycle, episodes, model_path, dataset_name, conf,verbos=False):
    log_dir = os.path.dirname(conf.log_file)
#    -- fix end cycle issue
    # print(freeze_cycle)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    if start_cycle <= 0:
        start_cycle = 0

    if end_cycle >= len(test_case_data)-1:
        end_cycle = len(test_case_data)
    # check for max cycle and end_cycle and set end_cycle to max if it is larger than max
    log_file = open(conf.log_file, "a")
    log_file_test_cases = open(log_dir+"/sorted_test_case.csv", "a",newline="")
    log_file.write("timestamp,mode,algo,model_name,episodes,steps,cycle_id,training_time,testing_time,winsize,test_cases,failed_test_cases,apfd,nrpa,random_apfd,optimal_apfd" + os.linesep)
    first_round: bool = True
    if start_cycle > 0:
        first_round = False
        previous_model_path = model_path + "/" + mode + "_" + algo + dataset_name + "_" + str(
            0) + "_" + str(start_cycle-1)
    model_save_path = None
    apfds=[]
    nrpas=[]
    for i in range(start_cycle, end_cycle - 1):
        if (test_case_data[i].get_test_cases_count() < 6) or \
                ( (conf.dataset_type == "simple") and
                  (test_case_data[i].get_failed_test_cases_count() < 1)):
            continue
        if mode.upper() == 'PAIRWISE':
            N = test_case_data[i].get_test_cases_count()
            steps = int(episodes * (N * (math.log(N,2)+1)))
            env = CIPairWiseEnv(test_case_data[i], conf)
        elif mode.upper() == 'POINTWISE':
            N = test_case_data[i].get_test_cases_count()
            steps = int(episodes * (N * (math.log(N,2)+1)))
            env = CIPointWiseEnv(test_case_data[i], conf)
        elif mode.upper() == 'LISTWISE':
            conf.max_test_cases_count = get_max_test_cases_count(test_case_data)
            N = test_case_data[i].get_test_cases_count()
            steps = int(episodes * (N * (math.log(N,2)+1)))
            env = CIListWiseEnv(test_case_data[i], conf)
        elif mode.upper() == 'LISTWISE2':
            conf.max_test_cases_count = get_max_test_cases_count(test_case_data)
            N = test_case_data[i].get_test_cases_count()
            steps = int(episodes * (N * (math.log(N,2)+1)))
            env = CIListWiseEnvMultiAction(test_case_data[i], conf)
        print("Training agent with replaying of cycle " + str(i) + " with steps " + str(steps))

        # if model_save_path exists, then assign previous model path
        if model_save_path:
            previous_model_path = model_save_path
        # if reach freezing cycle, then load the same model every time
        if i < (freeze_cycle - 1):    
            model_save_path = model_path + "/" + mode + "_" + algo + dataset_name + "_" + str(
            start_cycle) + "_" + str(i)
        else:
            model_save_path = model_path + "/" + mode + "_" + algo + dataset_name + "_" + str(
            start_cycle) + "_" + str(freeze_cycle - 2)
        env = Monitor(env, model_save_path +"_monitor.csv")
        callback_class = CustomCallback(svae_path=model_save_path,
                                        check_freq=int(steps/episodes), log_dir=log_dir, verbose=verbos)

        if first_round: # if in the first round, create model
            tp_agent = TPAgentUtil.create_model(algo, env)
            training_start_time = datetime.now()
            tp_agent.learn(total_timesteps=steps, reset_num_timesteps=True, callback=callback_class)
            training_end_time = datetime.now()
            first_round = False
        elif i < (freeze_cycle - 1):
            tp_agent = TPAgentUtil.load_model(algo=algo, env=env, path=previous_model_path+".zip")
            training_start_time = datetime.now()
            tp_agent.learn(total_timesteps=steps, reset_num_timesteps=True, callback=callback_class)
            training_end_time = datetime.now()
        ### if reach freezing cycle, skip training
        else:
            training_start_time = datetime.now()
            training_end_time = datetime.now()
            tp_agent = TPAgentUtil.load_model(algo=algo, env=env, path=previous_model_path+".zip")
        print("Training agent with replaying of cycle " + str(i) + " is finished")

        j = i+1   # test trained agent on next cycles
        while (((test_case_data[j].get_test_cases_count() < 6)
               or ((conf.dataset_type == "simple") and (test_case_data[j].get_failed_test_cases_count() == 0) ))
               and (j < end_cycle)):
            # or test_case_data[j].get_failed_test_cases_count() == 0) \
            j = j+1
            if j > end_cycle-1:
                break
        if j > end_cycle - 1:
            break

        if mode.upper() == 'PAIRWISE':
            env_test = CIPairWiseEnv(test_case_data[j], conf)
        elif mode.upper() == 'POINTWISE':
            env_test = CIPointWiseEnv(test_case_data[j], conf)
        elif mode.upper() == 'LISTWISE':
            env_test = CIListWiseEnv(test_case_data[j], conf)
        elif mode.upper() == 'LISTWISE2':
            env_test = CIListWiseEnvMultiAction(test_case_data[j], conf)

        test_time_start = datetime.now()
        test_case_vector = TPAgentUtil.test_agent(env=env_test, algo=algo, model_path=model_save_path+".zip", mode=mode)
        # #############
        # print(test_case_vector)
        test_time_end = datetime.now()
        test_case_id_vector = []

        for test_case in test_case_vector:
            test_case_id_vector.append(str(test_case['test_id']))
            cycle_id_text = test_case['cycle_id']
        if test_case_data[j].get_failed_test_cases_count() != 0:
            apfd = test_case_data[j].calc_APFD_ordered_vector(test_case_vector)
            apfd_optimal = test_case_data[j].calc_optimal_APFD()
            apfd_random = test_case_data[j].calc_random_APFD()
            apfds.append(apfd)
            # calculate failure metric
            df = pd.DataFrame(test_case_vector)  #########################################
            failure_metric = 0
            for row in df[(df['verdict'] > 0)].itertuples():
                failure_metric += (row[0] + 1) / len(df)
            failure_metric /= len(df[(df['verdict'] > 0)])
            df.insert(len(df.columns), 'failure_metric', [failure_metric] * len(df),
                              allow_duplicates=True)
            df.to_csv(conf.output_path + mode + "_" + algo + "_" + \
                        conf.dataset_name + "_" + args.episodes + "_" + str(conf.win_size) + "_detail.csv",
                        header=True, mode='a', index=False)  ################
        else:
            apfd = 0
            apfd_optimal = 0
            apfd_random = 0
        nrpa = test_case_data[j].calc_NRPA_vector(test_case_vector)
        nrpas.append(nrpa)
        test_time = millis_interval(test_time_start,test_time_end)
        training_time = millis_interval(training_start_time,training_end_time)
        print("Testing agent  on cycle " + str(j) +
              " resulted in APFD: " + str(apfd) +
              " , NRPA: " + str(nrpa) +
              " , optimal APFD: " + str(apfd_optimal) +
              " , random APFD: " + str(apfd_random) +
              " , # failed test cases: " + str(test_case_data[j].get_failed_test_cases_count()) +
              " , # test cases: " + str(test_case_data[j].get_test_cases_count()), flush=True)
        log_file.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "," + mode + "," + algo + ","
                       + Path(model_save_path).stem + "," +
                       str(episodes) + "," + str(steps) + "," + str(cycle_id_text) + "," + str(training_time) +
                       "," + str(test_time) + "," + str(conf.win_size) + "," +
                       str(test_case_data[j].get_test_cases_count()) + "," +
                       str(test_case_data[j].get_failed_test_cases_count()) + "," + str(apfd) + "," +
                       str(nrpa) + "," + str(apfd_random) + "," + str(apfd_optimal) + os.linesep)
        log_file_test_cases.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "," + mode + "," + algo + ","
                       + Path(model_save_path).stem + "," +
                       str(episodes) + "," + str(steps) + "," + str(cycle_id_text) + "," + str(training_time) +
                       "," + str(test_time) + "," + str(conf.win_size) + "," +
                                  ('|'.join(test_case_id_vector)) + os.linesep)
        if (len(apfds)):
            print(f"average apfd so far is {mean(apfds)}")
        print(f"average nrpas so far is {mean(nrpas)}")

        log_file.flush()
        log_file_test_cases.flush()
    log_file.close()
    log_file_test_cases.close()

def reportDatasetInfo(test_case_data:list):
    cycle_cnt = 0
    failed_test_case_cnt = 0
    test_case_cnt = 0
    failed_cycle = 0
    for cycle in test_case_data:
        if cycle.get_test_cases_count() > 5:
            cycle_cnt = cycle_cnt+1
            test_case_cnt = test_case_cnt + cycle.get_test_cases_count()
            failed_test_case_cnt = failed_test_case_cnt+cycle.get_failed_test_cases_count()
            if cycle.get_failed_test_cases_count() > 0:
                failed_cycle = failed_cycle + 1
    print(f"# of cycle: {cycle_cnt}, # of test case: {test_case_cnt}, # of failed test case: {failed_test_case_cnt}, "
          f" failure rate:{failed_test_case_cnt/test_case_cnt}, # failed test cycle: {failed_cycle}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DNN debugger')
    old_limit = sys.getrecursionlimit()
    print("Recursion limit:" + str(old_limit))
    sys.setrecursionlimit(1000000)
    # parser.add_argument('--traningData',help='tranind data folder',required=False)
    parser.add_argument('-m', '--mode', help='[pairwise,pointwise,listwise] ', required=True)
    parser.add_argument('-a', '--algo', help='[a2c,dqn,..]', required=True)
    parser.add_argument('-d', '--dataset_type', help='simple, enriched', required=False, default="simple")
    parser.add_argument('-e', '--episodes', help='Training episodes ', required=True)
    parser.add_argument('-w', '--win_size', help='Windows size of the history', required=False)
    parser.add_argument('-t', '--train_data', help='Train set folder', required=True)
    parser.add_argument('-f', '--first_cycle', help='first cycle used for training', required=False)
    parser.add_argument('-c', '--cycle_count', help='Number of cycle used for training', required=False)
    parser.add_argument('-l', '--list_size', help='Maximum number of test case per cycle', required=False)
    parser.add_argument('-o', '--output_path', help='Output path of the agent model', required=False)


    # parser.add_argument('-f','--flags',help='Input csv file containing testing result',required=False)
    supported_formalization = ['PAIRWISE', 'POINTWISE', 'LISTWISE','LISTWISE2']
    supported_algo = ['DQN', 'PPO2', "A2C", "ACKTR", "DDPG", "ACER", "GAIL", "HER", "PPO1", "SAC", "TD3", "TRPO"]
    args = parser.parse_args()
    assert supported_formalization.count(args.mode.upper()) == 1, "The formalization mode is not set correctly"
    assert supported_algo.count(args.algo.upper()) == 1, "The formalization mode is not set correctly"

    conf = Config()
    conf.train_data = args.train_data
    conf.dataset_name = Path(args.train_data).stem
    if not args.win_size:
        conf.win_size = 10
    else:
        conf.win_size = int(args.win_size)
    if not args.first_cycle:
        conf.first_cycle = 0
    else:
        conf.first_cycle = int(args.first_cycle)
    if not args.cycle_count:
        conf.cycle_count = 9999999


    if not args.output_path:
        conf.output_path = '../experiments/' + args.mode + "/" + args.algo + "/" + conf.dataset_name + "_" \
                           + str(conf.win_size) + "/"
        conf.log_file = conf.output_path + args.mode + "_" + args.algo + "_" + \
                        conf.dataset_name + "_" + args.episodes + "_" + str(conf.win_size) + "_log.txt"
    else:
        conf.output_path = args. output_path + "/" + args.mode + "/" + args.algo + "/" + conf.dataset_name + "_" \
                           + str(conf.win_size) + "/"
        conf.log_file = conf.output_path + args.mode + "_" + args.algo + "_" + \
                        conf.dataset_name + "_" + args.episodes + "_" + str(conf.win_size) + "_log.txt"

test_data_loader = TestCaseExecutionDataLoader(conf.train_data, args.dataset_type)
test_data = test_data_loader.load_data()
ci_cycle_logs = test_data_loader.pre_process()
### open data

reportDatasetInfo(test_case_data=ci_cycle_logs)

### get freeze_cycle
item_id = files.index(conf.train_data.split('/')[-1])
freeze_cycle = freeze_cycle_sample[item_id]

#training using n cycle staring from start cycle
conf.dataset_type = args.dataset_type
experiment(mode=args.mode, algo=args.algo.upper(), test_case_data=ci_cycle_logs, episodes=int(args.episodes),
           start_cycle=conf.first_cycle, verbos=False,
           end_cycle=conf.first_cycle + conf.cycle_count - 1, model_path=conf.output_path, dataset_name="", conf=conf)
# .. lets test this tommorow by passing args



