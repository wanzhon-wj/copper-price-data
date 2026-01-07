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
    
    # 更加强力的匹配：直接找“1#铜”后面那个带逗号的数字
    match = re.search(r'1#铜.*?(\d{3,3},\d{3,3})', html, re.S)
    
    if match:
        price_str = match.group(1).replace(',', '')
        price = int(price_str)
        today = datetime.now().strftime('%m-%d')

        # 强行生成数据，不检查旧数据
        new_data = [{"d": today, "v": price}]
        
        with open('data.json', 'w') as f:
            json.dump(new_data, f)
        print(f"写入成功: {price}")
    else:
        print("抓取失败，未找到价格数字")
except Exception as e:
    print(f"错误: {e}")
