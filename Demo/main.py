from airtest.core.api import *
from pages import MainMenuPage, BasicPage, ListViewPage,DragDropPage   # 导入页面类

# 初始化 Airtest 环境
auto_setup(__file__, devices=["Android://127.0.0.1:7555"])

# 实例化页面对象
main = MainMenuPage()
basic = BasicPage()
list_page = ListViewPage()


# 编写basic测试流程
main.click_basic()
basic.input_text("自动化测试")
basic.click_confirm()
result = basic.get_result_text()
assert result == "自动化测试", "输入结果校验失败"
basic.click_back()

# 编写list_view测试流程
sleep(2)                       # 等待返回主界面
main.btn_list.wait_for_appearance(timeout=10)   # 等待按钮出现
main.click_list()
sleep(2) 
items = list_page.get_items()
print(f"共{len(items)}个列表项")
list_page.get_list()
list_page.click_item_by_index(2)
print("选中项:", list_page.get_selected_text())
list_page.swipe_down()
assert list_page.is_last_item_visible(), "最后一项未出现"
list_page.click_back()

# 编写drag_and_drop测试流程
main.click_drag()
sleep(2)
#延迟实例化
drag_page = DragDropPage()
drag_page.init_drag_elements()
drag_page.demo_tuodong()
sleep(5)
drag_page.number_fenshu()













