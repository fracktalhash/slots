# 🎰 Terminal Slot Machine Game

**A Python-based slot machine game featuring animated spinning reels, symbol-based payouts, and line bonuses.**
---

## 🚀 Project Goals

This game began as a terminal-based Python application and is being expanded to include:
- 🔐 Player profile persistence
- 🌐 Cloud deployment as part of the **Google Cloud Resume Challenge**

---

## 🧪 Features (Current)

- Terminal slot animation using `Rich`
- 3x3 or 3x4 board configurations
- Weighted symbols with realistic rarity
- Diagonal & zigzag bonus lines
- Configurable betting and payout system
- Player bank tracking

---

## 📥 Run It Locally:

### Prerequisites
- Python 3.9+
- Create a environment (optional but recommended):
    * Initialize the environment:
      ```bash
      python3 -m venv venv
      ```
    * Activate in Linux or Mac:
      ```bash
      source env_name/bin/activate
      ```
    * Activate in Windows:
      ```cmd
      .\env_name\Scripts\activate
      ```
- Install Rich for animations:
  ```bash
  pip install rich
  ```
### Run the game
```bash
python3 slots.py
```

---

## 💠 To-Do (Roadmap)

### 1. ✅ Sanitize User Input
- [ ] Ensure `int`, `float`, and `str` inputs are validated
- [ ] Add guardrails for bet size, name length, invalid keypresses

### 3. 🧝 Add Player Profile System
- [ ] Save/load player name, bank, and bet preferences
- [ ] Store to `JSON`, `SQLite`, or integrate with Firebase
- [ ] Allow multiple user profiles for local play

### 4. ☁️  Port into GCP Resume Challenge
- [ ] Turn game logic into backend microservice (FastAPI)
- [ ] Host frontend on GCP Cloud Run or App Engine
- [ ] Store game state in Firestore
- [ ] Secure game endpoints and track session data
- [ ] Bonus: add live player leaderboard from Firestore

---

## 💰 current Pay Table

| Symbol    | Match 3 | Match 4 |
|-----------|---------|---------|
| ♥ / ♠     | 2x      | 4x      |
| Δ / Ω / Ψ | 5x      | 10x     |
| ♝ / ♞     | 15x     | 30x     |
| ♜ / ♛     | 50x     | 100x    |
| ♚         | 100x    | 200x    |


| Bonus Line | Bonus Amount  |
|------------|---------------|
|  Diagonal  | +50%          |
|  Zigzag    | + 100%        |


---

## ⚖️ Symbol Weights

Symbols are weighted differently to simulate rarity:

### 3x3 Slot Weights
| Symbol                  | Weight |
|-------------------------|--------|
| ♥ / ♠ / Δ / Ω           | 0.13   |
| Ψ / ♝ / ♞ / ♜ / ♛       | 0.07   |
| ♚                       | 0.02   |

### 3x4 Slot Weights
| Symbol              | Weight |
|---------------------|--------|
| ♥ / ♠               | 0.3    |
| Δ / Ω / Ψ           | 0.1    |
| ♝ / ♞               | 0.025  |
| ♜ / ♛               | 0.005  |
| ♚                   | 0.002  |

The lower the weight, the rarer the symbol — and the bigger the reward.

---

## 🤝 Contributing

Pull requests are welcome! Suggestions for GCP integrations are especially appreciated.

---

## 💬 Credits

This project was developed with:
- Curiosity and determination
- Input from family and friends 
- AI assistance via [ChatGPT](https://chatgpt.com/ ) and [Gemini](https://gemini.google.com/) assistance.

---

## 📄 License

This project is licensed under the [Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/).

You are free to:
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material

**Under the following terms:**
- **Attribution** — You must give appropriate credit.
- **NonCommercial** — You may not use the material for commercial purposes.

> ⚠️ Commercial use is **strictly prohibited** without the author's permission.