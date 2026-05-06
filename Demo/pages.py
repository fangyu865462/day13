from airtest.core.api import *
from poco.drivers.unity3d import UnityPoco
import pyautogui
import yaml
import os

auto_setup(__file__, devices=["Android://127.0.0.1:7555"])
poco = UnityPoco()
def load_config():
    config_path = os.path.join(os.path.dirname("E:\AirtestIDE脚本\Demo\config.yaml"), "config.yaml")
    with open(config_path, "r",encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config
CONFIG = load_config()
class MainMenuPage():
    """主菜单界面"""
    def __init__(self):
        self.poco = UnityPoco()
        # 主菜单按钮
        ctrl = CONFIG["controls"]["main_menu"]
        self.btn_basic = self.poco(ctrl["basic"])
        self.btn_drag = self.poco(ctrl["drag_and_drop"])
        self.btn_list = self.poco(ctrl["list_view"])
        self.btn_positioning = self.poco(ctrl["local_positioning"])
        self.btn_ui = self.poco(ctrl["wait_ui"])
        self.btn_ui2 = self.poco(ctrl["wait_ui2"])
        #返回按钮
        self.btn_back = self.poco(ctrl["btn_back"])

    def click_basic(self):
        self.btn_basic.click()
    def click_drag(self):
        self.btn_drag.click()
    def click_list(self):
        self.btn_list.click()
    def click_positioning(self):
        self.btn_positioning.click()
    def click_ui(self):
        self.btn_ui.click()
    def click_ui2(self):
        self.btn_ui2.click()
    def click_back(self):
        self.btn_back.click()
        #print("获取back按钮坐标", btn_tuichu.get_position())
        #print("获取back按钮尺寸", btn_tuichu.get_size())


    def click_with_retry(self,poco_node,retries=None,delay=None):
        """
        带重试机制的点击函数
        :param poco_node: Poco 节点对象（例如 poco("xxx")）
        :param img_template: 图像识别模板，例如 Template("xxx.png")
        :param retries: 重试次数
        :param delay: 每次重试间隔（秒）
        """
        if retries is None:
            retries = CONFIG["timeout"]["click_retry"]
        if delay is None:
            delay = CONFIG["timeout"]["click_delay"]
        for i in range(retries):
            try:
                if poco_node.exists():
                    poco_node.click()
                    print(f"Poco 点击成功 (尝试 {i+1}/{retries})")
                    return True
                else:
                    print(f"节点不存在，尝试 {i+1}/{retries}")
            except PocoNoSuchNodeException as e:
                print(f"Poco 定位失败 (尝试 {i+1}/{retries}): {e}")
            except Exception as e:
                print(f"未知错误 (尝试 {i+1}/{retries}): {e}")
            time.sleep(delay)
        print(f"重试 {retries} 次后仍失败")
        return False
    # -------------------- basic --------------------
class BasicPage():
    def __init__(self):
        self.poco = UnityPoco()
        ctrl = CONFIG["controls"]["basic_page"]
        # 输入框
        self.input_field = self.poco(ctrl["pos_input"])
        # 确定按钮（可通过文本定位）
        self.confirm_btn = Template(ctrl["tpl1776663679592.png"])
        # 获取显示文本的子节点
        self.text_node = self.input_field.child("Text")
        # 返回按钮
        self.back_basic = self.poco(ctrl["btn_back"])

    # 输入文本（自动清空原有内容）
    def input_text(self, text):
        self.input_field.click()
        self.input_field.set_text("")
        self.input_field.set_text(text)

    # 点击确定按钮（使用图像识别）
    def click_confirm(self):
        touch(self.confirm_btn)

    # 获取当前输入框显示的结果文本
    def get_result_text(self):
        if self.text_node.exists():
            return self.text_node.get_text()
        return None

    def click_back(self):
        self.back_basic.click()

    # -------------------- drag_and_drop --------------------
class DragDropPage():
    def __init__(self):
        self.poco = UnityPoco()
        ctrl = CONFIG["controls"]["drag_drop_page"]
        #drag_and_drop 按钮
        self.drag_drop = self.poco(ctrl["drag_and_drop"])


    def init_drag_elements(self):
        """进入界面后调用，初始化拖拽元素"""
        ctrl = CONFIG["controls"]["drag_drop_page"]
        self.demo = self.poco(ctrl["star_parent"]).child(ctrl["star_child"])[0]
        self.shell_tuodong = self.poco(ctrl["shell"])
        # 分数
        self.shell_number = self.poco(ctrl["score"])
     #判断节点名称并断言
    def drag_text(self):
        try:
            timeout = CONFIG["timeout"]["wait_appearance"]
            self.drag_drop.wait_for_appearance(timeout=timeout)
            print(self.drag_drop.get_name())
            self.assert_dad = self.drag_drop.child("Text")
            if self.drag_drop.exists():
                print("drag_and_drop节点存在")
                print("节点名称：", self.drag_drop.get_name())
                if self.assert_dad.exists():
                    self.drag_assert_text = self.assert_dad.get_text()
                    print("按钮文字：", self.drag_assert_text)
                    text_dad = "drag drop"
                    assert self.drag_assert_text == text_dad,f'文本不符：实际="{self.drag_assert_text}", 期望="{text_dad}"'
                    print("断言通过：文本匹配")
                else:
                    print("断言不通过：文本不匹配")
            else:
                print("drag_drop未找到节点存在")
        except Exception as e:
            print(f"drag_drop发生异常:{e}")
    #拖动
    def demo_tuodong(self):
        self.demo.drag_to(self.shell_tuodong)
    #判断分数变化
    def number_fenshu(self):
        self.numbers_text = self.shell_number.get_text()
        if self.numbers_text == "0":
            print("分数未增长")
        else:
            print("分数显示：",self.numbers_text)

    # -------------------- list_view --------------------
class ListViewPage:
    """列表视图界面，包含列表项、选中项显示和返回按钮"""
    def __init__(self):
        self.poco = UnityPoco()
        ctrl = CONFIG["controls"]["list_view_page"]
        # 列表内容区域（所有列表项的父容器）
        self.content = self.poco(ctrl["scroll_view"]).child(ctrl["viewport"]).child(ctrl["content"])
        # 当前选中项的显示控件
        self.selected_item = self.poco(ctrl["selected_item"])
        # 返回按钮
        self.back_btn = self.poco(ctrl["btn_back"])
        self._last_item_name = ctrl["last_item"]
    # 获取所有列表项（返回 Poco 节点列表）
    def get_items(self):
        return self.content.children()

    # 根据索引点击列表项（索引从0开始）

    def click_item_by_index(self, index):
        items = self.get_items()
        if 0 <= index < len(items):
            items[index].click()
        else:
            raise IndexError(f"索引 {index} 超出列表范围")
    # 获取当前选中项的文本

    def get_selected_text(self):
        if self.selected_item.exists():
            return self.selected_item.get_text()
        return None
    #打印列表
    def get_list(self):
        items = self.get_items()
        for idx, item in enumerate(items):
            print(f"第 {idx + 1} 项: {item.get_text()}")
    # 向下滑动列表（使内容向上滚动）

    def swipe_down(self):
        scroll = CONFIG["controls"]["list_view_page"]["scroll_view"]
        self.poco(scroll).swipe([0, -0.5])
        #self.poco("Scroll View").swipe([0, -0.5])

    # 判断最后一个列表项（Item 12）是否可见

    def is_last_item_visible(self):
        return self.poco(self._last_item_name).exists()

    def click_back(self):
        self.back_btn.click()

    # -------------------- local_positioning --------------------
    def go_position(self):
        try:
            timeout = CONFIG["timeout"]["wait_appearance"]
            poco("local_positioning").wait_for_appearance(timeout=timeout)
            lp = poco("local_positioning")
            print(lp.get_name())
            if lp.exists():
                print("local_positioning节点存在")
                print("节点名称：", lp.get_name())
                assert_lp = lp.child("Text")
                if assert_lp.exists():
                    assert_lp_text = assert_lp.get_text()
                    print("按钮文字：", assert_lp_text)
                    text_lp = "local positioning"
                    assert assert_lp_text == text_lp, f'文本不符：实际="{assert_lp_text}", 期望="{text_lp}"'
                    print("断言通过：文本匹配")
                else:
                    print("断言不通过：文本不匹配")
                #lp.click()
                # 使用带重试的点击函数（需要提前截取 local_positioning 按钮的图片，保存为 local_positioning_btn.png）
                self.click_with_retry(lp)

                pos_icon = poco(texture="icon").get_position()
                pos_shark = poco(texture="dec_shark").get_position()
                pos_citun = poco(texture="citun").get_position()
                screen_w,screen_h = device().get_current_resolution()
                # 转换为绝对坐标
                icon_abs = (int(pos_icon[0] * screen_w), int(pos_icon[1] * screen_h))
                shark_abs = (int(pos_shark[0] * screen_w), int(pos_shark[1] * screen_h))
                citun_abs = (int(pos_citun[0] * screen_w), int(pos_citun[1] * screen_h))
                pyautogui.click(icon_abs[0], icon_abs[1])
                print("已点击 icon")
                pyautogui.click(shark_abs[0], shark_abs[1])
                print("已点击 dec_shark")
                pyautogui.click(citun_abs[0], citun_abs[1])
                print("已点击 citun")
                self.go_back()
            else:
                print("local_positioning未找到节点")
        except Exception as e:
            print(f"local_positioning发生异常:{e}")


    # -------------------- wait_ui --------------------
    def go_ui(self):
        try:
            timeout = CONFIG["timeout"]["wait_appearance"]
            poco("wait_ui").wait_for_appearance(timeout=timeout)
            wu = poco("wait_ui")
            print(wu.get_name())
            if wu.exists():
                print("wait_ui节点存在")
                print("节点名称：", wu.get_name())
                assert_wu = wu.child("Text")
                if assert_wu.exists():
                    assert_wu_text = assert_wu.get_text()
                    print("按钮文字：", assert_wu_text)
                    text_wu = "wait UI"
                    assert assert_wu_text == text_wu, f'文本不符：实际="{assert_wu_text}", 期望="{text_wu}"'
                    print("断言通过：文本匹配")
                else:
                    print("断言不通过：文本不匹配")
                #wu.click()
                # 使用带重试的点击函数（需要提前截取 wu.click() 按钮的图片）
                self.click_with_retry(wu,retries=3)
                self.go_back()
            else:
                print("wait_ui未找到节点")
        except Exception as e:
            print(f"wait_ui发生异常:{e}")

    # -------------------- wait_ui2 --------------------
    def go_ui2(self):
        try:
            timeout = CONFIG["timeout"]["wait_appearance"]
            poco("wait_ui2").wait_for_appearance(timeout=timeout)
            wu2 = poco("wait_ui2")
            print(wu2.get_name())
            if wu2.exists():
                print("wait_ui2节点存在")
                print("节点名称：", wu2.get_name())
                assert_wu2 = wu2.child("Text")
                if assert_wu2.exists():
                    assert_wu2_text = assert_wu2.get_text()
                    print("按钮文字：", assert_wu2_text)
                    text_wu2 = "wait UI 2"
                    assert assert_wu2_text == text_wu2, f'文本不符：实际="{assert_wu2_text}", 期望="{text_wu2}"'
                    print("断言通过：文本匹配")
                else:
                    print("断言不通过：文本不匹配")
                #wu2.click()
                # 使用带重试的点击函数（需要提前截取 wu.click() 按钮的图片）
                self.click_with_retry(wu2,retries=3)
                self.go_back()
            else:
                print("wait_ui2未找到节点")
        except Exception as e:
            print(f"wait_ui2发生异常:{e}")





