import os
import configparser
import getpathInfo as getpathInfo  # 引入我们自己写的获取路径的类

'''
读取配置文件的方法，并返回文件中内容
'''

# 调用实例化，之前路径返回：E:\pycharm\interfaceTest
path = getpathInfo.get_Path()
# 这句话是在path路径下，再加一级E:\pycharm\interfaceTest\config.ini
config_path = os.path.join(path, 'config.ini')
# 调用外部的读取配置文件的方法
config = configparser.ConfigParser()
config.read(config_path, encoding='utf-8')


class ReadConfig():

    def get_email(self, name):
        value = config.get('EMAIL', name)
        return value

    def get_user(self, name):
        value = config.get('USER', name)
        return value

    def get_app(self, name):
        value = config.get('APP', name)
        return value

    def get_devices(self, name):
        value = config.get('DEVICES', name)
        return value


if __name__ == '__main__':
    print(ReadConfig().get_devices('device1'))
