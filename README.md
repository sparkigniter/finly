# 📈 Finly

> **AI-powered stock portfolio analyser for Indian investors** — upload your Zerodha export, get instant insights, live news, and smart buy/hold/sell recommendations.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![Status](https://img.shields.io/badge/Status-Work%20in%20Progress-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## ✨ What is Finly?

Finly is a lightweight, self-hosted web application that turns your **Zerodha holdings export** into an intelligent dashboard. In just a few clicks you can:

- 📂 **Upload** your Zerodha stocks CSV
- 📊 **View** live stock details for every holding
- 📰 **Read** the latest news for each ticker
- 🤖 **Get** AI-generated buy / hold / sell recommendations

No more juggling between browser tabs, news sites, and your broker dashboard — Finly brings everything into one clean interface.

---

## 🖥️ Screenshots

| Upload your portfolio | AI analysis & recommendations |
|---|---|
| ![Upload screen](https://github.com/sparkigniter/finly/raw/main/docs/upload.png) | ![Analysis screen](https://github.com/sparkigniter/finly/raw/main/docs/analysis.png) |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- A Zerodha account (to export your holdings as CSV)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/sparkigniter/finly.git
cd finly

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install frontend dependencies
cd app/frontend && npm install
```

### Running the app

You'll need **two terminals** — one for the backend, one for the frontend.

**Terminal 1 — Backend (API server)**
```bash
# From the project root
python3 -m app.backend.apis
```

**Terminal 2 — Frontend (Dev server)**
```bash
cd app/frontend
npm run dev
```

Then open your browser at the URL shown by the frontend dev server (usually `http://localhost:5173`).

### Exporting your Zerodha holdings

1. Log in to [Zerodha Kite](https://kite.zerodha.com)
2. Go to **Portfolio → Holdings**
3. Click **Download** (CSV export)
4. Upload the downloaded file to Finly

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python |
| Frontend | JavaScript, CSS, HTML |
| Data | Zerodha CSV export |
| AI recommendations | LLM-powered analysis |

---

## 🗺️ Roadmap

The project is actively under development. Planned features include:

- [ ] Support for multiple brokers (Groww, Angel One, Upstox)
- [ ] Historical performance charts per holding
- [ ] Portfolio-level P&L summary
- [ ] Email / push alerts for significant stock moves
- [ ] Watchlist management
- [ ] Mobile-friendly responsive UI

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request for bug fixes, new features, or improvements.

1. Fork the repo
2. Create your branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'Add my feature'`
4. Push: `git push origin feature/my-feature`
5. Open a Pull Request

---

## ⚠️ Disclaimer

Finly is a personal finance tool built for informational purposes only. The AI-generated recommendations are **not** financial advice. Always do your own research before making investment decisions.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<p align="center">Built with ❤️ for Indian retail investors &nbsp;•&nbsp; <a href="https://github.com/sparkigniter/finly">github.com/sparkigniter/finly</a></p>
