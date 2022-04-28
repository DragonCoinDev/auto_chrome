from time import sleep
from selenium.webdriver.common.by import By

class Auto_script():
    def __init__(self):
        self.plugin_name = 'Metamask钱包初始化'
        self.mnemonic = []

    def set_environment(self, environment):
        self.environment=environment

    def args_init(self):
        self.password = []
        print('初始化参数')
        self.password =  input("请输入需要钱包的密码:")

    def run(self,browserId):
        if browserId == None:
            for browserId in self.environment.run_driver_list:
                print(f'浏览器 {browserId} 开始运行 {self.plugin_name}')
                web_driver = self.environment.environment_data[browserId]['webdriver']
                self.open_welcome(web_driver)
                web_driver.max()
                web_driver.front_windows()
                mnemonic = self.get_mnemonic()
                try:
                    web_driver.click((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/button'))
                except:
                    print(f'浏览器 {browserId} 运行失败')
                    break
                web_driver.click((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div[2]/div/div[2]/div[1]/button'))
                web_driver.click((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[5]/div[1]/footer/button[2]'))
                if len(mnemonic) == 24:
                    web_driver.select_by_value((By.XPATH,'//*[@id="app-content"]/div/div[2]/div/div/div[2]/form/div[1]/div[2]/select'),'24')
                    for word_num in range(0,24):
                        #print(f'//*[@id="import-srp__srp-word-{word_num}"')
                        web_driver.send_key((By.XPATH, f'//*[@id="import-srp__srp-word-{word_num}"]'),mnemonic[word_num])
                else:
                    for word_num in range(0,12):
                        web_driver.send_key((By.XPATH, f'//*[@id="import-srp__srp-word-{word_num}"]'),mnemonic[word_num])
                web_driver.send_key((By.XPATH, '//*[@id="password"]'),self.password)
                web_driver.send_key((By.XPATH, '//*[@id="confirm-password"]'),self.password)
                web_driver.click((By.XPATH, '//*[@id="create-new-vault__terms-checkbox"]'))
                web_driver.click((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div[2]/form/button'))
                web_driver.click((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/button'))
                if web_driver.wait_element_bool((By.XPATH, '//button[@data-testid="popover-close"]')):     #处理钱包初始化的问题
                    web_driver.click((By.XPATH, '//button[@data-testid="popover-close"]'))
                if web_driver.wait_element_bool((By.XPATH, '//button[text()="明白了"]')):
                    web_driver.click((By.XPATH, '//button[text()="明白了"]'))
                web_driver.F5()

    def open_welcome(self,web_driver):
        if web_driver.switch_tab('MetaMask'):
            pass
        else:
            web_driver.open('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#initialize/welcome')
            web_driver.switch_tab('MetaMask')
    
    def get_mnemonic(self):
        while True:
            try:
                mnemonic = self.mnemonic.pop(0)
            except:
                mnemonic = input("请输入助记词:")
            mnemonic = mnemonic.split(' ')
            if len(mnemonic) == 12 or len(mnemonic) == 24:
                print(mnemonic)
                return mnemonic
            print('助记词输入错误，请重新输入')
        
            


def get_plugin_class():
    return Auto_script