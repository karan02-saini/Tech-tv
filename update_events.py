import asyncio
from playwright.async_api import async_playwright

PAGE_URL = "https://dekhobhai.pages.dev/"

async def fetch_live_events():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        try:
            print("Navigating with anti-detection...")
            await page.goto(PAGE_URL, timeout=60000, wait_until="networkidle")
            await page.wait_for_timeout(5000)
            
            # Asli rendered page ke saare links aur unka text nikal lete hain
            links = await page.evaluate('''() => {
                const anchors = Array.from(document.querySelectorAll('a'));
                return anchors.map(a => ({href: a.getAttribute('href'), text: a.innerText.trim()}));
            }''')
            
            print(f"Total links found: {len(links)}")
            for item in links:
                print(f"HREF: {item['href']} | TEXT: {item['text']}")
                
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(fetch_live_events())
