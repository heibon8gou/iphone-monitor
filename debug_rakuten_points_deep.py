
import asyncio
import re
from playwright.async_api import async_playwright

async def debug_rakuten_points_deep():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            # Main iPhone Page
            url = "https://network.mobile.rakuten.co.jp/product/iphone/"
            print(f"Visiting {url}")
            await page.goto(url, wait_until="domcontentloaded")
            await page.wait_for_timeout(3000)
            
            # Find campaign links
            # Valid patterns usually contain 'campaign' and 'point'
            links = await page.locator("a[href*='campaign']").all()
            
            campaign_urls = set()
            for link in links:
                href = await link.get_attribute("href")
                if href and "point" in href and "iphone" in href:
                    if not href.startswith("http"):
                        href = "https://network.mobile.rakuten.co.jp" + href
                    campaign_urls.add(href)
            
            print(f"Found {len(campaign_urls)} potential campaign URLs: {campaign_urls}")
            
            for c_url in campaign_urls:
                print(f"--- Visiting Campaign: {c_url} ---")
                try:
                    await page.goto(c_url, wait_until="domcontentloaded")
                    await page.wait_for_timeout(2000)
                    
                    content = await page.content()
                    
                    # 1. Identify Target Models
                    # Look for model names in Title or H1
                    title = await page.title()
                    h1s = await page.locator("h1").all_text_contents()
                    page_text = title + " " + " ".join(h1s)
                    
                    target_models = []
                    if "16e" in page_text: target_models.append("iPhone 16e")
                    if "16" in page_text and "16e" not in page_text: target_models.append("iPhone 16") # simplistic
                    
                    print(f"Target Models inferred: {target_models}")
                    
                    # 2. Extract Max Points
                    # Regex for "最大Xポイント" or "Xポイント還元"
                    # We want the largest number associated with points
                    matches = re.findall(r'([\d,]{4,})\s*ポイント', content)
                    if matches:
                        # cleanup
                        nums = [int(m.replace(',', '')) for m in matches]
                        max_points = max(nums)
                        print(f"Max Points Found: {max_points}")
                    else:
                        print("No point values found.")
                        
                except Exception as e:
                    print(f"Error checking {c_url}: {e}")
                    
        except Exception as e:
            print(e)
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_rakuten_points_deep())
