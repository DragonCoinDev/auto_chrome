import json
import requests
import emoji
from time import sleep
from selenium.webdriver.common.by import By

import re

#https://api.monaconft.io/api/forum/posts?forum_id=2&cursor=1273958
class Auto_script():
    def __init__(self):
        self.plugin_name = '自动发推'
        self.tweet_pool = []
        self.proxies = {
                'http': 'http://127.0.0.1:10809',
                'https': 'http://127.0.0.1:10809',
                }
        self.monaconft_url = "https://api.monaconft.io/api/discover/latest/"
        self.tweet_id = 0
        self.tweet_num = 0
        self.pattern = re.compile(r'<[^>]+>',re.S)
        self.img_path = 'C:\\Users\\moonly\\Desktop\\auto_chrome\\chromedriver\\temp\\'


    def set_environment(self, environment):
        self.environment = environment
        self.img_path = environment.temp_path

    def args_init(self):
        self.follow_users = []

    def run(self,browserId):
        self.get_tweet(1361362)
        if browserId == None:
            for browserId in self.environment.run_driver_list:
                print(f'浏览器 {browserId} 开始运行 {self.plugin_name}')
                web_driver = self.environment.environment_data[browserId]['webdriver']
                web_driver.open_new_window()
                web_driver.max()
                self.post_tweet(web_driver)
    
    def download_img(self,img_url,tw_id):
        #header = {"Authorization": "Bearer " + api_token} # 设置http header，视情况加需要的条目，这里的token是用来鉴权的一种方式
        r = requests.get(img_url, proxies=self.proxies, stream=True)
        img_file_name = self.img_path + str(tw_id) + '.png'
        if r.status_code == 200:
            open(img_file_name, 'wb').write(r.content) # 将内容写入图片
        del r
        return img_file_name

    def get_tweet(self,tw_id=None):
        if tw_id == None:
            res = requests.get(self.monaconft_url,proxies=self.proxies)
            res_json = json.loads(res.text)
        else:
            #print(111)
            url = f'https://api.monaconft.io/api/forum/posts?forum_id=2&cursor={str(tw_id)}'
            #print(url)
            res = requests.get(url,proxies=self.proxies)
            res_json = json.loads(res.text)
        for tw_data in res_json['data']:
            tw_id = tw_data['id']
            self.tweet_id = tw_id
            #print(f'self.tweet_id:{self.tweet_id}')
            content = self.pattern.sub('', tw_data['content'])
            if len(content.encode('utf-8')) > 280 or 'studio.glassnode.com' in content:
                continue
            content = self.remove_emoji(content)
            content = content.replace('&amp;quot;','') 
            img_url = tw_data['pictures']
            self.tweet_num += 1

            if img_url != []:
                img_url = self.download_img(img_url[0],tw_id)
            self.tweet_pool.append({
                'tw_id':tw_id,
                'content':content,
                'img_url':img_url
            })
            print(f'加载第{self.tweet_num}条推特 来源:https://monaconft.io/DIXMIX/premium/post/{tw_id}')


    def post_tweet(self,web_driver):
        try:
            tw_data = self.tweet_pool.pop(0)
            #self.tweet_id = tw_data['tw_id']
        except:
            self.get_tweet(self.tweet_id)
            tw_data = self.tweet_pool.pop(0)
            #self.tweet_id = tw_data['tw_id']
        web_driver.open('https://twitter.com/home')
        try:
            web_driver.element_wait('xpath','//div[@data-testid="tweetButtonInline"]',10)
        except:
            sleep(10)
        web_driver.send_key((By.XPATH, '//div[@aria-label="Tweet text"]'),tw_data['content'])    
        sleep(1)
        if tw_data['img_url'] != []:
            web_driver.send_key((By.XPATH, '//input[@data-testid="fileInput"]'),tw_data['img_url'])
        sleep(1)
        web_driver.click((By.XPATH, '//div[@data-testid="tweetButtonInline"]'))

    def remove_emoji(self,text):
        return emoji.replace_emoji(text, replace='')


def get_plugin_class():
    return Auto_script



if __name__=='__main__':
    rebot = Auto_script()
    rebot.get_tweet(1276269)