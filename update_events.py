import asyncio
import json
import re
from playwright.async_api import async_playwright

PAGE_URL = "https://dekhobhai.pages.dev/"
EVENTS_JSON_PATH = "events.json"

async def fetch_live_events():
    async with async_playwright() as p:
        # Headless browser launch karna
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            print("Navigating to live page with Playwright...")
            await page.goto(PAGE_URL, timeout=60000)
            
            # Page ka JavaScript load hone ka wait karna
            await page.wait_for_load_state("networkidle")
            
            # Poora rendered HTML uthana
            html_content = await page.content()
            
            # Match links aur titles extract karne ke liye regex
            matches = re.findall(r'href=["\'](play\.html\?[^"\']+)["\'][^>]*>(.*?)</a>', html_content, re.DOTALL)
            
            events_list = []
            for index, match in enumerate(matches):
                relative_url, title_raw = match
                clean_title = re.sub(r'<[^>]+>', '', title_raw).strip()
                
                if not clean_title or "http" in clean_title:
                    clean_title = f"Live Match {index + 1}"

                id_match = re.search(r'id=([a-zA-Z0-9_-]+)', relative_url)
                stream_id = id_match.group(1) if id_match else f"match_{index}"

                event_obj = {
                    "id": f"event_{stream_id}",
                    "title": clean_title,
                    "category": "Live Sports",
                    "webUrl": f"https://dekhobhai.pages.dev/{relative_url}" if not relative_url.startswith("http") else relative_url,
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
            with open(EVENTS_JSON_PATH, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=4)
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(fetch_live_events())
