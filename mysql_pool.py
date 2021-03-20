import pymysql
import re
import random
from IP.settings import INIT_SCORE
from IP.settings import sqlconf,patten



class Mysql:
    # 初始化 mysql 数据库
    def __init__(self, host='127.0.0.1'):
        self.connect = pymysql.connect(
            host=sqlconf['host'],
            port=3306,
            db=sqlconf['db'],
            user=sqlconf['user'],
            passwd=sqlconf['passwd'],
            charset=sqlconf['charset'],
            use_unicode=sqlconf['use_unicode']
        )
        # 通过cursor执行增删查
        self.cursor = self.connect.cursor()
        self.connect.autocommit(True)
        self.cursor.execute('show tables')
        if ('proxies',) in self.cursor.fetchall():
            pass
        else:
            sql = r"CREATE TABLE proxies(IP CHAR(15) NOT NULL,PORT CHAR(7) NOT NULL," \
                  r"CLASSIC CHAR(15) NOT NULL,GREADS CHAR(3) NOT NULL);"
            self.cursor.execute(sql)

    def add_proxy(self, proxies, INIT_SCORE):
        print(proxies)
        if type(proxies['classic']) is tuple:
            sql = "insert into proxies" + " values('%s','%s','%s','%s')"\
                   %(proxies['ip'],proxies['port'],proxies['classic'][0],INIT_SCORE)
            sql2 = "insert into proxies" + " values('%s','%s','%s','%s')" \
                  % (proxies['ip'], proxies['port'], proxies['classic'][1], INIT_SCORE)
            try:
                self.cursor.execute(sql)
                self.cursor.execute(sql2)
            except Exception as e:
                print(e)
                return e
        else:
            sql = "insert into proxies" + " values('%s','%s','%s','%s')" \
                   % (proxies['ip'], proxies['port'], proxies['classic'], INIT_SCORE)
            try:
                self.cursor.execute(sql)
            except Exception as e:
                print(e)
                return e


    def reduce_proxy_score(self, proxy):

        try:
            ip = re.findall(patten,proxy)[0]
            sql = 'update proxies set GREADS=GREADS-1 where IP="{}" && GREADS>=0'.format(ip)
            self.cursor.execute(sql)
        except Exception as e:
            print(e)

    def increase_proxy_score(self, proxy):

        try:
            ip = re.findall(patten, proxy)[0]
            sql = 'update proxies set GREADS=GREADS+1 where IP="{}" && GREADS<=10'.format(ip)
            self.cursor.execute(sql)
        except Exception as e:
            print(e)
    def order_(self):
        """
        返回全部代理，
        排序，降序展示出来
        """
        try:
            sql = "SELECT IP,`PORT` FROM proxies ORDER BY GREADS*-1 "
            self.cursor.execute(sql)
            proxies = self.cursor.fetchall()
            for proxe in proxies:
                yield proxe
            print('获取代理成功')
        except:
            print(Exception)

    def pop_proxy(self):

        try:
            id = random.choice([i for i in range(7,10)])
            sql = "SELECT IP,`PORT`,CLASSIC FROM proxies ORDER BY GREADS*-1 LIMIT 1"
            self.cursor.execute(sql)
            proxie = self.cursor.fetchone()
            proxie = '{}://{}:{}'.format(list(proxie)[2],list(proxie)[0], list(proxie)[1])
            print('获取成功 ：{} '.format(proxie))
            return proxie
        except Exception as e:
            print(e)


    def get_proxies(self, count=1):

        try:
            sql = "SELECT IP,`PORT` FROM proxies ORDER BY GREADS*-1 LIMIT {}".format(count)
            self.cursor.execute(sql)
            proxie = self.cursor.fetchall()
            for proxie in proxie:
                proxie = '{}://{}:{}'.format(list(proxie)[2],list(proxie)[0],list(proxie)[1])
                print('获取成功 ： '.format(proxie))
                return proxie
        except Exception as e:
            print(e)

    def count_all_proxies(self):

        sql = "select * from proxies"
        count = self.cursor.execute(sql)
        return count


    def count_score_proxies(self, score):

        try:
            pro_ = []
            sql = "SELECT IP,`PORT`,GREADS FROM proxies where GREADS='{}'".format(score)
            self.cursor.execute(sql)
            proxie = self.cursor.fetchall()
            for proxie in proxie:
                proxie = 'http://{}:{}'.format(list(proxie)[0],list(proxie)[1])
                pro_.append(pro_)
            print('获取成功 ： '.format(proxie))
            return pro_

        except:
            print(Exception)

    def clear_proxies(self, score):
        sql = "DELETE FROM proxies WHERE GREADS<='{}'".format(score)
        self.cursor.execute(sql)
        return 0

    def all_proxies(self):
        pro_ = []
        sql = "select IP,PORT,ClASSIC from proxies where GREADS>=5"
        self.cursor.execute(sql)
        proxies = set(self.cursor.fetchall())
        for proxy in list(proxies):
            ip = 'http://'+proxy[0]+':'+list(proxy)[1]
            yield ip