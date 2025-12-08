
import asyncio
import re
from playwright.async_api import async_playwright

async def debug_16e():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            # 1. Check Fee Page textual content for "16e"
            url = "https://network.mobile.rakuten.co.jp/product/iphone/fee/"
            print(f"Checking {url}...")
            await page.goto(url, wait_until="domcontentloaded")
            content = await page.content()
            if "16e" in content:
                print("FOUND '16e' in Fee Page source!")
            else:
                print("NOT FOUND '16e' in Fee Page source.")

            # 2. Check Specific Product Page (Guess)
            # Standard pattern: /product/iphone/iphone-16/ -> /product/iphone/iphone-16e/ ?
            url_prod = "https://network.mobile.rakuten.co.jp/product/iphone/iphone-16e/"
            print(f"Checking {url_prod}...")
            resp = await page.goto(url_prod, wait_until="domcontentloaded")
            if resp.status == 404:
                print("Product page 404.")
            else:
                print(f"Product page loaded! Title: {await page.title()}")
                # Try to find price
                # often hidden in a 'price' section or via API
                # Look for "円"
                txt = await page.body.text_content()
                prices = re.findall(r'([\d,]+)円', txt)
                print(f"Potential prices on product page: {prices[:5]}")
            
            # 3. Check Campaign Page for Price
            url_camp = "https://network.mobile.rakuten.co.jp/campaign/iphone-point-iphone-16e/"
            print(f"Checking {url_camp}...")
            await page.goto(url_camp, wait_until="domcontentloaded")
            txt_camp = await page.body.text_content()
            # "本体価格X円" ?
            prices_camp = re.findall(r'本体価格.*?([\d,]+)円', txt_camp)
            print(f"Potential Device Prices on Campaign: {prices_camp}")

        except Exception as e:
            print(e)
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_16e())
