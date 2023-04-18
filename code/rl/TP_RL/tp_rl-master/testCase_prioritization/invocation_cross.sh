#!/bin/bash

# for dataset in compress imaging io lang math
# for dataset in AxonFramework_result.csv JSqlParser_result.csv rewrite_result.csv rocketmq_result.csv spring-data-redis_result.csv 
# for dataset in commons-bcel_result.csv commons-csv_result.csv commons-dbcp_result.csv commons-text_result.csv java-faker_result.csv jedis_result.csv jsoup_result.csv jsprit_result.csv maxwell_result.csv nfe_result.csv spring-data-redis_result.csv
for dataset in commons-bcel_result.csv
do
    # for ACER-PA
    python TPDRL.py -m pairwise -a acer -d enriched -e 200 -w 4 -t ../data/cross-proj-data/${dataset} -o ../experiments/cross
    # for PPO2-PO
    # python TPDRL.py -m pointwise -a ppo2 -d enriched -e 200 -w 4 -t ../data/cross-proj-data/${dataset} -o ../experiments/cross
    # for PPO1-LI
    # python TPDRL.py -m listwise -a ppo1 -d enriched -e 200 -w 4 -t ../data/cross-proj-data/${dataset} -o ../experiments/cross
    echo "Completed ${dataset}"
done
