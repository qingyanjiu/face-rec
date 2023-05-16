import yaml

class DBConfig:

    def __init__ (self, config_path='db.yaml'):
        self.config_path = config_path

    # 读取配置文件
    def get_conf(self, key):
        f = open(self.config_path)
        config_data = yaml.load(f.read(), Loader=yaml.FullLoader)
        return config_data[key]
    