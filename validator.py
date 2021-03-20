import asyncio
import re
import logging
import aiohttp
from IP.settings import REQUEST_TIMEOUT
from IP.mysql_pool import Mysql
from IP.localinstore import PUDX,readout

# 验证url
VALIDATOR_BASE_URL = "http://baidu.com"

# 批量测试数量
VALIDATOR_BATCH_COUNT = 20
# proxy : {'ip':ip,'port':port,'classic':classic}
# 代理统计,失败量，成功量，总量，可用率
info = [0,0,0,0.00]

class Loc_Validator(PUDX):

    def __init__(self,queue=None,): # None or  list
        self.queue = queue

    async def testprox(self, proxy,oldpro):
        global info
        info[2] +=1
        if self.queue is None:
            async with aiohttp.ClientSession() as session:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode("utf8")
                try:
                    async with session.get(
                            VALIDATOR_BASE_URL, proxy=proxy, timeout=REQUEST_TIMEOUT
                    ) as resp:
                        print(resp.status)
                        if resp.status == 200:
                            info[1] += 1
                            self.upgreads(oldpro)
                        else:
                            info[0] += 1
                            self.dowgreads(oldpro)
                except Exception as e:
                     info[0] += 1
                     self.dowgreads(oldpro)
        else:
            async with aiohttp.ClientSession() as session:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode("utf8")
                try:
                    async with session.get(
                            VALIDATOR_BASE_URL, proxy=proxy, timeout=REQUEST_TIMEOUT
                    ) as resp:
                        print(resp.status)
                        if resp.status == 200:
                            info[1] += 1
                            self.upgreads(oldpro)
                            self.queue.append(proxy)
                        else:
                            info[0] += 1
                            self.dowgreads(oldpro)
                except Exception as e:
                     info[0] += 1
                     self.dowgreads(oldpro)

    def run(self,):
        if self.queue == None:
            proxies = readout()
            count = 0
            proxie_list = []
            for proxie in proxies:
                count +=1
                proxie_ = 'http://'+proxie[0].split(',')[-1]
                pro = [proxie_,proxie[2]]
                proxie_list.append(pro)
            print(proxie_list)
            loop = asyncio.get_event_loop()
            for i in range(0, count, VALIDATOR_BATCH_COUNT):
                _proxies =proxie_list[i: i + VALIDATOR_BATCH_COUNT]
                tasks = [self.testprox(proxy[0],proxy[1]) for proxy in _proxies]
                if tasks:
                    loop.run_until_complete(asyncio.wait(tasks))
        else:
            proxies = readout()
            count = 0
            proxie_list = []
            for proxie in proxies:
                count += 1
                proxie_ = 'http://' + proxie[0].split(',')[-1]
                pro = [proxie_, proxie[2]]
                proxie_list.append(pro)
            print(proxie_list)
            loop = asyncio.get_event_loop()
            for i in range(0, count, VALIDATOR_BATCH_COUNT):
                _proxies = proxie_list[i: i + VALIDATOR_BATCH_COUNT]
                tasks = [self.testprox(proxy[0], proxy[1]) for proxy in _proxies]
                if tasks:
                    loop.run_until_complete(asyncio.wait(tasks))
                return (self.queue)

localVirti = Loc_Validator()


# 本地验证
# if __name__ == '__main__':
#     lo = Loc_Validator()
#     pros = lo.run()
#     print(pros)


class Validator(Mysql):

    def __init__(self,queue=None,):
        Mysql.__init__(self,)
        self.queue = queue

    # mysql 验证方式
    async def test_proxy(self, proxy):
        """
        测试代理
        :param proxy: 指定代理
        """
        if self.queue == None:
            async with aiohttp.ClientSession() as session:
                try:
                    if isinstance(proxy, bytes):
                        proxy = proxy.decode("utf8")
                    async with session.get(
                        VALIDATOR_BASE_URL, proxy=proxy, timeout=REQUEST_TIMEOUT
                    ) as resp:
                        if resp.status == 200:
                            self.increase_proxy_score(proxy)
                        else:
                            self.reduce_proxy_score(proxy)
                except:
                    self.reduce_proxy_score(proxy)
        else:
            async with aiohttp.ClientSession() as session:
                try:
                    if isinstance(proxy, bytes):
                        proxy = proxy.decode("utf8")
                    async with session.get(
                            VALIDATOR_BASE_URL, proxy=proxy, timeout=REQUEST_TIMEOUT
                    ) as resp:
                        if resp.status == 200:
                            self.increase_proxy_score(proxy)
                            self.queue.append(proxy)
                        else:
                            self.reduce_proxy_score(proxy)
                except:
                    self.reduce_proxy_score(proxy)
    def run(self,):
        """
        启动校验器
        """
        if self.queue == None:
            self.clear_proxies(4)
            proxies = self.all_proxies()
            count = 0
            proxie_list = []
            for proxie in proxies:
                count +=1
                proxie_list.append(proxie)
            loop = asyncio.get_event_loop()
            for i in range(0, count, VALIDATOR_BATCH_COUNT):
                _proxies =proxie_list[i: i + VALIDATOR_BATCH_COUNT]
                tasks = [self.test_proxy(proxy) for proxy in _proxies]
                if tasks:
                    loop.run_until_complete(asyncio.wait(tasks))
            self.clear_proxies(4)
        else:
            self.clear_proxies(4)
            proxies = self.all_proxies()
            count = 0
            proxie_list = []
            for proxie in proxies:
                count += 1
                proxie_list.append(proxie)
            loop = asyncio.get_event_loop()
            for i in range(0, count, VALIDATOR_BATCH_COUNT):
                _proxies = proxie_list[i: i + VALIDATOR_BATCH_COUNT]
                tasks = [self.test_proxy(proxy) for proxy in _proxies]
                if tasks:
                    loop.run_until_complete(asyncio.wait(tasks))
            self.clear_proxies(4)
            return (self.queue)

validator = Validator()

# # 数据库验证
# if __name__ == '__main__':
#     ver = Validator()
#     ver.run()

