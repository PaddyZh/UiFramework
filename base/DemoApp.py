import os

from base.BasePage import BasePage

"""
具体APP相关的操作
"""


class DemoApp(BasePage):

    def init_setting(self):
        os.system('python -m uiautomator2 init')

    def start(self):
        """
            启动App
        """
        self.d.app_start('com.kugou.android')
        skip = self.d(description='跳过')
        if self.judge_existed('跳过'):
            skip.click()

    def login_to_main(self, account, password):
        """
        登录按钮
        """
        # 手机号登录
        self.click_element('com.kugou.android:id/n91')
        # 切换到密码登录
        self.click_element('//*[@resource-id="com.kugou.android:id/a42"]/android.widget.RelativeLayout[2]')
        self.click_element('//*[@text="请输入手机号"]')
        self.d.send_keys(account)
        self.click_element('//*[@text="请输入密码"]')
        self.d.send_keys(password)
        # 勾选隐私
        self.click_element('com.kugou.android:id/ace')
        # 登录按钮
        self.click_element('com.kugou.android:id/af4')

    def restart(self):
        """
            重启App
        """
        pass

    def clear_app(self):
        """
        清除app缓存
        """
        self.d.app_clear('com.kugou.android')

    def stop(self):

        """
        关闭App
        """
        self.d.app_stop('com.kugou.android')


if __name__ == '__main__':
    DemoApp().start()
