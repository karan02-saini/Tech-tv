import json
import re
import urllib.request

PAGE_URL = "https://dekhobhai.pages.dev/"
EVENTS_JSON_PATH = "events.json"

def fetch_live_events():
    req = urllib.request.Request(
        PAGE_URL, 
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    )
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            print("HTML length received:", len(html))
            
            # Saare href links dhoond kar print karwa lete hain
            hrefs = re.findall(r'href=["\']([^"\']+)["\']', html)
            print(f"Total hrefs found: {len(hrefs)}")
            for h in hrefs[:30]:  # Pehle 30 links print karwayenge logs mein dekhne ke liye
                print("Found link:", h)
                
    except Exception as e:
        print("Failed to fetch:", e)

if __name__ == "__main__":
    fetch_live_events()
