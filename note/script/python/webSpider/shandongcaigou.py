'''
山东采购网
'''
import requests
import time
import json
import base64
from bs4 import BeautifulSoup

def fetch_sdgp_search(title="机房运维", max_pages=5):
    url = "http://sdgp.sdcz.gov.cn:8087/api/website/site/searchAll"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "http://sdgp.sdcz.gov.cn:8087",
        "Referer": "http://sdgp.sdcz.gov.cn:8087/"
    }
    
    all_results = []
    
    for page in range(1, max_pages + 1):
        payload = {
            "type": "01,02,03",
            "currentPage": page,
            "pageSize": 10,
            "title": title,
            "area": "",
            "date": "",
            "homePage": 1
        }
        
        try:
            print(f"正在抓取第 {page} 页...")
            response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
            response.raise_for_status()
            data = response.json()
            # print("原始响应:", data)
            
            records = data.get("data").get("data").get("records")
            print(f"第 {page} 页获取 {len(records)} 条记录。")
            all_results.extend(records)
           
        except Exception as e:
            print(f"请求第 {page} 页时出错：{e}")
            break
        
        # 礼貌性延迟，避免触发反爬
        time.sleep(1)
    
    return all_results

def getDetail(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "http://sdgp.sdcz.gov.cn:8087/"
    }
    response = requests.get(url, headers=headers, timeout=10)
    data = response.json()
    # print("原始响应:", data)
    body = data.get("data").get("data").get("body")
    body_bytes = base64.b64decode(body)
    body_text = body_bytes.decode('gbk')
    # print("原始响应:", body_text)
    table = BeautifulSoup(body_text, 'html.parser')
    json_data = extract_table_text(table)
    print(clean_for_gbk(json_data))

def clean_for_gbk(text):
    # 方法1：用 errors='replace' 自动替换无法编码的字符为 ?
    # 方法2：用 errors='ignore' 直接丢弃
    # 方法3：手动替换常见问题字符
    text = text.replace('\u2003', ' ')  # EM SPACE → 普通空格
    text = text.replace('\u2002', ' ')  # EN SPACE
    text = text.replace('\u2009', ' ')  # THIN SPACE
    text = text.replace('\xa0', ' ')    # NO-BREAK SPACE
    return text
    
def extract_table_text(table, separator=' ', line_break=True):
    if line_break:
        # 按行提取，每行内部用 separator 连接
        lines = []
        for tr in table.find_all('tr'):
            cells = tr.find_all(['td', 'th'])
            texts = [cell.get_text(strip=True) for cell in cells if cell.get_text(strip=True)]
            if texts:
                lines.append(separator.join(texts))
        return '\n'.join(lines)
    else:
        # 所有文字合并成一段
        return table.get_text(separator=separator, strip=True)


if __name__ == "__main__":
    results = fetch_sdgp_search(title="机房运维", max_pages=3)
    
    print(f"\n共抓取到 {len(results)} 条公告。\n")
    
    for item in results:  # 打印前5条示例
        title = item.get("title", "N/A")
        userName = item.get("userName", "N/A")
        date = item.get("date", "")
        full_url = f"http://sdgp.sdcz.gov.cn:8087/api/website/site/getDetail?id="+item.get("id")+"&colCode="+item.get("colCode")+"&homePage=1"
        detail_page = f"http://www.ccgp-shandong.gov.cn/#/article/site/"+item.get("colCode")+"/"+item.get("id")
        print(f"{title} | {userName} | {date} | {detail_page}")
        getDetail(full_url)
        print("="*80)
        
        
        
        
        
        
        
        
        
        
        
        
        
