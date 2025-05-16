import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Replace this with your actual bot token
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# Dummy example motor data for demonstration
motor_data = {
    5.5: {
        "hp": 7.38,
        "flc": 10.2,
        "mpcb": {
            "Schneider": "GV2ME14 (6.3–10 A)",
            "ABB": "MS116-10 (6.3–10 A)",
            "Siemens": "3RV2011-1HA10 (6.3–10 A)",
            "L&T": "MU45E10 (6.3–10 A)",
            "Next Sizes": {
                "Schneider": "GV2ME16 (9–14 A)",
                "ABB": "MS116-16 (10–16 A)",
                "Siemens": "3RV2011-1KA10 (10–16 A)",
                "L&T": "MU45E16 (10–16 A)"
            }
        },
        "contactor": {
            "Schneider": "LC1D12 (9–12 A)",
            "ABB": "AF16-30-10",
            "Siemens": "3RT2025-1AP00",
            "L&T": "MNX-18 (9–18 A)"
        },
        "mccb": "Schneider EZC100F310 (10–16 A)",
        "bearing": {
            "ABB": {
                "DE": "6205",
                "NDE": "6204"
            },
            "Siemens": {
                "DE": "6205",
                "NDE": "6204"
            }
        }
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the Motor Selector Bot! Send me a motor kW value (e.g., 5.5)")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    try:
        kw = float(text)
        if kw in motor_data:
            data = motor_data[kw]
            response = f"Motor: {kw} kW ({data['hp']} HP)\n"
            response += f"FLC: {data['flc']} A\n"
            response += f"MPCB:\n"
            for brand, model in data['mpcb'].items():
                if brand != "Next Sizes":
                    response += f"  {brand}: {model}\n"
            response += f"  Next Sizes:\n"
            for brand, model in data['mpcb']['Next Sizes'].items():
                response += f"    {brand}: {model}\n"
            response += "Contactor:\n"
            for brand, model in data['contactor'].items():
                response += f"  {brand}: {model}\n"
            response += f"MCCB: {data['mccb']}\n"
            response += "Bearings:\n"
            for brand, bearing in data['bearing'].items():
                response += f"  {brand} - DE: {bearing['DE']}, NDE: {bearing['NDE']}\n"
            await update.message.reply_text(response)
        else:
            await update.message.reply_text("Motor kW not found in database. Please try another value.")
    except ValueError:
        await update.message.reply_text("Please send a valid motor kW number.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
