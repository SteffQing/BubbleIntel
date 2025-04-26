from playwright.async_api import async_playwright
from io import BytesIO

from services.httpx import get_client
from datatypes.constants import Network
from datatypes.bubblemap import AvailabilityResponse, BubbleMapData, ScoreResponse
from utils.index import format_dt_update, format_large_number, truncate_address

class BubbleMap:
    async def isIframeAvailable(self, token: str, chain: Network):
        url= f"https://api-legacy.bubblemaps.io/map-availability?chain={chain}&token={token}"
        client = get_client()
        response = await client.get(url)
        is_available: AvailabilityResponse = response.json()
        
        if is_available["status"] == "OK":
            return is_available["availability"]
        else: 
            return False
        
    async def getScore(self, token: str, chain: Network):
        url = f"https://api-legacy.bubblemaps.io/map-metadata?chain={chain}&token={token}"
        client = get_client()
        response = await client.get(url)
        score: ScoreResponse = response.json()
        
        if score["status"] == "OK":
            return score
        else:
            return score["message"]
        
    async def getBubblemapData(self, token: str, chain: Network):
        url = f"https://api-legacy.bubblemaps.io/map-data?token={token}&chain={chain}"
        client = get_client()
        response = await client.get(url)
        
        if response.status_code == 401:
            return None
        bubblemap_data: BubbleMapData = response.json()
        return bubblemap_data
        
        

    # This method shows the full bubblemap and also includes the wallet list for users to see
    async def screenshot_bubblemap(self, token_address: str, chain: Network):
        url = f"https://app.bubblemaps.io/{chain}/token/{token_address}?hide_context&small_text&prevent_scroll_zoom&mode=0"

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
            page = await context.new_page()

            await page.goto(url, wait_until="load")

            try:
                await page.wait_for_selector("text=Bubblemaps is optimized for Chrome", timeout=10000)
                await page.click("text=CLOSE")
            except:
                pass
                
            screenshot_bytes = b""
            try:
                svg = await page.wait_for_selector("svg#svg", timeout=20000)
                await page.wait_for_timeout(2000)
                if svg:
                    # await svg.screenshot(path=image_bytes)
                    screenshot_bytes = await svg.screenshot(type="png")

            finally:
                await browser.close()
                
            image_bytes = BytesIO(screenshot_bytes)
            image_bytes.seek(0)
            return image_bytes
            
       
from collections import defaultdict


def generate_advanced_bubblemap_insight(token_symbol: str, bubblemap: BubbleMapData | None) -> str:
    if not bubblemap:
        return "No data available to generate insights."
    nodes, links = bubblemap["nodes"], bubblemap["links"]
    
    dead_wallets: list[float] = []
    sent_amounts = defaultdict(float)
    received_amounts = defaultdict(float)
    clusters = defaultdict(set)

    for node in nodes:
        name = str(node.get("name", "")).lower()
        address = node.get("address", "").lower()
        if "null" in name or "dead" in name or "0xdead" in address:
            dead_wallets.append(node["percentage"])

    for link in links:
        src, tgt = link["source"], link["target"]
        fwd, bwd = link["forward"], link["backward"]

        if fwd > 0:
            sent_amounts[src] += fwd
            received_amounts[tgt] += fwd
            clusters[src].add(tgt)
            clusters[tgt].add(src)

        if bwd > 0:
            sent_amounts[tgt] += bwd
            received_amounts[src] += bwd
            clusters[src].add(tgt)
            clusters[tgt].add(src)

    lines = [f"\n\n💡 <b>BubbleMap Insights</b> <i>({format_dt_update(bubblemap['dt_update'])})</i>"]

    if dead_wallets:
        percentage = sum(p for p in dead_wallets)
        count = len(dead_wallets)
        lines.append(f"🔥 {count} Burn Wallet{'s' if count > 1 else ''} holds {percentage:.2f}% of supply")
        
        
    if received_amounts:
        top_receiver = max(received_amounts.items(), key=lambda x: x[1])
        idx, amt = top_receiver
        lines.append(f"📥 Top Receiver: <code>{truncate_address(nodes[idx]["address"])}</code> received {format_large_number(amt)} {token_symbol}")
        
    if sent_amounts:
        top_sender  = max(sent_amounts.items(), key=lambda x: x[1])
        idx, amt = top_sender 
        lines.append(f"📤 Top Sender: <code>{truncate_address(nodes[idx]["address"])}</code> received {format_large_number(amt)} {token_symbol}")
    

    cluster_loops = [grp for grp in clusters.values() if len(grp) > 5]
    if cluster_loops:
        lines.append(f"🔗 Clustered Wallets: {len(cluster_loops)} sets of wallets exchanged large volumes")

    top_20_total = sum(received_amounts[i] + sent_amounts[i] for i in sorted(
        set(received_amounts) | set(sent_amounts), key=lambda x: -(received_amounts[x] + sent_amounts[x])
    )[:20])
    overall_flow = sum(received_amounts.values()) + sum(sent_amounts.values())
    if overall_flow > 0:
        pct = (top_20_total / overall_flow) * 100
        lines.append(f"🧠 Transfer Density: Top 20 wallets account for {pct:.2f}% of all observed flow")

    return "\n".join(lines)

