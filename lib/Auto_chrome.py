#import undetected_chromedriver as webdriver
import os
import _thread

from time import sleep
from urllib.parse import urlparse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class Auto_chrome():
    def __init__(self,browser_data,script_path,openurl='startUrl',type_='se'):
        self.browser_data = browser_data
        self.script_path = script_path
        self.webdriver_path = self.script_path + 'plugin' + os.sep + 'chromedriver.exe'
        self.wallet_url = {
            "MetaMask" : 'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html',
            "Keplr" : "chrome-extension://dmkamcknogkgcdfhhbddcghachkejeap/popup.html" 
        }
        print(self.webdriver_path)
        self.user_path = self.script_path + browser_data['user_path']
        self.extension_path = self.script_path + browser_data['user_path'] + os.sep + 'ExtensionPath' + os.sep
        self.proxys = browser_data['account']['proxys']
        self.startUrl = browser_data["startUrl"]
        print(f'\tstart {browser_data["name"]} {self.proxys} {browser_data["user_path"]}')
        if type_ ==  'se':
            import selenium.webdriver as webdriver
            from selenium.webdriver import ChromeOptions
            options = ChromeOptions()
            if self.proxys != None and self.proxys != '':
                options.add_argument(f'--proxy-server={self.proxys}')
            options.add_argument(f"user-data-dir={self.user_path}")
            #options.add_argument('--ignore-certificate-errors') 
            #options.add_argument('--ignore-ssl-errors') 
            options.add_argument('--disable-features=Translate')
            options.add_argument('--force-color-profile=srgb')
            options.add_argument('--metrics-recording-only')
            options.add_argument('--no-first-run')
            options.add_argument('--password-store=basic')
            options.add_argument('--use-mock-keychain')
            options.add_argument('--enable-blink-features=IdleDetection')
            options.add_argument('--export-tagged-pdf')
            options.add_argument('--window-position=0,0')
            options.add_argument('--no-default-browser-check')
            options.add_argument('--start-maximized')
            options.add_argument('--disable-features=FlashDeprecationWarning,EnablePasswordsAccountStorage')
            options.add_argument('--lang=zh-HK')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-setuid-sandbox')
            options.add_argument('--disable-background-mode')
            options.add_argument('--enable-webgl')
            #options.add_extension(self.matemask_path)
            options.add_experimental_option('useAutomationExtension', False)
            #options.add_argument('--log-level=3')
            #options.add_experimental_option('excludeSwitches', [])
            options.add_experimental_option("excludeSwitches", ["enable-automation","enable-logging"])
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument(f"load-extension={self.extension_path + os.sep + 'jxtools'},{self.extension_path + os.sep + 'metamask'}")
            #options.add_argument(f"load-extension={self.extension_path + os.sep + 'metamask'}")
            options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4877.2 Safari/537.36')
            self.driver = webdriver.Chrome(options=options,executable_path=self.webdriver_path)
            def first_open():
                sleep(5)
                self.open_new_window()
                if openurl == "startUrl":
                    #self.driver.get(self.startUrl)
                    self.driver.get('https://www.premint.xyz/pop-allowlist-public-raffle/verify/')
                else:
                    self.driver.get(openurl)
            _thread.start_new_thread(first_open,())
        elif type_ ==  'uc':
            import undetected_chromedriver as webdriver
            self.driver = webdriver.Chrome(suppress_welcome=False,use_subprocess=False,user_data_dir=self.user_path)
        elif type_ == 'create':
            import selenium.webdriver as webdriver
            from selenium.webdriver import ChromeOptions
            options = ChromeOptions()
            options.add_argument('--no-sandbox')
            #options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--ignore-certificate-errors') 
            options.add_argument('--ignore-ssl-errors') 
            options.add_argument('--log-level=3')
            options.add_experimental_option("excludeSwitches", ["enable-automation","enable-logging"])
            options.add_argument(f"user-data-dir={self.user_path}")
            self.driver = webdriver.Chrome(options=options,executable_path=self.webdriver_path)
            self.driver.get(self.startUrl)
            self.driver.quit()

    def max(self):
        self.driver.maximize_window()

    def open(self, url, title='', timeout=10):
        u"""???????????????,??????title???????????????"""
        timeout = int(timeout)
        self.driver.get(url)
        try:
            WebDriverWait(self.driver, timeout, 1).until(EC.title_contains(title))
        except TimeoutException:
            print("open %s title error" % url)
        except Exception as msg:
            print("Error:%s" % msg)

    def find_element(self, locator, timeout=10):
        u"""????????????,??????locator?????????"""
        try:
            element = WebDriverWait(self.driver, timeout, 1).until(EC.presence_of_element_located(locator))
            return element
        except:
            print("%s ????????????????????? %s" % (self, locator))
    
    def wait_element_bool(self, locator, timeout=10):
        u"""????????????,??????locator?????????,??????bool"""
        try:
            element = WebDriverWait(self.driver, timeout, 1).until(EC.presence_of_element_located(locator))
            return True
        except:
            return False
            print("%s ????????????????????? %s" % (self, locator))

    def find_elements(self, locator, timeout=10):
        u"""??????????????????"""
        elements = WebDriverWait(self.driver, timeout, 1).until(EC.presence_of_all_elements_located(locator))
        return elements

    def find_elements_xpath(self, xpath):
        try:
            elements = self.driver.find_element_by_xpath(xpath)
            return True
        except:
            return False

    def element_wait(self, by, value, secs=5):
        """
        ??????????????????
        """
        try:
            if by == "id":
                WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.ID, value)))
            elif by == "name":
                WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.NAME, value)))
            elif by == "class":
                WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.CLASS_NAME, value)))
            elif by == "link_text":
                WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.LINK_TEXT, value)))
            elif by == "xpath":
                WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.XPATH, value)))
            elif by == "css":
                WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, value)))
            else:
                raise NoSuchElementException(
                    "???????????????,????????????????????????")
        except TimeoutException:
            print("?????????????????????????????????")

    def get_element(self, css):
        """
        ????????????????????????,???????????????
        """
        if "=>" not in css:
            by = "css"  # ?????????css????????????#aaa,???????????????????????????????????????=>????????????css???????????????element_wait????????????????????????
            value = css
            # wait element.
            self.element_wait(by, css)
        else:
            by = css.split("=>")[0]
            value = css.split("=>")[1]
            if by == "" or value == "":
                raise NameError(
                    "????????????,??????: 'id=>kw ??? xpath=>//*[@id='kw'].")
            self.element_wait(by, value)

        if by == "id":
            element = self.driver.find_element(By.ID, value)
        elif by == "name":
            element = self.driver.find_element(By.NAME, value)
        elif by == "class":
            element = self.driver.find_element(By.CLASS_NAME, value)
        elif by == "link_text":
            element = self.driver.find_element(By.LINK_TEXT, value)
        elif by == "xpath":
            element = self.driver.find_element(By.XPATH, value)  # ?????????xpath?????????????????????xpath=>//*[@id='su']
        elif by == "css":
            element = self.driver.find_element(By.CSS_SELECTOR, value)
        else:
            raise NameError(
                "Please enter the correct targeting elements,'id','name','class','link_text','xpath','css'.")
        return element

    def get_elements(self, css):
        """
        ????????????????????????,???????????????
        """
        if "=>" not in css:
            by = "css"  # ?????????css????????????#aaa,???????????????????????????????????????=>????????????css???????????????element_wait????????????????????????
            value = css
            # wait element.
            self.element_wait(by, css)
        else:
            by = css.split("=>")[0]
            value = css.split("=>")[1]
            if by == "" or value == "":
                raise NameError(
                    "????????????,??????: 'id=>kw ??? xpath=>//*[@id='kw'].")
            self.element_wait(by, value)

        if by == "id":
            element = self.driver.find_elements(By.ID, value)
        elif by == "name":
            element = self.driver.find_elements(By.NAME, value)
        elif by == "class":
            element = self.driver.find_elements(By.CLASS_NAME, value)
        elif by == "link_text":
            element = self.driver.find_elements(By.LINK_TEXT, value)
        elif by == "xpath":
            element = self.driver.find_elements(By.XPATH, value)  # ?????????xpath?????????????????????xpath=>//*[@id='su']
        elif by == "css":
            element = self.driver.find_elements(By.CSS_SELECTOR, value)
        else:
            raise NameError(
                "Please enter the correct targeting elements,'id','name','class','link_text','xpath','css'.")
        return element

    def click(self, locator):
        u"""??????????????????"""
        element = self.find_element(locator)
        element.click()

    def send_key(self, locator, text):
        u"""???????????????????????????"""
        element = self.find_element(locator)
        element.clear()
        if text  in ['username','password','email','email_passwd','phone','wallet_addres']:
            text = self.browser_data['account'][text]
        element.send_keys(text)
    
    def AC_send_key(self,text):
        actions = ActionChains(self.driver)
        actions.send_keys(text)
        actions.send_keys(Keys.ENTER)
        actions.perform()

    def is_text_in_element(self, text, locator, timeout=10):
        u"""???????????????????????????"""
        try:
            result = WebDriverWait(self.driver, timeout, 1).until(EC.text_to_be_present_in_element(locator, text))
        except TimeoutException:
            print
            u"??????????????????:" + str(locator)
            return False
        else:
            return result

    def is_title(self, title, timeout=10):
        u"""??????title????????????"""
        result = WebDriverWait(self.driver, timeout, 1).until(EC.title_is(title))
        return result

    def is_title_contains(self, title, timeout=10):
        u"""??????????????????title"""
        result = WebDriverWait(self.driver, timeout, 1).until(EC.title_contains(title))
        return result

    def is_select(self, locator, timeout=10):
        u"""???????????????????????????"""
        result = WebDriverWait(self.driver, timeout, 1).until(EC.element_located_to_be_selected(locator))
        return result

    def is_select_be(self, locator, timeout=10, selected=True):
        u"""?????????????????????"""
        return WebDriverWait(self.driver, timeout, 1).until(EC.element_located_selection_state_to_be(locator, selected))

    def is_alert_present(self, timeout=10):
        u"""??????????????????alert?????????,???alert??????alert,???alert??????FALSE"""
        try:
            return WebDriverWait(self.driver, timeout, 1).until(EC.alert_is_present())
        except:
            print
            "No Alert Present"

    def is_visibility(self, locator, timeout=10):
        u"""????????????????????????,??????????????????,???????????????FALSE"""
        return WebDriverWait(self.driver, timeout, 1).until(EC.visibility_of_element_located(locator))

    def is_invisibility(self, locator, timeout=10):
        u"""????????????????????????,?????????,?????????????????????True"""
        return WebDriverWait(self.driver, timeout, 1).until(EC.invisibility_of_element_located(locator))

    def is_clickable(self, locator, timeout=10):
        u"""??????????????????????????????,????????????????????????,??????????????????FALSE"""
        return WebDriverWait(self.driver, timeout, 1).until(EC.element_to_be_clickable(locator))

    def is_located(self, locator, timeout=10):
        u"""?????????????????????????????????????????????????????????,?????????????????????Element,??????????????????FALSE"""
        return WebDriverWait(self.driver, timeout, 1).until(EC.presence_of_element_located(locator))

    def move_is_element(self, locator):
        u"""??????????????????"""
        element = self.find_element(locator)
        ActionChains(self.driver).move_to_element(element).perform()

    def back(self):
        u"""?????????????????????"""
        self.driver.back()

    def forward(self):
        u"""??????????????????"""
        self.driver.forward()

    def close(self):
        u"""????????????"""
        self.driver.close()

    def quit(self):
        u"""??????driver???????????????"""
        self.driver.quit()

    def get_window_rect(self):
        u"""??????driver?????????????????????"""
        return self.driver.get_window_rect()

    def set_window_rect(self,x,y,height,width):
        u"""??????driver?????????????????????"""
        self.driver.set_window_rect(x=x,y=y,height=height,width=width)
    

    def get_title(self):
        u"""?????????????????????title"""
        return self.driver.title

    def get_netloc(self):
        u"""?????????????????????url"""
        #res = urlparse(self.driver.current_url)
        #print(self.driver.current_url)
        return self.driver.current_url

    def is_netloc(self,url: str) -> bool:
        res = urlparse(url)
        if res.netloc == "":
            return True
        return False

    def get_current_url(self):
        u"""??????????????????url"""
        return self.driver.current_url

    def get_text(self, locator):
        u"""??????????????????"""
        return self.find_element(locator).text

    def get_browser_log_level(self):
        u"""?????????????????????????????????"""
        lists = self.driver.get_log('browser')
        list_value = []
        if lists.__len__() != 0:
            for dicts in lists:
                for key, value in dicts.items():
                    list_value.append(value)
        if 'SEVERE' in list_value:
            return "SEVERE"
        elif 'WARNING' in list_value:
            return "WARNING"
        return "SUCCESS"

    def get_attribute(self, locator, name):
        u"""????????????"""
        return self.find_element(locator).get_attribute(name)

    def execjs(self, js):
        u"""??????js"""
        return self.driver.execute_script(js)

    def js_fours_element(self, locator):
        u"""????????????"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        js = "window.scrollBy(0,-300)"
        self.driver.execute_script(js)

    def js_scroll_top(self):
        u"""?????????????????????"""
        js = "window.scrollTo(0,0)"
        self.driver.execute_script(js)

    def js_scroll_end(self):
        u"""?????????????????????"""
        js = "window.scrollTo(0, document.body.scrollHeight)"
        self.driver.execute_script(js)

    def select_by_index(self, locator, index):
        u"""????????????index,0??????,????????????"""
        element = self.find_element(locator)
        Select(element).select_by_index(index)

    def select_by_value(self, locator, value):
        u"""??????value????????????"""
        element = self.find_element(locator)
        Select(element).select_by_value(value)

    def select_by_text(self, locator, text):
        u"""??????text????????????"""
        element = self.find_element(locator)
        Select(element).select_by_visible_text(text)

    def F5(self):
        """
        ??????????????????.
        ??????:
        driver.F5()
        """
        self.driver.refresh()

    def open_new_window(self):
        """
        ?????????????????????????????????????????????,??????????????????????????????
        """
        self.driver.switch_to.new_window('tab')
        original_window = self.driver.current_window_handle
        all_handles = self.driver.window_handles
        for handle in all_handles:
            if handle != original_window:
                self.driver.switch_to.window(handle)
                self.driver.close()
        self.switch_tab_or_window(original_window)
        return original_window

    def get_window_handle(self):
        return self.driver.current_window_handle

    def open_tab(self):
        u"""??????????????????????????????????????????"""
        self.driver.switch_to.new_window('tab')
        #original_window = self.driver.current_window_handle
        #all_handles = self.driver.window_handles

    def open_window(self):
        u"""??????????????????????????????????????????"""
        self.driver.switch_to.new_window('window')

    def switch_tab_or_window(self,original_window:any):
        u"""??????????????????????????????"""
        self.driver.switch_to.window(original_window)

    def front_windows(self):
        u"""?????????????????????"""
        self.driver.switch_to.window(self.driver.current_window_handle)

    def switch_tab_title(self,title):
        u"""???????????????title????????????"""
        all_handles = self.driver.window_handles
        print(f'?????????{len(all_handles)}?????????')
        for handles in all_handles:
            self.driver.switch_to.window(handles)
            print(f'?????????{self.driver.title}')
            #print(self.get_netloc())
            if self.driver.title == title or title in self.driver.title:
                return True
        return False

    def switch_tab_url(self,url):
        u"""???????????????url????????????"""
        all_handles = self.driver.window_handles
        print(f'?????????{len(all_handles)}?????????')
        for handles in all_handles:
            self.driver.switch_to.window(handles)
            print(f'?????????{self.driver.current_url}')
            #print(self.get_netloc())
            if self.driver.current_url == url or url in self.driver.current_url:
                return True
        return False

    def open_wallet(self,wallet_name):
        u"""????????????????????????,????????????????????????,???????????????????????????ID"""
        if wallet_name not in self.wallet_url.keys():
            print(f'???????????????????????????:wallet_url.keys()')
            return False
        original_window = self.get_window_handle()
        if self.switch_tab_title(wallet_name):
            print(1)
            self.open(self.wallet_url[wallet_name])
        else:
            print(2)
            self.open_tab()
            self.open(self.wallet_url[wallet_name])
        return original_window

    def changeNetworkByChainList(self,network_name):
        """
        ??????Chainlist.org??????????????????
        :Args:
            - network_name: string ??????????????????.
        :Usage:
            auto.changeNetworkByChainList('Binance Smart Chain Mainnet')
        """
        self.open('https://chainlist.org/')
        self.js_fours_element((By.XPATH, '//h5[text()="Connect Wallet"]'))   #????????????
        self.click((By.XPATH, '//h5[text()="Connect Wallet"]'))
        self.matemask_allinone()
        # search Network
        self.click((By.XPATH,"//span[text()='Testnets']"))
        sleep(1)
        self.send_key((By.XPATH,'//input[@type="text"]'),network_name)
        sleep(1)
        self.click((By.XPATH, "//span[text()='Add to Metamask']"))
        self.matemask_allinone()
        sleep(3)
        self.open_new_window()

    def change_network(self,wallet_name,network_name):
        if wallet_name not in self.wallet_url.keys():
            print(f'??????????????????????????????wallet_url.keys()')
            return False
        original_window = self.open_wallet(wallet_name)
        if wallet_name == "Metamask":
            self.click((By.XPATH, '//div[@class="app-header__network-component-wrapper"]/div'))
            num = 1
            while True:
                xpath = f'//div[@class="network-dropdown-list"]/li[{num}]'
                #print(xpath)
                if self.find_elements_xpath(xpath):
                    if network_name in self.get_text((By.XPATH, xpath)):
                        self.click((By.XPATH, xpath))
                        break
                else:
                    print('not find')
                    break
                num += 1
        if wallet_name == 'Keplr':
            js = f'document.evaluate(\'//div[text()="{network_name}"]\', document).iterateNext().click();'
            self.execjs(js)


    def open_testnet(self):
        # ??????????????????
        self.open_new_window()
        self.open('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#settings/advanced')
        self.click((By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[1]/div/button[2]/div'))
        self.js_fours_element((By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div[2]/div[7]/div[2]/div/div/div[1]'))
        self.click((By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div[2]/div[7]/div[2]/div/div/div[1]'))
        self.open(f'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')

    def set_password(self,wallet_name,password):
        if wallet_name not in self.wallet_url.keys():
            print(f'???????????????????????????:wallet_url.keys()')
            return False
        if wallet_name == 'MetaMask':
            if self.wait_element_bool((By.XPATH, '//*[@id="password"]')):
                self.send_key((By.XPATH, '//*[@id="password"]'),password)
                self.click((By.XPATH, '//button[@variant="contained"]'))    #??????????????????
            self.open(self.wallet_url[wallet_name])
        if wallet_name == 'Keplr':
            if self.wait_element_bool((By.XPATH, '//input[@name="password"]')):
                self.send_key((By.XPATH, '//input[@name="password"]'),password)
                self.click((By.XPATH, '//button[@type="submit"]'))    #??????????????????
                sleep(2)
            self.open(self.wallet_url[wallet_name])

    def keplr_allinone(self):
        original_window = self.open_wallet('Keplr')
        while True:
            self.F5()
            sleep(1)
            url = urlparse(self.get_netloc())
            print(url)
            if '/unlock' in url.fragment:
                print('run unlock')
                self.set_password('Keplr','0xPlay666')
                #sleep(3)
            if url.fragment == '/' or url.scheme != 'chrome-extension':
                print('succ')
                self.switch_tab_or_window(original_window)
                break

    def matemask_allinone(self):
        original_window = self.open_wallet('MetaMask')
        while True:
            self.F5()
            sleep(1)
            url = urlparse(self.get_netloc())
            if url.fragment == 'unlock':
                print('run unlock')
                self.set_password('MetaMask','0xPlay666')
            if url.fragment == 'confirmation':
                print('run confirmation')
                self.click((By.XPATH, '//button[@class="button btn--rounded btn-primary"]'))
            if 'connect' in url.fragment and 'confirm-permissions' in url.fragment:
                self.click((By.XPATH, '//button[@class="button btn--rounded btn-primary"]'))
            elif 'connect' in url.fragment:
                self.click((By.XPATH, '//button[@data-testid="page-container-footer-next"]'))
            if url.fragment == '' or url.scheme != 'chrome-extension':
                print('succ')
                self.switch_tab_or_window(original_window)
                break