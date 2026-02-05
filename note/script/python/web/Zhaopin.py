#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取滨州事业编信息

"""
import requests
from bs4 import BeautifulSoup

def getZhaopinInfo():
    url = "https://www.shiyebian.com/shandong/binzhou/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    div = soup.find('div', class_='ws-list-items')
    first_li = div.find('li')
    items = []
    title = first_li.find('a').get_text(strip=True)
    href = first_li.find('a').get('href')
    publish_time = first_li.find('span').get_text(strip=True)
    items.append({
        "title": title,
        "url": href,
        "publish_time": publish_time
    })
    return items
    
if __name__ == '__main__':
    item = getinfo()
    print(item)
    print(item[0]['title'])