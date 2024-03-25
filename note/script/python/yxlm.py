import time,sys,datetime
from pymouse import PyMouse
from pykeyboard import PyKeyboard
k = PyKeyboard()
m = PyMouse()

def get_location():
    while 1:
        time.sleep(3)
        print(m.position()) # 获取当前坐标的位置
def clink(x, y, s):
    m.click(x, y) 
    time.sleep(s)
    
# get_location()
while 1:  # 循环条件为1必定成立
    # clink(839,260,1) #辅助
    # clink(807,325,1) #大头
    
    clink(955,721,1) #找到队伍
    clink(1855,780,1) #禁用英雄
    clink(959,749,5) #确定英雄