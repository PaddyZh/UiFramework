"""
    首页
"""

from base.DemoApp import DemoApp


class MainPage(DemoApp):
    # python 类型提示
    def __init__(self, driver):
        # 拿到上个页面的driver
        self.d = driver

    def click_login(self):
        """
            点击会员登录按钮
        """
