 ## 文件说明
    crawl2.py ：收集函数
    get_in.py ： 代理提取
    localinstore.py ： 代理以csv 文档处理
    mysql_pool.py ： 代理数据库处理
    reqajax.py  ： 构造异步请求
    Schedure_.py ： 调度器 可以按时间间隔运行
    settings.py ： 配置文件
    validator.py ： 验证文件

## 使用 

    1、配置文件有一个参数 ： USQL 如果是用 数据库 设为Ture,修改配置文件，自动建表，
    2、不然会在目录下建立一个proxies文件夹，产生procies1.txt 用于保存代理
    3、获取 以及验证都实现了，具体使用可以按照自己的逻辑，默认提取代理直接运行get_in.py 的ip_poool函数
       自动完成代理验证、提取。
    4、具体使用可以修改逻辑
