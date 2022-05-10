

#https://api.monaconft.io/api/forum/posts?forum_id=2&cursor=1273958
class Auto_script():
    def __init__(self):
        self.plugin_name = '自动发推'

    def set_environment(self, environment):
        self.environment=environment

    def args_init(self):
        self.follow_users = []

    def run(self,browserId):
        if browserId == None:
            for browserId in self.environment.run_driver_list:
                print(f'浏览器 {browserId} 开始运行 {self.plugin_name}')
                web_driver = self.environment.environment_data[browserId]['webdriver']
                web_driver.switch_tab('111')
                #web_driver.driver.switch_to.window(web_driver.driver.window_handles[0])
                #web_driver.open_tab()


def get_plugin_class():
    return Auto_script