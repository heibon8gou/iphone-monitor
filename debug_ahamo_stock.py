
import asyncio
from playwright.async_api import async_playwright
import re

async def debug_ahamo_stock():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # 1. Visit main product list
        url = "https://ahamo.com/products/iphone/"
        print(f"Checking {url}...")
        await page.goto(url, wait_until="networkidle") # Wait for network idle
        
        # Explicit wait
        await page.wait_for_selector("a.a-product-thumbnail-link")
        
        # 2. Pick first product link
        links = await page.locator("a.a-product-thumbnail-link").all()
        if not links:
            print("No product links found.")
            await browser.close()
            return

        first_link = links[0]
        href = await first_link.get_attribute("href")
        full_url = "https://ahamo.com" + href if not href.startswith("http") else href
        print(f"Visiting Product: {full_url}")
        
        await page.goto(full_url, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        
        # 3. Look for Color / Stock selectors
        # Usually there are radio buttons or buttons for Color
        # And storage buttons.
        # Stock status often changes based on selection.
        
        # Dump buttons
        buttons = await page.locator("button, input[type='radio']").all()
        print(f"Found {len(buttons)} interactables.")
        
        # Look for "在庫" (Stock) text in page
        content = await page.content()
        if "在庫" in content:
            print("Found '在庫' in content.")
            matches = re.findall(r'.{0,20}在庫.{0,20}', content)
            for m in matches[:5]:
                print(f"Match: {m}")
        
        # Try to find specific color elements
        # Hints: aria-label="Black", class="color-swatch", etc.
        color_els = await page.locator("[class*='color'], [class*='Color']").all()
        print(f"Found {len(color_els)} potential color elements.")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_ahamo_stock())
