import os
from time import sleep
from lib.Environment import *
from selenium.webdriver.common.by import By
from prompt_toolkit import prompt
from prompt_toolkit import PromptSession


class Auto_rebot():
    def __init__(self):
        self.script_path = os.getcwd() + os.sep    #脚本所在目录
        self.environment = Environment(self.script_path)

    def quit(self):
        self.environment.close_all()
    
    def create(self,xlsx_file):
        self.environment.create(xlsx_file)
    
    def start(self,browserId_str):
        self.environment.start(browserId_str)
    
    def taskkill(self): #关闭所有chrome进程，防止存在孤岛进程，会误杀所有chrome进程
        os.system('taskkill /im chromedriver.exe /F')
        os.system('taskkill /im chrome.exe /F')
    
    def ls(self):
        self.environment.list_environment()
        self.environment.list_plugins()
    
    def sort(self):
        self.environment.sort()
    
    def max(self):
        self.environment.max()
    
    def open(self,openurl,new_tab=False):
        self.environment.open(openurl,new_tab)


    def close(self,browserId_str):
        self.environment.close_one(browserId_str)
    
    def run_plugin(self,plugin_id):
        self.environment.run_plugin(plugin_id)
    
    def exec_js(self,js):
        self.environment.exec_js(js)



if __name__=='__main__':
    chrome = Auto_rebot()
    #交互式运行
    session = PromptSession()
    help_dict ={
        "help" : "帮助",
        "all":"所有浏览器全部执行操作，可以运行",
        "open":"打开URL，判断title是否为预期",
        "execjs":"执行js",
        "sort":"对浏览器窗口进行排序，需要管理员权限且coinlist页面登录完成",
        "create":"导入环境,环境配置写入目录下文件‘环境导入.xlsx’",
        "ls":"输出当前环境情况",
        "start":"启动的浏览器环境",
        "run":"执行插件",
        "exit/quit":"关闭所有环境并退出脚本",
    }

    while True:
        cmd = session.prompt(">>> ")
        try:
            if cmd == "help" or cmd == "h":
                    print("可执行命令：")
                    for comm,info in help_dict.items():
                        print(f"\t{comm}:{info}")
            if cmd == 'exit' or cmd == 'quit':
                chrome.quit()
                sleep(2)
                break
            if cmd == "create" :
                chrome.create('./环境导入.xlsx')
            if cmd == "start" :
                print('请输入需要启动的浏览器序号，多个用逗号分隔，或者用- 来批量启动，例如 1,3-6 会启动1,3,4,5,6')
                amount_str = session.prompt("输入浏览器序号: ")
                chrome.start(str(amount_str))
            if cmd == "discord" :
                print('请输入需要启动的浏览器序号，多个用逗号分隔，或者用- 来批量启动，例如 1,3-6 会启动1,3,4,5,6')
                amount_str = session.prompt("输入浏览器序号: ")
                chrome.start(str(amount_str),'https://discord.com/channels/@me')
            if cmd == "close":
                print('请输入需要关闭的浏览器序号，多个用逗号分隔，或者用- 来批量启动，例如 1,3-6 会启动1,3,4,5,6')
                amount_str = session.prompt("输入浏览器序号: ")
                chrome.close(str(amount_str))
            if cmd == "run" :
                chrome.environment.list_plugins()
                print('请输入需要运行的插件ID，所有开启的浏览器都会执行')
                plugin_id = session.prompt("输入插件序号: ")
                chrome.run_plugin(str(plugin_id))
            if cmd == "taskkill":
                print('关闭所有chrome进程，防止存在孤岛进程，会误杀所有chrome进程')
                YN = session.prompt("Yes or No: ")
                if 'Y' in YN or 'y' in YN:
                    chrome.taskkill()
            if cmd == "open":
                openurl = session.prompt("输入请求的url: ")
                YN = session.prompt("是否打开新的标签页Yes or No: ")
                if 'Y' in YN or 'y' in YN:
                    chrome.open(openurl,True)
                else:
                     chrome.open(openurl)
            if cmd == "js":
                js = session.prompt("输入需要执行的js: ")
            if cmd in ['ls','sort','max'] :  #无参数命令 
                getattr(chrome, cmd)()
            if cmd == "test" :
                code = session.prompt("输入code: ")
                code = f'chrome.environment.' + code
                print(exec(code))
        except Exception as e:
            print("error:", e)

