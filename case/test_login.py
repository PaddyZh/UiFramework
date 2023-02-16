#coding=utf-8

from time import sleep
from public.common import mytest
from public.pages import loginPage
# from public.common import datainfo


class TestBaiduIndex(mytest.MyTest):
    """登录测试"""

    def _search(self,searchKey):
        """封装登录函数"""
        login = loginPage.LoginPage(self.dr)
        login.into_login_page()
        login.input_count(searchKey)
        login.input_password(searchKey)
        login.click_login_button()
        sleep(2)
        self.assertIn(searchKey, login.return_title())

    def test_search(self):
        """直接搜索"""
        login = loginPage.LoginPage(self.dr)
        login.into_login_page()
        login.input_count("18376611530")
        login.input_password("yan5201314")
        login.click_login_button()
        sleep(2)
        self.assertIn('淘宝网 - 淘！我喜欢',login.return_title())

    # def test_search_excel(self):
    #     """使用数据驱动,进行测试"""
    #     datas = datainfo.get_xls_to_list('searKey.xlsx','Sheet1')
    #     for data in datas:
    #         self._search(data)

