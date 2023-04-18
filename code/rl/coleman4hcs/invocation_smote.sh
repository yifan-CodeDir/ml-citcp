#!/bin/bash

for dataset in commons-bcel commons-csv commons-dbcp commons-text java-faker jedis jsoup jsprit maxwell spring-data-redis nfe
do 
    python main.py --project_dir './data/smote'  --policies  'FRR' --output_dir 'results/smote' --datasets ${dataset} --rewards TimeRankReward
    echo "Completed ${dataset}"
done