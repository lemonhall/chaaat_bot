import os,time
import pyautogui
from parser import ChatBoxParser
from persistence import Persistence
from servant import Servant
import xerox

#https://pyautogui.readthedocs.io/en/latest/
screenWidth, screenHeight = pyautogui.size()

print(screenWidth, screenHeight)

#找到微信，单击并且打开，奇怪的地方其实是，x，y的坐标必须除以2，似乎。。。这是？mac屏幕高像素？
#im2 = pyautogui.screenshot('my_screenshot.png')
main_icon_box = pyautogui.locateOnScreen('main_icon.png', grayscale=True,confidence=0.9)
#print(main_icon_box)
im = pyautogui.screenshot('my_screenshot.png',region=main_icon_box)
main_icon_x,main_icon_y= pyautogui.locateCenterOnScreen('main_icon.png', grayscale=True,confidence=0.9)
print("icon_location:")
print(main_icon_x/2,main_icon_y/2)
pyautogui.moveTo(main_icon_x/2-20,main_icon_y/2,0.3)
pyautogui.click()


#找到群名称，并且点击
group_name_box = pyautogui.locateOnScreen('group_name.png', grayscale=True,confidence=0.9)
im = pyautogui.screenshot('my_screenshot2.png',region=group_name_box)
group_name_x,group_name_y= pyautogui.locateCenterOnScreen('group_name.png', grayscale=True,confidence=0.9)
print("group_name:")
print(group_name_x/2,group_name_y/2)
pyautogui.moveTo(group_name_x/2, group_name_y/2,0.3)
#pyautogui.click()

#开始试图截图聊天画面
chat_window_leftTopPoint_x = group_name_x/2-55
chat_window_leftTopPoint_y  = group_name_y/2+35
pyautogui.moveTo(chat_window_leftTopPoint_x, chat_window_leftTopPoint_y,0.3)

chat_window_RightBottomPoint_x = chat_window_leftTopPoint_x+650
chat_window_RightBottomPoint_y = chat_window_leftTopPoint_y+564
pyautogui.moveTo(chat_window_RightBottomPoint_x, chat_window_RightBottomPoint_y,0.3)
chat_box=(int(chat_window_leftTopPoint_x*2),int(chat_window_leftTopPoint_y*2),int(650*2),int(564*2))

#不支持直接输入，只能模拟敲击，所以用剪切板做了中转，所以，这里封装了一下这个流程
def send_to_ui_textbox(msg_tobe_send):
	#https://blog.csdn.net/saw471/article/details/124765952
	#pip install xerox
	xerox.copy(msg_tobe_send)
	#不支持中文，那么看来就必须用曲线救国的办法了，用剪贴板来做中转，mac下面的粘贴是command+v
	with pyautogui.hold('command'):
		pyautogui.press('v')
	time.sleep(1)
	pyautogui.press('enter')


db = Persistence()
#db.init_db()
while True:
	#截图
	im = pyautogui.screenshot('chat_box.png',region=chat_box)
	#在打印chat_box的坐标
	print("chat_box:")
	print(chat_box)
	chat_content = ChatBoxParser.getChatContent()
	print(chat_content)
	s=Servant()
	reaction = s.wait_for_call(chat_content)
	if reaction:
		#不支持直接输入，只能模拟敲击，所以用剪切板做了中转，所以，这里封装了一下这个流程
		send_to_ui_textbox(reaction)
	#db.sav_to_db(chat_content)
	time.sleep(5)