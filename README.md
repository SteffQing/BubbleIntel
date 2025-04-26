
## 🧠 Bubble Intel

**Bubble Intel** is a Telegram bot that delivers instant, insightful analytics for any token—powered by Bubblemaps.

### ✨ Features
- 📍 **Visual Bubble Maps** – Get an auto-generated screenshot of a token's bubble map based on its contract address.
- 📊 **Token Metrics** – View market cap, price, volume, and liquidity in real-time.
- 📈 **Decentralization Score** – Assess token distribution health instantly.
- 🧠 **Bubblemap Insights** – Includes top sender and receiver data, wallet clusers, transfer density, and other helpful token stats.

### ⚙️ Tech Stack
- **Python** + **Aiogram** for the Telegram bot
- **Mobula** and **BubbleMaps APIs** for data aggregation
- **Playwright**/**Selenium** for generating dynamic screenshots

### 📦 Use Case
A tool for casual users, researchers, and degens to quickly evaluate the health and risk of any token straight from Telegram.

---

## 🔧 Installation

> Requires Python 3.9+

```bash
git clone https://github.com/SteffQing/BubbleIntel.git
cd BubbleIntel
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

- Fetch a bubble map

- Generate a screenshot

- Provide token data + decentralization score

## 🧪 Demo & Case Study
Coming soon: Demo Video & Investigation Case Study
- [SHIB Case Study](https://gist.github.com/SteffQing/58e8692a2e654d834329113f5dec4980)

### 🧠 Methodologies
- Screenshot Rendering using headless Chromium with Playwright

- Data Fetching from decentralized mobula APIs

- Bot Flow designed for minimal latency and ease of use

## 📄 License
MIT — free to use, share, and remix
