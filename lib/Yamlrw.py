import os
import yaml

class Yamlrw():
    def __init__(self):
        self.conffile_name = 'conf.yaml'

    def read(self,path):
        yaml_file = path + os.sep + self.conffile_name
        file = open(yaml_file, 'r', encoding="utf-8")
        file_data = file.read()
        yaml_data = yaml.safe_load(file_data)
        file.close()
        return yaml_data

    def write(self,path,dict_data):
        yaml_file = path + os.sep + self.conffile_name
        file = open(yaml_file, 'w', encoding='utf-8')
        yaml.dump(dict_data, file)
        file.close()
