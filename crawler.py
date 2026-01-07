import requests
import json
import datetime
import re

def get_price():
    url = 'http://www.100ppi.com/price/plist-123.html'
    try:
        r = requests.get(url, timeout=10)
        match = re.search(r'(\d{5,6})', r.text)
        return int(match.group(1)) if match else None
    except:
        return None

def update():
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    price = get_price()
    if not price: return

    with open('data.json', 'r') as f:
        data = json.load(f)
    
    if any(item['d'] == today for item in data): return

    data.append({"d": today, "v": price})
    with open('data.json', 'w') as f:
        json.dump(data, f)

if __name__ == '__main__':
    update()
