import requests
import re
import json
import os
from datetime import datetime

# 目标网址
url = "https://www.metcom.com.cn/market/shanghai_spot.html"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers, timeout=30)
    response.encoding = 'utf-8'
    html = response.text
    
    # 查找“1#铜”后面那个带逗号的均价数字
    match = re.search(r'1#铜.*?今日均价/涨跌.*?([\d,]+)', html, re.S)
    
    if match:
        # 提取并清理数字：去掉逗号，转为整数
        price_val = match.group(1).replace(',', '')
        price = int(price_val)
        today = datetime.now().strftime('%m-%d')

        # 强制重写：直接覆盖 data.json 为当前最新数据
        # 这样可以解决之前因为旧数据对比导致不更新的问题
        final_data = [{"d": today, "v": price}]
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(final_data, f)
            
        print(f"抓取成功！今日均价：{price}")
    else:
        # 如果正则匹配不到，打印一部分网页源码分析原因
        print("匹配失败，请检查网页结构是否变化")
        print(html[:500]) 

except Exception as e:
    print(f"发生错误: {e}")
