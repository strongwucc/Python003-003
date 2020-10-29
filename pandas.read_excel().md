<style type="text/css">
    h1 { counter-reset: h2counter; }
    h2 { counter-reset: h3counter; }
    h3 { counter-reset: h4counter; }
    h2:before {
      counter-increment: h2counter;
      content: counter(h2counter) ".\0000a0\0000a0";
    }
    h3:before {
      counter-increment: h3counter;
      content: counter(h2counter) "."
                counter(h3counter) ".\0000a0\0000a0";
    }

</style>

# pd.read_excel() 全参数详解

## 选取读取范围

### `io` 必填参数, 要读取的文件对象

支持类型: str, bytes, ExcelFile, xlrd.Book, path object, or file-like object

> 支持的类型有很多, 通常写文件的路径即可

### `sheet_name=0` 选取工作表

支持类型: str, int, list, None

- int: 默认为 0, 表示第 1 张工作表；如果是 1, 表示第 2 张工作表
- str: 例如 'sheet', 表示名称为 'sheet' 的工作表
- list: 例如 [0, 1, 'sheet'], 表示第 1, 2 张以及名称为 'sheet' 的工作表, 以字典形式返回
- None: 以字典形式返回所有工作表

### `header=0` 指定列索引行

支持类型: int, list of int, None

- int: 默认为 0, 指定第 1 行为列索引行
- list of int: 多重索引
- None: 不指定列索引行, 列索引名称为 0, 1, 2, ...

> 使用频率高

### `nrows=None` 指定要读取的行数数量上限

支持类型: int, None

- None: 默认不操作
- int: 例如整数 N, 表示最多读取 N 行

> **不能与 `skipfooter` 同时使用**
> 当工作表无效行数（行数据全部为缺失值, 但是又可以被 pandas 读取, 往往由人为失误造成）太多, 读取全部数据会花费很多时间, 这个时候就很适合使用这个参数

### `usecols=None` 指定要读取的列

支持类型: str, list-like, or callable

- None: 默认读取全部列
- str: 例如 'A,B,D:E', 表示读取 A, B, D 到 E 这四列
- list of int: 例如 list(range(4)), 表示读取前四列
- list of str: 例如 ['col'], 表示读取名称为 'col' 的列
- callable: 例如 `lambda col: col is not None`, 返回 True 的列

> 能有效地在一开始就筛选需要的列

### `skiprows=None` 跳过指定行

支持类型: int, list of int, None

- None: 默认不操作
- int: 例如整数 N, 跳过（不读取）前 N 行
- list of int: 例如 [1,3], 跳过第 1, 3 行

> `header` 与 `skiprows` 的区别:
> `skiprows` 比 `header` 先执行, 即 skiprows 先执行跳过操作, 操作过后, df 的第 1 行是 header=0 的指向的行
> `header` 只能跳过前 N 行, `skiprows` 能指定跳过的行

### `skipfooter=0` 跳过末 N 行

支持类型: int

- int: 例如整数 N, 跳过（不读取）末 N 行

## 处理表结构

### `name=None` 取列索引名称

支持类型: list

- None: 默认不操作
- list: 为每一列的索引起名字, 列表长度要和列数量相等

> 挺实用, 可以结合 `partial` 函数使用
> 能够让不同的工作表统一列索引, 省去 `df.rename(columns={'old_name': 'new_name'}, inplace=True)` 语句

### `index_col=None` 指定索引列

支持类型: int, list of int

- None: 默认不操作
- int: 例如整数 N, 取第 N + 1 列取作索引列
- list of int: 多重索引

### `squeeze=False` 是否压缩成 Series

支持类型: Bool

- True: 如果只读取一列数据, 则返回一个 Series
- False: 默认不操作

## 处理数据类型

### `converters=None` 按指定函数解析

支持类型: dict

- None: 默认不操作
- dict: 例如 {'col': function}, 将名称为 'col' 的列, 按指定 function 方法解析

> 个人觉得非常实用的一个参数, 可以转换数据类型, 比如将数值型数据(特别是 0 开头的)转换成文本型数据
> function 可以是内置函数名称, 如 int, str, pd.to_datetime
> 也可以是 lambda 表达式或自定义函数, 用来进行相对复杂的数据处理

### `dtype=None` 解析成指定数据类型

支持类型: dict

- None: 默认不操作
- dict: 例如 {'col': type}, 将名称为 'col' 的列, 解析成 type 数据类型

> 这里的 type, 主要是指 float, int, str 这三种类型, 不支持解析成 datetime64 类型
> `dtype` 和 `converters` 在转换的类型上有细微的差别, 如转换成 int 时, `dtype` 转换出来的是 int32 类型, `converters` 转换出来的是 int64 类型
> 不考虑转换类型的话, `dtype` 能实现的功能 `converters` 似乎都能实现, 完全可以用 `converters` 来代替

