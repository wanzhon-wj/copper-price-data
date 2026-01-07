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
    
    # 【策略升级】直接搜索页面上紧跟在“1#铜”之后，且带有逗号的数字 (如 103,690)
    # 或者直接搜索类似 103XXX 的六位数字
    match = re.search(r'(\d{3,3},\d{3,3})', html)
    
    if match:
        price_str = match.group(1).replace(',', '')
        price = int(price_str)
        today = datetime.now().strftime('%m-%d')

        # 只要抓到数字大于 50000，就认为是合理的铜价
        if price > 50000:
            final_data = [{"d": today, "v": price}]
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(final_data, f)
            print(f"抓取成功！价格为: {price}")
        else:
            print(f"抓取到的数字 {price} 似乎不是铜价，请检查")
    else:
        print("依然无法匹配，正在打印网页前500字供调试：")
        print(html[:500])

except Exception as e:
    print(f"程序运行报错: {e}")
