#!/bin/bash

for dataset in commons-bcel commons-csv commons-dbcp commons-text java-faker jedis jsoup jsprit maxwell nfe spring-data-redis
# for dataset in commons-bcel 
do
    ./repetitions_smote.sh ${dataset}
    echo "Completed ${dataset}"
done

