import schedule
from IP.validator import validator,localVirti
from IP.mysql_pool import Mysql
from IP.crawl2 import crawlers
msql = Mysql()

# 爬取ip检查时间（分）
CRAWLER_RUN_CYCLE = 60

# 验证ip检查时间（分）
VALIDATOR_RUN_CYCLE = 20

def run_schedule():
    """
    启动客户端
    """
    #启动收集器
    schedule.every(CRAWLER_RUN_CYCLE).minutes.do(crawlers.run).run()

    # 启动验证器 ---- 数据库
    # schedule.every(VALIDATOR_RUN_CYCLE).minutes.do(validator.run).run()
    # msql.clear_proxies(4)

    # 启动验证器，本地文件操作
    schedule.every(VALIDATOR_RUN_CYCLE).minutes.do(localVirti.run).run()
    while True:
        try:
            schedule.run_pending()
        except KeyboardInterrupt:
            return 0

run_schedule()



