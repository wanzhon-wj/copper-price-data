import requests
import re
import json
from datetime import datetime

# 目标网址：上海金属网长江现货
url = "https://www.metcom.com.cn/market/shanghai_spot.html"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers, timeout=30)
    response.encoding = 'utf-8'
    html = response.text
    
    # 【精准匹配】直接定位图片中显示的“今日均价/涨跌”下方的绿色数字
    # 这里的正则专门寻找紧跟在“1#铜”之后且符合“10X,XXX”格式的数字
    match = re.search(r'1#铜.*?(\d{3,3},\d{3,3})', html, re.S)
    
    if match:
        # 清理提取到的字符串（去掉逗号），转换为纯数字 103690
        price_val = match.group(1).replace(',', '')
        price = int(price_val)
        today = datetime.now().strftime('%m-%d')

        # 强制更新 data.json，不进行旧数据对比，确保立即生效
        final_data = [{"d": today, "v": price}]
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(final_data, f)
            
        print(f"成功抓取今日均价: {price}")
    else:
        print("未能在页面中匹配到 1#铜 的价格数据，请核对网页源码")

except Exception as e:
    print(f"抓取过程中发生错误: {e}")
