
import asyncio
import re
from playwright.async_api import async_playwright

async def debug_rakuten_campaigns():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            # Rakuten iPhone Main Page
            url = "https://network.mobile.rakuten.co.jp/product/iphone/"
            print(f"Visiting {url}")
            await page.goto(url, wait_until="domcontentloaded")
            await page.wait_for_timeout(5000)
            
            # Look for Campaign Banners / Text
            # Rakuten often puts "Max 20000 points" in large text.
            
            content = await page.content()
            
            # Simple regex for points
            # "最大20,000ポイント"
            point_matches = re.findall(r'最大([\d,]+)ポイント', content)
            print(f"Captured 'Max ... Points' text: {point_matches}")
            
            # Look for specific model campaigns
            # e.g. "iPhone 16e" ... "10,000 points"
            
            # Dump headings
            headings = await page.locator("h1, h2, h3, .heading").all()
            for h in headings:
                txt = await h.text_content()
                if "ポイント" in txt:
                    print(f"Heading with Points: {txt.strip()}")

        except Exception as e:
            print(e)
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_rakuten_campaigns())
