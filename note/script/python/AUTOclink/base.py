'''
pip install pyautogui pykeyboard

'''

import pyperclip 
import time,sys,datetime
import pyautogui
from pykeyboard import PyKeyboard
import win32api
import win32con
import ctypes 
from pynput.mouse import Controller, Button
k = PyKeyboard()
m = pyautogui()
mouse = Controller()
# 1920 * 1080
import win32api,win32con
wx = int(win32api.GetSystemMetrics(win32con.SM_CXSCREEN)/2)  # 获取屏幕分辨率X
wy = int(win32api.GetSystemMetrics(win32con.SM_CYSCREEN)/2)  # 获取屏幕分辨率Y
print (wx,wy)
import win32gui

import pyperclip     
#pyperclip.copy("人工客服，订单号: 2572475617476043036。投诉编号：2505014846241149为什么拒绝投诉？")  # 复制到剪切板

def get_location():
    while 1:
        time.sleep(3)
        print(m.position()) # 获取当前坐标的位置
        
def paste():
    k.press_key(k.control_key)
    time.sleep(1)
    k.tap_key('v')
    time.sleep(1)
    k.release_key(k.control_key)
    time.sleep(1)
  
def clink(x, y, s):
    m.click(x, y) 
    time.sleep(s)

def tap_key(key, t, s):
    k.tap_key(key, n=t, interval=s)   #点击k键t次，每次间隔s秒
    
def tap_esc():
    pyautogui.press('esc')

def dclick(x, y, s):
    # 移动鼠标到指定位置（例如：(100, 200)）
    mouse.position = (x, y)
    # 双击鼠标左键
    mouse.click(Button.left, 2)
    time.sleep(s)

# 单击左键
# mouse.click(Button.left, 1)

# 双击左键
# mouse.click(Button.left, 2)

# 单击右键
# mouse.click(Button.right, 1)
def rclick(x, y, s):
    # 移动鼠标到指定位置（例如：(100, 200)）
    mouse.position = (x, y)
    # 双击鼠标左键
    mouse.click(Button.right, 1)
    time.sleep(s)