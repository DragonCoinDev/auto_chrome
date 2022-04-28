import os
import random
from distutils import dir_util  

class Extension():
    def __init__(self,script_path):
        self.script_path = script_path
        extension_template_path = script_path + 'plugin' + os.sep   #插件模板目录
        self.jxtools_template = extension_template_path + 'jxtools'
        self.metamask_template = extension_template_path  + 'MetaMask'
        self.fingerprint_warehouse = {
            'audio.js' :{
                '[[audio-fingerprint]]' : ['0.0250727152568627','0.0352288154117897','0.0976548800699668','0.132216872708973','0.132704136489287','0.196446723396167','0.266755602912398','0.267153977075198','0.294587372008053','0.326117982774097','0.329584421277784','0.334203004061339','0.396353401428253','0.436948953865538','0.43971052460359','0.4688130544819','0.540927509097814','0.541872744700812','0.601454979554496','0.612180887540887','0.61564598261176','0.62479445926137','0.69568815068141','0.760972232912189','0.790522216721681','0.80803283714132','0.849443129659371','0.851316201431358','0.867772122317819','0.874596239940541','0.899653350421997','0.970504968413387'],
                },
            'bottominfobar.js':{
                '[[bottominfobar]]':''
                },
            'canvas.js':{
                '[[canvas]]': ['106','108','111','113','119','122','127','132','141','174','178','185','194','20','209','211','227','233','234','244','249','251','35','55','57','68','74','79','81','85','88']
                },
            'font.js':{
                '[[font]]' : ['\[10,10,5,7,10,2,5,10,1,8,3,2,9,6,3,3\]','\[10,10,6,8,5,3,3,8,5,4,6,3,8,4,4,3\]','\[10,1,7,1,4,9,2,6,5,5,7,6,8,10,1\]','\[10,4,7,5,2,5,5,5,4,7,10,3,6,3,8,4,2,6,10,9\]','\[10,5,1,3,1,7,6,7,5\]','\[10,7,7,2,8,3,1,9,6,3,4,5,9,10,6,2\]','\[10,8,2,5,10,4,8,9,8,4,8,10,8,10,2,6,1\]','\[10,9,10,8,4,9,8,9,1,3,2\]','\[1,4,5,4,1,8,7,5,1,6\]','\[1,8,5,10,10,5,7,4,2,4,6,6\]','\[2,10,5,4,9,9,3,7,8,2,7,2,5,7,5\]','\[2,7,4,3,4\]','\[2,9,7,3,6,1,9,7,8,9,6,9,10,10\]','\[3,3,2,6,10,8,9,8,6,3,2,3,10,3,4,9,4,7\]','\[3,3,5,4,5\]','\[3,6,3,7,7,4,7,7,7,2,7,4,8,3,9\]','\[3,8,8,5,8,1,1,1,5,1,9\]','\[4,10,9,4,7,1,1,1,2,9\]','\[4,3,3,1,4,8,2,9,2,3,2,7,8,7,10,1,1\]','\[4,4,5,7,10,1,8,2,6,5,4,5,7,4\]','\[4,6,3,8,2\]','\[5,4,8,4,7,10,2,10,1,1,9,8,3,4,1,8,9\]','\[5,8,10,8,5,6,6,2,4,4,3,7\]','\[5,8,2,2,8,7,10,4\]','\[5,9,9,5,4,4,8,7,7,10,6,1,4,7\]','\[7,1,2,6,2,7,4,10,7,3,5\]','\[7,3,7,5,8,3,5,3,5,6\]','\[7,9,1,7,2,10,4,5\]','\[8,1,3,4,3,2,7,5,3\]','\[8,5,3,9,7,3,5,6,1,1,1,1,10,1\]','\[8,5,6,4,3,4,10,9,8,8,6,2,4,1,3,4,8,9,4,3\]','\[9,4,7,2,10,3,4,4,5,7,9,10,7,8,1,2,10\]']
                }
            #'geo_content.js':{
            #    '[[latitude]]': [0],
            #    '[[longitude]]': [0],
            #    }
            }
          
    def add_fingerprint(self,browser_data,type_='init'):
        extension_path = self.script_path + browser_data['user_path'] + os.sep + 'ExtensionPath'  #环境的指纹插件地址
        jx_tools_path = extension_path + os.sep + 'jxtools' 
        if type_ == 'update' and os.path.exists(jx_tools_path):
            dir_util.remove_tree(jx_tools_path)
        self.fingerprint_warehouse['bottominfobar.js']['[[bottominfobar]]'] = [f'[["环境","{browser_data["name"]}"],["账户","{browser_data["account"]["username"]}"],["邮箱","{browser_data["account"]["email"]}"],["代理地址","{browser_data["account"]["proxys"]}"],["钱包地址","{browser_data["account"]["wallet_addres"]}"],["时区","本地时区"]]']
        isExists=os.path.exists(extension_path) #判断目录是否存在
        if not isExists:
            os.mkdir(extension_path)
        dir_util.copy_tree(self.jxtools_template, jx_tools_path) #不存在则拷贝模板文件
        for js_file,fingerprint_data in self.fingerprint_warehouse.items():     #加载指纹数据替换模板内容
            js_file = jx_tools_path + os.sep  + 'contentscripts' + os.sep + js_file
            for old_str,fingerprint_list in fingerprint_data.items():
                fingerprint = str(random.sample(fingerprint_list, 1)[0])
                self.updateFile(js_file, old_str, fingerprint)
        if type_ == 'init':
            metamask_path = extension_path + os.sep + 'metamask'
            dir_util.copy_tree(self.metamask_template,metamask_path)

                


    def updateFile(self,file_path,old_str,new_str):
        with open(file_path, "rt",encoding='utf-8') as file:
            x = file.read()
        with open(file_path, "wt",encoding='utf-8') as file:
            x = x.replace(old_str,new_str)
            file.write(x)
    
    def __del__(self):
        pass
    