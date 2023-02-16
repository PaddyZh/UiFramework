import os
import configparser
import getpathInfo as getpathInfo #引入我们自己写的获取路径的类

'''
读取配置文件的方法，并返回文件中内容
'''

#调用实例化，之前路径返回：E:\pycharm\interfaceTest
path = getpathInfo.get_Path()
#这句话是在path路径下，再加一级E:\pycharm\interfaceTest\config.ini
config_path = os.path.join(path,'config\config.ini')
#调用外部的读取配置文件的方法
config = configparser.ConfigParser()
config.read(config_path,encoding='utf-8')

class ReadConfig():

    def get_http(self,name):
        value = config.get('HTTP',name)
        return value
    def get_email(self,name):
        value = config.get('EMAIL', name)
        return value
    def get_user(self,name):
        value = config.get('USER', name)
        return value

    def get_browser(self,name):
        value = config.get('BROWSER', name)
        return value

    #写好，留着以后备用，暂时没有操作数据库
    def get_mysql(self,name):
        value = config.get('DATABASE', name)
        return value


if __name__ == '__main__':
    print(ReadConfig().get_browser("browser"))