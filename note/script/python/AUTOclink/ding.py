from PIL import Image
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib
import pyautogui
import pyperclip 
import time,sys,datetime
from pymouse import PyMouse
from pykeyboard import PyKeyboard
import win32api
import win32con
import ctypes 
wx = int(win32api.GetSystemMetrics(win32con.SM_CXSCREEN)/4)  # 获取屏幕分辨率X
wy = int(win32api.GetSystemMetrics(win32con.SM_CYSCREEN)/2)  # 获取屏幕分辨率Y
print (wx,wy)
k = PyKeyboard()
m = PyMouse()
import win32gui
import requests
import json

def get_W(wname):
    w1hd=win32gui.FindWindow(0,wname)
    # w2hd=win32gui.FindWindowEx(w1hd,None,None,None)
    win32gui.SetForegroundWindow(w1hd)
    time.sleep(3)

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
    
# 按键睡觉几秒
def tapK(t, s):
    k.tap_key(t)
    time.sleep(s)
    
#control+字母
def ctl(t):
    k.press_key(k.control_key)
    time.sleep(1)
    k.tap_key(t)
    time.sleep(1)
    k.release_key(k.control_key)
    time.sleep(2)
    
#alt+字母
def altK(t):
    k.press_key(k.alt_key)
    time.sleep(1)
    k.tap_key(t)
    time.sleep(1)
    k.release_key(k.alt_key)
    time.sleep(2)
        
def rolls(t):
    m.move(wx, wy)#中间
    for k in range(0, t):
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -100)
        time.sleep(1)

def scan3(x, y, c):
    for k in range(0, 3):
        clink(x, y, 10)
        m.move(wx, wy)#中间
        for k in range(0, c):
            time.sleep(1)
            win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -100)
        clink(wx+70, 700, 10)#系统返回

def watcht(x, y, t):
    clink(x, y, 5)
    m.move(wx, wy)#中间
    for k in range(0, t):
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -100)
        time.sleep(10)
    clink(185, 65, 5)  #内部返回
#文章2分钟
def watch(x, y):
    watcht(x, y, 12)#120s
#视频10分钟
def movie(x, y):
    clink(x, y, 5)#点击小标题
    watcht(wx, 300, 60);#600s
    watcht(wx, 550, 60);#600s
    
# 给1发微信消息
def sendmsg():
    # k.tap_key(k.print_screen_key)   #截屏
    altK('a')           #微信截屏
    m.click(80, wy, 1, 2) #截屏
    time.sleep(3)       #睡眠3秒
    altK('z')           #唤起微信
    ctl('f')            #查找
    tapK('1', 1)        #1
    tapK(k.enter_key, 3)#确认
    ctl('v')            #粘贴截屏
    tapK(k.enter_key, 3)#发送
    altK('z')           #缩小微信
    time.sleep(10)      #睡眠10s
    
# 截屏发邮件
def sendmail():
    ctime = time.strftime("%Y年%m月%d日  %H:%M:%S", time.localtime())
    cstime = int(time.time())
    image_path = 'C://pic/' + str(cstime) + '.png'  # 图片路径
    path = 'C://pic'
    if not os.path.exists(path):
        os.makedirs(path) 
    screenWidth, screenHeight = pyautogui.size()
    img = pyautogui.screenshot(region=[0, 0, screenWidth, screenHeight])  # x,y,w,h
    out = img.transpose(Image.ROTATE_90)  # 旋转90度
    out.save(image_path)
    # 第三方 SMTP 服务
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user = "584066697"  # 用户名
    mail_pass = "dqdcupiqmubnbfij"  # 口令 
     
    sender = '584066697@qq.com'
    receivers = ['3349868908@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
     
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = Header("收件人", 'utf-8')
    message['Subject'] = Header(ctime + '_dingding', 'utf-8')
    
    # 图片添加到邮件内容中
    content = MIMEText('<html><style></style><body><img src="cid:imageid" alt="imageid"></body></html>', 'html', 'utf-8')  # 正文
    message.attach(content)
    img = MIMEImage(open(image_path, 'rb').read())
    img.add_header('Content-ID', 'imageid')
    message.attach(img)
    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)  
        smtpObj.sendmail(sender, receivers, message.as_string())
        print (time.strftime("%Y年%m月%d日  %H:%M:%S 星期%w", time.localtime()) + "_邮件发送成功!")
    except smtplib.SMTPException:
        print ("Error: 无法发送邮件")
    time.sleep(5)  # 睡眠5分钟
    
#学习强国
def xuexiqiangguo():
    get_W(u"Redmi Note 5")
    clink(wx, 700, 5) #主屏
    clink(wx-70, 700, 5) #多任务
    clink(wx, 620, 10) #关闭
    clink(220, 80, 10) #学习强国+80
        
    watch(wx, 250);#第一篇
    watch(wx, 450);#第二篇
    watch(wx, 550);#第三篇
    
    clink(245, 110, 5)#要闻
    for k in range(0, 3):
        watch(wx, 300+k*80);#1
    clink(300, 110, 5)#新思想
    for k in range(0, 3):
        watch(wx, 300+k*80);#1
    clink(360, 110, 5)#山东
    clink(350, 200, 20)#山东卫视
    clink(185, 65, 5)#内部返回
    
    movie(410, 650)#电台-第一频道-全部
    movie(265, 150)#电台-第一频道-重要活动
    movie(350, 150)#电台-第一频道-重要会议
    
    clink(485, 65, 5);#我的
    clink(220, 320, 5)#学习积分

    print(time.strftime("%Y年%m月%d日  %H:%M:%S 星期%w", time.localtime()) + "_xuexi!")
    time.sleep(10 * 60)#睡眠10分钟
 
