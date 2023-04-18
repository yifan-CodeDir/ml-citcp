import pandas as pd
import numpy as np


if __name__ == '__main__':

    projects = ['commons-bcel.csv', 'commons-csv.csv', 'commons-dbcp.csv', 'commons-text.csv', 'java-faker.csv', 'jedis.csv', 'jsoup.csv', 'jsprit.csv', 'maxwell.csv','spring-data-redis.csv']
    start_cycle_num = [185,185,185,185,185,185,185,185,185,185]
    for project in projects:

        df = pd.read_csv(project, header=0, sep=';')
        
        start_cycle = start_cycle_num[projects.index(project)]

        # select test cycle
        test_df = df[start_cycle:]

        # select failing cycle
        fail_test_df = test_df.loc[test_df['DDP'] >= 0.0]
        ddp = np.mean(fail_test_df['DDP'].values)

        print(project)
        print(ddp)