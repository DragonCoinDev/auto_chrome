import os 
import math
import _thread
import importlib
from time import sleep
from lib.Auto_chrome import Auto_chrome
from lib.Yamlrw import Yamlrw
from lib.Xlsxdata import Xlsxdata
from prettytable import PrettyTable
from lib.Fingerprint import Extension
from distutils import dir_util  
from selenium.webdriver.common.by import By



class Environment():
    def __init__(self,script_path,type_='se'):
        self.script_path = script_path
        self.data_path = script_path  + 'user_data' + os.sep #浏览器用户数据目录
        self.plugins_path = script_path  + 'script' + os.sep #自动化脚本目录
        self.temp_path = script_path + 'temp' + os.sep #临时文件存放目录
        self.conf_rw = Yamlrw()  #用于读取环境配置文件
        self.xlsxread = Xlsxdata(self.data_path)    #用于导入环境
        self.type_ = type_      #浏览器运行类型 se = selenium us = undetected_chromedriver  create = 创建环境

        self.run_driver_list = []   #记录当前运行的web_driver
        self.environment_data = {} #用于存放所有环境的数据
        self.load_environment() #执行一次加载
        self.load_plugins()


    #创建浏览器环境 前缀  数量
    def create(self,filename):
        extension = Extension(self.script_path)     #用于给插件添加部分指纹信息
        environment_data = self.xlsxread.read(filename)     #读取用户表格
        for browser_name,browser_data in environment_data.items():
            path = self.script_path + os.sep +  browser_data['user_path']    
            isExists=os.path.exists(path)       #判断是否已经创建
            if not isExists:
                try:
                    os.makedirs(path) 
                    extension.add_fingerprint(browser_data)     #复制指纹插件
                    Auto_chrome(browser_data,self.script_path,'create')
                    self.conf_rw.write(path, browser_data)
                    print(f'{browser_name}创建成功,用户目录{path}')
                except:
                    isExists=os.path.exists(path)
                    if  isExists:
                        dir_util.remove_tree(path)
            else:       #如果目录已经存在,则只更新配置文件
                os.remove(path + os.sep + 'conf.yaml')
                self.conf_rw.write(path, browser_data)
                extension.add_fingerprint(browser_data,'update')
                print(f'{browser_name}环境目录已存在,跳过')
        self.load_environment()
        extension.__del__()
        return True

    def load_environment(self): #加载本地环境
        self.environment_paths = os.listdir(self.data_path)
        for path in self.environment_paths:
            try:
                environment_path = self.data_path + os.sep + path
                environment_data = self.conf_rw.read(environment_path)
            except:
                break
            browserId = environment_data['browserId']
            self.environment_data[browserId] = self.conf_rw.read(environment_path)
            if browserId not in self.run_driver_list:
                self.environment_data[browserId]['status'] = False
            else:
                self.environment_data[browserId]['status'] = True
        print(f'加载本地环境 {len(self.environment_data.keys())}')

    def load_plugins(self):
        self.plugins_data = {}  #存放插件信息
        plugins_id = 1
        for filename in os.listdir(self.plugins_path):
            if not filename.endswith(".py") or filename.startswith("_"):
                continue
            self.plugins_data[plugins_id] = {
                'name' : filename.split('.')[0],
                'info' : '',
                'path' : self.plugins_path + os.sep + filename,
                } 
            plugins_id += 1
        print(f'加载本地插件 {len(self.plugins_data.keys())}')

    def list_environment(self):     #打印当前环境的数据
        if self.environment_paths == {}:
            self.load_environment()
        environment_table = PrettyTable(['浏览器ID','分组','环境名称','站点','账号','代理','启动状态'])
        environment_table.sortby = "浏览器ID"
        for browserId,environment_data in self.environment_data.items():
            environment_table.add_row([
                environment_data['browserId'],
                environment_data['group'],
                environment_data['name'],
                environment_data['account']['siteUrl'],
                environment_data['account']['username'],
                environment_data['account']['proxys'],
                environment_data['status']
                ])
        print(environment_table)
    
    def list_plugins(self):
        if self.plugins_data == {}:
            self.load_plugins()
        plugins_table = PrettyTable(['插件ID','插件名','介绍','插件文件路径'])
        plugins_table.sortby = "插件ID"
        for plugin_id,plugin in self.plugins_data.items():
            plugins_table.add_row([
                plugin_id,
                plugin['name'],
                plugin['info'],
                plugin['path']
            ])
        print(plugins_table)

    def run_plugin(self,plugin_id,browserId=None):
        plugin_name = self.plugins_data[int(plugin_id)]['name']
        print(f'开始初始化插件{plugin_name}')
        plugin = __import__("script."+plugin_name, fromlist=[plugin_name])
        importlib.reload(plugin)
        clazz=plugin.get_plugin_class()
        Auto_script=clazz()
        Auto_script.set_environment(self)
        Auto_script.args_init()
        Auto_script.run(browserId)



    def start(self,browserId_str,openurl='startUrl'):      #启动的浏览器序号,多个用逗号分隔,或者用- 来批量启动,例如 1,3-6 会启动1,3,4,5,6'
        def _start(browserId):
            print(f'开始启动环境 {browserId}')
            #print(self.environment_data)
            browser_data = self.environment_data[browserId]
            proxys = browser_data['account']['proxys']
            self.environment_data[browserId]['webdriver'] = Auto_chrome(browser_data,self.script_path,openurl,self.type_)
            self.environment_data[browserId]['status'] = True 
            self.run_driver_list.append(browserId)
            sleep(2)
        for tmp_browserId in browserId_str.split(','):
            if '-' in tmp_browserId:
                for browserId in range(int(tmp_browserId.split('-')[0]),int(tmp_browserId.split('-')[1])+1):
                    _start(int(browserId))
            else:
                _start(int(tmp_browserId))

    def sort(self): #对浏览器窗口进行排序
        if len(self.run_driver_list) <=5:
            line_num = 1
            column_num = len(self.run_driver_list)
        else:
            for line_num in range(2,10):
                clone = len(self.run_driver_list) / line_num 
                column_num = math.ceil(clone)
                if clone <= 10:
                    break
        self.environment_data[self.run_driver_list[0]]['webdriver'].max()   #最大化一个窗口获取浏览器大小
        windwos_rect = self.environment_data[self.run_driver_list[0]]['webdriver'].get_window_rect()
        height = windwos_rect['height'] / line_num
        width = windwos_rect['width'] / column_num
        x = windwos_rect['x']
        y = windwos_rect['y']
        num = 1 
        for browserId in self.run_driver_list:
            #self.environment_data[browserId]['webdriver'].max()
            self.environment_data[browserId]['webdriver'].set_window_rect(x,y,height,width)
            print(self.environment_data[browserId]['webdriver'].get_window_rect())
            x += width
            num += 1    #本行的浏览器个数
            if num > column_num:
                y += height
                x = windwos_rect['x']
                num = 1

    def max(self): #最大化所有浏览器窗口
        for browserId in self.run_driver_list:
            self.environment_data[browserId]['webdriver'].max() 

    def open(self,url,new_tab=False,timeout=10):    #打开URL
        u"""打开浏览器,判断title是否为预期"""
        for browserId in self.run_driver_list:
            web_driver = self.environment_data[browserId]['webdriver']
            if new_tab:
               web_driver.open_tab()
            web_driver.open(url,'',timeout)
    
    def thread_open(self,url):
        for browserId in self.run_driver_list:
            web_driver = self.environment_data[browserId]['webdriver']
            _thread.start_new_thread(web_driver.open,(url,))




    def find_element(self, locator, timeout=10):
        u"""定位元素,参数locator为元素"""
        for browserId in self.run_driver_list:
            web_driver = self.environment_data[browserId]['webdriver']
            web_driver.find_element(locator,timeout)

    def wait_element_bool(self, locator, timeout=10):
        u"""定位元素,参数locator为原则,返回bool"""
        for browserId in self.run_driver_list:
            web_driver = self.environment_data[browserId]['webdriver']
            web_driver.wait_element_bool(locator, timeout)

    def click(self,locator):    #点击元素
        for browserId in self.run_driver_list:
            web_driver = self.environment_data[browserId]['webdriver']
            web_driver.click(locator)

    def send_key(self, locator, text):  #往元素填充字符
        for browserId in self.run_driver_list:
            web_driver = self.environment_data[browserId]['webdriver']
            if text  in ['username','password','email','email_passwd','phone','wallet_addres']:
                text = self.environment_data[browserId]['account'][text]
            #print(f'send key {text}')
            if locator == "":
                web_driver.AC_send_key(text)
            else:
                web_driver.send_key(locator, text)
    
    def select_by_value(self, locator, value):  #通过value定位元素
        for browserId in self.run_driver_list:
            web_driver = self.environment_data[browserId]['webdriver']
            web_driver.select_by_value(locator, value)

    def switch_tab_title(self,title):   #切换到指定title的标签页
        for browserId in self.run_driver_list:
            web_driver = self.environment_data[browserId]['webdriver']
            web_driver.switch_tab_title(title)
    
    def switch_tab_url(self,url):   #切换到指定url的标签页
        for browserId in self.run_driver_list:
            web_driver = self.environment_data[browserId]['webdriver']
            web_driver.switch_tab_url(url)
    
    def get_text(self, locator):
        u"""获取文本内容"""
        for browserId in self.run_driver_list:
            web_driver = self.environment_data[browserId]['webdriver']
            self.environment_data[browserId]['tmp_text'] = web_driver.get_text(locator)
            print(self.environment_data[browserId]['tmp_text'])

    def exec_js(self,js):
        for browserId in self.run_driver_list:
            web_driver = self.environment_data[browserId]['webdriver']
            web_driver.execjs(js)

    def open_window(self):
        u"""打开一个新窗口并切换到新窗口"""
        for browserId in self.run_driver_list:
            web_driver = self.environment_data[browserId]['webdriver']
            web_driver.open_window()
    
    def open_wallet(self,wallet_name):
        u"""切换到钱包标签页,如果不存在则创建,并返回旧标签页对象ID"""
        for browserId in self.run_driver_list:
            web_driver = self.environment_data[browserId]['webdriver']
            self.environment_data[browserId]['original_window'] = web_driver.open_wallet(wallet_name)

    def keplr_allinone(self):
        for browserId in self.run_driver_list:
            print(f'start {browserId}')
            web_driver = self.environment_data[browserId]['webdriver']
            web_driver.keplr_allinone()
    
    def matemask_allinone(self):
        for browserId in self.run_driver_list:
            web_driver = self.environment_data[browserId]['webdriver']
            web_driver.matemask_allinone()


    def close_one(self,browserId_str):
        def _close(browserId):
            if browserId in self.run_driver_list:
                self.environment_data[browserId]['webdriver'].quit()
                self.run_driver_list.remove(browserId)
                self.environment_data[browserId]['status'] = 'False'
            else: 
                print(f'环境{browserId} 不在运行')
        for tmp_browserId in browserId_str.split(','):
            if '-' in tmp_browserId:
                for browserId in range(int(tmp_browserId.split('-')[0]),int(tmp_browserId.split('-')[1])+1):
                    _close(int(browserId))
            else:
               _close(int(tmp_browserId))




    def close_all(self):
        for browserId in self.run_driver_list:
            #_thread.start_new_thread(self.environment_data[browserId]['webdriver'].close,())
            _thread.start_new_thread(self.environment_data[browserId]['webdriver'].quit,())
