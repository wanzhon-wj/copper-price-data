import requests
import re
import json
import os
from datetime import datetime

url = "https://www.metcom.com.cn/market/shanghai_spot.html"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

try:
    response = requests.get(url, headers=headers, timeout=30)
    response.encoding = 'utf-8'
    html = response.text
    
    # 尝试匹配 103,690 这种格式
    match = re.search(r'1#铜.*?(\d{3},\d{3})', html, re.S)
    
    # 如果上面没抓到，尝试匹配纯 6 位数字
    if not match:
        match = re.search(r'1#铜.*?(\d{6})', html, re.S)

    if match:
        price_str = match.group(1).replace(',', '')
        price = int(price_str)
        today = datetime.now().strftime('%m-%d')
        
        # 强制保存最新数据
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump([{"d": today, "v": price}], f)
        print(f"数据更新成功: {price}")
    else:
        print("依然无法匹配，请检查网页内容")
except Exception as e:
    print(f"出错: {e}")
