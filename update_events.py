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
        print("Fetching page content...")
        req = urllib.request.Request(PAGE_URL, headers=headers)
        with urllib.request.urlopen(req) as response:
            html_content = response.read().decode('utf-8')
            
        print(f"HTML fetched successfully. Length: {len(html_content)}")
        
        # Sabse broad regex jo kisi bhi href ke andar 'play.html' ho usko pakad lega
        pattern = r'href=["\']([^"\']*play\.html[^"\']*)["\'][^>]*>(.*?)</a>'
        matches = re.findall(pattern, html_content, re.DOTALL | re.IGNORECASE)
        print(f"Total matches found: {len(matches)}")
        
        events_list = []
        for index, match in enumerate(matches):
            relative_url, title_raw = match
            clean_title = re.sub(r'<[^>]+>', '', title_raw).strip()
            
            if not clean_title or "http" in clean_title or len(clean_title) < 2:
                clean_title = f"Live Match {index + 1}"

            # ID extract karne ke liye
            id_match = re.search(r'id=([a-zA-Z0-9_-]+)', relative_url)
            stream_id = id_match.group(1) if id_match else f"match_{index}"

            # URL formatting
            if relative_url.startswith("http"):
                web_url = relative_url
            elif relative_url.startswith("/"):
                web_url = f"https://dekhobhai.pages.dev{relative_url}"
            else:
                web_url = f"https://dekhobhai.pages.dev/{relative_url}"

            event_obj = {
                "id": f"event_{stream_id}",
                "title": clean_title,
                "category": "Live Sports",
                "webUrl": web_url,
                "streamUrl": "", 
                "isLive": True
            }
            
            if event_obj not in events_list:
                events_list.append(event_obj)
                
        with open(EVENTS_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(events_list, f, indent=4)
            
        print(f"Successfully generated {len(events_list)} live events in events.json.")
        
    except Exception as e:
        print(f"Error fetching live events: {e}")

if __name__ == "__main__":
    fetch_live_events()
