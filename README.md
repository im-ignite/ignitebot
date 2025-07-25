<p align="center">
  <img src="https://github.com/user-attachments/assets/4e31464e-889c-4cdc-8728-c56b1843bf23" alt="Ignite Logo" width="300px" style="border-radius: 50%; border: 2px solid #f36f21;">
</p>

<h1 align="center">
  <b>Ignite Telegram Bot</b>
</h1>

<p align="center">
  <b>A feature-rich Telegram bot with QR code generation and admin management capabilities.</b>
</p>

<p align="center">
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-v3.10-blue" alt="Python">
  </a>
  <a href="https://github.com/im-ignite/ignitebot/graphs/commit-activity">
    <img src="https://img.shields.io/badge/Maintained%3F-yes-green.svg" alt="Maintenance">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-blue" alt="License">
  </a>
  <a href="https://github.com/im-ignite/ignitebot">
    <img src="https://badges.frapsoft.com/os/v2/open-source.svg?v=103" alt="Open Source Love">
  </a>
</p>

---

## 🚀 Features
- **QR Code Generation**: Easily generate QR codes from text.
- **User Management**: Manage users with ease.
- **Admin Commands**: Special commands for administrators.
- **Command Logging**: Keep track of all commands used.
- **Error Handling**: Robust error management.

## 🛠️ Setup and Deployment

### Deploy to Heroku
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/im-ignite/ignitebot)

### Prerequisites
- **Python 3.10** or higher
- **Telegram Bot Token** from [@BotFather](https://t.me/BotFather)

### Local Deployment
1. **Clone the repository**:
   ```bash
   git clone https://github.com/im-ignite/ignitebot.git
   cd ignitebot
   ```
   OR YOU CAN DIRECTLY  DOUBLE CLICK ON SETUP.BAT
2. Install requirements :
   
   ```bash
   pip install -r requirements.txt
    ```
3. Create a .env file with your configuration:
   
   ```env
   BOT_TOKEN=your_bot_token_here
   ADMIN_IDS=your_admin_id
    ```
4. Run the bot :
   
   ```bash
   python bot.py
    ```
   OR YOU CAN DOUBLE CLICK ON SETUP.BAT
## ⚙️ Configuration Variables
- BOT_TOKEN : Your Telegram Bot Token from @BotFather
- ADMIN_IDS : Telegram user IDs of bot administrators (comma-separated for multiple admins)
## 📜 Commands
- /start : Start the bot and show available commands
- /qr : Generate QR code from text
- /stats : Show bot statistics (admin only)
## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Contact
- Telegram: @im_ignite
Made with ❤️ by Ignite
