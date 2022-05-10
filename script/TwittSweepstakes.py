import random
from time import sleep
from urllib.parse import urlparse
from selenium.webdriver.common.by import By



class Auto_script():
    def __init__(self):
        self.plugin_name = '推特抽奖'
        self.taguser_list = ['yxcv2gP1Kon7akY','Kimberl48446119','0xPalladium','tw70742277','MeltdownNFT','Kristen86044195','RobinMearite3','0x3bAlan','AlexHirsh18','LaserCatNft','trait_sniper','0xKiraa','BitCloutCat','LaserCatNft','PandaDAO_Office','0xPalladium','killergfnft','yxcv2gP1Kon7akY','Summerli520','topgun886','PS320417826','Blackkimki','PlayAscenders','PandaDAO_Office','yxcv2gP1Kon7akY','Rothandchild','LaserCatNft','trait_sniper','0xKiraa','BitCloutCat','LaserCatNft','bigbong80705902','Johnny20010208','tatolsnft','hfhelan','laofeiyyds','Bitcoin_daheng','hcx2997','hbz7353','hfhelan','1ys70BjNnUQj1FT','hanfeng415','laofeiyyds','Bitcoin_daheng','hbz7353','hcx2997','zhaomao152','lubenwe32646589','qisheng21709030','Hamilto19970','ChangyinN2','trait_sniper','0xKiraa','XfhfhV','pyg97dfbrd','DdwfgDsvdd','Arthurac14','Kevinli69096682','Josefa85402540','Bbxu16','Hyundai_NFT','Mengyuan911','h','','jinxiaoming5','Bbxu16','tigerbobNFT','harmvddorpel','1QkEKZ37tS4g5SR','wenkai49905563','noraning666','chen_abcd','skix18','PiroPito','min88815','kasteve1009','min88815','ofo19149882','Indexgamehk','trait_sniper','FhdddbnBfdds121','philoseok','erververververw','Peileizi1','alphafrenz','trait_sniper','FhdddbnBfdds121','philoseok','erververververw','Peileizi1','NFT_Pioneers','trait_sniper','FhdddbnBfdds121','philoseok','erververververw','Peileizi1','EricNelson','trait_sniper','FhdddbnBfdds121','philoseok','erververververw','Peileizi1','Blockchainleeyo','trait_sniper','FhdddbnBfdds121','philoseok','erververververw','Peileizi1','nekomuraclub','trait_sniper','0xKiraa','FhdddbnBfdds121','philoseok','erververververw','Peileizi1','joinsui','trait_sniper','0xKiraa','FhdddbnBfdds121','philoseok','erververververw','Peileizi1','handsoff_studio','trait_sniper','0xKiraa','XfhfhV','pyg97dfbrd','DdwfgDsvdd','FhdddbnBfdds121','philoseok','Peileizi1','KingdomNFT','trait_sniper','0xKiraa','FhdddbnBfdds121','philoseok','erververververw','Peileizi1','Unipioneer','EmoHeadsNFT','FhdddbnBfdds121','philoseok','erververververw','Peileizi1','guilang8','trait_sniper','0xKiraa','FhdddbnBfdds121','philoseok','erververververw','LauraQu91877082','0xPalladium','AmandaJ16190747','0xPalladium','Kimberl48446119','0xPalladium','Christi16128857','0xPalladium','PS_onlyL','kpopvoteina','PandaDAO_Office','0xPalladium','killergfnft']      #可以用来at的用户名列表

    def set_environment(self, environment):
        self.environment=environment
    
    def args_init(self):
        self.follow_users = [
           'avycnft',
            'memeland',
            '9gagceo',
            'keung',
            'memeland',
            'takoa',
            'TakoaGiving',
            'OnChainMonkey',
            'memeland',
            'CyberKongmunity',
            'memeland',
            '9gagceo',
            'keung',
            'CyberKongz',
            'memeland',
            '9gagceo',
            'sneakyninjaNFTs',
            'Yogapetz',
            'keung',
            '0xElectricSheep',
            'UltiverseDAO',
            'McLarenAuto',
            'BitCloutCat',
            'LaserCatNft',
            '0xElectricsheep',
            'GodJiraslove',
            'PGodjira',
        ]
        #self.follow_users = []
        self.tw_link = ''
        self.tw_links = [
            'https://twitter.com/avycnft/status/1523708085021581315',
            'https://twitter.com/takoa/status/1523890580891316226',
            'https://twitter.com/cubexnft/status/1523726345104019456',
            'https://twitter.com/OnChainMonkey/status/1523686883494006785',
            'https://twitter.com/CyberKongmunity/status/1523982187196035077',
            'https://twitter.com/SneakyninjaNFTs/status/1522979144874688515',
            'https://twitter.com/Yogapetz/status/1523029923669045248',
            'https://twitter.com/0xElectricsheep/status/1524022318892466182',
            'https://twitter.com/BitCloutCat/status/1523989331865907200',
            'https://twitter.com/GodJiraslove/status/1523903223643664384',
        ]
        self.tag_user_num = 3
        """
        print('请输入需要关注的用户,英文逗号分隔')
        follow_user =  input("需要关注的用户:")
        for user in follow_user.split(','):
            self.follow_users.append(user)
        print('请输入需要转发的推特链接,不输入则只进行关注操作')
        self.tw_link =  input("推特链接:")
        print('请输入需要@的人数')
        self.tag_user_num = input("@的人数:")
        print('确认参数如下：')
        print(f'\t关注用户 : {self.follow_users}')
        print(f'\t转发推特链接 : {self.tw_link}')
        print(f'\t@人数 : {self.tag_user_num}')
        """

    def run(self,browserId):
        if browserId == None:
            for browserId in self.environment.run_driver_list:
                print(f'浏览器 {browserId} 开始运行 {self.plugin_name}')
                web_driver = self.environment.environment_data[browserId]['webdriver']
                windwos_rect = web_driver.get_window_rect()
                username = self.environment.environment_data[browserId]["account"]["username"]
                web_driver.open_new_window()
                web_driver.max()
                self.follow(web_driver)
                #self.follow(web_driver,self.taguser_list)
                if self.tw_link != '':
                    sleep(2)
                    text = self.get_taguser(web_driver)
                    self.re_tweet(web_driver, username,text)
                    #self.set_reply(web_driver,'wallet_addres')
                if self.tw_links != []:
                    text = self.get_taguser(web_driver)
                    for tw_link in set(self.tw_links):
                        self.tw_link = tw_link
                        self.re_tweet(web_driver, username,text)
                    self.tw_link = ''
                #web_driver.click((By.XPATH, '//div[@aria-label="Like"]'))
                web_driver.set_window_rect(windwos_rect['x'],windwos_rect['y'],windwos_rect['height'],windwos_rect['width'] )


    def follow(self,web_driver,user_list=None):
        if user_list == None:
            user_list = set(self.follow_users)
        for user in user_list:
            url = f'https://twitter.com/{user}'
            web_driver.open(url)
            sleep(3)
            if web_driver.wait_element_bool((By.XPATH, f'//div[@aria-label="Follow @{user}"]'),5):
                #document.evaluate('//div[@aria-label="Follow @projectPXN"]', document).iterateNext().click();
                web_driver.execjs(f'document.evaluate(\'//div[@aria-label="Follow @{user}"]\', document).iterateNext().click();')
                sleep(1)
            else:
                print(f'{user}已经关注')


    def like_tweet(self,web_driver):
        if web_driver.wait_element_bool((By.XPATH, '//div[@aria-label="Share Tweet"]'),5):    #利用转发按钮定位元素滑动窗口
            web_driver.js_fours_element((By.XPATH, '//div[@aria-label="Share Tweet"]'))
        if web_driver.wait_element_bool((By.XPATH, '//div[@aria-label="Like"]'),5):
            web_driver.click((By.XPATH, '//div[@aria-label="Like"]'))

    def get_taguser(self,web_driver):
        taguser = random.sample(self.taguser_list, self.tag_user_num) 
        self.follow(web_driver,taguser)
        tw_text = ''
        for user in taguser:
            tw_text += '@' + user + '%20'
        return tw_text


    def re_tweet(self,web_driver,username,text):
        """
        https://twitter.com/intent/tweet?text=Another great article by @BByrne_SF! Check it out.&hashtags=Communi3&in_reply_to=1520903185157734401
        https://twitter.com/intent/tweet?text=I'm claiming my free tokens for the @KYVENetwork Korellia testnet
        """
        web_driver.open(self.tw_link)
        print(f'start {self.tw_link}')
        sleep(3)
        tw_id = urlparse(self.tw_link).path.split('/')[-1] 
        sleep(2)
        if web_driver.wait_element_bool((By.XPATH, '//div[@data-testid="unlike"]'),2):
            print('已经转发')
            return True
        print(f'开始喜欢转发tag')
        self.like_tweet(web_driver)
        sleep(2)
        #转发推特
        web_driver.click((By.XPATH, '//div[@aria-label="Retweet"]'))
        sleep(1)
        web_driver.click((By.XPATH, '//div[@data-testid="retweetConfirm"]'))
        #tag 用户
        #web_driver.send_key((By.XPATH, '//div[@aria-label="Tweet text"]'), text)
        sleep(2)
        url = f'https://twitter.com/intent/tweet?text={text}&in_reply_to={tw_id}'
        web_driver.open(url)
        if web_driver.wait_element_bool((By.XPATH, '//div[@data-testid="tweetButton"]')):
            #web_driver.click((By.XPATH, '//*[@id="layers"]/div[3]/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div/div'))
            web_driver.click((By.XPATH, '//div[@data-testid="tweetButton"]'))
        sleep(2)
        url = f'https://twitter.com/{username}/with_replies'
        web_driver.open(url)

    def set_reply(self,web_driver,text):
        self.like_tweet(web_driver)
        if web_driver.wait_element_bool((By.XPATH, '//div[@aria-label="Share Tweet"]'),5):    #利用转发按钮定位元素滑动窗口
            web_driver.js_fours_element((By.XPATH, '//div[@aria-label="Share Tweet"]'))
        #web_driver.click((By.XPATH, '//div[@aria-label="reply"]'))
        web_driver.send_key((By.XPATH, '//div[@aria-label="Tweet text"]'), text)
        sleep(1)
        web_driver.click((By.XPATH, '//div[@data-testid="tweetButtonInline"]'))



def get_plugin_class():
    return Auto_script