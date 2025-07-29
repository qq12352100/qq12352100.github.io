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

#从屏幕中间向上向下滑动，负数是向上滑动（拖动）
def mroll(p,s):
    pyautogui.mouseDown(wx,wy)
    pyautogui.moveRel(0, p, duration=0.5)  # duration为滑动持续时间
    pyautogui.mouseUp()
    time.sleep(s)

#从屏幕中间向上向下滑动，负数是向上滑动（鼠标滚轮）
def smroll(p,s):
    pyautogui.scroll(p)
    time.sleep(s)
    
#设置标签
def setlable():
    clink(1134, 832, 2) # 点击标签
    clink(1222, 732, 1) # 选择标签
    clink(wx, wy, 3)    # 屏幕中间
    smroll(-100,3)      # 向上滚动滑轮


    
time.sleep(5)
print(time.strftime("%Y年%m月%d日  %H:%M:%S 星期%w", time.localtime()) + "_start!")
# get_location()


for i in range(10):
    setlable()


# for i in range(30):
    # pyautogui.scroll(-100)
    # time.sleep(3)
    
# while 1:  # 循环条件为1必定成立
    # time.sleep(60*10)
    # ttime = int(time.strftime("%H%M", time.localtime()))


