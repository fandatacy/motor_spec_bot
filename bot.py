import json
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Load data from JSON
with open("data.json", "r") as file:
    motor_data = json.load(file)

def find_closest_kw(input_kw):
    available_kws = sorted(float(k) for k in motor_data.keys())
    closest_kw = min(available_kws, key=lambda x: abs(x - input_kw))
    return str(closest_kw)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send /motor <kW> to get motor details.")

async def motor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        kw = float(context.args[0])
        kw_key = find_closest_kw(kw)
        specs = motor_data[kw_key]
        response = f"**Motor Details for {kw_key} kW**:\n"
        for key, value in specs.items():
            response += f"{key}: {value}\n"
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text("Usage: /motor <kW>\nExample: /motor 7.5")

if __name__ == "__main__":
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("motor", motor))
    app.run_polling()