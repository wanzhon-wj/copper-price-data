import requests
import re
import json
import os
from datetime import datetime

# 目标网址：长江现货
url = "https://www.metcom.com.cn/market/shanghai_spot.html"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers, timeout=30)
    response.encoding = 'utf-8'
    html = response.text
    
    # 【核心修改】精准定位：先找到“1#铜”，再找它后面紧跟的带逗号的6位数字
    # 这个正则会过滤掉像 99811 这种不带逗号或位数不对的杂质
    match = re.search(r'1#铜.*?(\d{3,3},\d{3,3})', html, re.S)
    
    if match:
        price_str = match.group(1).replace(',', '') # 把 "103,690" 变成 103690
        price = int(price_str)
        today = datetime.now().strftime('%m-%d')

        data_file = 'data.json'
        if os.path.exists(data_file):
            with open(data_file, 'r') as f:
                try:
                    data = json.load(f)
                except:
                    data = []
        else:
            data = []

        # 更新逻辑：如果今天没数据，或者数值变了，就更新
        if not data or data[-1]['d'] != today or data[-1]['v'] != price:
            data.append({"d": today, "v": price})
            # 只保留最近 7 天数据，防止文件过大
            data = data[-7:] 
            with open(data_file, 'w') as f:
                json.dump(data, f)
            print(f"成功抓取正确均价: {price}")
        else:
            print("数据已是最新，无需更新")
    else:
        print("未能匹配到价格，请检查网页结构")

except Exception as e:
    print(f"运行出错: {e}")
