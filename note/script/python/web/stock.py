#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

http://qt.gtimg.cn/q=sh600028,sz159998
http://qt.gtimg.cn/q=s_sh600028,s_sz159998

腾讯财经提供的一个非官方支持的API,所以它的稳定性和长期可用性无法得到保证。 
pip install redis
pip install flask
pip install akshare   #需要高版本python3.13


"""
import flask
app = flask.Flask(__name__)

import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from datetime import datetime, time
import time as t
import redis
import json
import logging
import akshare as ak
# 配置日志
logging.basicConfig(level=logging.INFO, filename='log.file', format='%(asctime)s - %(levelname)s - %(filename)s %(lineno)d - %(message)s')

# 用户提供的成本价字典, '601989': [4.791, 4200, 1, '中国重工']  1 邮件通知 0 不通知
cost_prices = json.loads('''
{
    "002230": [50.425, 200, 1, "科大讯飞"],
    "159998": [0.90, 33000, 0, "计算机ETF"],
    "512710": [0.620, 20000, 1, "军工龙头ETF"],
    "600028": [6.201, 3300, 0, "中国石化"],
    "601989": [4.791, 4200, 1, "中国重工"]
}
''')

r = redis.Redis(host='8.152.208.138', password='lL2oOkEc')
# 从redis中获取成本价
def get_cost_redis():
    global cost_prices, r
    # print(r.ping())
    # r.set('cost_key', json.dumps(cost_prices))
    cost_prices = eval(r.get('cost_key').decode('utf-8'))

# QQ邮箱发送邮件
def send_qq_email(subject, content):
    sender = '584066697@qq.com'
    receivers = ['447841461@qq.com']
    try:
        # 创建MIMEText对象
        message = MIMEText(content, 'plain', 'utf-8')
        # 设置邮件头信息
        message['Subject'] = Header(subject, 'utf-8')
        message['From'] = formataddr((Header(sender, 'utf-8').encode(), sender))
        message['To'] = ', '.join([formataddr((Header('447841461', 'utf-8').encode(), recv)) for recv in receivers])
        # 连接到QQ邮箱的SMTP服务器并登录
        smtp_server = "smtp.qq.com"
        server = smtplib.SMTP_SSL(smtp_server, 465)  # QQ邮箱的SMTP服务器端口是465
        server.login(sender, 'xodvmwwxdpgabdac')
        # 发送邮件
        server.sendmail(sender, receivers, message.as_string())
        logging.info("邮件发送成功")
    except smtplib.SMTPException as e:
        logging.info(f"Error: 无法发送邮件. {e}")
    finally:
        server.quit()

# 判断股市是否开盘
def is_market_open():
    TRADE_TIMES = [(time(9, 30), time(11, 30)), (time(13, 0), time(15, 0))]
    now = datetime.now().time()
    return any(start <= now <= end for start, end in TRADE_TIMES)

# 获取股票信息并发送邮件
def get_stock_info():
    global cost_prices, r
    get_cost_redis() # 获取redis最新股票代码
    stock_codes = '.'.join(cost_prices.keys())
    url = f"http://qt.gtimg.cn/q=" + ','.join([f"s_sh{code}" if code.startswith(('5', '6', '9')) else f"s_sz{code}" for code in stock_codes.split('.')])
    response = requests.get(url)

    mailhead = ''   # redis缓存头
    mailcontent = ''   # 邮件内容
    totalG = 0 # 总收益
    # 解析返回的数据
    data_list = response.text.split(';')[:-1]  # 去掉最后一个元素
    #0: 未知 1: 名字 2: 代码 3: 当前价格 4: 涨跌额 5: 涨跌幅 6: 成交量（手）7: 成交额（万）8: 总市值 9: 股票类型
    #0: 未知 1: 名字 2: 代码 3: 当前价格 4: 昨收 5: 今开 6: 成交量（手） 7: 外盘 8: 内盘 9: 买一 10: 买一量（手） 11-18: 买二 买五 19: 卖一 20: 卖一量 21-28: 卖二 卖五 29: 最近逐笔成交 30: 时间 31: 涨跌 32: 涨跌% 33: 最高 34: 最低 35: 价格/成交量（手）/成交额 36: 成交量（手） 37: 成交额（万） 38: 换手率 39: 市盈率 40: 41: 最高 42: 最低 43: 振幅 44: 流通市值 45: 总市值 46: 市净率 47: 涨停价 48: 跌停价
    for one in data_list:
        data = one.split('~')
        cost_price = cost_prices.get(data[2], 0)[0] # 成本价
        cost_num = cost_prices.get(data[2], 0)[1]   # 购买数量
        notify_mail = cost_prices.get(data[2], 0)[2]    # 是否发送邮件
        earnings = round((float(data[3]) - cost_price) * cost_num, 2) # 单股收益
        totalG += earnings  # 总收益
        if(earnings > 1000 and notify_mail): # 单股收益超过100元就发邮件
            mailhead += data[2]
            mailcontent += f"{data[1]}({data[2]}) 当前价格：{data[3]} 涨跌幅：{data[5]}% 成本价：{cost_price} 收益：{earnings}\n"
    
    now = datetime.now()
    logging.info(f"当前时间：{now.strftime('%Y-%m-%d %H:%M:%S')}, 收益：{totalG:.2f}")

    # 发送邮件
    if mailcontent.strip() and not r.exists(mailhead):
        send_qq_email('股票回本', mailcontent) 
        r.set(mailhead, mailcontent, ex=3600) # 1小时内不重复发送邮件

# 获取金价
def getgold():
    gold_price_data = ak.futures_foreign_commodity_realtime(symbol='XAU,BTC')
    if gold_price_data is not None and not gold_price_data.empty:
        result_list = []
        for index, row in gold_price_data.iterrows():
            result = {
                "name": str(row["名称"]),
                "USD_price": float(row["最新价"]),
                "CNY_price": round(float(row["人民币报价"]), 2),  # 保留三位小数
                "rise_fall": round(float(row["涨跌幅"]), 2)
            }
            result_list.append(result)
        result_json = json.dumps(result_list, ensure_ascii=False, indent=4)
        # print(result_json)
    return result_json
    
#http://127.0.0.1:5000/getstock
@app.route('/getstock', methods=['GET'])
def getstock():
    global cost_prices
    get_cost_redis() # 获取redis最新股票代码
    gold_price_data = getgold() # 获取金价
    html_content = '''
    <!DOCTYPE html>
    <html>
        <head>
            <title>股票</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
            <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
            <style>
            /* 重置默认样式 */
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            html, body {
                height: 100%;
                width: 100%;
                overflow: hidden; /* 确保内容不会溢出 */
            }
            table {
                width: 100%;
            }
            .negative {
                background-color: #d4edda; /* 绿色背景 */
                color: #155724;
            }
            .positive {
                background-color: #f8d7da; /* 红色背景 */
                color: #721c24;
            }
            </style>
        </head>
        <body>
            <div><input id="codenum" style="width: 100%;"></input></div>
            <div id="contentArea" >
                <table id="stockTable">
                    <thead>
                        <tr>
                            <th>名称</th>
                            <th>代码</th>
                            <th>现价</th>
                            <th>成本价</th>
                            <th>涨跌</th>
                            <th>收益</th>
                        </tr>
                    </thead>
                    <tbody>
                    <!-- 行将在这里动态添加 -->
                    </tbody>
                </table>
            </div>
            <script>
                var costPrices = {{ cost_prices|tojson|safe }}
                var gold_price_data = JSON.parse({{ gold_price_data|tojson|safe }})
                console.log(gold_price_data)
                var keysJoinedByHash = Object.keys(costPrices).sort().join('.');
                $('#codenum').val(keysJoinedByHash);
                
                
               // 将数据填充到表格中
               function populateTableFromResponse(response) {
                    var totalG = 0;//总收益
                    var dataArray = response.split(';').filter(item => item.trim() !== '');// 分割响应字符串并移除可能存在的最后一个空元素
                    var $tbody = $('#stockTable tbody').empty(); // 清空现有内容
                    dataArray.forEach(function(item) {
                        var dataList = item.split('~');// 拆分字符串成列表
                        // 确保关键字段存在且有效
                        if (dataList.length >= 9 && dataList[1] && dataList[2]) {
                            var rowClass = parseFloat(dataList[5]) < 0 ? 'negative' : 'positive'; // 根据涨跌幅设置行的颜色
                            var costPrice = parseFloat(costPrices[dataList[2]]?.[0]) || 0; // 获取成本价，默认为0
                            var costNum = parseFloat(costPrices[dataList[2]]?.[1]) || 0; // 获取购买数量，默认为0
                            var currentPrice = parseFloat(dataList[3]); // 当前价格
                            var profitLoss = costPrice !== 0 ? ((currentPrice - costPrice) * costNum).toFixed(2) : 0; // 计算收益/亏损
                            totalG += Number(profitLoss);
                            // 直接构建并添加行到表格
                            var row = `<tr class="${rowClass}">
                                    <td>${dataList[1]}</td> <!-- 名称 -->
                                    <td>${dataList[2]}</td> <!-- 代码 -->
                                    <td>${parseFloat(dataList[3]).toFixed(3)}</td> <!-- 当前价格 -->
                                    <td>${costPrice.toFixed(3)}</td> <!-- 成本价 -->
                                    <td>${parseFloat(dataList[5]).toFixed(2)}%</td> <!-- 涨跌幅 -->
                                    <td>${profitLoss}</td> <!-- 收益/亏损 -->
                                </tr>`;
                            $tbody.append(row);
                        }
                    });
                    $tbody.append(`<tr><td colspan="5"></td><td style="color: #0058ff;">${totalG.toFixed(2)}</td></tr>`);
                    gold_price_data.forEach(function(item) {
                        var rowClass = item.rise_fall < 0 ? 'negative' : 'positive'; // 根据涨跌幅设置行的颜色
                        $tbody.append(`<tr  class="${rowClass}"><td >${item.name}</td><td >${item.USD_price}</td><td ></td><td >${item.CNY_price}</td><td >${item.rise_fall}%</td></tr>`);
                        console.log(`名称: ${item.name}, 美元价格: ${item.USD_price}, 人民币价格: ${item.CNY_price}, 涨跌幅: ${item.rise_fall}`);
                    });
                    
                }

                // 转换函数
                function convertCodes(codes) {
                    return codes.map(function(code) {
                        if (/^[569]/.test(code)) {
                            return 's_sh' + code;
                        } else {
                            return 's_sz' + code;
                        }
                    });
                }
                // 请求数据
                function getContent() {
                    var codenum = $('#codenum').val();
                    $.ajax({
                        url: 'http://qt.gtimg.cn/q=s_sh000001,'+convertCodes(codenum.split('.')),
                        type: 'GET',
                        success: function(response) {
                        var dataArray = response.split(';');
                            // 将数据填充到表格中
                            populateTableFromResponse(response);
                            console.log(response);
                        },
                        error: function(error) {
                            console.error('Error saving content:', error);
                        }
                    });
                }
                getContent()
                // 自动每秒发送一次内容
                setInterval(getContent, 5 * 1000);
            </script>
        </body>
    </html>
    '''
    return flask.render_template_string(html_content, cost_prices=cost_prices, gold_price_data=gold_price_data)

if __name__ == "__main__":
    # send_qq_email('xinxin','content')
    # get_cost_redis()
    # get_stock_info()
    # while 1:
    #     if is_market_open():
    #         get_stock_info()
    #     t.sleep(600)  # 休眠10分钟

    app.run(host='0.0.0.0', debug=True, port=5000)