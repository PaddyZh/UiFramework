from base.DemoApp import DemoApp

import readConfig as readConfig
import unittest

rc = readConfig.ReadConfig()


class TestLogin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = DemoApp()
        print('this is setUpClass')

    def setup(self):
        # 每个用例开始之前，启动应用
        print('this is setUp')
        self.app.init_setting()

    # 用例一、登录
    def test_login(self):
        self.app.start()
        print('888')
        self.app.login_to_main(rc.get_user('account'), rc.get_user('password'))

    def teardown(self):
        # 每个用例执行完成后，就默认返回到首页
        # self.app.clear()
        self.app.back(3)

    @classmethod
    def teardown_class(cls):
        # 所有用例都结束后，则关闭应用
        pass