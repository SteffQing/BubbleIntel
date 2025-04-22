
## 🧠 BubbleIntel

**BubbleIntel** is a Telegram bot that delivers instant, insightful analytics for any token—powered by Bubblemaps.

### ✨ Features
- 📍 **Visual Bubble Maps** – Get an auto-generated screenshot of a token's bubble map based on its contract address.
- 📊 **Token Metrics** – View market cap, price, volume, and liquidity in real-time.
- 📈 **Decentralization Score** – Assess token distribution health instantly.
- 🧠 **Extra Insights** – Includes wallet count, top holders, creation date, and other helpful token stats.

### ⚙️ Tech Stack
- **Python** + **Aiogram** for the Telegram bot
- **Coingecko**, **BubbleMaps API**, and more for data aggregation
- **Playwright**/**Selenium** (planned) for generating dynamic screenshots

### 📦 Use Case
A tool for casual users, researchers, and degens to quickly evaluate the health and risk of any token straight from Telegram.

---

## 🔧 Installation

> Requires Python 3.9+

```bash
git clone https://github.com/yourusername/bubbleintel.git
cd bubbleintel
pip install -r requirements.txt
```

Add your bot token to .env:

``` bash
BOT_TOKEN=your_telegram_bot_token
```

Then start the bot:
```bash
python app.py
```

## 📱 Usage
Start a chat with your bot and send:

/network <contract_address>

The bot will:

- Detect the chain

- Fetch a bubble map

- Generate a screenshot

- Provide token data + decentralization score

## 🧪 Demo & Case Study
Coming soon: Demo Video & Investigation Case Study

For now, try inspecting this token: 0x95ad61b0a150d79219dcf64e1e6cc01f0b64c4ce

### 🧠 Methodologies
- Chain Detection via token metadata aggregation

- Screenshot Rendering using headless Chromium with Playwright

- Data Fetching from decentralized and centralized APIs

- Bot Flow designed for minimal latency and ease of use

## 📄 License
MIT — free to use, share, and remix

## 📝 Documentation
For advanced setup, dev notes, and architecture diagram, visit:
 [📖 Notion Docs](https://google.com) or [GitHub Gist](https://gist.github.com/SteffQing/58e8692a2e654d834329113f5dec4980)
