# 🍳 Recipe Bot

A Telegram bot that suggests recipes based on user input. Built with Python and Aiogram.

---

## Features

- Browse recipes by category using inline keyboard buttons
- Get recipe details including ingredients and steps
- Simple and fast interaction via Telegram

---

## Tech Stack

- **Language:** Python
- **Framework:** Aiogram
- **Interface:** Inline keyboards, message handlers

---

## Getting Started

**1. Clone the repository**
```bash
git clone https://github.com/Kotelaa/recipe-bot.git
cd RecipeBot
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install aiogram
```

**4. Add your bot token**

Create a `.env` file or config file and add your Telegram bot token:
```
BOT_TOKEN=your-telegram-bot-token
```

**5. Run the bot**
```bash
python main_bot.py
```

---

## Project Structure

```
RecipeBot/
├── main_bot.py          # Bot entry point and handlers
├── recipes_handler.py   # Recipe logic
├── app_keyboards.py     # Inline keyboard definitions
└── .gitignore
```
