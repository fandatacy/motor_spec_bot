import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Replace this with your actual token
BOT_TOKEN = "7885279501:AAFU7y-RsZ9S3OGNp1ekh1KIX1fBibbtchI"

# Load motor data
with open("data.json") as f:
    motor_data = json.load(f)

# Format reply for Telegram
def format_motor_info(data):
    return (
        f"<b>Motor kW:</b> {data['kW']} kW\n"
        f"<b>HP:</b> {data['HP']}\n"
        f"<b>FLC (Star):</b> {data['FLC_Star']} A\n"
        f"<b>FLC (Delta):</b> {data['FLC_Delta']} A\n"
        f"<b>MPCB (Tyses V2):</b> {data['MPCB_Tyses_V2']}\n"
        f"<b>MPCB (Tyses V3):</b> {data['MPCB_Tyses_V3']}\n"
        f"<b>Contactor:</b>\n"
        f"  - Siemens: {data['Contactor_Siemens']}\n"
        f"  - ABB: {data['Contactor_ABB']}\n"
        f"  - L&T: {data['Contactor_L&T']}\n"
        f"<b>MCCB:</b> {data['MCCB']}\n"
        f"<b>Cable Size:</b>\n"
        f"  - Copper: {data['Cable_Copper']}\n"
        f"  - Aluminium: {data['Cable_Aluminium']}\n"
        f"<b>Cable Gland:</b> {data['Cable_Gland']}\n"
        f"<b>Bearings:</b>\n"
        f"  - DE: {data['Bearing_DE']}\n"
        f"  - NDE: {data['Bearing_NDE']}"
    )

# /start and /help command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to the Motor Selector Bot!\n\n"
        "Send me a motor kW value (e.g., 5.5) and I’ll give you full specs!",
    )

# Handler for motor data query
async def get_motor_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kW_input = update.message.text.strip()
    try:
        kW = float(kW_input)
    except ValueError:
        await update.message.reply_text("Please enter a valid number (e.g., 5.5 or 22).")
        return

    # Match with rounding if exact key not found
    kW_str = str(round(kW, 2))
    result = motor_data.get(kW_str)
    if result:
        reply = format_motor_info(result)
        await update.message.reply_text(reply, parse_mode="HTML")
    else:
        await update.message.reply_text("Motor kW not found in database. Please try another value.")

# App init
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Command and message handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_motor_details))

# Run the bot
print("Bot is running...")
app.run_polling()
