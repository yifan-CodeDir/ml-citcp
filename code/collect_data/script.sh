#!/bin/bash

export U_DB_DIR=U_DB_DIR

db_path="U_DB_DIR/"$(basename "$PWD")".udb"
echo '############################# CLASS #############################'
#echo 'git fetch'
#git fetch
#echo 'git diff --name-only origin/TEST'
lastID=`git log --format="%H" -n 2`


diff_files_M=`git diff --name-only --diff-filter=M ${lastID}| xargs`
#diff_files_M=`git diff --name-only --diff-filter=M a668a4798163cbf2ca33584270a439369d33fedc e1618fa2327967562c6af0848c8d5873e0040542 | xargs`
#echo "M - ${diff_files_M}"
printf "\033[1;33mM - ${diff_files_M}\033\n"

diff_files_A=`git diff --name-only --diff-filter=A ${lastID}| xargs`
#diff_files_A=`git diff --name-only --diff-filter=A a668a4798163cbf2ca33584270a439369d33fedc e1618fa2327967562c6af0848c8d5873e0040542 | xargs`
#echo "A - ${diff_files_A}"
printf "\033[1;32mA - ${diff_files_A}\032\n"

diff_files_D=`git diff --name-only --diff-filter=D ${lastID}| xargs`
#diff_files_D=`git diff --name-only --diff-filter=D a668a4798163cbf2ca33584270a439369d33fedc e1618fa2327967562c6af0848c8d5873e0040542 | xargs`
#echo "D - ${diff_files_D}"
printf "\033[1;31mD - ${diff_files_D}\033[0m\n"

echo "###########################"
if [[  $diff_files_A   ||   $diff_files_D  ]] 
then
    modList_D=()
    for x in ${diff_files_D}
    do
        if [[ ${x} = *".java"* ]]
        then 
          echo "D - .java character detected in ${x}"
          module=`echo ${x}`  #| rev | cut -d '/' -f 1 | rev`
          #printf "\033[1;31mD - ${module}[0m\n"
          printf "\033[1;31mD - ${module}\033[0m\n"
          #echo "D - ${module}"
          if [[ "${modList_D[@]}" =~ "${module}" ]]
          then
            echo "D - yep, it's there"
          else
        	  modList_D+=("${module}")
          fi 
        fi  
    done
    echo "D[list] - ${modList_D[@]}"
    
    
    for y in ${modList_D[@]}
    do
        echo "FILES NELLA LISTA RIMOSSI - ${y}"
        python3 dependency_searching.py ${y}
    done
    
    echo "[A,D] - Understand rescan"
    und -db ${db_path} analyze
    
    modList_A=()
    for x in ${diff_files_A}
    do
        if [[ ${x} = *".java"* ]]
        then 
          echo "A - .java character detected in ${x}"
          module=`echo ${x}`
          printf "\033[1;32mA - ${module}\033[0m\n"
          #echo "A - ${module}"
          if [[ "${modList_A[@]}" =~ "${module}" ]]
          then
            echo "A - yep, it's there"
          else
        	  modList_A+=("${module}")
          fi 
        fi  
    done
    echo "A[list] - ${modList_A[@]}"

    for y in ${modList_A[@]}
    do
        echo "FILES NELLA LISTA AGGIUNTI - ${y}"
        python3 dependency_searching.py ${y}
    done
    
else
    echo "[M] - Understand changed"
    und -db ${db_path} analyze -changed
fi


modList_M=()
for x in ${diff_files_M}
do
    if [[ ${x} = *".java"* ]]
    then 
      echo "M - .java character detected in ${x}"
      module=`echo ${x}`
      printf "\033[1;33mM - ${module}\033[0m\n"
      #echo "M - ${module}"
      if [[ "${modList_M[@]}" =~ "${module}" ]]
      then
        echo "M - yep, it's there"
      else
    	  modList_M+=("${module}")
      fi 
    fi 
done
echo "M[list] - ${modList_M[@]}" 

for y in ${modList_M[@]}
do
    echo "FILES NELLA LISTA MODIFICATI - ${y}"
    python3 dependency_searching.py ${y}
done


