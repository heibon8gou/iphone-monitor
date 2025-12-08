
import asyncio
import re
from playwright.async_api import async_playwright

async def debug_ahamo_v3():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            url = "https://ahamo.com/products/iphone/"
            print(f"Visiting {url}")
            await page.goto(url, wait_until="domcontentloaded")
            await page.wait_for_timeout(5000)
            
            links = await page.locator("a.a-product-thumbnail-link").all()
            print(f"Found {len(links)} links")
            
            for i, link in enumerate(links):
                # Name
                name_el = link.locator(".a-product-thumbnail__name")
                if await name_el.count() == 0:
                    name_el = link.locator(".a-product-thumbnail-link__name")
                
                if await name_el.count() > 0:
                    name = await name_el.first.text_content()
                    print(f"--- {name.strip()} ---")
                
                # Dump all text with "円" to see what we have
                text_content = await link.text_content()
                prices = re.findall(r'[\d,]+円', text_content)
                print(f"All captured prices: {prices}")
                
                # Check specific new selectors
                # 1. Main Price Label (often Gross or "Case of XXX GB")
                main_price_block = link.locator(".a-product-thumbnail__price")
                if await main_price_block.count() > 0:
                     print(f"Main Price Block: {await main_price_block.first.text_content()}")
                
                # 2. Kaedoki (Program) Exemption
                # We inferred Exemption = Gross - Effective - Discount, but maybe it's listed?
                # Look for "residual" or "exemption" related text?
                # Actually, ahamo lists:
                # "Customer Burden" (Effective)
                # "Discount" (Official)
                # Does it listing Exemption?
                # Let's see the full text again.
                # Let's see the full text again.
                sanitized_text = text_content.replace('\n', ' ')[:200]
                print(f"Full Text: {sanitized_text}...")

        except Exception as e:
            print(e)
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_ahamo_v3())
