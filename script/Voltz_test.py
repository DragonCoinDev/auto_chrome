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
                self.matemask_allinone(web_driver)
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
        self.matemask_allinone(web_driver)
        #
        web_driver.click((By.XPATH, '//button[text()="TRADE"][1]'))
        web_driver.send_key((By.XPATH, '//input[@value="0 USDC"]'),'10000')
        web_driver.send_key((By.XPATH, '//input[@value="0 USDC"]'),'5000')
        web_driver.click((By.XPATH, '//button[text()="Trade Fixed Rate"]'))
        while web_driver.find_elements_xpath('//button[text()="Go to your portfolio"]'):
            self.matemask_allinone(web_driver)
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
            self.matemask_allinone(web_driver)
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
        self.matemask_allinone(web_driver)

        
        



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



    def open_metamask(self,web_driver):
        original_window = web_driver.get_window_handle()
        print(f'当前窗口{original_window}')
        if web_driver.switch_tab('MetaMask'):
            url = urlparse(web_driver.get_netloc())
            if url.path != '/home.html':  
                web_driver.close()
                web_driver.driver.switch_to.window(web_driver.driver.window_handles[0])
                self.open_metamask(web_driver)
            else:
                web_driver.F5()
        else:
            web_driver.open_tab()
            web_driver.open(f'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
            #web_driver.switch_tab('MetaMask')
        return original_window

    
    def set_password(self,web_driver,password):
        if web_driver.wait_element_bool((By.XPATH, '//*[@id="password"]')):
            web_driver.send_key((By.XPATH, '//*[@id="password"]'),password)
            web_driver.click((By.XPATH, '//button[@variant="contained"]'))    #点击解锁按钮
        else:
            web_driver.open(f'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
    
    def get_wallet_adders(self,web_driver):
        self.open_metamask(web_driver)
        web_driver.click((By.XPATH, '//button[@data-testid="account-options-menu-button"]')) #点击账户选项
        sleep(0.5)
        web_driver.click((By.XPATH, '//button[@data-testid="account-options-menu__account-details"]'))
        sleep(0.5)
        wallet_adders = web_driver.get_text((By.XPATH, '//div[@class="qr-code__address"]'))  #点击复制剪切板
        web_driver.click((By.XPATH, '//button[@class="account-modal__close"]'))
        print(wallet_adders)
        return wallet_adders
        


    def changeNetworkByChainList(self,web_driver,network_name):
            """
            通过Chainlist.org切换指定网络

            :Args:
                - network_name: string 完整的网络名.

            :Usage:
                auto.changeNetworkByChainList('Binance Smart Chain Mainnet')
            """
            web_driver.open('https://chainlist.org/')
            web_driver.js_fours_element((By.XPATH, '//h5[text()="Connect Wallet"]'))
            web_driver.click((By.XPATH, '//h5[text()="Connect Wallet"]'))
            original_window = self.open_metamask(web_driver)
            web_driver.execjs("window.scrollBy(0, document.body.scrollHeight)")
            #sleep(1)
            print(web_driver.wait_element_bool((By.XPATH, '//div[@class="selected-account__name"]')))
            if not web_driver.wait_element_bool((By.XPATH, '//div[@class="selected-account__name"]')):
                #web_driver.click((By.XPATH, '//button[text()="下一步"]'))
                web_driver.click((By.XPATH, '//button[@class="button btn--rounded btn-primary"]'))
                #web_driver.click((By.XPATH, '//button[text()="连接"]'))
                web_driver.click((By.XPATH, '//button[@data-testid="page-container-footer-next"]'))
            web_driver.close()
            web_driver.switch_tab_or_window(original_window)
            # search Network
            web_driver.click((By.XPATH,"//span[text()='Testnets']"))
            sleep(1)
            web_driver.send_key((By.XPATH,'//input[@type="text"]'),network_name)
            sleep(1)
            web_driver.click((By.XPATH, "//span[text()='Add to Metamask']"))
            self.open_metamask(web_driver,'/home.html')
            web_driver.click((By.XPATH, "//button[text()='批准']"))
            web_driver.click((By.XPATH, "//button[text()='切换网络']"))
            sleep(3)
            web_driver.open_new_window()
    
    def change_network(self,web_driver,network_name):
        original_window = self.open_metamask(web_driver)
        sleep(1)
        web_driver.click((By.XPATH, '//div[@class="app-header__network-component-wrapper"]/div'))
        num = 1
        while True:
            xpath = f'//div[@class="network-dropdown-list"]/li[{num}]'
            #print(xpath)
            if web_driver.find_elements_xpath(xpath):
                if network_name in web_driver.get_text((By.XPATH, xpath)):
                    web_driver.click((By.XPATH, xpath))
                    break
            else:
                print('not find')
                break
            num += 1

    def open_testnet(self,web_driver):
        # 打开网络下拉框
        web_driver.open_new_window()
        web_driver.open('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#settings')
        web_driver.click((By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[1]/div/button[2]/div'))
        web_driver.js_fours_element((By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div[2]/div[7]/div[2]/div/div/div[1]'))
        web_driver.click((By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div[2]/div[7]/div[2]/div/div/div[1]'))
        web_driver.open(f'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
        
        


    def matemask_allinone(self,web_driver):
        original_window = self.open_metamask(web_driver)
        
        while True:
            web_driver.F5()
            sleep(1)
            url = urlparse(web_driver.get_netloc())
            print(url)
            sleep(2)
            if url.fragment == 'unlock':
                print('run unlock')
                self.set_password(web_driver,'0xPlay666')
            if url.fragment == 'confirmation':
                print('run confirmation')
                web_driver.click((By.XPATH, '//button[@class="button btn--rounded btn-primary"]'))
            if 'connect' in url.fragment and 'confirm-permissions' in url.fragment:
                web_driver.click((By.XPATH, '//button[@data-testid="page-container-footer-next"]'))
            elif 'connect' in url.fragment:
                web_driver.click((By.XPATH, '//button[@class="button btn--rounded btn-primary"]'))
            if url.fragment == '/swap':
                web_driver.click((By.XPATH, '//button[@class="button btn--rounded btn-primary"]'))
                confirm-transaction
            if 'confirm-transaction' in url.fragment:
                sleep(2)
                web_driver.click((By.XPATH, '//button[@data-testid="page-container-footer-next"]'))
                web_driver.open(f'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
            if url.fragment == '':
                web_driver.switch_tab_or_window(original_window)
                break
            



    

def get_plugin_class():
    return Auto_script