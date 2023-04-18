#!/bin/bash

# git log --format="%H" -n 800 --reverse >log800.txt

mkdir U_DB_DIR
und create -db U_DB_DIR/bcel.udb -languages java add /home/bcel/src

# git checkout -b FIRST_TRY                          #crete a new local branch
# git push origin FIRST_TRY:FIRST_TRY                #synchronized with GitHub

while IFS='' read -r line || [[ -n "$line" ]]; do
    git checkout $line
#    git push origin $line:FIRST_TRY --force-with-lease
    echo "$line has been pushed to the github"
    start=`date +%s`
    ./script.sh
    ./testing.sh dependsby.txt
    end=`date +%s`
    runtime=$((end-start))
    echo "TIME - ${runtime}"
    echo Execution time was `expr $end - $start` seconds.

    python3 data_collection_new.py ${runtime} ${line}

    rm -d "dependsby.txt"

    #sleep 5
done < "log800.txt"
