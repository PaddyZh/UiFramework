import os
import re
from time import sleep
import random
import urllib3
import uiautomator2 as u2
import readConfig as readConfig
from typing import Union

'''
封装基本操作
'''

readConfig = readConfig.ReadConfig()
urllib3.disable_warnings()


class BasePage:  # 构造函数

    def __init__(self):
        self.d = u2.connect(readConfig.get_devices('device1'))

    # 返回
    def back(self, num):
        for i in range(num):
            self.d.send_keys('back')

    # 点击
    def click_element(self, element, sleepTime=0):
        if str(element).startswith("com"):  # 若开头是com则使用ID定位
            self.d(resourceId=element).click()  # 点击定位元素
        elif re.findall("//", str(element)):  # 若//开头则使用正则表达式匹配后用xpath定位
            self.d.xpath(element).click()  # 点击定位元素
        else:  # 若以上两种情况都不是，则使用描述定位
            self.d(description=element).click()  # 点击定位元素
        sleep(sleepTime)

    # 点击直到元素消失
    def click_until_gone(self, element, kind):
        if kind == "id":
            self.d(resourceId=element).click_gone()
        elif kind == "class":
            self.d(className=element).click_gone()
        elif kind == "text":
            self.d(text=element).click_gone()
        else:  # 若以上两种情况都不是，则使用描述定位
            self.d(description=element).click_gone()  # 点击定位元素

    # 组合定位classname和text
    def click_by_classname_text(self, element1, element2):
        self.d(className=element1, text=element2).click()

    # 组合定位classname和description
    def click_by_classname_description(self, element1, element2):
        self.d(className=element1, description=element2).click()

    # 组合定位text和description
    def click_by_text_description(self, element1, element2):
        self.d(text=element1, description=element2).click()

    # 根据id点击(包括非com开头的id点击定位元素)
    def click_by_id(self, element, sleepTime=0):
        self.d(resourceId=element).click()
        sleep(sleepTime)

    # 根据文本点击
    def click_by_text(self, element, sleepTime=0):
        self.d(text=element).click()  # 点击定位元素
        sleep(sleepTime)

    # 根据百分比坐标点击
    def click_by_zuobiao(self, x, y, sleepTime=0):
        size = self.d.window_size()
        self.d.click(int(size[0] * x), int(size[1] * y))
        sleep(sleepTime)

    # 根据坐标点击元素
    def click_coord(self, x, y):
        self.d.click(x, y)

    # 根据坐标双击元素
    def double_click_by_zuobiao(self, x, y, sleepTime=0):
        size = self.d.window_size()
        self.d.double_click(int(size[0] * x), int(size[1] * y))
        sleep(sleepTime)

    # 超时时间设置点击，根据文本定位，针对点击屏幕元素反应慢的元素
    def click_by_text_time_out(self, element, timeout=30, sleepTime=0):
        self.d(text=element).click(timeout=timeout)
        sleep(sleepTime)

    # 长按
    def long_click_extend(self, element, dur=1, sleepTime=0):
        zhmodel = re.compile(u'[\u4e00-\u9fa5]')
        if str(element).startswith("com"):  # 若开头是com则使用ID定位
            self.d(resourceId=element).long_click(dur)  # 点击定位元素
        elif re.findall("//", str(element)):  # 若//开头则使用正则表达式匹配后用xpath定位
            self.d.xpath(element).long_click()  # 点击定位元素
        elif zhmodel.search(str(element)):
            self.d(description=element).long_click(dur)
        else:
            self.d(className=element).long_click(dur)
        sleep(sleepTime)

    # 通过文本长击
    def long_click_by_text(self, element, dur=0.5, sleepTime=0):
        self.d(text=element).long_click(dur)
        sleep(sleepTime)

    #  通过坐标长击
    def long_click_by_zuobiao(self, x, y, sleepTime=0, duration: float = 1):
        self.d.long_click(x, y, duration)
        sleep(sleepTime)

    # 清空输入框中的内容
    def clear(self, element):
        if str(element).startswith("com"):  # 若开头是com则使用ID定位
            self.d(resourceId=element).clear_text()  # 清除文本
        elif re.findall("//", str(element)):  # 若//开头则使用正则表达式匹配后用xpath定位
            self.d.xpath(element).clear_text()  # 清除文本
        else:  # 若以上两种情况都不是，则使用描述定位
            self.d(description=element).clear_text()  # 清除文本

    # 输入
    def input(self, element, value, sleepTime=0):
        if str(element).startswith("com"):  # 若开头是com则使用ID定位
            self.d(resourceId=element).set_text(value)  # send_keys
        elif re.findall("//", str(element)):  # 若//开头则使用正则表达式匹配后用xpath定位
            self.d.xpath(element).set_text(value)
        else:  # 若以上两种情况都不是，则使用描述定位
            self.d(description=element).set_text(value)
        sleep(sleepTime)

    # 不存在搜索按钮的搜索
    def input_by_send_keys(self, element, value):
        self.d.set_fastinput_ime(True)  # 切换成FastInputIME输入法
        if str(element).startswith("com"):  # 若开头是com则使用ID定位
            self.d(resourceId=element).send_keys(value)  # send_keys
        elif re.findall("//", str(element)):  # 若//开头则使用正则表达式匹配后用xpath定位
            self.d.xpath(element).send_text(value)
        else:  # 若以上两种情况都不是，则使用描述定位
            self.d(description=element).send_keys(value)
        self.d.set_fastinput_ime(False)  # 切换成正常的输入法
        self.d.send_action("search")  # 模拟输入法的搜索

    # 查找元素
    def find_elements(self, element, timeout=5):  # 找元素
        is_exited = False
        try:
            while timeout > 0:
                xml = self.d.dump_hierarchy()  # 获取网页层次结构
                if re.findall(element, xml):
                    is_exited = True
                    break
                else:
                    timeout -= 1
        except:
            print("元素未找到!")
        finally:
            return is_exited

    # 断言元素是否存在, 不能判定xpath元素
    def assert_existed(self, element):  #
        # assert self.find_elements(element) == True, "断言失败，{}元素不存在!".format(element)
        return self.find_elements(element) == True

    # 判断元素是否存在，如随机弹窗等
    def judge_existed(self, element, type: str = "text", timeout=2):
        if re.findall("//", str(element)):  # 若//开头则使用正则表达式匹配后用xpath定位
            return self.d.xpath(element).exists == True
        elif type == "text":
            return self.d(text=element).exists(timeout=timeout) == True
        elif type == "dec":
            return self.d(description=element).exists(timeout=timeout) == True
        else:
            pass

    def clear_input_x_by_resourceId(self, location, value, x):
        """
            清空已填写的选项，重新传值
            :param location: 元素定位字符串
            :param value： 重新传的值
            :param x ：索引
        """
        self.d(resourceId=location)[x].click()  # 定位到元素
        self.d(focused=True).clear_text()
        self.d.send_keys(value)

    def clear_input_by_resourceId(self, location, value):
        """
            清空已填写的选项，重新传值
            :param location: 元素定位字符串
            :param value： 重新传的值
        """
        self.d(resourceId=location).click()  # 定位到元素
        self.d(focused=True).clear_text()
        self.d.send_keys(value)
        return self

    def close_popup(self, text, locationType, location):
        """
            关闭弹窗
            :param text：字符串，弹窗包含的text文本
            :param locationType：定位方式 xpath or resourceId
            :param location：定位元素字符串，例："//*[@text='登录']"
        """
        element = self.d(text=text)
        while True:
            if element:
                element.click()
                continue
            else:
                print("权限校验弹窗不存在")
                break
        if locationType == "xpath":
            self.d.xpath(location).click()
        elif locationType == "resourceId":
            self.d(resourceId=location).click()

    def swipe_until_element_found(self, param, wait_after_found=0.0, **kwargs):
        """
        检查元素是否存在，若不存在则进行上滑，滑动后再次检查，直到滑动到页面底部
        若找到元素则返回，否则滑动到页面底部后，仍未找到元素，则抛出异常，提示找不到元素
        :param param: xpath字符串 或 元素对象
        :param wait_after_found: 找到元素后，原地等待时间
        :param kwargs:
        :return:
        """
        element = self.d.xpath(param) if isinstance(param, str) else param
        param = param if isinstance(param, str) else param.selector
        while True:
            try:
                assert element.exists
                if wait_after_found:
                    print("Element found，sleep {} seconds".format(wait_after_found))
                sleep(wait_after_found)
                return element
            except AssertionError:
                print("Element 【 {} 】 Not found, Continue to swipe up...".format(param))
                # 获取滑动前页面下半部分的所有元素
                page_content = self.d.dump_hierarchy()[(len(self.d.dump_hierarchy()) // 2):]
                # self.up(**kwargs)
                self.d.swipe_ext("up")
                sleep(0.5)
                # 获取滑动后页面下半部分的所有元素，并与上一次滑动前的页面元素对比，页面元素没有变化时跳出循环
                if self.d.dump_hierarchy()[(len(self.d.dump_hierarchy()) // 2):] == page_content:
                    break
        if not element.exists:
            raise AssertionError("Element 【 {} 】 located failed in this page".format(param))

    def swipe_for_click(self, param, wait_after_click=0.0, **kwargs):
        """
        判断UI元素是否存在, 不存在则持续向上滑动到底部，直到UI元素在页面内出现，再进行点击
        :param param: xpath字符串 或 元素对象
        :param wait_after_click: 点击后等待时间
        :return:
        """
        element = self.swipe_until_element_found(param, **kwargs)
        element.click()
        if wait_after_click:
            print("Element found and click，then sleep {} seconds".format(wait_after_click))
        sleep(wait_after_click)

    def up(self, scale=0.9, times=1, duration=1.0, **kwargs):
        """
        上滑操作
        :param scale: 滑动单位，默认0.9个单位
        :param times: 滑动次数，默认1次
        :param duration: 滑动时间，默认1.0秒
        :return:
        """
        for i in range(times):
            self.d.swipe_ext("up", scale, duration=duration, **kwargs)

    def down(self, scale=0.9, times=1, duration=1.0, **kwargs):
        """
        下滑操作
        :param scale: 滑动单位，默认0.9个单位
        :param times: 滑动次数，默认1次
        :param duration: 滑动时间，默认1.0秒
        :return:
        """
        for i in range(times):
            self.d.swipe_ext("down", scale, duration=duration, **kwargs)

    def left(self, scale=0.9, times=1, duration=1.0, **kwargs):
        """
        左滑操作
        :param scale: 滑动单位，默认0.9个单位
        :param times: 滑动次数，默认1次
        :param duration: 滑动时间，默认1.0秒
        :return:
        """
        for i in range(times):
            self.d.swipe_ext("left", scale, duration=duration, **kwargs)

    def right(self, scale=0.9, times=1, duration=1.0, **kwargs):
        """
        右滑操作
        :param scale: 滑动单位，默认0.9个单位
        :param times: 滑动次数，默认1次
        :param duration: 滑动时间，默认1.0秒
        :return:
        """
        for i in range(times):
            self.d.swipe_ext("right", scale, duration=duration, **kwargs)

    #  截图
    def screenshot(self, imageName):
        if os.path.exists(r"./images"):
            if os.path.exists(fr"./images/{imageName}.png"):
                image = self.d.screenshot()
                image.save(fr"./images/{imageName}_bak.png")
            else:
                image = self.d.screenshot()
                image.save(fr"./images/{imageName}.png")
        else:
            os.mkdir(r"./images")
            image = self.d.screenshot()
            image.save(fr"./images/{imageName}.png")

    # 拿取文本
    def get_text_extend(self, element=None, type: str = "id"):

        if re.findall("//", str(element)):  # 若//开头则使用正则表达式匹配后用xpath定位
            return self.d.xpath(element).get_text()
        elif type == "id":
            return self.d(resourceId=element).get_text()
        elif type == "selected":
            return self.d(selected=True).get_text()
        else:
            pass

    # 滑动  (正常屏幕滑动,向上滑动解锁，返回主界面，解锁等通用)
    # 坐标支持数据类型：Union[int, str]
    def swipe_extend(self, x1=0.5, y1=0.99, x2=0.5, y2=0.3, dur: Union[int, str] = 0.2,
                     sleepTime=0, type: str = "percent"):
        if type == "percent":
            size = self.d.window_size()
            x1 = int(size[0] * x1)
            y1 = int(size[1] * y1)
            x2 = int(size[0] * x2)
            y2 = int(size[1] * y2)
            self.d.swipe(x1, y1, x2, y2, dur)
            sleep(sleepTime)
        else:
            self.d.swipe(x1, y1, x2, y2, dur)
            sleep(sleepTime)

    # 按下之后滑动，长按滑动
    def long_click_swipe(self, x1, y1, x2, y2, dur=0.8, sleepTime=0):
        self.d.touch.down(x1, y1).sleep(dur).move(x1, y1).move(x2, y2).up(x2, y2)
        sleep(sleepTime)

    # 向上滑动解锁，返回主界面，解锁用
    def swipe_up(self, time=0.2):
        size = self.d.window_size()
        x1 = int(size[0] * 0.5)
        y1 = int(size[1] * 1)
        y2 = int(size[1] * 0.3)
        self.d.swipe(x1, y1, x1, y2, time)

    # 缩放
    def pinch_extend(self, element, kind: str = "out or in", percent=100, steps=50):
        """ 在元素上面，做两个手指缩放的操作，kind in 或者out,放大或者缩小"""
        zhmodel = re.compile(u'[\u4e00-\u9fa5]')
        if str(element).startswith("com"):
            selector = self.d(resourceId=element)
        elif not zhmodel.search(str(element)):
            selector = self.d(className=element)
        elif zhmodel.search(str(element)):  # 若以上两种情况都不是，则使用描述定位
            selector = self.d(description=element)

        if kind == "in":
            selector.pinch_in(percent, steps)
        elif kind == "out":
            selector.pinch_out(percent, steps)
        else:
            raise Exception("输入kind不能是非in/out")

    # 关机
    def reboot_physical_key(self):
        self.d.shell("sendevent /dev/input/event0 1 116 1")
        self.d.shell("sendevent /dev/input/event0 0 0 0")
        sleep(3)
        self.d.shell("sendevent /dev/input/event0 1 116 0")
        self.d.shell("sendevent /dev/input/event0 0 0 0")
        sleep(1)
        self.click_by_text("关闭电源")

    #   截图
    def screenshot_physical_key(self):
        self.d.shell("sendevent /dev/input/event0 1 114 1")
        self.d.shell("sendevent /dev/input/event0 0 0 0")
        self.d.shell("sendevent /dev/input/event0 1 116 1")
        self.d.shell("sendevent /dev/input/event0 0 0 0")
        self.d.shell("sendevent /dev/input/event0 1 116 0")
        self.d.shell("sendevent /dev/input/event0 0 0 0")
        self.d.shell("sendevent /dev/input/event0 1 114 0")
        self.d.shell("sendevent /dev/input/event0 0 0 0")

    # 推送文件到手机
    def push_extend(self, root: Union[list, str], target, sleepTime=1):
        peojectPath = "\\".join(os.path.abspath(os.path.dirname(__file__)).split("\\")[:-1])
        if isinstance(root, list):
            for i in root:
                self.d.push(peojectPath + i, target)
        elif isinstance(root, str):
            self.d.push(root, target)
        sleep(sleepTime)

    def randmon_phone(self):
        """ 随机生成一个手机号，或者其他想生成的数据 """
        while True:
            phone = "AAAAA新建"
            for i in range(8):
                num = random.randint(0, 9)
                phone += str(num)
            return phone

    def power(self, kind: str = 'power or kill'):
        '''模拟power键'''
        if kind == 'power':
            self.d.screen_on()  # 息屏
        elif kind == 'kill':
            self.d.screen_off()  # 亮屏
        else:
            raise Exception("输入kind有误")

    def virtual_key(self,
                    kind: str = "home or delete or up or down or volume_up or volume_down or volume_mute or power or back"):
        """ 常用虚拟按键 """
        if kind == "home":
            self.d.press("home")  # 点击home键
        elif kind == "delete":
            self.d.press("delete")  # 点击删除键
        elif kind == "up":
            self.d.press("up")  # 点击上键
        elif kind == "down":
            self.d.press("down")  # 点击下键
        elif kind == "volume_up":
            self.d.press("volume_up")  # 点击音量+
        elif kind == "volume_down":
            self.d.press("volume_down")  # 点击音量-
        elif kind == "volume_mute":
            self.d.press("volume_mute")  # 点击静音
        elif kind == "power":
            self.d.press("power")  # 点击电源键
        elif kind == "back":
            self.d.press("back")  # 点击返回键
        else:
            raise Exception("输入kind有误")
