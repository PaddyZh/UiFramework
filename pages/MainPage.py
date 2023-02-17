from base.DemoApp import DemoApp

"""
首页(登录等，可自行添加)
"""


class MainPage(DemoApp):
    # python 类型提示
    def __init__(self, driver):
        # 拿到上个页面的driver
        self.d = driver


