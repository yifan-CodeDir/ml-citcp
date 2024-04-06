# Revisiting Machine Learning based Test Case Prioritization for Continuous Integration
This repository contains a replication package for a research paper submitted to the [ICSME 2023](https://conf.researchr.org/home/icsme-2023). We provide our code, data and result for the ease of replicating our experiments.

#### Code

In the **collect_data** subdirectory, scripts for constructing TCP datasets are provided. We do dependency analysis using [Understand]([SciTools](https://www.scitools.com/)), so please download the related tools in advance.

For usage:

1. Choose and clone a repository 

   ```
   git clone https://github.com/xxx/xxxx
   ```

2. Copy the scripts to the downloaded repository. In script *push.sh*, fill the project name in the command

   ```
   und create -db U_DB_DIR/xxx.udb -languages java add /home/xxx/src
   ```

    Then run command

   ```
   git log --format="%H" -n 800 --reverse >log800.txt
   ```

   and `git checkout` to the first commit id in *log800.txt*. 

1. Run the invocation command 

   ```
   bash push.sh
   ```

In the **rl** subdirectory, we provide the python implementation for algorithms RL, COLEMAN, PPO2-PO, ACER-PA, PPO1-LI. 

In the **supervised_learning** subdirectory, we provide implementations for MART, RankNet, RankBoost, CA, L-MART, which mainly rely on [Ranklib](https://sourceforge.net/p/lemur/wiki/RankLib/.). We also provide implementation for DeepOrder.

#### Data

The **origin** subdirectory contains the original datasets collected from github using our scripts, including 11 projects.

The **smote** subdirectory contains the datasets pre-processed by SMOTE.

#### Result

Results for RQ1, RQ2, RQ3 are provided in the corresponding directory. Scripts for plotting figures are also provided.

#### Reference

We adopt code from previous work

[Learning-to-Rank vs Ranking-to-Learn: Strategies for Regression Testing in Continuous Integration](https://dl.acm.org/doi/abs/10.1145/3377811.3380369) Github repository: https://github.com/icse20/RT-CI

[Reinforcement Learning for Test Case Prioritization](https://ieeexplore.ieee.org/abstract/document/9394799) Github repository: https://github.com/moji1/tp_rl 

[DeepOrder: Deep Learning for Test Case Prioritization in Continuous Integration Testing](https://ieeexplore.ieee.org/abstract/document/9609187) Github repository: https://github.com/AizazSharif/DeepOrder-ICSME21

[A Multi-Armed Bandit Approach for Test Case Prioritization in Continuous Integration Environments](https://ieeexplore.ieee.org/abstract/document/9086053) Github repository: https://github.com/jacksonpradolima/coleman4hcs

#### Citing

```
@inproceedings{zhao2023revisiting,
  title={Revisiting Machine Learning based Test Case Prioritization for Continuous Integration},
  author={Zhao, Yifan and Hao, Dan and Zhang, Lu},
  booktitle={2023 IEEE International Conference on Software Maintenance and Evolution (ICSME)},
  pages={232--244},
  year={2023},
  organization={IEEE}
}
```
