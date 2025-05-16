import json
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Insert your actual bot token here
BOT_TOKEN = "7885279501:AAFU7y-RsZ9S3OGNp1ekh1KIX1fBibbtchI"

# Load motor data from JSON file
with open("data.json") as f:
    motor_data = json.load(f)

def find_closest_kw(input_kw):
    available_kws = [float(k) for k in motor_data.keys()]
    closest = min(available_kws, key=lambda x: abs(x - input_kw))
    return str(closest)

def format_motor_info(data):
    return (
        f"**Motor Details for {data['kW']} kW**\n\n"
        f"* Horsepower (HP): `{data['HP']}`\n"
        f"* Full Load Current (Star): `{data['FLC_Star']} A`\n"
        f"* Full Load Current (Delta): `{data['FLC_Delta']} A`\n"
        f"* MPCB Rating: `{data['MPCB']}`\n"
        f"* Contactor:\n"
        f"  - Siemens: `{data['Contactor']['Siemens']}`\n"
        f"  - ABB: `{data['Contactor']['ABB']}`\n"
        f"  - L&T: `{data['Contactor']['L&T']}`\n"
        f"* MCCB: `{data['MCCB']}`\n"
        f"* Cable Size (Al): `{data['Cable_Al']}`\n"
        f"* Cable Size (Cu): `{data['Cable_Cu']}`\n"
        f"* Cable Gland: `{data['Cable_Gland']}`\n"
        f"* Bearing:\n"
        f"  - DE (ABB): `{data['Bearing']['ABB']['DE']}` | NDE: `{data['Bearing']['ABB']['NDE']}`\n"
        f"  - DE (Siemens): `{data['Bearing']['Siemens']['DE']}` | NDE: `{data['Bearing']['Siemens']['NDE']}`"
    )

async def get_motor_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        input_kw = float(update.message.text.strip())
        key = str(input_kw)
        if key not in motor_data:
            key = find_closest_kw(input_kw)
        data = motor_data[key]
        data["kW"] = key
        reply = format_motor_info(data)
    except Exception as e:
        reply = "Please enter a valid motor kW value like `5.5` or `22`."
    await update.message.reply_text(reply, parse_mode="Markdown")

# Run the bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_motor_details))
    print("Bot is running...")
    app.run_polling()
