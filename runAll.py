import os
import common.HTMLTestRunner as HTMLTestRunner
import getpathInfo
import unittest
import readConfig as readConfig
from common.configEmail import SendEmail
# import pythoncom
import datetime
import time
import logs.Log

"""
可以说是项目总开关,下面可以配置Email.
"""
rc = readConfig.ReadConfig()
path = getpathInfo.get_Path()
report_path = os.path.join(path, 'report')
on_off = rc.get_email('on_off')
log = logs.Log.logger


class AllTest:  # 定义一个类AllTest
    def __init__(self):  # 初始化一些参数和数据
        global resultPath
        now = time.strftime('%Y-%m-%d_%H_%M_%S')
        resultPath = os.path.join(report_path, now + '.html')
        self.caseListFile = os.path.join(path, "caseList.txt")  # 配置执行哪些测试文件的配置文件路径
        self.caseFile = os.path.join(path, "case")  # 真正的测试断言文件路径
        self.caseList = []
        log.info('resultPath:%s', resultPath)  # 将resultPath的值输入到日志里面，方便定位问题
        log.info('caseListFile:%s', self.caseListFile)  # 同上
        log.info('caseList:%s', self.caseList)  # 同上

    def set_case_list(self):
        """
        读取caselist.txt文件中的用例名称，并添加到caselist元素组
        :return:
        """
        fb = open(self.caseListFile)
        for value in fb.readlines():
            data = str(value)
            if data != '' and not data.startswith("#"):  # 如果data非空且不以#开头
                self.caseList.append(data.replace("\n", ""))  # 读取每行数据会将换行转换为\n，去掉每行数据中的\n
        fb.close()

    def set_case_suite(self):
        """
        :return:
        """
        self.set_case_list()  # 通过set_case_list()拿到caselist元素组
        test_suite = unittest.TestSuite()
        suite_module = []
        for case in self.caseList:  # 从caselist元素组中循环取出case
            case_name = case.split("/")[-1]  # 通过split函数来将aaa/bbb分割字符串，-1取后面，0取前面
            # print(case_name + ".py")  # 打印出取出来的名称
            # 批量加载用例，第一个参数为用例存放路径，第一个参数为路径文件名
            discover = unittest.defaultTestLoader.discover(self.caseFile, pattern=case_name + '.py', top_level_dir=None)
            suite_module.append(discover)  # 将discover存入suite_module元素组
            # print('suite_module:' + str(suite_module))
        if len(suite_module) > 0:  # 判断suite_module元素组是否存在元素
            for suite in suite_module:  # 如果存在，循环取出元素组内容，命名为suite
                for test_name in suite:  # 从discover中取出test_name，使用addTest添加到测试集
                    test_suite.addTest(test_name)
        else:
            print('else:')
            return None
        return test_suite  # 返回测试集

    def run(self):
        """
        run test
        :return:
        """
        try:
            suit = self.set_case_suite()  # 调用set_case_suite获取test_suite
            print('try')
            if suit is not None:  # 判断test_suite是否为空
                fp = open(resultPath, 'wb')  # 打开report.html测试报告文件，如果不存在就创建
                # 调用HTMLTestRunner
                runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='Test Report', description='Test Description')

                run_suit = str(runner.run(suit))
            else:
                print("Have no case to test.")
        except Exception as ex:
            print(str(ex))
            log.info(str(ex))

        finally:
            print("*********TEST END*********")
            log.info("*********TEST END*********")
            fp.close()
            # send_mail.send_email()

        # 发送邮件
        send_mail = SendEmail(
            username='1019356500@qq.com',
            passwd='oszryhkywbolbfdj',
            recv=['1019356500@qq.com'],
            title=str(datetime.date.today()) + rc.get_app('app1') + '应用动化测试',
            content="执行结果：" + "\n" + run_suit[35:67] + "\n" + "附件需下载,然后使用谷歌浏览器打开！",
            file=resultPath,
            # file=r'/Users/icc-hi/PycharmProjects/pythonProject/iCC_interface/interfaceTest/result/report.html',
            ssl=True,
        )
        # 判断邮件发送的开关
        # if on_off == 'on':
        #     send_mail.send_email()
        # else:
        #     print("邮件发送开关配置关闭，请打开开关后可正常自动发送测试报告")


# pythoncom.CoInitialize()
# scheduler = BlockingScheduler()
# scheduler.add_job(AllTest().run, 'cron', day_of_week='1', hour=10, minute=59)
# scheduler.start()

if __name__ == '__main__':
    AllTest().run()
