import requests
import re
import json
import os

# 目标网址：长江现货铜价
url = "https://www.metcom.com.cn/market/shanghai_spot.html"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers, timeout=30)
    response.encoding = 'utf-8'
    html = response.text
    
    # 使用正则表达式精准匹配“1#铜”这一行之后的均价数字
    # 匹配逻辑：在“1#铜”后面找第一个出现的包含逗号的数字
    match = re.search(r'1#铜.*?(\d{1,3}(?:,\d{3})+)', html, re.S)
    
    if match:
        price_str = match.group(1).replace(',', '') # 去掉逗号，变成 103690
        price = int(price_str)
        from datetime import datetime
        today = datetime.now().strftime('%m-%d') # 匹配你图上的 01-07 格式

        # 读取并更新 data.json
        data_file = 'data.json'
        if os.path.exists(data_file):
            with open(data_file, 'r') as f:
                data = json.load(f)
        else:
            data = []

        # 检查今天是否已记录，防止重复
        if not data or data[-1]['d'] != today:
            data.append({"d": today, "v": price})
            with open(data_file, 'w') as f:
                json.dump(data, f)
            print(f"成功抓取价格: {price}")
        else:
            print("今日价格已存在，无需更新")
    else:
        print("未匹配到价格，请检查网页结构")

except Exception as e:
    print(f"发生错误: {e}")
