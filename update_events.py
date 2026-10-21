import json
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
            # Print first 500 chars of HTML to check what we are getting
            print("Snippet:", html[:500])
    except Exception as e:
        print("Failed to fetch:", e)

if __name__ == "__main__":
    fetch_live_events()
