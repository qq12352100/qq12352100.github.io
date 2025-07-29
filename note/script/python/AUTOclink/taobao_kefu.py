'''
pip install windows
pip install pymouse
pip install pyperclip

'''

import pyperclip

pyperclip.copy("人工客服，订单编号4326495807022043036，售后为什么拒绝退款？")  # 复制到剪切板

def startW():
    base.clink(603, 849,3) #联系人工客服
    base.clink(603, 849,3) #联系人工客服
    base.clink(850,900,3) #对话框
    base.paste();
    base.clink(1396, 897,3) #发送

base.get_location()

while 1:  # 循环条件为1必定成立
    base.time.sleep(3)
    startW()
