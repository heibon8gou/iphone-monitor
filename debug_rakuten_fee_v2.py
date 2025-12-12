
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(locale='ja-JP')
        page = await context.new_page()
        
        url = "https://network.mobile.rakuten.co.jp/product/iphone/fee/"
        print(f"Navigating to {url}...")
        await page.goto(url, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        
        sections = await page.locator(".product-iphone-Fee_Media").all()
        if len(sections) > 0:
            html = await sections[0].inner_html()
            with open("rakuten_section_dump.html", "w", encoding="utf-8") as f:
                f.write(html)
            print("Dumped rakuten_section_dump.html")
        else:
            print("No sections found, dumping full body")
            html = await page.content()
            with open("rakuten_full_dump.html", "w", encoding="utf-8") as f:
                f.write(html)
                
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
