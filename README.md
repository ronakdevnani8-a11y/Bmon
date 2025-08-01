# Discord Music Bot for Render

## ✅ Features
- Play music using `!yap <query or URL>`
- Auto queue system
- Shows song title, duration, and who requested it

## 🚀 Render Setup
1. Upload this zip to your GitHub repo or Render's new web service.
2. Set the **Start Command**:
   ```bash
   python main.py
   ```
3. Set the **Build Command**:
   ```bash
   pip install -r requirements.txt
   ```
4. Set environment variable:
   - `DISCORD_BOT_TOKEN`: Your bot token

## ⚠️ Python Version
Make sure Render uses Python 3.11 by using the included `runtime.txt`.