import logging
import time
from IP.settings import USQL
from IP.validator import Validator,Loc_Validator

class Get_IN_sql(Validator):

    def __init__(self,host='127.0.0.1'):
        Validator.__init__(self,queue=[])

    def retur_ip_list(self):
        ip = self.run()
        return (ip)

class Get_IN_Local(Loc_Validator):

    def __init__(self):
        Loc_Validator.__init__(self,queue=[])

    def retur_list_pro(self):
        ip = self.run()
        return (ip)


def ip_pool(host='127.0.0.1'):
    if USQL is True:
        time.sleep(4)
        proxies = Get_IN_sql(host=host)
        IP = proxies.retur_ip_list()
        logging.warning('******************* IP 提取成功！可用 IP {}'.format(str(len(IP))))
        time.sleep(5)
        return IP
    else:
        time.sleep(4)
        proxies = Get_IN_Local()
        IP = proxies.retur_list_pro()
        logging.warning('******************* IP 提取成功！可用 IP {}'.format(str(len(IP))))
        time.sleep(5)
        return IP

if __name__ == '__main__':
    print(ip_pool())



