import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "7885279501:AAFU7y-RsZ9S3OGNp1ekh1KIX1fBibbtchI"

with open("data.json") as f:
    motor_data = json.load(f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Send me a motor kW value (e.g., 5.5) to get specifications.")

async def get_motor_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        kW = float(update.message.text.strip())
    except ValueError:
        await update.message.reply_text("Please enter a valid motor kW value.")
        return

    str_kW = f"{kW:.2f}"
    if str_kW in motor_data:
        data = motor_data[str_kW]
        reply = f"""
<b>Motor Size:</b> {str_kW} kW

<b>HP:</b> {data["hp"]}

<b>Full Load Current (Star):</b> {data["flc_star"]} A
<b>Full Load Current (Delta):</b> {data["flc_delta"]} A

<b>Contactors:</b>
- Siemens: {data["contactor"]["siemens"]}
- ABB: {data["contactor"]["abb"]}
- L&T: {data["contactor"]["lt"]}

<b>MPCB:</b>
- Siemens: {data["mpcb"]["siemens"]} (Next: {data["mpcb"]["siemens_next"]})
- ABB: {data["mpcb"]["abb"]} (Next: {data["mpcb"]["abb_next"]})
- L&T: {data["mpcb"]["lt"]} (Next: {data["mpcb"]["lt_next"]})
- Schneider: {data["mpcb"]["schneider"]} (Next: {data["mpcb"]["schneider_next"]})

<b>Cable Size:</b>
- Copper: {data["cable"]["copper"]}
- Aluminium: {data["cable"]["aluminium"]}

<b>Cable Gland:</b> {data["cable_gland"]}

<b>Bearings:</b>
- DE: {data["bearing"]["de"]}
- NDE: {data["bearing"]["nde"]}
""".strip()
        await update.message.reply_text(reply, parse_mode='HTML')
    else:
        await update.message.reply_text("Motor kW not found in database. Please try another value.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(CommandHandler("kw", get_motor_details))
    app.add_handler(MessageHandler(None, get_motor_details))
    app.run_polling()
