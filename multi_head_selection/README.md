# "Joint entity recognition and relation extraction as a multi-head selection problem" (Expert Syst. Appl, 2018)

引用论文[paper](https://arxiv.org/abs/1804.07847)

引用数据 百度比赛多形态信息抽取之关系抽取

# Requirement

* python 3.7
* pytorch 1.10

# Dataset
	 训练集	开发集	测试集
	171293	2067	13080
raw_data/chinese

# Run
```shell
python main.py --mode preprocessing --exp_name chinese_selection_re
python main.py --mode train --exp_name chinese_selection_re 
python main.py --mode evaluation --exp_name chinese_selection_re
```

If you want to try other experiments:

set **exp_name** as **conll_selection_re** or **conll_bert_re**



# Result

## Chinese

|  | precision | recall | f1 |
| ------ | ------ | ------ | ------ |
| bert(dev) | 0.6996 | 0.5596|  0.6177 |
| LSTM(dev) | 0.6268 |0.5425 | 0.5816 |
| GRU(dev) | 0.6680 |0.5303 | 0.5912 |


# Details

The model was originally used for Chinese IE, thus, it's a bit different from the official paper:

They use pretrained char-word embedding while we use word embedding initialized randomly; they use 3-layer LSTM while we use 1-layer LSTM.

# TODO

* Tune the hyperparameters for conll_bert_re
