from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes

TOKEN = '7885279501:AAFzKMmLZ6JLzpQHOuSKlE8SMsXN5pykz8k'

motor_data = {
    0.37: {
        "HP": "0.5",
        "FLC_Star": "1.2 A",
        "FLC_Delta": "2.1 A",
        "MPCB": "GV2ME01 / 2A",
        "Contactor": {
            "Siemens": "3RT2015-1BB41 (9A)",
            "ABB": "AF09-30-10",
            "L&T": "MNX-9"
        },
        "MCCB": "ABB S203-C2",
        "Cable": {
            "Al": "4C x 2.5 mm²",
            "Cu": "4C x 1.5 mm²"
        },
        "Gland": "20 mm",
        "Bearing": {
            "ABB": {"DE": "6201", "NDE": "6201"},
            "Siemens": {"DE": "6201-ZZ", "NDE": "6201-ZZ"}
        }
    },
    5.5: {
        "HP": "7.5",
        "FLC_Star": "10.2 A",
        "FLC_Delta": "17.6 A",
        "MPCB": "GV2ME20 / 20A",
        "Contactor": {
            "Siemens": "3RT2026-1BB40 (18A)",
            "ABB": "AF09-30-10",
            "L&T": "MNX-18"
        },
        "MCCB": "ABB S203-C20",
        "Cable": {
            "Al": "4C x 6 mm²",
            "Cu": "4C x 4 mm²"
        },
        "Gland": "25 mm",
        "Bearing": {
            "ABB": {"DE": "6205", "NDE": "6204"},
            "Siemens": {"DE": "6205-ZZ", "NDE": "6204-ZZ"}
        }
    }
    # Add more kW entries here...
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me motor kW (e.g., 5.5) to get details.")

async def handle_kw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        kw = float(update.message.text)
        nearest_kw = min(motor_data.keys(), key=lambda x: abs(x - kw))
        data = motor_data[nearest_kw]
        reply = f"""Motor Details for {nearest_kw} kW

Horsepower (HP): {data["HP"]}
Full Load Current (Star): {data["FLC_Star"]}
Full Load Current (Delta): {data["FLC_Delta"]}
MPCB Rating: {data["MPCB"]}
Contactor:
 - Siemens: {data['Contactor']['Siemens']}
 - ABB: {data['Contactor']['ABB']}
 - L&T: {data['Contactor']['L&T']}
MCCB: {data['MCCB']}
Cable Size (Al): {data['Cable']['Al']}
Cable Size (Cu): {data['Cable']['Cu']}
Cable Gland: {data['Gland']}
Bearing:
 - DE (ABB): {data['Bearing']['ABB']['DE']} | NDE: {data['Bearing']['ABB']['NDE']}
 - DE (Siemens): {data['Bearing']['Siemens']['DE']} | NDE: {data['Bearing']['Siemens']['NDE']}
"""
        await update.message.reply_text(reply)
    except:
        await update.message.reply_text("Please send a valid motor kW number like 0.75, 5.5, 22, etc.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_kw))

app.run_polling()
