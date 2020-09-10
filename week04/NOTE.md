### pandas 简介

[pandas 中文文档](https://www.pypandas.cn/)

[Numpy 学习文档](https://numpy.org/doc/)

[matplotlib 学习文档](https://matplotlib.org/contents.html)

### pandas 基本数据类型

##### Series

从列表创建 Series

```
import pandas as pd
import numpy as np

pd.Series(['a', 'b', 'c'])
```
通过字典创建自带索引的 Series

```
series1 = pd.Series({'a': 11, 'b': 22, 'c': 33})
```

通过关键字创建带索引的 Series

```
series2 = pd.Series([11, 22, 33], index = ['a', 'b', 'c'])
```

获取全部索引

```
series1.index
```
获取全部值

```
series2.values
```
类型

```
type(series1.values) # <class 'numpy.ndarray'>
type(np.array(['a', 'b']))
```

转化为列表

```
series1.values.tolist()
```
> 使用 index 会提升查询性能
> 
> 如果 index 唯一，pandas 会使用哈希表优化，查询性能为 O(1)
> 
> 如果 index 有序不唯一，pandas 会使用二分查找算法，查询性能为 O(logN)
> 
> 如果 index 完全随机，每次查询都要扫全表，查询性能为 O(N)


##### DataFrame

列表创建 dataFrame

```
df1 = pd.DataFrame(['a', 'b', 'c', 'd'])
```

嵌套列表创建 dataFrame

```
df2 = pd.DataFrame(
    [
        ['a', 'b'],
        ['c', 'd']
    ]
)
```

自定义列索引


```
df2.columns = ['one', 'two']
```

自定义行索引


```
df2.index = ['first', 'second']
```


可以在创建时直接锁定

```
df3 = pd.DataFrame([...], colums=[], index=[])
```
查看索引

```
df2.columns
df2.index
```

### pandas 数据导入

##### Pandas 支持大量格式的导入，使用的是 read_*() 的形式


```
import pandas as pd

pd.read_excel(r'1.xlsx')

# sep 分隔符
# nrows 读取的行数
# encoding 编码
pd.read_csv(r'c:\file.csv', sep='', nrows=10, encoding='utf-8')

# sql 查询 sql
# conn 数据库连接
pd.read_sql(sql, conn)
```


### pandas 数据预处理

##### 缺失值处理


```
import pandas as pd
import numpy as np

x = pd.Series([1, 2, np.nan, 3, 4, 5, 6, np.nan, 8])
```

是否存在缺失值

```
x.hasnans
```

将缺失值填充为平均值

```
x.fillna(value = x.mean())
```

向前填充缺失值

```
df = pd.DataFrame({
    "A": [5, 3, None, 4],
    "B": [None, 2, 4, 3],
    "C": [4, 3, 8, 5],
    "D": [5, 4, 2, None]
})

# 查看缺失值汇总
df.isnull().sum()

# 用上一行填充
df.ffill()

# 用前一列填充
df.ffill(axis=1)
```

缺失值删除

```
df.info()
df.dropna()
```

填充缺失值

```
df.fillna('无')
```


##### 重复值处理


```
df.drop_duplicates()
```

### pandas 数据调整

##### 行列调整


```
df = pd.DataFrame({"A":[5,3,None,4], 
                 "B":[None,2,4,3], 
                 "C":[4,3,8,5], 
                 "D":[5,4,2,None]}) 
```
列的选择，多个列要用列表


```
df[ ['A', 'C'] ]
```

某几列


```
# :表示所有行，获得第1和第3列
df.iloc[:, [0,2]]

```

行选择

```
# 选择第1行和第3行
df.loc[ [0, 2] ]

# 选择第1行到第3行
df.loc[ 0:2 ]

# 比较，满足 A 行小于 5，C 行小于 4
df[ (df['A'] < 5) & (df['C'] < 4) ]
```


##### 数值替换

一对一替换

```
# C 列中的 4 替换成 40
df['C'].replace(4, 40)
```

多对一替换

```
# 4，5,8 替换成 1000
df.replace([4, 5, 8], 1000)
```

多对多替换

```
df.replace({4: 400, 5: 500, 8: 800})
```

##### 排序


```
# 按照指定列降序排列
df.sort_values( by = ['A'], ascending = False )
# 多列排序
df.sort_values( by = ['A', 'C'], ascending = [True, False] )
```


##### 删除


```
# 删除列
df.drop('A', axis=1)

# 删除行
df.drop(3, axis=0)

# 删除特定行
df[ df['A'] < 4 ]
```


##### 行列互换


```
df.T
df.T.T
```

##### 索引重塑


```
# 数据透视表
df.stack()
df.unstack()

# 充值索引
df.stack().reset_index()

```


### pandas 基本操作

##### [Pandas 计算功能操作文档](https://pandas.pydata.org/docs/user_guide/computation.html#method-summary)

##### 算数运算

```
df['A'] + df['C']
```

##### 比较运算

```
df['A'] < df['C']
```

##### 非空值计数

```
df.count()
```

##### 非空值列求和

```
df.sum()
df['A'].sum()
```

##### 求平均值

```
df.mean()
```

##### 求最大值

```
df.max()
```

##### 求最小值

```
df.min()
```

##### 求中位数

```
df.median()
```

##### 求众数

```
df.mode()
```

##### 求方差

```
df.var()
```

##### 求标准差

```
df.std()
```

### pandas 分组聚合

#####  分组

```
import pandas as pd
import numpy as np

groups = ['x', 'y', 'z']

df = pd.DataFrame({
    'group': [groups[i] for i in np.random.randint(0, len(groups), 10)],
    "salary":np.random.randint(5,50,10),
    "age":np.random.randint(15,50,10)
})

# 分组
df.groupby('group')
```

#####  聚合计算

```
# 分组后求平均值
df.groupby('group').agg('mean')

# 分组后求 salary 的平均值，和 age 的方差
df.groupby('group').agg( {'salary': 'mean', 'age': 'var'} )

# 如果 agg 中只有一个函数，则可以直接计算
df.groupby('group').mean()

# 计算结果转换为 python 的字典
df.groupby('group').mean().to_dict()

# 使用 transform 代替 agg
df.groupby('group').transform('mean')

# 透视表
pd.pivot_table(df, values='salary', columns='group', index='age', aggfunc='count', margins=True).reset_index()

```

### pandas 多表拼接

##### [merge](https://pandas.pydata.org/docs/reference/api/pandas.merge.html)

```
# left 左数据
# right 有数据
# how 链接方式 inner left right outer
# on 如果有多个相同字段就通过 on 指定
merge(left, right, how: str="inner", on=None, left_on=None, right_on=None, left_index: bool=False, right_index: bool=False, sort: bool=False, suffixes=("_x", "_y"), copy: bool=True, indicator: bool=False, validate=None) 
```

##### [concat](https://pandas.pydata.org/docs/reference/api/pandas.concat.html)

### pandas 输出和绘图

##### [plot 学习文档](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.html)

##### [seaborn 学习文档](http://seaborn.pydata.org/tutorial.html)

##### 导出为 .xlsx 文件


```
# excel_writer 文件名称
# sheet_name Sheet 名称
# index 是否去掉索引
# columns 要导出的列
# encoding 设置编码
# na_rep 缺失值处理
# inf_rep 无穷值处理

df.to_excel( excel_writer = f'file.xlsx', sheet_name = 'sheet1', index = False, columns = ['col1', 'col2'], encoding='utf-8', na_rep=0, inf_rep=0 )
```
##### 导出为 .csv 文件

```
df.to_csv()
```
##### 导出为 .pkl 文件（性能好）

```
df.to_pickle('xx.pkl')
```
> agg 中尽量使用内置函数
> 
> agg(sum) 快
> 
> agg( lambda x: x.sum() ) 慢

##### 导出为 plt 和 seaborn 图像


```
import matplotlib.pyplot as plt

# df.index 为横坐标，df['A'] 为纵坐标
plt.plot(df.index, df['A'])

# color 颜色
# linestyle 线条颜色
# linewidth 线条宽度
# marker 点标记
plt.plot(df.index, df['A'], color='#ffaa00', linestyle='--', linewidth=3, marker='D')

# 显示
plt.show()
```

```
import seaborn as sns

# 绘制散点图
plt.scatter(df.index, df['A'])
plt.show()

# 美化 plt
sns.set_style('darkgrid')
plt.scatter(df.index, df['A'])
plt.show()
```


### jieba 分词与提取关键词

##### [jieba 学习文档](https://github.com/fxsjy/jieba/blob/master/README.md)

##### 分词

精确模式

```
jieba.cut(string, cut_all=False)
```

全模式

```
jieba.cut(string, cut_all=True)
```

搜索引擎模式

```
jieba.cur_for_search()
```

自定义用户词典

```
jieba.load_userdict(r'user_dict.txt')
```

--user_dict.txt
```
# 词的内容 权重 词性
Python进阶训练营 3 nt
```
动态添加词典

```
jieba.add_word('极客大学')
```
动态删除词典

```
jieba.del_word('自定义词')
```
关闭自动计算词频

```
jieba.cut(string, HMM=False)
```
调整分词，合并

```
jieba.suggest_freq('中出', True)
# 结合 HMM= False
jieba.cut(string, HMM=False)
```

调整分词，分开

```
jieba.suggest_freq(('中','将'), True)
# 结合 HMM= False
jieba.cut(string, HMM=False)
```


##### 关键字提取

```
# 基于TF-IDF算法进行关键词抽取
tfidf = jieba.analyse.extract_tags(text,
topK=5,                   # 权重最大的topK个关键词
withWeight=True)         # 返回每个关键字的权重值
# 基于TextRank算法进行关键词抽取
textrank = jieba.analyse.textrank(text,
topK=5,                   # 权重最大的topK个关键词
withWeight=False)         # 返回每个关键字的权重值
```

> 通过 jieba.analyse.set_stop_words('jieba/stop_words.txt') 方法添加需要排除的词


### SnowNLP 情感倾向分析

##### [snowNLP 参考学习地址](https://github.com/isnowfy/snownlp/blob/master/README.md)

中文分词

```
from snownlp import SnowNLP

text = ''

s = SnowNLP(text)
s.words
```

词性标注（隐马尔可夫模型）

```
s.tags
```

情感分析（朴素贝叶斯分类器）

```
s.sentiments
```

拼音（Trie树）

```
s.pinyin
```

繁体转简体

```
s.han
```

提取关键字

```
s.keywords(limit=5)
```

信息衡量

```
# 词频越大越重要
s.tf

# idf 越大，说明词条越重要
s.idf
```

训练

```
from snownlp import seg

seg.train('data.txt')
seg.save('seg.marshal')
```
