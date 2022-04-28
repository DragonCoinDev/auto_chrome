# auto_chrome
基于Selenium的多环境管理脚本
可以热插拔插件
## 使用方式
使用前需要创建二个目录**user_data**和**temp**
并且导入环境的文件名目前是写死的为**环境导入.xlsx**
你需要创建并且需要存在以下列
|浏览器ID*|分组*|应用网址*|用户名*|密码*|邮箱地址*|邮箱密码*|手机号码|钱包地址*|钱包密码*|打开页面*|代理类型*|代理地址*|cookie

如下图(标红的为必填项)
![](https://i.bmp.ovh/imgs/2022/04/24/bf6ebac6eb63461a.png)
```bash
pip3 install -r requirements.txt  -i https://pypi.tuna.tsinghua.edu.cn/simple
python3 new_main.py
>>> help
可执行命令：
        help:帮助
        all:所有浏览器全部执行操作，可以运行
        open:打开URL，判断title是否为预期
        execjs:执行js
        sort:对浏览器窗口进行排序，需要管理员权限且coinlist页面登录完成
        create:导入环境,环境配置写入目录下文件‘环境导入.xlsx’
        ls:输出当前环境情况
        start:启动的浏览器环境
        run:执行插件
        exit/quit:关闭所有环境并退出脚本
```
## 目录结构介绍
1.lib

存放各种封装好了的文件

2.plugin

存放浏览器插件模板以及webdriver

3.script

存放插件的地方，脚本会自动读取目录下的py文件作为插件

4.temp

临时目录

5.user_data

存放浏览器用户数据的地方

## 目前可用的插件
| 插件ID |  插件名 | 介绍 |
| :----:| :----: | :---- |
| 1 | Metamask_init | 初始化小狐狸钱包的，环境创建之后用来导入助记词，支撑12和24词 |
| 2 | PostTwitt | 自动发推，推文来源勿问 |
| 3 | TwittSweepstakes | 推特抽奖，支撑指定关注者，喜欢并转发推文，关注tag用户 |
| 4 | wallet_test | 钱包交互测试插件，未完善 |



## 插件模板
```python
class Auto_script():
    def __init__(self):
        self.plugin_name = '自动发推'   #插件名称

    def set_environment(self, environment):
        self.environment=environment    #lib.environment 对象 包含了所有运行环境的数据
        self.environment_data = self.environment.environment_data #存放浏览器数据的地方

    def args_init(self):    #插件进行批量运行前会独立运行，可以传入全局参数，具体用法可以看推特抽奖的插件script/TwittSweepstakes.py
        self.follow_users = []      

    def run(self,browserId):    #框架会调用插件的主运行函数，插件的具体流程写在这里
        #browserId 环境ID
        #web_driver lib.Auto_chrome 对象
        if browserId == None:
            for browserId in self.environment.run_driver_list:
                print(f'浏览器 {browserId} 开始运行 {self.plugin_name}')
                web_driver = self.environment.environment_data[browserId]['webdriver']

def get_plugin_class():  #加载插件必备，不可删除，无需修改
    return Auto_script
```

