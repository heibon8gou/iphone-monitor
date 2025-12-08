
import asyncio
from playwright.async_api import async_playwright

async def debug_rakuten_stock():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # 1. Try known stock URL
        url_stock = "https://network.mobile.rakuten.co.jp/product/iphone/stock/"
        print(f"Checking {url_stock}...")
        resp = await page.goto(url_stock, wait_until="domcontentloaded")
        
        if resp.status == 404:
            print("Stock page 404.")
        else:
            print("Stock page loaded.")
            # Dump headings or look for tables
            headings = await page.locator("h1, h2, h3").all_text_contents()
            print(f"Headings: {headings[:5]}")
            
        # Dump HTML
        content = await page.content()
        with open("debug_stock_dump.html", "w", encoding="utf-8") as f:
            f.write(content)
        print(" dumped HTML to debug_stock_dump.html")

        await browser.close()

        await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_rakuten_stock())
