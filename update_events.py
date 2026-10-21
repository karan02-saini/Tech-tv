import urllib.request
import json
import re

PAGE_URL = "https://dekhobhai.pages.dev/"
EVENTS_JSON_PATH = "events.json"

def fetch_live_events():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36",
        "Referer": PAGE_URL
    }
    
    try:
        print("Fetching live page content...")
        req = urllib.request.Request(PAGE_URL, headers=headers)
        with urllib.request.urlopen(req) as response:
            html_content = response.read().decode('utf-8')
            
        # Matches aur link endpoints extract karne ke liye pattern
        matches = re.findall(r'href=["\'](play\.html\?id=([a-zA-Z0-9_]+))["\'][^>]*>(.*?)</a>', html_content, re.DOTALL)
        
        events_list = []
        for index, match in enumerate(matches):
            relative_url, stream_id, title_raw = match
            clean_title = re.sub(r'<[^>]+>', '', title_raw).strip()
            
            if not clean_title:
                clean_title = f"Live Match {index + 1}"

            event_obj = {
                "id": f"event_{stream_id}",
                "title": clean_title,
                "category": "Live Sports",
                "webUrl": f"{PAGE_URL}{relative_url}",
                "streamUrl": "", 
                "isLive": True
            }
            events_list.append(event_obj)
            
        with open(EVENTS_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(events_list, f, indent=4)
            
        print(f"Successfully generated {len(events_list)} live events in events.json.")
        
    except Exception as e:
        print(f"Error fetching live events: {e}")

if __name__ == "__main__":
    fetch_live_events()
