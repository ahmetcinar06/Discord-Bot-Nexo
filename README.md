

# 🤖 Nexo Discord Bot

Nexo is a multi-purpose Discord bot built with **discord.py** and **OpenAI API**.

## 📁 File Structure

```
bot.py        # Main bot and commands (423 lines)
poke.py       # Pokemon system and database (226 lines)
pc.py         # PC management functions (73 lines)
game.py       # Game and entertainment modules (117 lines)
config.py     # Bot token (1 line)
bellek.db     # SQLite database
README.md     # This file
__pycache__/  # Compiled Python files
```

## 🚀 Features

- AI chat mode (GPT-4.1-mini)
- Moderation (ad/link detection and ban)
- Message and image filtering
- Server and user info
- PC hardware and system management
- Games: Number guessing, Pokémon battle, trivia
- Pokémon system: Normal, Fighter, Wizard types
- Pokémon are stored in the database, persistent after bot restart
- Uptime and system statistics

## ⚙️ Requirements

- Python 3.9+
- `discord.py` (`pip install discord.py`)
- `openai` (`pip install openai`)

## 📥 Installation

1. **Download or clone the source code.**
2. **Install required packages:**
   ```bash
   pip install discord.py openai
   ```
3. **Add your bot token to config.py:**
   ```python
   token = "YOUR_DISCORD_BOT_TOKEN"
   ```
4. **Start the bot:**
   ```bash
   python bot.py
   ```

## 💬 Commands

### AI & General
- `nexo ai` : Enable AI chat mode
- `nexo çık` : Disable AI chat mode
- `nexo version` : Show AI model version
- `nexo help` : List all commands

### Moderation & Server
- Automatic ad/link ban
- `nexo temizle [n]` : Delete messages
- `nexo aktif` : List online members
- `nexo roller` : List server roles
- `nexo davet` : Create invite link
- `nexo uptime` : Show bot uptime

### PC Management
- `nexo pc_about` : Hardware info
- `nexo pc_status` : System usage
- `nexo antivirus` : Antivirus scan
- `nexo update` : System update
- `nexo processes` : List running processes

### Games & Fun
- `nexo game` : Game menu
- `nexo go` : Create new Pokémon (with type selection)
- `nexo pokemon` : Pokémon info and image
- `nexo feed` : Feed Pokémon
- `nexo evolve` : Evolve Pokémon
- `nexo delete_pokemon` : Delete Pokémon (also from database)

### Other
- `nexo ping` : Bot latency
- `nexo avatar [user]` : Show avatar
- `nexo kullanici` : User info
- `nexo sunucu` : Server name and member count
- `nexo sunucuinfo` : Server creation date and region
- `nexo rastgele` : Random number
- `nexo about` : About the bot
- `nexo info` : Bot info
- `nexo hello` : Greeting
- `nexo dm [message]` : Send DM

## 🗂️ Notes
- Pokémon are stored in the database with types like Fighter and Wizard.
- Deleted Pokémon are also removed from the database.
- The codebase is modular and easily extendable.

For questions or feature requests, feel free to review the code or contact me!