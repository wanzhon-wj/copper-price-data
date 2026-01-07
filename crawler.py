import requests
import re
import json
import os
from datetime import datetime

# 目标：抓取图片中的 103,690
url = "https://www.metcom.com.cn/market/shanghai_spot.html"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Referer": "https://www.metcom.com.cn/"
}

try:
    # 增加 verify=False 防止 SSL 证书拦截
    response = requests.get(url, headers=headers, timeout=30, verify=False)
    response.encoding = 'utf-8'
    html = response.text
    
    # 策略：直接在全网页搜索“1#铜”之后第一个出现的带逗号的 6 位数字
    match = re.search(r'1#铜.*?(\d{3,3},\d{3,3})', html, re.S)
    
    if match:
        price_val = match.group(1).replace(',', '')
        price = int(price_val)
        today = datetime.now().strftime('%m-%d')

        # 强制写死数据结构，确保小程序能读到
        final_data = [{"d": today, "v": price}]
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(final_data, f)
        print(f"成功！抓取到价格: {price}")
    else:
        # 如果还是抓不到，说明网页返回了防爬虫页面
        print("依然匹配不到数字。网页前300个字符如下：")
        print(html[:300])

except Exception as e:
    print(f"运行出错: {e}")
