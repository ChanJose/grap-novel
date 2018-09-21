# -*- coding:utf-8 -*-
# 爬取《一念永恒》整本小说：就要获取每个章节的链接

from bs4 import BeautifulSoup
import requests
import sys


'''
类说明:下载《笔趣看》网小说《一念永恒》
Parameters:
    无
Returns:
    无
Modify:
    2018-09-01
'''
class downloader(object):
    def __init__(self):  # 构造函数
        self.server = 'http://www.biqukan.com'  # 笔趣阁网址
        self.target = 'http://www.biqukan.com/1_1094/'  # 笔趣阁《一念永恒》首页网址
        self.names = []  # 存放章节名
        self.urls = []  # 存储章节链接
        self.nums = 0  # 章节数

    """
    函数说明:获取下载链接
    Parameters:
        无
    Returns:
        无
    Modify:
        2018-09-01
    """
    def get_download_url(self):
        req = requests.get(url=self.target)
        html = req.text  # 获取数据
        div_bf = BeautifulSoup(html, "html.parser")  # 解释获取到的数据
        div = div_bf.find_all('div', class_='listmain')  # 找类为listmain的div
        #  a_bf = BeautifulSoup(str(div[0]))
        a_bf = div[0]  # 可能有很多类为listmain的<div>,所以声明变量div是一个数组，取数组的第一个<div>
        a = a_bf.find_all('a')  # 找出所有<a>标签
        self.nums = len(a[15:])  # 剔除前15个不必要的章节，并统计章节数
        for eachA in a[15:]:
            self.names.append(eachA.string)  # 在列表names中添加章节名
            self.urls.append(self.server + eachA.get('href'))  # 添加章节链接

    """
    函数说明:获取章节内容
    Parameters:
        target - 下载连接(string)
    Returns:
        texts - 章节内容(string)
    Modify:
        2018-09-01
    """
    def get_contens(self, target):
        req = requests.get(url=target)
        html = req.text
        bf = BeautifulSoup(html, "html.parser")
        texts = bf.find_all('div', class_='showtxt')
        text = texts[0].text.replace('\xa0'*8, '\n\n')  # 去掉空格符&nbsp;
        return text

    """
    函数说明:将爬取的文章内容写入文件
    Parameters:
        name - 章节名称(string)
        path - 当前路径下,小说保存名称(string)
        text - 章节内容(string)
    Returns:
        无
    Modify:
        2018-09-01
    """
    def writer(self, name, path, text):
        with open(path, 'a', encoding='utf-8') as f:  # a模式：追加, 从 EOF 开始, 必要时创建新文件
            f.write(name+'\n')  # 章节名，并空行
            f.writelines(text)  # 写入文本内容
            f.write('\n')  # 空行


# 单进程跑，没有开进程池。下载速度略慢，喝杯茶休息休息吧
if __name__ == "__main__":
    dl = downloader()  # 初始化一个对象
    dl.get_download_url()  # 获取a链接
    print('《一念永恒》正在下载：')
    for i in range(dl.nums):
        # print(dl.names[i], dl.urls[i])
        dl.writer(dl.names[i], 'all.txt', dl.get_contens(dl.urls[i]))
        sys.stdout.write('\r') # 每一次输出，从头输出
        sys.stdout.write("已下载%.3f%%" % float(i/dl.nums))
        sys.stdout.flush()  # 刷新缓冲，每执行一次，输出一次，不用等程序结束才输出
    print('《一念永恒》下载完成')
