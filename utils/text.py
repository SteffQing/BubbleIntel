import re
from typing import Callable, Any

from datatypes.bubblemap import BubbleMapData, ScoreResponse
from datatypes.mobula import TokenData

from services.bubblemap import generate_advanced_bubblemap_insight
from utils.index import format_large_number, format_small_number


def generate_token_caption(
    data: TokenData,
    score: ScoreResponse | str,
    bubblemap: BubbleMapData | None = None
) -> str:

    caption = format_token_data(data)

    caption +=  generate_advanced_bubblemap_insight( data["symbol"], bubblemap)
    

    caption += format_score_insight(score)
    caption += generate_summary(caption)
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
    rank_badge = f"🏅 Ranked #{rank}" if 0 < rank <= 100 else None

    return (
        f"<b>{name} ({symbol})</b>\n\n"
        f"💠 <b>Token Info</b>\n"
        f"{rank_badge + "\n" if rank_badge else ""}"
        f"💵 Price: ${format_small_number(price)}\n"
        f"📊 Market Cap: ${market_cap:,.0f}\n"
        f"🔄 Volume (24h): ${volume:,.0f}\n"
        f"💧 Liquidity: ${liquidity:,.0f}\n"
        f"{change_text}\n"
        f"🔺 All-Time High: ${format_large_number(ath)}  🔻 All-Time Low: ${format_small_number(atl)}"
    )


def format_score_insight(score: ScoreResponse | str) -> str:
    if isinstance(score, str):
        return f"\n\n📊 <b>Token Score</b>\n⚠️ Error fetching score: {score}"

    return (
        f"\n\n📊 <b>Token Score</b>\n"
        f"🔹 Decentralization: {score['decentralisation_score']:.2f}%\n"
        f"🏦 In CEX: {score['identified_supply']['percent_in_cexs']:.2f}%\n"
        f"📜 In Contracts: {score['identified_supply']['percent_in_contracts']:.2f}%"
    )

def generate_summary(caption: str) -> str:
    def extract(pattern: str, type_fn=Callable[[str], Any], default=None):
        match = re.search(pattern, caption)
        return type_fn(match.group(1)) if match else default

    def extract_percentage(pattern: str):
        match = re.search(pattern, caption)
        return float(match.group(1)) if match else 0.0

    market_cap = extract(r"Market Cap: \$([\d,]+)", lambda x: int(x.replace(",", "")))
    liquidity = extract(r"Liquidity: \$([\d,]+)", lambda x: int(x.replace(",", "")))
    change_24h = extract(r"24h Change: ([\d\.\-]+)%", float)
    burn_pct = extract_percentage(r"Burn Wallet.*?(\d+\.\d+)%")
    top20_pct = extract_percentage(r"Top 20 wallets account for (\d+\.\d+)%")
    decentralization = extract_percentage(r"Decentralization: (\d+\.\d+)")

    header = ["\n\n🧾 <b>Summary</b>"]
    
    lines = []
    
    if market_cap:
        cap_word = "large-cap" if market_cap > 1_000_000_000 else "mid-cap" if market_cap > 100_000_000 else "low-cap"
        lines.append(f"{cap_word.capitalize()} token with a market cap of ${format_large_number(market_cap)}.")

    if change_24h is not None:
        if change_24h > 5:
            lines.append("Strong positive momentum in the last 24h.")
        elif change_24h < -5:
            lines.append("Notable price dip over the last 24h.")
        elif abs(change_24h) < 1:
            lines.append("Stable price action recently.")

    if liquidity is not None:
        if liquidity < 500_000:
            lines.append("Low on-chain liquidity — could be volatile.")
        elif liquidity > 2_000_000:
            lines.append("Healthy liquidity levels for smoother trading.")
        else:
            lines.append("Moderate level of liquidity")


    if burn_pct > 30:
        lines.append(f"Deflationary design — {burn_pct:.0f}% of supply burned.")
    elif burn_pct > 0:
        lines.append(f"{burn_pct:.0f}% of supply locked in burn wallets.")

    if top20_pct >= 80:
        lines.append("Token transfers are highly concentrated among top holders.")
    elif top20_pct >= 50:
        lines.append("Moderate concentration of token flow among top wallets.")
    else:
        lines.append("Token flow appears broadly distributed.")

    if decentralization > 70:
        lines.append("Decentralization score is strong.")
    elif decentralization > 40:
        lines.append("Moderately decentralized token.")
    else:
        lines.append("Low decentralization score indicates central control risk.")

    header += [f"- {line}" for line in lines]
    return "\n".join(header)
