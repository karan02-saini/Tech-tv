import asyncio
import json
import re
from playwright.async_api import async_playwright

PAGE_URL = "https://dekhobhai.pages.dev/"
EVENTS_JSON_PATH = "events.json"

async def fetch_live_events():
    async with async_playwright() as p:
        # Launch browser with anti-detection arguments
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox"
            ]
        )
        
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        
        page = await context.new_page()
        
        try:
            print("Navigating to site bypassing bot detection...")
            await page.goto(PAGE_URL, timeout=60000, wait_until="networkidle")
            
            # Extra wait for Cloudflare challenge or JS rendering
            await page.wait_for_timeout(6000)
            
            html_content = await page.content()
            print(f"Rendered HTML length: {len(html_content)}")
            
            # Match links extract karne ke liye regex
            matches = re.findall(r'href=["\']([^"\']*play\.html\?[^"\']*)["\'][^>]*>(.*?)</a>', html_content, re.DOTALL)
            print(f"Total match links found: {len(matches)}")
            
            events_list = []
            for index, match in enumerate(matches):
                relative_url, title_raw = match
                clean_title = re.sub(r'<[^>]+>', '', title_raw).strip()
                
                if not clean_title or "http" in clean_title or len(clean_title) < 2:
                    clean_title = f"Live Match {index + 1}"

                id_match = re.search(r'id=([a-zA-Z0-9_-]+)', relative_url)
                stream_id = id_match.group(1) if id_match else f"match_{index}"

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
            print(f"Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(fetch_live_events())
