#!/bin/bash

# for dataset in compress imaging io lang math
# files = ['commons-bcel_result.csv', 'commons-csv_result.csv', 'commons-dbcp_result.csv', 'commons-text_result.csv', 'java-faker_result.csv', 'jedis_result.csv', 'jsoup_result.csv', 'jsprit_result.csv', 'maxwell_result.csv', 'spring-data-redis_result.csv', 'nfe_result.csv']  

for dataset in commons-bcel_result.csv commons-csv_result.csv commons-dbcp_result.csv commons-text_result.csv java-faker_result.csv jedis_result.csv jsoup_result.csv jsprit_result.csv maxwell_result.csv spring-data-redis_result.csv nfe_result.csv
# for dataset in math
do
    # for ACER-PA
    python TPDRL_freeze.py -m pairwise -a acer -d enriched -e 200 -w 4 -t ../data/real_new/${dataset} -o ../experiments/freeze
    # for PPO2-PO
    # python TPDRL_freeze.py -m pointwise -a ppo2 -d enriched -e 200 -w 4 -t ../data/real_new/${dataset} -o ../experiments/freeze
    # for PPO1-LI
    # python TPDRL_freeze.py -m listwise -a ppo1 -d enriched -e 200 -w 4 -t ../data/real_new/${dataset} -o ../experiments/freeze
    echo "Completed ${dataset}"
done
