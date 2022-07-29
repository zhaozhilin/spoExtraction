# 基于百度Duie2.0数据的实体信息抽取任务

# 引用论文
[multi_head_selection](https://arxiv.org/abs/1804.07847)

[casrel](https://arxiv.org/pdf/1909.03227.pdf)

# 引用数据 
百度比赛多形态信息抽取之关系抽取(https://aistudio.baidu.com/aistudio/competition/detail/65/0/introduction)

# 任务介绍
该任务旨在从非结构化自然语言文本中提取结构化知识，如实体、关系等。在给定的长尾关系schema约束下进行关系抽取，也就是在给定关系集合下，从自然语言文本中抽取出符合关系 schema 约束的 SPO 三元组知识，但是对 O 值形态进行了复杂化的扩展。

# 工作介绍
1、使用casrel方法，即指针网络的方法，构建了一个先抽取主语实体subject，再根据主语实体subject与句子抽取谓语predicate和宾语实体object的模型——基于主语感知的层叠式指针网络

2、使用mutil_head_selection方法，即多头标注的方法，构建使用CRF（条件随机场)层对实体识别任务进行建模，并将关系提取任务作为一个多头选择问题，在这里最重要的是关系分类器的构造，即是实体pair的一个线性分类器，每个实体pair只选取当前实体span的最后一个字符进行关系预测

# Requirement

* python 3.7
* pytorch 1.10
* pytorch-crf 0.7.2
* transformers
* prefetch-generator 1.0.1
* tqdm 4.26.0

# Dataset
	 训练集	开发集	测试集
	171293	2067	13080

# Result

## Chinese

|  | precision | recall | f1 |
| ------ | ------ | ------ | ------ |
| 多头选择(Bert)+指针标注 | 0.6996 | 0.5596|  0.6177 |
| 多头选择(BiLstm)+指针标注 | 0.6268 | 0.5425 | 0.5816 |
| 多头选择(GRU)+指针标注 | 0.6680 | 0.5303 | 0.5912 |
| 层叠式指针标注 | 0.7277 | 0.6811 | 0.7036 |


# TODO

* Tune the hyperparameters
