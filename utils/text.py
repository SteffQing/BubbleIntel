from datatypes.bubblemap import BubbleMapData, ScoreResponse
from datatypes.mobula import TokenData

from services.bubblemap import generate_bubblemap_insight


def generate_token_caption(
    data: TokenData,
    score: ScoreResponse | str,
    bubblemap: BubbleMapData | None = None
) -> str:

    caption = format_token_data(data)
    caption += format_score_insight(score)

    if bubblemap:
        bmap_caption =  generate_bubblemap_insight(bubblemap['full_name'], bubblemap["symbol"], data['total_supply'], bubblemap["nodes"])
        print(f"Bubblemap Caption: {len(bmap_caption)}")
        return bmap_caption
        caption += bmap_caption

    return caption

def format_token_data(data: TokenData):
    
    name = data["name"]
    symbol = data["symbol"]
    price = data["price"]
    market_cap = data["market_cap"]
    volume = data["volume"]
    liquidity = data["liquidity"]
    price_change_24h = data["price_change_24h"]
    ath = data["ath"]
    atl = data["atl"]
    rank = data["rank"]

    trend_emoji = "📈" if price_change_24h >= 0 else "📉"
    change_text = f"{trend_emoji} 24h Change: {price_change_24h:.2f}%"
    rank_badge = f"🏅 Ranked #{rank}" if 0 < rank <= 100 else ""

    return (
        f"💠 <b>{name} ({symbol})</b>\n"
        f"{rank_badge}\n\n"
        f"💵 Price: ${price:,.4f}\n"
        f"📊 Market Cap: ${market_cap:,.0f}\n"
        f"🔄 Volume (24h): ${volume:,.0f}\n"
        f"💧 Liquidity: ${liquidity:,.0f}\n"
        f"{change_text}\n"
        f"🔺 All-Time High: ${ath:,.4f}\n"
        f"🔻 All-Time Low: ${atl:,.4f}"
    )


def format_score_insight(score: ScoreResponse | str) -> str:
    if isinstance(score, str):
        return f"\n\n📊 <b>Token Score</b>\n⚠️ Error fetching score: {score}"

    return (
        f"\n\n📊 <b>Token Score</b>\n"
        f"🔹 Decentralization: {score['decentralisation_score']:.2f}\n"
        f"🏦 In CEX: {score['identified_supply']['percent_in_cexs']:.2f}%\n"
        f"📜 In Contracts: {score['identified_supply']['percent_in_contracts']:.2f}%"
    )
