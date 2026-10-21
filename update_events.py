import asyncio
from playwright.async_api import async_playwright

PAGE_URL = "https://dekhobhai.pages.dev/"

async def fetch_live_events():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            print("Navigating with Playwright...")
            await page.goto(PAGE_URL, timeout=60000)
            await page.wait_for_timeout(5000)
            
            # Page ke saare anchor (<a>) tags ke innerHTML aur href nikal lete hain
            links = await page.evaluate('''() => {
                const anchors = Array.from(document.querySelectorAll('a'));
                return anchors.map(a => ({href: a.href, text: a.innerText.trim()}));
            }''')
            
            print(f"Total <a> tags found: {len(links)}")
            for item in links[:20]:
                print(f"Link -> {item['href']} | Text -> {item['text']}")
                
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(fetch_live_events())
