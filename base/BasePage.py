import os
import re
import time
import random
from typing import Union


class BasePage:  # 构造函数
    def __init__(self, driver):
        self.driver = driver

    # 点击
    def click(self, element, sleepTime=0):
        if str(element).startswith("com"):  # 若开头是com则使用ID定位
            self.driver(resourceId=element).click()  # 点击定位元素
        elif re.findall("//", str(element)):  # 若//开头则使用正则表达式匹配后用xpath定位
            self.driver.xpath(element).click()  # 点击定位元素
        else:  # 若以上两种情况都不是，则使用描述定位
            self.driver(description=element).click()  # 点击定位元素
        time.sleep(sleepTime)


    # 点击直到元素消失
    def click_until_gone(self, element, kind):
        if kind == "id":
            self.driver(resourceId=element).click_gone()
        elif kind == "class":
            self.driver(className=element).click_gone()
        elif kind == "text":
            self.driver(text=element).click_gone()
        else:  # 若以上两种情况都不是，则使用描述定位
            self.driver(description=element).click_gone()  # 点击定位元素

    # 组合定位classname和text
    def click_by_classname_text(self, element1, element2):
        self.driver(className=element1, text=element2).click()

    # 组合定位classname和description
    def click_by_classname_description(self, element1, element2):
        self.driver(className=element1, description=element2).click()

    # 组合定位text和description
    def click_by_text_description(self, element1, element2):
        self.driver(text=element1, description=element2).click()


    # 根据id点击(包括非com开头的id点击定位元素)
    def click_by_id(self, element, sleepTime=0):
        self.driver(resourceId=element).click()
        time.sleep(sleepTime)


    # 根据文本点击
    def click_by_text(self, element, sleepTime=0):
        self.driver(text=element).click()  # 点击定位元素
        time.sleep(sleepTime)


    # 根据百分比坐标点击
    def click_by_zuobiao(self, x, y, sleepTime=0):
        size = self.driver.window_size()
        self.driver.click(int(size[0] * x), int(size[1] * y))
        time.sleep(sleepTime)


    # 根据坐标点击元素
    def click_coord(self, x, y):
        self.driver.click(x, y)


    # 根据坐标双击元素
    def double_click_by_zuobiao(self, x, y, sleepTime=0):
        size = self.driver.window_size()
        self.driver.double_click(int(size[0] * x), int(size[1] * y))
        time.sleep(sleepTime)


    # 超时时间设置点击，根据文本定位，针对点击屏幕元素反应慢的元素
    def click_by_text_time_out(self, element, timeout=30, sleepTime=0):
        self.driver(text=element).click(timeout=timeout)
        time.sleep(sleepTime)


    # 长按
    def long_click_extend(self, element, dur=1, sleepTime=0):
        zhmodel = re.compile(u'[\u4e00-\u9fa5]')
        if str(element).startswith("com"):  # 若开头是com则使用ID定位
            self.driver(resourceId=element).long_click(dur)  # 点击定位元素
        elif re.findall("//", str(element)):  # 若//开头则使用正则表达式匹配后用xpath定位
            self.driver.xpath(element).long_click()  # 点击定位元素
        elif zhmodel.search(str(element)):
            self.driver(description=element).long_click(dur)
        else:
            self.driver(className=element).long_click(dur)
        time.sleep(sleepTime)


    # 通过文本长击
    def long_click_by_text(self, element, dur=0.5, sleepTime=0):
        self.driver(text=element).long_click(dur)
        time.sleep(sleepTime)


    #  通过坐标长击
    def long_click_by_zuobiao(self, x, y, sleepTime=0,duration: float = 1):
        self.driver.long_click(x, y,duration)
        time.sleep(sleepTime)


    # 清空输入框中的内容
    def clear(self, element):
        if str(element).startswith("com"):  # 若开头是com则使用ID定位
            self.driver(resourceId=element).clear_text()  # 清除文本
        elif re.findall("//", str(element)):  # 若//开头则使用正则表达式匹配后用xpath定位
            self.driver.xpath(element).clear_text()  # 清除文本
        else:  # 若以上两种情况都不是，则使用描述定位
            self.driver(description=element).clear_text()  # 清除文本


    # 输入
    def input(self, element, value, sleepTime=0):
        if str(element).startswith("com"):  # 若开头是com则使用ID定位
            self.driver(resourceId=element).set_text(value)  # send_keys
        elif re.findall("//", str(element)):  # 若//开头则使用正则表达式匹配后用xpath定位
            self.driver.xpath(element).set_text(value)
        else:  # 若以上两种情况都不是，则使用描述定位
            self.driver(description=element).set_text(value)
        time.sleep(sleepTime)

    # 不存在搜索按钮的搜索
    def input_by_send_keys(self, element, value):
        self.driver.set_fastinput_ime(True)  # 切换成FastInputIME输入法
        if str(element).startswith("com"):  # 若开头是com则使用ID定位
            self.driver(resourceId=element).send_keys(value)  # send_keys
        elif re.findall("//", str(element)):  # 若//开头则使用正则表达式匹配后用xpath定位
            self.driver.xpath(element).send_text(value)
        else:  # 若以上两种情况都不是，则使用描述定位
            self.driver(description=element).send_keys(value)
        self.driver.set_fastinput_ime(False)  # 切换成正常的输入法
        self.driver.send_action("search")  # 模拟输入法的搜索


    # 查找元素
    def find_elements(self, element, timeout=5):  # 找元素
        is_exited = False
        try:
            while timeout > 0:
                xml = self.driver.dump_hierarchy()  # 获取网页层次结构
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
            return self.driver.xpath(element).exists == True
        elif type == "text":
            return self.driver(text=element).exists(timeout=timeout) == True
        elif type == "dec":
            return self.driver(description=element).exists(timeout=timeout) == True
        else:
            pass


    #  截图
    def screenshot(self, imageName):
        if os.path.exists(r"./images"):
            if os.path.exists(fr"./images/{imageName}.png"):
                image = self.driver.screenshot()
                image.save(fr"./images/{imageName}_bak.png")
            else:
                image = self.driver.screenshot()
                image.save(fr"./images/{imageName}.png")
        else:
            os.mkdir(r"./images")
            image = self.driver.screenshot()
            image.save(fr"./images/{imageName}.png")


    # 拿取文本
    def get_text_extend(self, element=None, type: str = "id"):

        if re.findall("//", str(element)):  # 若//开头则使用正则表达式匹配后用xpath定位
            return self.driver.xpath(element).get_text()
        elif type == "id":
            return self.driver(resourceId=element).get_text()
        elif type == "selected":
            return self.driver(selected=True).get_text()
        else:
            pass


    # 滑动  (正常屏幕滑动,向上滑动解锁，返回主界面，解锁等通用)
    # 坐标支持数据类型：Union[int, str]
    def swipe_extend(self, x1=0.5, y1=0.99, x2=0.5, y2=0.3, dur: Union[int, str] = 0.2,
                     sleepTime=0, type: str = "percent"):
        if type == "percent":
            size = self.driver.window_size()
            x1 = int(size[0] * x1)
            y1 = int(size[1] * y1)
            x2 = int(size[0] * x2)
            y2 = int(size[1] * y2)
            self.driver.swipe(x1, y1, x2, y2, dur)
            time.sleep(sleepTime)
        else:
            self.driver.swipe(x1, y1, x2, y2, dur)
            time.sleep(sleepTime)


    # 按下之后滑动，长按滑动
    def long_click_swipe(self, x1, y1, x2, y2, dur=0.8, sleepTime=0):
        self.driver.touch.down(x1, y1).sleep(dur).move(x1, y1).move(x2, y2).up(x2, y2)
        time.sleep(sleepTime)


    # 向上滑动解锁，返回主界面，解锁用
    def swipe_up(self, time=0.2):
        size = self.driver.window_size()
        x1 = int(size[0] * 0.5)
        y1 = int(size[1] * 1)
        y2 = int(size[1] * 0.3)
        self.driver.swipe(x1, y1, x1, y2, time)


    # 滑动，根据方向滑动
    def swipe_ext_extend(self, direction: Union[SwipeDirection, str] = "up", scale=0.9, sleepTime=0):
        self.driver.swipe_ext(direction, scale=scale)
        time.sleep(sleepTime)


    # 缩放
    def pinch_extend(self, element, kind: str = "out or in", percent=100, steps=50):
        """ 在元素上面，做两个手指缩放的操作，kind in 或者out,放大或者缩小"""
        zhmodel = re.compile(u'[\u4e00-\u9fa5]')
        if str(element).startswith("com"):
            selector = self.driver(resourceId=element)
        elif not zhmodel.search(str(element)):
            selector = self.driver(className=element)
        elif zhmodel.search(str(element)):  # 若以上两种情况都不是，则使用描述定位
            selector = self.driver(description=element)

        if kind == "in":
            selector.pinch_in(percent, steps)
        elif kind == "out":
            selector.pinch_out(percent, steps)
        else:
            raise Exception("输入kind不能是非in/out")


    # 关机
    def reboot_physical_key(self):
        self.driver.shell("sendevent /dev/input/event0 1 116 1")
        self.driver.shell("sendevent /dev/input/event0 0 0 0")
        time.sleep(3)
        self.driver.shell("sendevent /dev/input/event0 1 116 0")
        self.driver.shell("sendevent /dev/input/event0 0 0 0")
        time.sleep(1)
        self.click_by_text("关闭电源")


    #   截图
    def screenshot_physical_key(self):
        self.driver.shell("sendevent /dev/input/event0 1 114 1")
        self.driver.shell("sendevent /dev/input/event0 0 0 0")
        self.driver.shell("sendevent /dev/input/event0 1 116 1")
        self.driver.shell("sendevent /dev/input/event0 0 0 0")
        self.driver.shell("sendevent /dev/input/event0 1 116 0")
        self.driver.shell("sendevent /dev/input/event0 0 0 0")
        self.driver.shell("sendevent /dev/input/event0 1 114 0")
        self.driver.shell("sendevent /dev/input/event0 0 0 0")


    # 推送文件到手机
    def push_extend(self, root: Union[list, str], target, sleepTime=1):
        peojectPath = "\\".join(os.path.abspath(os.path.dirname(__file__)).split("\\")[:-1])
        if isinstance(root, list):
            for i in root:
                self.driver.push(peojectPath+i, target)
        elif isinstance(root, str):
            self.driver.push(root, target)
        time.sleep(sleepTime)


    def randmon_phone(self):
        """ 随机生成一个手机号，或者其他想生成的数据 """
        while True:
            phone = "AAAAA新建"
            for i in range(8):
                num = random.randint(0, 9)
                phone += str(num)
            return phone


    def power(self, kind: str='power or kill'):
        '''模拟power键'''
        if kind == 'power':
            self.driver.screen_on()  # 息屏
        elif kind == 'kill':
            self.driver.screen_off()  # 亮屏
        else:
            raise Exception("输入kind有误")


    def virtual_key(self,kind: str = "home or delete or up or down or volume_up or volume_down or volume_mute or power or back"):
        """ 常用虚拟按键 """
        if kind == "home":
            self.driver.press("home")           # 点击home键
        elif kind == "delete":
            self.driver.press("delete")         # 点击删除键
        elif kind == "up":
            self.driver.press("up")             # 点击上键
        elif kind == "down":
            self.driver.press("down")           # 点击下键
        elif kind == "volume_up":
            self.driver.press("volume_up")      # 点击音量+
        elif kind == "volume_down":
            self.driver.press("volume_down")    # 点击音量-
        elif kind == "volume_mute":
            self.driver.press("volume_mute")    # 点击静音
        elif kind == "power":
            self.driver.press("power")          # 点击电源键
        elif kind == "back":
            self.driver.press("back")           # 点击返回键
        else:
            raise Exception("输入kind有误")