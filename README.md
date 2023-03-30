# 厦门树洞小程序爬虫

## 项目介绍

本项目是一个爬虫，用于爬取厦门树洞小程序的树洞留言。核心技术是使用了 `selenium` 模拟浏览器行为。

## 项目结构

```text
README.md
crawl.py
log.py
requirements.txt
output
  |-- ...
```

- crawl.py: 爬虫主程序
- log.py: 日志模块
- log.txt: 日志文件
- requirements.txt: 依赖包
- README.md: 项目说明
- output: 爬取结果（运行时自动创建）
  - 其中的数据文件以日期命名，如 `2022-02-14.txt`

## 用法

### 安装依赖

需要安装的软件包在 `requirements.txt` 中，包括：

- pandas：数据处理
- selenium：浏览器自动化
- colorlog：彩色日志

### 修改配置

在 `crawl.py` 中修改 `start_date` 和 `today` 的值，分别为爬取的日期和结束日期。

```python
start_date = '20220214' # 厦门树洞小程序上线日期
today = '20230330'
```

### 运行

最后运行 `crawl.py` 即可。

```shell
python crawl.py
```

## 其他

### 为什么要写这个爬虫？

这是来自北航11系的一个冯如杯项目，具体干啥的我不懂，反正就是要爬厦门树洞小程序的数据。

### 项目难点

众所周知小程序的API是不公开的，因此我先在电脑上使用了抓包软件来抓取数据包，分析得到了小程序的请求地址，然后使用 `selenium` 模拟浏览器来爬取数据。

