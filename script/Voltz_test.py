from time import sleep
from urllib.parse import urlparse
from selenium.webdriver.common.by import By

#https://api.monaconft.io/api/forum/posts?forum_id=2&cursor=1273958
class Auto_script():
    def __init__(self):
        self.plugin_name = 'Voltz测试网'
        self.EXTENSION_ID = 'nkbihfbeogaeaoehlefnkodbefgpgknn'

    def set_environment(self, environment):
        self.environment=environment
        self.environment_data = self.environment.environment_data

    def args_init(self):
        self.follow_users = []

    def run(self,browserId):
        if browserId == None:
            for browserId in self.environment.run_driver_list:
                print(f'浏览器 {browserId} 开始运行 {self.plugin_name}')
                web_driver = self.environment_data[browserId]['webdriver']
                #窗口初始化
                web_driver.driver.switch_to.window(web_driver.driver.window_handles[0])
                web_driver.open_new_window()
                #领取测试币
                #self.get_testcoin(web_driver)
                #切换网络
                web_driver.matemask_allinone()
                #self.change_network(web_driver,'Kovan')
                #兑换测试币
                #self.uniswap(web_driver)
                #开始测试流程
                self.voltz_test(web_driver)

                """
                self.matemask_allinone(web_driver)
                self.change_network(web_driver,'Goerli')
                #self.matemask_allinone(web_driver)
                
                self.changeNetworkByChainList(web_driver, 'Avalanche C-Chain')
                self.open_metamask(web_driver)
                #web_driver.max()
                #web_driver.front_windows()
                sleep(0.5)
                self.set_password(web_driver,'0xPlay666')
                wallet_adders = self.get_wallet_adders(web_driver)
                print(f'{self.environment_data[browserId]["id"]}-{wallet_adders}')
                """
    
    def voltz_test(self,web_driver):
        web_driver.open('https://app.voltz.xyz/#/trader-pools')
        #链接钱包
        web_driver.click((By.XPATH, '//button[text()="Connect Wallet"]'))
        web_driver.click((By.XPATH, '//button/h6[text()="Metamask"]'))
        web_driver.matemask_allinone()
        #
        web_driver.click((By.XPATH, '//button[text()="TRADE"][1]'))
        web_driver.send_key((By.XPATH, '//input[@value="0 USDC"]'),'10000')
        web_driver.send_key((By.XPATH, '//input[@value="0 USDC"]'),'5000')
        web_driver.click((By.XPATH, '//button[text()="Trade Fixed Rate"]'))
        while web_driver.find_elements_xpath('//button[text()="Go to your portfolio"]'):
            web_driver.matemask_allinone()
            sleep(3)
        web_driver.click((By.XPATH, '//button[text()="Go to your portfolio"]'))
        sleep(2)
        web_driver.open('https://app.voltz.xyz/#/lp-pools') 
        web_driver.click((By.XPATH, '//tbody/tr[1]/td[5]/button'))
        #web_driver.click((By.XPATH, ''))  web_driver.send_key((By.XPATH, ''),'')


    def uniswap(self,web_driver):
        web_driver.open('https://app.uniswap.org/#/swap?chain=kovan&lng=zh-CN')
        if web_driver.find_elements_xpath('//button[@id="connect-wallet"]'):
            web_driver.click((By.XPATH, '//button[@id="connect-wallet"]'))
            web_driver.click((By.XPATH, '//button[@id="connect-METAMASK"]'))   
            web_driver.matemask_allinone()
        if not web_driver.find_elements_xpath('//*[@id="swap-currency-output"]'):
            web_driver.open('https://app.uniswap.org/#/swap?chain=kovan&lng=zh-CN')
        web_driver.click((By.XPATH, '//*[@id="swap-currency-output"]/div/div/button'))
        #导入输出代币
        web_driver.send_key((By.XPATH, '//*[@id="token-search-input"]'),'0xe22da380ee6B445bb8273C81944ADEB6E8450422')
        sleep(1)
        if web_driver.wait_element_bool((By.XPATH, '//button[@width="fit-content"]')):
            web_driver.click((By.XPATH, '//button[@width="fit-content"][1]'))
            web_driver.click((By.XPATH, '//button[text()="导入"]')) 
        else:
            web_driver.click((By.XPATH, '//div[@role="dialog"]/div/div[3]/div/div/div/div[1]'))
        sleep(1)
        web_driver.send_key((By.XPATH, '//*[@id="swap-currency-input"]/div/div[1]/input'),'0.5')
        if web_driver.wait_element_bool((By.XPATH, '//button/div[text()="兑换"]')):
            sleep(2)
            web_driver.click((By.XPATH, '//*[@id="swap-button"]'))
            web_driver.click((By.XPATH, '//*[@id="confirm-swap-or-send"]'))
        sleep(1)
        web_driver.matemask_allinone()

        
        
    def get_testcoin(self,web_driver):
        web_driver.open('https://faucet.paradigm.xyz/')
        if web_driver.find_elements_xpath('//button[text()="Sign In with Twitter"]'):
            web_driver.click((By.XPATH, '//button[text()="Sign In with Twitter"]'))
        sleep(2)
        if web_driver.find_elements_xpath('//*[@id="allow"]'):
            web_driver.click((By.XPATH, '//*[@id="allow"]'))
        if not web_driver.find_elements_xpath('//button[text()="Tokens Already Claimed"]'):
            web_driver.send_key((By.XPATH, '//input[@type="text"]'),'wallet_addres')
            web_driver.click((By.XPATH, '//input[@type="checkbox"]'))
            web_driver.click((By.XPATH, '//button[text()="Claim"]'))
        else:
            print('已经领取')
        #web_driver.click((By.XPATH, ''))



def get_plugin_class():
    return Auto_script