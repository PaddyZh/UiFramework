"""
    具体APP相关的操作
"""
from time import sleep

from base.BasePage import BasePage


class DemoApp(BasePage):
    def start(self):
        """
            启动App
        """
        if self.driver == None:
            self.driver.app_start('具体APP')
        return self.driver

    def restart(self):
        """
            重启App
        """
        pass

    def clear(self):
        """
            清除app缓存
        """
        self.driver.app_clear('具体APP')

    def stop(self):
        """
            关闭App
        """
        self.driver.app_stop('具体APP')


if __name__ == '__main__':
    DemoApp().clear()
