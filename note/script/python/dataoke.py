import time
import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.header import Header


def sendmail(text):
    # 创建 SMTP 对象
    smtp = smtplib.SMTP()
    # 连接（connect）指定服务器
    smtp.connect("smtp.qq.com", port=25)
    # 登录，需要：登录邮箱和授权码
    smtp.login(user="584066697", password="dqdcupiqmubnbfij")

    # 构造MIMEText对象，参数为：正文，MIME的subtype，编码方式
    message = MIMEText(text, 'plain', 'utf-8')
    message['From'] = '584066697@qq.com'  # 发件人的昵称
    message['To'] = Header("3349868908@qq.com", 'utf-8')  # 收件人的昵称
    message['Subject'] = Header(text, 'utf-8')  # 定义主题内容
    print(message)

    smtp.sendmail(from_addr="584066697@qq.com", to_addrs="3349868908@qq.com", msg=message.as_string())


lastt = 0
def dataoke(ttime):
    try:
        global lastt
        if ttime > 900 and ttime < 2200:
            x = requests.get('https://dtkapi.ffquan.cn/go_getway/proxy/search?platform=1&page=1&px=zh&is_choice=1&sortType=9&cids=9&version=1&api_v=1&flow_identifier=normal')
            jsons = json.loads(x.text)
            first = jsons['data']['search']['list'][0]
            strtitle = first['price']+first['d_title']#+'||https://item.taobao.com/item.htm?id='+first['goodsid']+'||'+first['coupon_link']
            if float(first['price'])< 8 and ttime-lastt > 120 :
                lastt = ttime
                sendmail(strtitle)
                print(str(ttime)+'||'+strtitle)
        else:
            lastt = 0
    except Exception as e:
        print('ZeroDivisionError', e)

        
        

while 1:  # 循环条件为1必定成立
    ttime = int(time.strftime("%H%M", time.localtime()))
    dataoke(ttime)
    time.sleep(60*10)