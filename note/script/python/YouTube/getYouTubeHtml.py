#!/usr/bin/python
# encoding:utf-8
# 抓取YouTube视频
import requests
from bs4 import BeautifulSoup
import socks
import socket
import re,json,sys,os


#方法一
'''通过请求主页获取第一页的视频数据   todu-下滑异步加载未实现抓取'''
def get1():
    # 目标网页的URL
    url = 'https://www.youtube.com/@DocumentaryCN/videos'
    # 设置socks代理
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 10808)
    socket.socket = socks.socksocket
    # 使用requests库发送GET请求，并通过代理服务器
    response = requests.get(url)

    # 检查请求是否成功
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        text=str(soup)
        result=soup
        # print(text)

        start_index = text.index("ytInitialData") + len("ytInitialData") + 3  # 找到"ytInitialData"后加3得到起始索引
        start_result = text[start_index:].strip()  # 移除前导和尾随的空白
        
        end_index = start_result.index(";")  # 直接找到"programming"的起始索引作为结束位置
        end_result = start_result[:end_index].strip()  #移除前导和尾随的空白
        
        # with open('D://1.txt', 'w', encoding='utf-8') as f: f.write(str(end_result)) #截取网页内完整json

        data = json.loads(end_result).get('contents').get('twoColumnBrowseResultsRenderer').get('tabs')[1].get('tabRenderer').get('content').get('richGridRenderer').get('contents')
        print(type(data))
        # with open('D://1.txt', 'w', encoding='utf-8') as f:f.write(str(data[0].get('richItemRenderer')))
        # sys.exit()
        k=0
        with open('D://1.txt', 'w', encoding='utf-8') as f:
            for i in data:
                try:
                    videoRenderer = json.loads(json.dumps(i)).get('richItemRenderer').get('content').get('videoRenderer')
                    title = videoRenderer.get('title').get('runs')[0].get('text')
                    videoId =  videoRenderer.get('videoId')
                    print(videoId+'---'+title)
                    # os.system('yt-dlp_x86.exe --proxy socks4://127.0.0.1:10808 -P "D:/test" https://www.youtube.com/watch?v='+videoId)
                    k=k+1
                    f.write(videoId+'---'+title+'\n')
                except AttributeError:
                    print("尝试访问的对象不是一个字典")
            print('总计：'+ str(k))
    else:
        print(f"请求失败，状态码：{response.status_code}")
        

#方法二
'''通过打开网页加载完全部视频，通过js获取视频连接地址，然后复制为本地文件读取下载 todo-需要手动处理文件'''
""" 1、点击播放列表。2、点击查看完整播放列表。3、下滑加载所有内容。

let videoLinks = document.querySelectorAll('a#video-title-link');
videoLinks.forEach((link, i) => console.log(link.href, '==', link.title, i+1 ));

"""
def get2():
    with open('E:/YouTube/1.txt', 'r', encoding='utf-8') as f:
        for line in f:
            link = line[:line.index("==")]
            title = line[line.index("=="):]
            print(link,title)  # trip()用于去除每行末尾的换行符
            os.system('E:\YouTube\yt-dlp.exe --proxy socks4://127.0.0.1:10808 -P "E:/YouTube/test" '+ link.strip())
            
# startMysql()
get2()
# getSql('youdianyisi2020')
# endMysql()

'''
E:\YouTube\yt-dlp.exe --proxy socks4://127.0.0.1:10808 -P "E:/YouTube/test" https://www.youtube.com/watch?v=LK9ynpPcj-U

yt-dlp.exe --proxy socks4://127.0.0.1:10808 -P "E:/YouTube" https://www.youtube.com/playlist?list=PLlD7SeKBB31cwPtRZgsbceAJye9k8r1ZO -f "bv+ba" 





'''










