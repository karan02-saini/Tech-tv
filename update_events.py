import asyncio
import json
import re
from playwright.async_api import async_playwright

PAGE_URL = "https://dekhobhai.pages.dev/"
EVENTS_JSON_PATH = "events.json"

async def fetch_live_events():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            print("Navigating to live page with Playwright...")
            await page.goto(PAGE_URL, timeout=60000)
            await page.wait_for_load_state("networkidle")
            
            html_content = await page.content()
            
            # Updated Regex: Ab ye /Fancodee/ ya kisi bhi folder ke andar ke play.html links ko bhi pakad lega
            matches = re.findall(r'href=["\']([^"\']*play\.html\?[^"\']*)["\'][^>]*>(.*?)</a>', html_content, re.DOTALL)
            
            events_list = []
            for index, match in enumerate(matches):
                relative_url, title_raw = match
                clean_title = re.sub(r'<[^>]+>', '', title_raw).strip()
                
                if not clean_title or "http" in clean_title:
                    clean_title = f"Live Match {index + 1}"

                id_match = re.search(r'id=([a-zA-Z0-9_-]+)', relative_url)
                stream_id = id_match.group(1) if id_match else f"match_{index}"

                # Handle absolute vs relative URLs properly
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
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(fetch_live_events())
