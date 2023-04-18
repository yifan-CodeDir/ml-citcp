 #!/bin/bash

while IFS='' read -r line || [[ -n "$line" ]]; do
    echo "#################################### {[TESTING]} ####################################"
    #echo "{[TEST CLASS]} - $line"
    mvn -Dtest=$line test -Drat.skip=true package
done < "$1"