#淘宝
def taobao():
    get_W(u"Redmi Note 5")
    clink(wx, 700, 5) #主屏
    clink(wx-70, 700, 5) #多任务
    clink(wx, 620, 10) #关闭
    clink(300, 80, 10) #淘宝+80
    
    clink(190, 65, 10)#左上角每天签到
    clink(wx, 345, 10)#立即签到
    for k in range(0, 3):clink(wx+70, 700, 10)#系统返回
    
    clink(wx, 210, 60)#金币
    for k in range(0, 3):clink(wx+70, 700, 10)#系统返回
    clink(wx, 210, 60)#金币
    clink(wx, 240, 10)#签到
    clink(wx, 300, 6)#赚金币
    for k in range(0, 3):clink(wx+70, 700, 10)#系统返回
    
    clink(270, 210, 60)#农场
    for k in range(0, 3):clink(wx+70, 700, 10)#系统返回
    clink(270, 210, 60)#农场
    for k in range(0, 3):
        clink(wx, 490-70*k, 0)#收菜
        clink(280, 450-70*k, 0)#收菜
        clink(400, 450-70*k, 0)#收菜
    clink(wx, 280, 5)#收最后一块菜
    for k in range(0, 3):clink(wx+70, 700, 10)#系统返回
    
    clink(270, 210, 60)#农场
    for k in range(0, 3):
        for k in range(0, 5):
            clink(222+50*k, 312, 0)#收阳光
            clink(280+20*k, 276, 0)#收阳光
            clink(wx, 250, 3)#收阳光
            clink(wx, 230, 0)#收阳光
            clink(420, 270, 0)#收阳光
            clink(480, 300, 0)#收阳光
            clink(300, 330, 0)#收阳光
            clink(400, 330, 0)#收阳光
    clink(410, 580, 5)#阳光
    clink(460, 320, 10)#推荐采集
    for k in range(0, 8):
        clink(460, 320, 3)#立即收集
        clink(460, 560, 15)#继续采
        
    clink(wx, 700, 5) #主屏
    print(time.strftime("%Y年%m月%d日  %H:%M:%S 星期%w", time.localtime()) + "_taobao!")
    time.sleep(10 * 60)#睡眠10分钟

#钉钉
def dingding(send):
    get_W(u"Redmi Note 5")
    clink(wx, 700, 5) #主屏
    clink(wx-70, 700, 5) #多任务
    clink(wx, 620, 10) #关闭
    clink(380, 80, 30) #钉钉+80 
    print(time.strftime("%Y年%m月%d日  %H:%M:%S 星期%w", time.localtime()) + "_ding!")
    if(send==1):
        sendmsg()#睡眠10s
    time.sleep(10 * 60)#睡眠10分钟
        
def ding(ttime):
    send=1
    weekday_ = int(time.strftime("%w", time.localtime()))
    if(weekday_ == 0 or weekday_ == 6):
        send=0 #周末免打扰不发消息
    if ttime > 805 and ttime < 820:
        dingding(send)
        taobao()
    elif ttime > 1205 and ttime < 1220 or ttime > 1305 and ttime < 1320 :
        dingding(0)
    elif ttime > 1805 and ttime < 1820:
        dingding(send)
        taobao()
        # xuexiqiangguo()
        sendmail() 
        dingding(0)
#大淘客
lastt = 0
def dataoke(ttime):
    try:
        global lastt
        if ttime > 900 and ttime < 2200:
            x = requests.get('https://dtkapi.ffquan.cn/go_getway/proxy/search?platform=1&page=1&px=zh&is_choice=1&sortType=9&cids=9&version=1&api_v=1&flow_identifier=normal')
            jsons = json.loads(x.text)
            first = jsons['data']['search']['list'][0]
            strtitle = first['price']+first['d_title']#+'||https://item.taobao.com/item.htm?id='+first['goodsid']+'||'+first['coupon_link']
            if float(first['price'])< 9 and ttime-lastt > 120 :
                lastt = ttime
                print(str(ttime)+'||'+strtitle)
        else:
            lastt = 0
    except Exception:
        print('error')


# 1360 * 768
time.sleep(5)
print(time.strftime("%Y年%m月%d日  %H:%M:%S 星期%w", time.localtime()) + "_start!")
# get_location()
# dingding(0)
taobao()
# xuexiqiangguo()
while 1:  # 循环条件为1必定成立
    ttime = int(time.strftime("%H%M", time.localtime()))
    # holiday = int(time.strftime("%m%d", time.localtime()))
    ding(ttime)
    time.sleep(60*10)


