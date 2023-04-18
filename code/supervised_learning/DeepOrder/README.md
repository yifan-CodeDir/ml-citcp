# DeepOrder

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Implementation of DeepOrder for the paper "DeepOrder: Deep Learning for Test Case Prioritization in Continuous Integration Testing".

 * [Project Page](https://aizazsharif.github.io/DeepOrder-site/)
 * [Paper](https://arxiv.org/abs/2110.07443)

## Installation


1. Install Anaconda (for creating and activating a separate environment)
2. Run: 
```
$ conda create -n DeepOrder python==3.6
$ conda activate DeepOrder
```
3. Inside the enviroment, run:
```
$ pip install -r requirements.txt
```
## Instructions

There are 3 python scripts leading to 3 separate experiments. 

For running all the scripts together use: 
```

$ ./scripts_all.sh

```


## Citing
```BibTeX
@INPROCEEDINGS{sharif2021deeporder,
  author    = {Sharif, Aizaz and Marijan, Dusica and Liaaen, Marius},
  title     = {DeepOrder: Deep Learning for Test Case Prioritization in Continuous Integration Testing},
  journal   = {ICSME},
  year      = {2021},
}
```
