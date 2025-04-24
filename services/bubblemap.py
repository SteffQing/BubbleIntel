from playwright.async_api import async_playwright

from services.httpx import get_client
from utils.constants import cexs
from datatypes.constants import Network
from datatypes.bubblemap import AvailabilityResponse, BubbleMapData, Node, ScoreResponse
from utils.index import truncate_address

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
        out_path = f"bubblemap/{token_address}.png"

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
                
            try:
                svg = await page.wait_for_selector("svg#svg", timeout=20000)
                await page.wait_for_timeout(2000)
                if svg:
                    await svg.screenshot(path=out_path)
            finally:
                await browser.close()
            
            
def generate_bubblemap_insight(token_name: str, token_symbol: str, total_supply: float, nodes: list[Node]):
    if not nodes:
        return "No data available to generate insights."

    total_percent = 0
    dead_wallet = None
    top_exchanges = []
    top_individuals = []
    defi_contracts = []

    for node in nodes:
        percentage = node.get("percentage", 0)
        name = str(node.get("name", "")).lower()
        
        total_percent += percentage
        
        # Identify dead/burn wallet
        if "null" in name or "dead" in name or "0xdead" in node.get("address", "").lower():
            dead_wallet = node
        
        # Identify exchanges
        elif any(keyword in name for keyword in cexs):
            top_exchanges.append(node)
            
            
        elif node["is_contract"] is True:
            defi_contracts.append(node)

        # Otherwise, assume individual/private whale
        elif percentage >= 0.3:
            top_individuals.append(node)

    lines = [f"💡 <b>{token_name} ({token_symbol}) BubbleMap Insights </b>\n", f"<b>Total Supply (approx.):</b> {total_supply} {token_symbol}\n", f"<b>Top Holders Overview:</b> The top {len(nodes)} addresses alone hold around {total_percent}% of the total {token_symbol} supply\n", ]

    # Dead wallet insight
    if dead_wallet:
        lines.append(f"\n🔥 <b>Burn Wallet</b>\n{truncate_address(dead_wallet['address'])} holds {dead_wallet['percentage']:.2f}% of the total supply. "
                     f"This suggests a deflationary mechanism or intentional supply reduction.\n")

    # Exchange concentration
    if top_exchanges:
        lines.append(f"\n🏦 <b>Top Exchanges Holding {token_symbol}</b>\n")
        for ex in sorted(top_exchanges, key=lambda x: -x["percentage"])[:5]:
            lines.append(f"- {ex['name']} holds <b>{ex['percentage']:.2f}%</b> of supply.")
        lines.append("These wallets are likely used for liquidity and user deposits, but indicate some centralization risk.\n")

    # Individual whales
    if top_individuals:
        lines.append("\n🐋 <b>Top Non-Exchange Whales</b>\n")
        for whale in sorted(top_individuals, key=lambda x: -x["percentage"])[:5]:
            lines.append(f"- {whale['name']} with <b>{whale['percentage']:.2f}%</b> of supply.")
        lines.append("These addresses may belong to early investors or team wallets.\n")

    # Overall insight
    num_wallets_1p = sum(1 for n in nodes if n.get("percentage", 0) >= 1)
    if num_wallets_1p > 10:
        decentralization_note = "⚠️ <b>Token appears heavily concentrated</b>, with many wallets holding over 1% of supply."
    elif num_wallets_1p > 5:
        decentralization_note = "🔍 <b>Moderately decentralized</b>, but still some large holders to watch."
    else:
        decentralization_note = "✅ <b>Supply appears well-distributed</b>, with limited concentration among wallets."

    lines.append(f"\n📊 <b>Summary</b>:\n- Total wallets tracked: {len(nodes)}\n"
                 f"- Wallets holding ≥ 1%: {num_wallets_1p}\n"
                 f"{decentralization_note}")

    return "\n".join(lines)
