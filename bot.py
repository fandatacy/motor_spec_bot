from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from flask import Flask, request
import asyncio

# === Replace this with your actual bot token ===
BOT_TOKEN = "7885279501:AAFzKMmLZ6JLzpQHOuSKlE8SMsXN5pykz8k"

WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = "https://your-app-name.up.railway.app" + WEBHOOK_PATH  # Replace with Railway URL

app = Flask(__name__)

telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

# === Handlers ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Send me motor kW (e.g., 5.5) to get motor data.")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a motor size (e.g., 22) in kW.")

async def motor_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        kw = float(update.message.text.strip())
    except ValueError:
        await update.message.reply_text("Please send a valid number (e.g., 5.5)")
        return

    # Dummy logic — replace with real data or formula
    response = f"""
Motor Details for {kw} kW

Horsepower (HP): {kw * 1.341}
Full Load Current (Star): {round(kw * 1.8, 2)} A
Full Load Current (Delta): {round(kw * 3.1, 2)} A

MPCB Ratings:
- ABB: GV2ME{int(kw * 3)}
- Siemens: 3RV2011-{int(kw * 2)}
- L&T: MU-G{int(kw * 2)}

Contactor:
- ABB: AF{int(kw * 2)}-30-10
- Siemens: 3RT2{int(kw * 1.5)}
- L&T: MNX-{int(kw * 2)}

MCCB: S203-C{int(kw * 4)}
Cable Sizes:
- Al: 4C x {int(kw * 1.2)} mm²
- Cu: 4C x {int(kw * 1)} mm²
Gland: 25 mm

Bearings:
- ABB: DE - 6206 | NDE - 6205
- Siemens: DE - 6206-ZZ | NDE - 6205-ZZ
    """
    await update.message.reply_text(response)

# Register handlers
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("help", help_cmd))
telegram_app.add_handler(CommandHandler("", motor_data))

# === Webhook Setup ===
@app.route(WEBHOOK_PATH, methods=["POST"])
async def webhook():
    await telegram_app.update_queue.put(Update.de_json(request.get_json(force=True), telegram_app.bot))
    return "OK"

@app.route("/", methods=["GET"])
def index():
    return "Bot is running!"

async def set_webhook():
    await telegram_app.bot.set_webhook(WEBHOOK_URL)

def start_bot():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(set_webhook())
    telegram_app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        webhook_path=WEBHOOK_PATH
    )

if __name__ == "__main__":
    start_bot()
