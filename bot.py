import json
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

BOT_TOKEN = "7885279501:AAFU7y-RsZ9S3OGNp1ekh1KIX1fBibbtchI"

# Load motor data
with open("data.json") as f:
    motor_data = json.load(f)

# Function to fetch and format motor details
def get_motor_info(kW):
    kW = str(round(float(kW), 2))  # round to 2 decimals for matching
    if kW in motor_data:
        data = motor_data[kW]
        reply = f"**Motor Details for {kW} kW**\n\n"
        reply += f"**HP**: {data['HP']}\n"
        reply += f"**FLC (Star)**: {data['FLC_Star']} A\n"
        reply += f"**FLC (Delta)**: {data['FLC_Delta']} A\n"
        reply += f"**MPCB (Tyses V2)**: {data['MPCB_V2']}\n"
        reply += f"**MPCB (Tyses V3)**: {data['MPCB_V3']}\n"
        reply += f"**Contactor (ABB)**: {data['Contactor_ABB']}\n"
        reply += f"**Contactor (Siemens)**: {data['Contactor_Siemens']}\n"
        reply += f"**Contactor (L&T)**: {data['Contactor_L&T']}\n"
        reply += f"**MCCB Rating**: {data['MCCB']}\n"
        reply += f"**Cable (Cu Armoured)**: {data['Cable_Cu']}\n"
        reply += f"**Cable (Al Armoured)**: {data['Cable_Al']}\n"
        reply += f"**Cable Gland Size**: {data['Cable_Gland']}\n"
        reply += f"**Bearing (ABB)**:\n- DE: {data['Bearing_ABB_DE']}\n- NDE: {data['Bearing_ABB_NDE']}\n"
        reply += f"**Bearing (Siemens)**:\n- DE: {data['Bearing_Siemens_DE']}\n- NDE: {data['Bearing_Siemens_NDE']}\n"
        return reply
    else:
        return "Motor kW not found in database. Please try another value (e.g., 5.5 or 7.5)."

# Handler for incoming text
async def get_motor_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        kW_text = update.message.text.strip().lower().replace("kw", "").strip()
        reply = get_motor_info(kW_text)
    except Exception:
        reply = "Please enter a valid motor kW value like `5.5` or `7.5`."
    await update.message.reply_text(reply, parse_mode="Markdown")

# Main bot setup
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_motor_details))

if __name__ == "__main__":
    app.run_polling()
