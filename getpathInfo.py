import os

'''
获取项目绝对路径
'''
def get_Path():
    path = os.path.split(os.path.realpath(__file__))[0]
    return path


