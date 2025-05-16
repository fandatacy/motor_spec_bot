import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
BOT_TOKEN = "7885279501:AAFU7y-RsZ9S3OGNp1ekh1KIX1fBibbtchI"

with open("data.json") as f:
    motor_data = json.load(f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to MotorBot! Enter motor kW value (e.g., 5.5) to get full details.")

async def motor_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        kw = update.message.text.strip()
        data = motor_data.get(kw)
        if not data:
            await update.message.reply_text("Motor kW not found in database. Please try another value.")
            return

        text = f"**Motor Selection for {data['kW']} ({data['HP']})**\n"
        text += f"**Voltage:** 415V\n"
        text += f"**Full Load Current:**\n  • Star: {data['FLC_Star']}\n  • Delta: {data['FLC_Delta']}\n\n"

        text += "**MPCB Ratings:**\n"
        for brand, details in data["MPCB"].items():
            text += f"  • {brand}: {details['Model']} ({details['Range']}) | Next: {details['Next Size']}\n"

        text += "\n**Contactor Ratings:**\n"
        for brand, model in data["Contactor"].items():
            text += f"  • {brand}: {model}\n"

        text += f"\n**MCCB:** {data['MCCB']}\n"

        text += f"\n**Cable Size:**\n  • Aluminum: {data['Cable']['Aluminum']}\n  • Copper: {data['Cable']['Copper']}\n"
        text += f"**Cable Gland Size:** {data['Cable_Gland']}\n"

        text += "\n**Bearing Numbers:**\n"
        for brand, bearings in data["Bearing"].items():
            text += f"  • {brand}: DE - {bearings['DE']}, NDE - {bearings['NDE']}\n"

        await update.message.reply_text(text, parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text("Error: " + str(e))

app = ApplicationBuilder().token("REPLACE_YOUR_BOT_TOKEN_HERE").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", start))
app.add_handler(CommandHandler("", motor_info))
app.run_polling()
