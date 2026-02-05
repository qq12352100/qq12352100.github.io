'''
滨州事业编
'''
import requests
from bs4 import BeautifulSoup

url = "https://www.shiyebian.com/shandong/binzhou/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

response = requests.get(url, headers=headers)

# 👇 关键：强制指定编码为 UTF-8
response.encoding = 'utf-8'

# 现在 response.text 就是正确解码的中文
soup = BeautifulSoup(response.text, 'html.parser')

div = soup.find('div', class_='ws-list-items')
if div:
    for li in div.find_all('li'):
        text = li.find('a').get_text(strip=True)
        print(text)
        a_href = li.find('a').get('href')
        print(a_href)
        l_span = li.find('span').get_text(strip=True)
        print(l_span)
        break
        
else:
    print("未找到目标区域")




