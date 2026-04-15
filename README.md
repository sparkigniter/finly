# 📈 Finly

> **AI-powered stock portfolio analyser for Indian investors** — upload your Zerodha export, get instant insights, live news, and smart recommendations.

<p align="center">
  <img alt="Python 3.10+" src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img alt="JavaScript ES6+" src="https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" />
  <img alt="Status: WIP" src="https://img.shields.io/badge/Status-Active%20Development-orange?style=for-the-badge" />
  <img alt="MIT License" src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
</p>

---

## ✨ What is Finly?

Finly transforms your **Zerodha holdings export** into an intelligent, all-in-one investment dashboard. Skip the endless tab switching between your broker, news sites, and financial apps.

**What you get:**
- 📂 Upload your Zerodha stocks CSV in seconds
- 📊 Live stock data and metrics for every holding
- 📰 Latest news aggregated for each ticker
- 🤖 AI-generated buy/hold/sell recommendations
- 🎯 One clean interface, zero friction

Perfect for Indian retail investors who want smarter, faster portfolio insights.

---

## 🖼️ Visual Tour

### Dashboard & Analysis
<div align="center">
  <table>
    <tr>
      <td align="center"><b>Portfolio Overview</b></td>
      <td align="center"><b>Live Stock Metrics</b></td>
    </tr>
    <tr>
      <td><img width="450" alt="Portfolio Dashboard" src="https://github.com/user-attachments/assets/bc0a7ed0-3822-4c86-9f5b-95cb943182f4" /></td>
      <td><img width="450" alt="Stock Details" src="https://github.com/user-attachments/assets/ee01d6f8-e9e9-49f9-bf9e-f69593626f72" /></td>
    </tr>
  </table>
</div>

### News & AI Recommendations
<div align="center">
  <table>
    <tr>
      <td align="center"><b>Latest News Feed</b></td>
      <td align="center"><b>Smart Recommendations</b></td>
    </tr>
    <tr>
      <td><img width="450" alt="News Section" src="https://github.com/user-attachments/assets/fb3ad282-8ddf-4aad-9fdd-95abfd7b05d6" /></td>
      <td><img width="450" alt="AI Recommendations" src="https://github.com/user-attachments/assets/26caa577-ed20-4cf4-9027-cc5c8a9944a7" /></td>
    </tr>
  </table>
</div>

---

## 🚀 Quick Start

### Requirements
- **Python** 3.10 or higher
- **Zerodha account** (free, to export your holdings)

### Installation (One Command)

**Linux / macOS:**
```bash
git clone https://github.com/sparkigniter/finly.git && cd finly && chmod +x setup.sh && ./setup.sh
```

> **Windows users:** Run the above command inside WSL2 (Ubuntu) for best results.

### Manual Installation

```bash
# Clone the repo
git clone https://github.com/sparkigniter/finly.git
cd finly

# Install dependencies
pip install -r requirements.txt
cd app/frontend && npm install
```

### Run the App

**Terminal 1 — Backend API:**
```bash
python3 -m app.backend.apis
```

**Terminal 2 — Frontend:**
```bash
cd app/frontend && npm run dev
```

Open your browser at `http://localhost:5173` and you're in! 🎉

---

## 📤 Getting Your Zerodha Data

1. Log in to **[Zerodha Kite](https://kite.zerodha.com)**
2. Navigate to **Portfolio → Holdings**
3. Click **Download** to export as CSV
4. Upload the file to Finly
5. Watch the magic happen ✨

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend API** | Python with async support |
| **Frontend UI** | Modern JavaScript, HTML, CSS |
| **Data Source** | Zerodha CSV export |
| **Intelligence** | LLM-powered recommendations |
| **Styling** | Responsive, mobile-first design |

---

## 🗺️ Roadmap

We're building fast. Coming soon:

- 🏦 Multi-broker support (Groww, Angel One, Upstox)
- 📊 Historical performance charts per stock
- 💼 Portfolio-level P&L summaries
- 🔔 Email & push alerts for major moves
- ⭐ Watchlist management
- 📱 Mobile-optimized responsive design
- 📈 Advanced analytics & backtesting tools

---

## 🤝 Contributing

Love Finly? Help make it better!

```bash
git checkout -b feature/your-awesome-feature
git commit -m "✨ Add your awesome feature"
git push origin feature/your-awesome-feature
```

Then open a Pull Request. All contributions are welcome — bug fixes, features, docs, you name it.

---

## ⚠️ Disclaimer

**Finly is for educational and informational purposes only.** The AI-generated recommendations are **not** financial advice. Always conduct your own research and consult a financial advisor before making investment decisions. Past performance doesn't guarantee future results.

Use Finly responsibly. Happy investing! 📈

---

## 📄 License

Licensed under the **MIT License** — feel free to use, modify, and distribute. See the [LICENSE](LICENSE) file for full terms.

---

<div align="center">
  <p>
    <strong>Built with ❤️ for Indian retail investors</strong>
  </p>
  <p>
    <a href="https://github.com/sparkigniter/finly">⭐ Star on GitHub</a> •
    <a href="https://github.com/sparkigniter/finly/issues">Report a bug</a> •
    <a href="https://github.com/sparkigniter/finly/discussions">Start a discussion</a>
  </p>
</div>

---

<p align="center">
  <em>Made by investors, for investors. No fluff, just insights.</em>
</p>
