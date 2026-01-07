import requests
import re
import json
from datetime import datetime

# 切换到生意社数据源，这个网址对机器人更友好
url = "http://www.100ppi.com/show/shanghai-1.html"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers, timeout=30)
    response.encoding = 'utf-8'
    html = response.text
    
    # 匹配生意社页面上的“1#电解铜”价格，通常是 10XXXX 格式
    # 这里的正则兼容 10万以上 和 10万以下 的价格
    match = re.search(r'1#电解铜.*?(\d{5,6})', html, re.S)
    
    if match:
        price = int(match.group(1))
        today = datetime.now().strftime('%m-%d')

        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump([{"d": today, "v": price}], f)
        print(f"抓取成功！备用源价格为: {price}")
    else:
        print("备用源匹配失败，请检查网页结构")
        print("源码片段:", html[:300].replace('\n', ' '))

except Exception as e:
    print(f"运行报错: {e}")
