# EE208-Stock_news_data_analysis

## `Astocks.csv`
股票数据的集大成者，一应俱全，直接读入可以用为其量身打造的`Tools.read_and_write.py` 中的`read_Astocks_data`函数，可直接得到任意项的所有数据
###信息包含
    code,代码  name,名称  industry,所属行业   area,地区   pe,市盈率   outstanding,流通股本(亿)   totals,总股本(亿)   totalAssets,总资产(万)   liquidAssets,流动资产

    fixedAssets,固定资产   reserved,公积金   reservedPerShare,每股公积金   esp,每股收益   bvps,每股净资   pb,市净率   timeToMarket,上市日期

    undp,未分利润   perundp, 每股未分配   rev,收入同比(%)   profit,利润同比(%)   gpr,毛利率(%)   npr,净利润率(%)   holders,股东人数

`Astocks.csv`  文件用于存储A股中所有股市的信息，注意，`Astocks.csv` 文件是一切的根基，这个文件是经过了很多转换和手工清洗操作的，不要随意更改
### 格式
    code name industry area pe outstanding totals totalAssets liquidAssets fixedAssets reserved reservedPerShare esp bvps pb timeToMarket undp perundp rev profit gpr npr holders
    300812 N易天 专用机械 深圳 24.94 0.19 0.78 7.37 7.01 0.09 0.67 0.87 0.929 9.24 3.34 20200109 1.94 2.5 0.0 0.0 45.6 20.83 38744.0
    688058 宝兰德 软件服务 北京 162.22 0.09 0.4 1.98 1.8 0.02 0.15 0.39 0.527 22.48 5.07 20191101 1.3 3.24 0.0 0.0 0.0 29.2 11488.0
    688258 卓易信息 软件服务 江苏 319.35 0.2 0.87 3.99 2.94 0.56 0.69 0.79 0.221 9.59 9.8 20191209 1.71 1.97 0.0 0.0 48.88 14.46 20266.0


## `stars.csv`
根据新闻分析得出对于每一只股票**未来走势预测**，从1🌟到5🌟五个评级，生成代码在`Tools/analyzer.py`
###格式
    股票代码 星级

   
## `history.csv`
注：Searcher 类支持现已损坏

A股中所有股票近两年以来的股价信息
### 格式
    股票代码A
    日期 开盘价格 最低价格 最高价格 收盘价格
    日期 开盘价格 最低价格 最高价格 收盘价格
    ...
    
    股票代码B
    ...

如

    300812
    2020-01-10 33.99 33.99 33.99 33.99
    2020-01-09 25.75 25.75 30.9 30.9


## `Acodes.csv`
A股中所有股票的代码
### 格式
    300812
    688058
    688258

## `Acodes_names.csv`
A股中所有股票的代码和名称
### 格式
    300812 N易天
    688058 宝兰德
    688258 卓易信息
    
## `dirty_date.csv` and `dates.csv`
用于生成history.csv所需要的dates列表，属于数据清洗工作，这里不赘述，工作详情请看`Get_stock_datas`
