import requests, re, json, os
from datetime import datetime
url = "https://www.metcom.com.cn/market/shanghai_spot.html"
res = requests.get(url, timeout=30)
res.encoding = 'utf-8'
# 精准匹配 1#铜 后的均价
match = re.search(r'1#铜.*?(\d{3,3},\d{3,3})', res.text, re.S)
if match:
    price = int(match.group(1).replace(',', ''))
    today = datetime.now().strftime('%m-%d')
    with open('data.json', 'w') as f:
        json.dump([{"d": today, "v": price}], f)
