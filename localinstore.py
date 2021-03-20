# --coding:GBK --
import os
from IP.settings import *


singl_prox = True

def rename(p1,p2):
    os.remove(p1)
    os.renames(p2,p1)

def readout():
    # return  list  -1 表示文件名，用于更新......
    s = set()
    #'68.183.221.156,43934,5'
    with open(p1,'r') as f:
        data = f.read().strip().split('\n')
        for i in data:
            if i.strip() is not '':
                s.add(i.strip())
    li = list()
    for i in s:
        ip = i.split(',')[0]
        greads = i.split(',')[1]
        li.append([ip,greads,i])
    return li


class PUDX:
    """
    文档更新策略：自动过滤

    代理每次分数变化自动调用clear ,清除不可用代理
    """
    def upgreads(self,pros):
        data = pros.strip().split(',')
        print(data)
        pro1 = eval(data[1])
        pro0 = data[0]
        if  pro1 < MAX_SCORE:
            pro1 = pro1 + 1
            nws = '%s,%s' % (pro0, pro1)
            print(nws)
            self.alter(pros, nws)
        else:
            nws = '%s,%s' % (pro0, MAX_SCORE)
            self.alter(pros, nws)
        print(pros)

    def dowgreads(self,pros):
        data = pros.strip().split(',')
        print(data)
        pro1 = eval(data[1])
        pro0 = data[0]
        pro1 = pro1 - 1
        if pro1 == CLI_SCORE:
            nws = '%s,%s' % (pro0, pro1)
            print(nws)
            self.alter(pros, CLI_SCORE)
        else:
            nws = '%s,%s' % (pro0, pro1)
            self.alter(pros, nws)
        print(pros)

    # 更换 字符替换
    def alter(self, old_str, new_str):
        li = set()
        with open(p1, "r", encoding="utf-8") as f1:
            for lin in f1.read().split('\n'):
                try:
                    grs = lin.strip().split(',')[1]
                    if old_str in lin.strip() and int(new_str.split(',')[-1]) > CLI_SCORE :
                        li.add(new_str)
                        continue
                    if old_str not in lin.strip() and int(grs) > CLI_SCORE:
                        li.add(lin.strip())
                        continue
                    else:
                        pass
                except:
                    pass
        with open(p2, "a+", encoding="utf-8") as f2:
            for i in list(li):
                f2.write(str(i)+'\n')
            f2.close()
        rename(p1,p2)
