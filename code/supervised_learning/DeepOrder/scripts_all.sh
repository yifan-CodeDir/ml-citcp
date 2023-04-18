#!/bin/sh
start=$(date '+%d-%m-%Y %H:%M:%S')
rm -r time.csv
rm -r values.csv
rm -r output.csv

echo "$start Starting DeepOrder"
echo "$(date '+%d-%m-%Y %H:%M:%S') DeepOrder on normal data"
./DeepOrder_on_normal_data.py
echo "========================================"
echo "$(date '+%d-%m-%Y %H:%M:%S') DeepOrder on smote"
./DeepOrder_on_smote_data.py
echo "========================================"
echo "$(date '+%d-%m-%Y %H:%M:%S') DeepOrder on finetune data"
./DeepOrder_on_finetune_data.py
end=$(date '+%d-%m-%Y %H:%M:%S')
echo "$end DeepOrder Completed"
