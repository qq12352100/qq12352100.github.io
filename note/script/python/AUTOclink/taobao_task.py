import time
import pyautogui
import win32api
import win32con
import win32gui
wx = int(win32api.GetSystemMetrics(win32con.SM_CXSCREEN)/2)  # 获取屏幕分辨率X
wy = int(win32api.GetSystemMetrics(win32con.SM_CYSCREEN)/2)  # 获取屏幕分辨率Y
print (wx,wy)

# pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
# pip install pyautogui
# pip install pypiwin32

def get_W(wname):
    w1hd=win32gui.FindWindow(0,wname)
    win32gui.SetForegroundWindow(w1hd)
    time.sleep(3)

#获取当前鼠标位置
def get_location():
    while True:
        time.sleep(1)
        print(tuple(pyautogui.position())) # 获取当前坐标的位置

#左键单击
def clink(x, y, s):
    pyautogui.click(x, y) 
    time.sleep(s)
    
#中间位置右键单击
def click_right(s):
    pyautogui.click(wx, wy, button='right')
    time.sleep(s)

#从屏幕中间向上向下滑动，负数是向上滑动
def roll(p,s):
    pyautogui.mouseDown(wx,wy)
    pyautogui.moveRel(0, p, duration=0.5)  # duration为滑动持续时间
    pyautogui.mouseUp()
    time.sleep(s)

#金币任务
def taobao_jinbi():
    clink(650, 200, 10) # 首页金币
    clink(950, 430, 10) # 赚体力
    for i in range(5):
        clink(944, 375, 10) # 第一块
        clink(944, 375, 10) # 第一块
        for i in range(3):
            roll(-300,6)
        click_right(5)
        click_right(5)
    click_right(10)
    click_right(10)
    click_right(10)

    
time.sleep(5)
print(time.strftime("%Y年%m月%d日  %H:%M:%S 星期%w", time.localtime()) + "_start!")
# get_location()

for i in range(30):
    # clink(943, 378, 20) # 第一块
    # click_right(10)
    taobao_jinbi()
    
# while 1:  # 循环条件为1必定成立
    # time.sleep(60*10)
    # ttime = int(time.strftime("%H%M", time.localtime()))


