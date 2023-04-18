#!/bin/bash

for dataset in commons-bcel commons-csv commons-dbcp commons-text java-faker jedis jsoup jsprit maxwell spring-data-redis
do 
    python main.py --project_dir './data/cross'  --policies  'FRR' --output_dir 'results/cross' --datasets ${dataset} --rewards TimeRankReward
    echo "Completed ${dataset}"
done