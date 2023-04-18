import pandas as pd

p = "spring-data-redis"
data = pd.read_csv(f"{p}_result.csv", header=0, sep=",")

commit_id_list = list(data['cycle_id'])
commit_id_list = list(dict.fromkeys(commit_id_list))

with open (f"{p}_log800.txt", "w") as f:
    for commit_id in commit_id_list:
        f.write(commit_id + "\n")