### `convert_float=True` 是否把整数从 float 转换为 int

支持类型: bool

- True: 把表示整数的浮点型数据转换成整型, 比如 1.0 → 1
- False: 不转换

> pandas 从 Excel 文件中读取的所有数值都是 float 类型的

### `parse_dates=False` 解析成 datetime64 类型

支持类型: bool, list, or dict

- False: 默认不操作
- True: 把索引列解析成 datetime64 类型
- list of int/str: 例如 [1,2], 则分别解析第 1,2 列为 datetime64
- list of list: 例如 [[1,2\]], 则合并第 1,2 列, 然后解析为 datetime64
- dict: 例如 {'date': [1,2]}, 则合并第 1,2 列, 然后解析为 datetime64 并取列索引名称 'date'

> 对于一列为 date, 另一列为 time 类型的数据, 可以合并成 datetime64 类型的数据
> `parse_dates` 合并并命名新列索引, 这个功能 `converters` 是做不到的

### `date_parser=None` 自定义日期解析函数

支持类型: function

在 `parse_dates` 参数中, 使用的解析日期的方法是 ``dateutil.parser.parser``。
解析出来的是 datetime64 类型的数据, 格式形如 YYYY-MM-DD HH:MM:ss[.uuu]][TZ]。
然而这不一定是我们想要的日期格式, 这个时候就可以自己写一个处理日期的函数或表达式, 使用 `date_parser=func` 来解析成我们想要的格式。例如:

```python
func = lambda date: pd.datetime.strptime(date, '%Y/%m/%d')
```

### `thousands=None` 处理包含千分位分割符的文本型数据

支持类型: str

- None: 默认不操作
- str: 例如 ',', 表示千分位分割符, 会将数值的千分位分隔符去掉

> 要转化的数据本身必须为文本类型
> 当遇到包含千分位分割符的文本行数据时十分实用
> 有时候也可以代替 replace() 方法 (但是不稳定)

## 处理数据

### `true_values=None` 把指定值转换成 True 值

支持类型: list

### `false_values=None` 把指定值转换成 False 值

支持类型: list

### `na_filter=True` 是否检测缺失值

支持类型: bool

- True: 默认检测, 如果判定为缺失值, 那么值将被修改为 NaN
- False: 不检测, 在没有空值的情况下能提升性能

> 以下数据会被判定为缺失值: '', '#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan', '1.#IND', '1.#QNAN', '<NA\>', 'N/A', 'NA', 'NULL', 'NaN', 'n/a', 'nan', 'null'
> **如果 `na_filter` 的值为 False, 那么参数 `keep_default_na` and `na_values` 将会失效**

### `na_values=None` 把指定值转换成 NaN 值

支持类型: scalar, str, list-like, or dict

> 把你不需要的值转换成 NaN 值, 之后再统一处理 NaN 值
> 这个参数不受 `keep_default_na` 值的影响

### `keep_default_na=True` 是否将缺失值转换成 NaN 值

支持类型: bool

- True: 默认为 True, 将缺失值转换成 NaN 值
- False: 缺失值将保留原始值

> 这个参数用来控制是否要将被判定的缺失值转换成 NaN 值

### `comment=None` 指定注释符, 其后面的内容将不会被读取

支持类型: str

指定一个字符串为注释符, 比如 '#', 那么在带 '#' 的行中, '#' 及后面的数据全部不会被读取

> 类似于用 `.split()` 函数进行分割然后取第一段字符的功能

## 其他

### `engine=None` 选择引擎

支持字符: 'xlrd', 'openpyxl', 'odf', 'pyxlsb'

- xlrd: 默认引擎, 支持大多数 Excel 文档, 需要 pip 安装 `xlrd`
- openpyxl: 支持最新版本的 Excel 文档, 需要 pip 安装 `openpyxl`
- odf: 支持 (.odf, .ods, .odt) 格式的文档, 需要 pip 安装 `odfpy`
- pyxlsb: 支持二进制 Excel 文档, 需要 pip 安装 `pyxlsb`

> 不同引擎要通过 pip 下载对应的库

### `mangle_dupe_cols=True` 是否处理重复列索引

支持类型: bool

- True: 遇到重复的列索引 X, 将处理为 'X', 'X.1', …'X.N'
- False: 不进行处理, 可能会导致数据覆盖问题

> 目前 pandas 最新版本 (1.1.3) 暂不支持把参数值设置为 False

### `verbose=False` 是否打印非数值列中缺失值的数量

支持类型: bool

> 默认 False, 参数值设为 True 后, 除了看见它多 print 了一个 Reading 'sheet_name', 并没有发现什么特别... 所以归在了其他类别中, 欢迎补充!
> 官方解释: Indicate number of NA values placed in non-numeric columns.
