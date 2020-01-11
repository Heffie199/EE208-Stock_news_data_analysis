# EE208-Stock_news_data_analysis

## `analyzer.py`
用于读取html文件并生成星级评级🌟

## `Searcher.py`
用于在python文件中使用`Data/stocks/`下的所有数据，一站式封装搜索类

## `read_write.py`
读写方便的函数库
### `def read_Astocks_data(index="code",path="../Data/stocks/Astocks.csv"):`
用于返回你所索引的信息（A股所有股票对于该索引信息下的列表），详情请看函数内部参数说明
### `def open_file_and_save(file_path, data):`
用于将列表数据data（支持一维列表和二维列表）写成csv文件保存