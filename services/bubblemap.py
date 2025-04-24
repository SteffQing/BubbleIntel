from playwright.sync_api import sync_playwright

from services.httpx import get_client
from utils.constants import Network
from utils.types import AvailabilityResponse

class BubbleMap:
    async def isIframeAvailable(self, token: str, chain: Network):
        url= f"https://api-legacy.bubblemaps.io/map-availability?chain={chain}&token={token}"
        client = get_client()
        response = await client.get(url)
        is_available: AvailabilityResponse = response.json()
        if is_available["status"] is "OK":
            return is_available["availability"]
        else: 
            return False
        
    # This method returns only the bubblemap, takes 10 seconds at average
    def screenshot_bubblemap(self, token_address: str, chain: Network ='eth'):
        url = f"https://app.bubblemaps.io/{chain}/token/{token_address}"
        out_path = f"bubblemap/{token_address}.png"
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1200, "height": 800})
            page.goto(url, wait_until="load", timeout=60000) 
            try:
                page.wait_for_selector("text=Bubblemaps is optimized for Chrome", timeout=10000)
                page.click("text=CLOSE")
            except:
                print("No Chrome optimization popup appeared.")
                
            page.wait_for_timeout(5000)
            page.screenshot(path=out_path)
            browser.close()

    # This method shows the full bubblemap but also includes the wallet list for users to see
    def screenshot_bubblemap_with_wallets(self, token_address: str, chain: Network ='eth'):
        url = f"https://app.bubblemaps.io/{chain}/token/{token_address}?hide_context&small_text&prevent_scroll_zoom"
        out_path = f"bubblemap/{token_address}.png"

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)  # use .launch(headless=False) to debug
            context = browser.new_context(viewport={'width': 1920, 'height': 1080})
            page = context.new_page()

            page.goto(url, wait_until="load")

            try:
                page.wait_for_selector("text=Bubblemaps is optimized for Chrome", timeout=10000)
                page.click("text=CLOSE")
            except:
                print("No Chrome optimization popup appeared.")
                
            try:
                svg = page.wait_for_selector("svg#svg", timeout=20000)
            except:
                print("SVG did not load in time.")
                browser.close()
                return

            page.wait_for_timeout(2000)

            if svg:
                svg.screenshot(path=out_path)

            browser.close()