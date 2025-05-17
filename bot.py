
import csv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Replace 'YOUR_BOT_TOKEN' with your actual Telegram Bot Token
BOT_TOKEN = "7885279501:AAHM88TmaaotUUcpIpG-nJZhSMkydYIr62I"

# Load motor data from CSV into a dictionary
motor_data = {}
with open("motor_data.csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            kw = float(row["kW"])
            motor_data[kw] = row
        except ValueError:
            continue  # Skip rows with invalid kW

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Send me a motor kW value (e.g., 1.5) to get motor specifications.")

async def motor_lookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_input = update.message.text.strip()
        kw = float(user_input)

        if kw not in motor_data:
            await update.message.reply_text("Motor data for this kW not found.")
            return

        row = motor_data[kw]

        response = f"""Motor Selection for {kw} kW

Horsepower (HP): {row['HP']}
FLC (Star): {row['FLC_Star']} A
FLC (Delta): {row['FLC_Delta']} A

MPCB Ratings:
- ABB: {row['MPCB_ABB']} (Next: {row['MPCB_ABB_Next']})
- Siemens: {row['MPCB_Siemens']} (Next: {row['MPCB_Siemens_Next']})
- L&T: {row['MPCB_L&T']} (Next: {row['MPCB_L&T_Next']})
- Schneider: {row['MPCB_Schneider']} (Next: {row['MPCB_Schneider_Next']})

Contactor Models:
- ABB: {row['Contactor_ABB']} ({row['Contactor_ABB_Amps']} A)
- Siemens: {row['Contactor_Siemens']} ({row['Contactor_Siemens_Amps']} A)
- L&T: {row['Contactor_L&T']} ({row['Contactor_L&T_Amps']} A)

MCCB: {row['MCCB']}

Cable Sizes:
- Aluminium: {row['Cable_Al']} mm^2
- Copper: {row['Cable_Cu']} mm^2

Cable Gland Size: {row['Cable_Gland']}

Bearings:
- ABB DE: {row['ABB_DE']}, NDE: {row['ABB_NDE']}
- Siemens DE: {row['Siemens_DE']}, NDE: {row['Siemens_NDE']}
"""
        await update.message.reply_text(response)
    except ValueError:
        await update.message.reply_text("Please enter a valid kW value (e.g., 2.2).")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, motor_lookup))
    app.run_polling()

if __name__ == "__main__":
    main()
