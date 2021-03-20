import logging
from lxml import etree
from IP.reqajax import requests
from IP.mysql_pool import Mysql
from IP.settings import *
Msql_con = Mysql()
all_funcs = []

def collect_funcs(func):
    """
    装饰器，用于收集爬虫函数
    """
    all_funcs.append(func)
    return func


class Crawler(Mysql):

    def __init__(self):
        self.sqc = USQL
        if self.sqc is False:
            logging.warning('没有启用数据库')

    def run(self):
        logging.warning('启动搜集器')
        for func in all_funcs:
            for proxy in func():
                if self.sqc is True:
                    Msql_con.add_proxy(proxy,INIT_SCORE)
                else:
                    with open(p1,'a+')as f:
                        f.write('%s:%s,%s'%(proxy['ip'],proxy['port'],INIT_SCORE)+'\n')
                        f.close()
        time.sleep(3)
        logging.warning('收集结束')


"""
requests 用的是 reqajax.py 模块的 异步requests 方法
返回格式 ：{'ip':ip,'port':port,'classic':classic}
直接保存到数据库
"""

@collect_funcs
def crawl_xila():
    """
    西拉代理：http://www.xiladaili.com/gaoni/
    """
    url = "http://www.xiladaili.com/gaoni/{}/"
    logging.warning('---------------------------西拉代理开始运行')
    items = [1,2]
    for page in items:
        html = requests(url.format(page))
        if html:
            Html = etree.HTML(html)
            for proxy in Html.xpath('//tbody/tr'):
                i = ''
                ip = proxy.xpath('./td[1]/text()')[0].split(':')[0]
                port = proxy.xpath('./td[1]/text()')[0].split(':')[-1]
                classic= proxy.xpath('./td[2]/text()')[0]
                if classic == 'HTTPS代理':
                    i = 'HTTPS'
                if classic == 'HTTP代理':
                     i = 'HTTP'
                if classic == "HTTP,HTTPS代理":
                    i  = ('HTTP', 'HTTPS')
                yield {'ip':ip,'port':port,'classic':i}
    logging.warning('---------------------------西拉代理运行结束')


@collect_funcs
def crawl_qiyun():
    """
    其云代理：https://www.7yip.cn/free/?action=china&page=1
    """
    url = "https://www.7yip.cn/free/?action=china&page={}"
    logging.warning('---------------------------旗云代理开始运行')
    items = [p for p in range(1, 2)]
    for page in items:
        html = requests(url.format(page))
        if html:
            Html = etree.HTML(html)
            for proxy in Html.xpath('//tbody/tr'):
                ip = re.findall("\d+.\d+.\d+.\d+",proxy.xpath('./td[1]/text()')[0])[0]
                port = re.findall("\d+",proxy.xpath('./td[2]/text()')[0])[0]
                classic= re.findall('HTTP|HTTPS',proxy.xpath('./td[4]/text()')[0])[0]
                if ip and port:
                    yield {'ip':ip,'port':port,'classic':classic}
    logging.warning('---------------------------旗云代理运行结束')

@collect_funcs
def crawl_kuaidaili():
    """
    快代理：https://www.kuaidaili.com/free/inha/4/
    """
    url = "https://www.kuaidaili.com/free/inha/{}/"
    logging.warning('---------------------------快代理开始运行')
    items = [1,2]
    for page in items:
        html = requests(url.format(page))
        if html:
            Html = etree.HTML(html)
            for proxy in Html.xpath('//tbody/tr'):
                ip = proxy.xpath('./td[1]/text()')[0]
                port = proxy.xpath('./td[2]/text()')[0]
                classic= proxy.xpath('./td[4]/text()')[0]
                if ip and port:
                    yield {'ip':ip,'port':port,'classic':classic}
    logging.warning('---------------------------快代理运行结束')

@collect_funcs
def crawl_gaokeyondaili():
    """
    全球高可用高匿名代理：https://ip.jiangxianli.com/?page=1&anonymity=2
    """
    url = "https://ip.jiangxianli.com/?page={}&anonymity=2"
    logging.warning('---------------------------高可用代理开始运行')
    items = [p for p in range(1, 3)]
    for page in items:
        html = requests(url.format(page))
        if html:
            Html = etree.HTML(html)
            for proxy in Html.xpath('//tbody/tr'):
                ip = proxy.xpath('./td[1]/text()')[0]
                port = proxy.xpath('./td[2]/text()')[0]
                classic= proxy.xpath('./td[4]/text()')[0]
                if ip and port:
                    yield {'ip':ip,'port':port,'classic':classic}
    logging.warning('---------------------------高可用代理运行结束')


@collect_funcs
def crawl_gaonoming():
    """
    高匿名代理：http://www.nimadaili.com/gaoni/6/
    max_page : 20
    """
    url = "http://www.nimadaili.com/gaoni/{}/"
    logging.warning('---------------------------高匿名代理开始运行')
    items = [p for p in range(1, 3)]
    for page in items:
        html = requests(url.format(page))
        if html:
            Html = etree.HTML(html)
            for proxy in Html.xpath('//tbody/tr'):
                i = ''
                ip = re.findall("\d+.\d+.\d+.\d+",proxy.xpath('./td[1]/text()')[0])[0]
                port = re.findall(patten1,proxy.xpath('./td[1]/text()')[0])[0]
                classic= proxy.xpath('./td[2]/text()')[0]
                if classic == 'HTTPS代理':
                    i = 'HTTPS'
                if classic == 'HTTP代理':
                    i = 'HTTP'
                if classic == 'HTTP代理':
                    i = 'HTTP'
                if classic == "HTTP,HTTPS代理":
                    i = ('HTTP', 'HTTPS')
                yield {'ip': ip, 'port': port, 'classic': i}
    logging.warning('---------------------------高匿名代理运行结束')

@collect_funcs
def crawl_nimadaili():
    """
    nima：http://www.nimadaili.com/gaoni/6/
    max_page : 70
    """
    url = "https://www.89ip.cn/index_{}.html"
    logging.warning('---------------------------nima代理开始运行')
    items = [p for p in range(1, 3)]
    for page in items:
        html = requests(url.format(page))
        if html:
            Html = etree.HTML(html)
            for proxy in Html.xpath('//tbody/tr'):
                ip = re.findall("\d+.\d+.\d+.\d+", proxy.xpath('./td[1]/text()')[0])[0]
                port = re.findall('\d+', proxy.xpath('./td[2]/text()')[0])[0]
                classic = ('HTTP','HTTPS')
                if ip and port:
                    yield {'ip': ip,'port': port,'classic': classic}
    logging.warning('--------------------------- nima 代理运行结束')


@collect_funcs
def kaaixing():
    """
    kaixing：http://www.kxdaili.com/dailiip/1/7.html
    """
    url = "http://www.kxdaili.com/dailiip/1/{}.html"
    logging.warning('---------------------------开心代理开始运行')
    items = [p for p in range(1, 3)]
    for page in items:
        html = requests(url.format(page))
        if html:
            Html = etree.HTML(html)
            for proxy in Html.xpath('//tbody/tr'):
                i = ''
                ip = proxy.xpath('./td[1]/text()')[0]
                port = proxy.xpath('./td[2]/text()')[0]
                classic = proxy.xpath('./td[4]/text()')[0]
                if classic == "HTTP,HTTPS":
                    i = ('HTTP', 'HTTPS')
                else:
                    i = classic
                yield {'ip': ip, 'port': port, 'classic': i}
    logging.warning('---------------------------开心代理运行结束')



# 然后实例个对象
crawlers = Crawler()


