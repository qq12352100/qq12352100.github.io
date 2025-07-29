#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
nohup python3 app.py > log.file 2>&1 &
"""

from flask import Flask
from threading import Thread
import time as t
import TOTP
import online_note
import stock

app = Flask(__name__)

# MFA 设备验证器 
app.add_url_rule('/getkey', 'TOTP.getkey', TOTP.getkey) # 主页 /getkey
app.add_url_rule('/getkeyjson', 'TOTP.getkeyjson', TOTP.getkeyjson) #返回json
# 在线笔记本
app.add_url_rule('/note/<path:subpath>', 'online_note.note', online_note.note) # 主页 /note/bkk
app.add_url_rule('/save_content', 'online_note.save_content', online_note.save_content, methods=['POST']) # 每隔10秒推送一次
# 股票
app.add_url_rule('/getstock', 'stock.getstock', stock.getstock) 

def run_stock_info():
    while True:
        if stock.is_market_open():
            stock.get_stock_info()
        t.sleep(600)  # 休眠10分钟

if __name__ == '__main__':
    stock_info_thread = Thread(target=run_stock_info)
    stock_info_thread.start()
    app.run(debug=True, port=5000)
    stock_info_thread.join()