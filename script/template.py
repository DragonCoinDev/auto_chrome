from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

#https://api.monaconft.io/api/forum/posts?forum_id=2&cursor=1273958
class Auto_script():
    def __init__(self):
        self.plugin_name = '自动发推'

    def set_environment(self, environment):
        self.environment=environment
        

    def args_init(self):
        self.follow_users = []

    def run(self,browserId):
        environment = self.environment
        #self.discord_faucet(environment)
        environment.thread_open('https://app.kyve.network/#/pools/1/delegation')
        environment.keplr_allinone()
        web_driver.change_network("Keplr","Korellia")
        environment.switch_tab_url('https://app.kyve.network')
        

    def discord_faucet(self,environment):
        #environment = self.environment
        environment.thread_open('https://discord.com/channels/817113909957361664/960469010246434828')
        environment.open('https://app.kyve.network/#/faucet',True)
        environment.keplr_allinone()
        environment.get_text((By.XPATH, '//code'))
        for browserId in environment.environment_data.keys():
            if 'tmp_text' in environment.environment_data[browserId]:
                print(f'{browserId},{environment.environment_data[browserId]["tmp_text"]}')
        environment.switch_tab_url('https://discord.com')
        sleep(20)
        sleep(3)
        for browserId in environment.run_driver_list:
            web_driver = environment.environment_data[browserId]['webdriver']
            print(f'{browserId},{environment.environment_data[browserId]["tmp_text"][:-13]}')
            web_driver.AC_send_key(environment.environment_data[browserId]["tmp_text"][:-13])
            #web_driver.change_network("Keplr","Korellia")
            #web_driver.send_key((By.XPATH, '(//div[@aria-haspopup="listbox"])[2]'),Keys.ENTER)


def get_plugin_class():
    return Auto_script