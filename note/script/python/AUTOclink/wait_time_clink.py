'''
简化版定时点击程序

pip install pyautogui keyboard
'''
import pyautogui
import time
import datetime
import sys,os

def simple_autoclick(target_hour=18, target_minute=25, click_x=1533, click_y=824):  # 1533，824 微信全屏之后的右下角发送按钮  1699 * 900
    """
    target_hour: 目标小时
    target_minute: 目标分钟
    click_x: 点击X坐标
    click_y: 点击Y坐标
    """
    try:
        while True:
            now = datetime.datetime.now()
            # 显示当前时间
            current_time = now.strftime("%H:%M:%S")
            sys.stdout.write(f"\r当前时间: {current_time} - 等待中...")
            sys.stdout.flush()
            # 检查是否到达目标时间
            if now.hour == target_hour and now.minute == target_minute:
                print(f"\n\n到达目标时间 {target_hour:02d}:{target_minute:02d}，开始点击...")
                # 移动到目标位置并点击
                pyautogui.moveTo(click_x, click_y, duration=0.5)
                pyautogui.click()
                break
            time.sleep(3)
            
    except KeyboardInterrupt:
        print("\n\n程序已退出")
        
# t秒后锁定屏幕
def lock_screen_shortcut(t):
    print(f"{t}秒后锁定屏幕")
    time.sleep(t)
    os.system("rundll32.exe user32.dll,LockWorkStation")
    sys.exit(0)
       
# 使用示例
if __name__ == "__main__":
    # 设置目标时间，点击位置
    simple_autoclick(19, 23)
    lock_screen_shortcut(5)
    # while 1: time.sleep(3); print(pyautogui.position()) # 获取鼠标当前位置
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    