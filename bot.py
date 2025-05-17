import csv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Load data from CSV
motor_data = {}
with open('motor_data.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            kw = float(row["kW"])
            motor_data[kw] = row
        except ValueError:
            continue  # Skip invalid entries

# Bot reply function
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Send me a motor kW value (e.g., 15 or 22.5) to get motor selection details.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    try:
        kw_input = float(text)
        data = motor_data.get(kw_input)
        if not data:
            await update.message.reply_text("Motor data for this kW not found.")
            return

        response = f"""Motor Selection for {data["kW"]} kW:

- Horsepower (HP): {data["HP"]}
- Full Load Current (Star): {data["FLC_Star"]} A
- Full Load Current (Delta): {data["FLC_Delta"]} A

- MPCB Ratings:
  - ABB: {data["MPCB_ABB"]} (Next: {data["MPCB_ABB_Next"]})
  - Siemens: {data["MPCB_Siemens"]} (Next: {data["MPCB_Siemens_Next"]})
  - L&T: {data["MPCB_L&T"]} (Next: {data["MPCB_L&T_Next"]})
  - Schneider: {data["MPCB_Schneider"]} (Next: {data["MPCB_Schneider_Next"]})

- Contactor (with Amp Rating):
  - ABB: {data["Contactor_ABB"]}
  - Siemens: {data["Contactor_Siemens"]}
  - L&T: {data["Contactor_L&T"]}

- MCCB: {data["MCCB"]}

- Cable Size:
  - Aluminium: {data["Cable_Al"]}
  - Copper: {data["Cable_Cu"]}

- Cable Gland Size: {data["Cable_Gland"]}

- Bearings:
  - ABB DE: {data["ABB_DE_Bearing"]}, NDE: {data["ABB_NDE_Bearing"]}
  - Siemens DE: {data["Siemens_DE_Bearing"]}, NDE: {data["Siemens_NDE_Bearing"]}
"""
        await update.message.reply_text(response)
    except ValueError:
        await update.message.reply_text("Please enter a valid motor kW value (e.g., 11, 18.5, 75).")

# Start the bot
def main():
    app = ApplicationBuilder().token("7885279501:AAHM88TmaaotUUcpIpG-nJZhSMkydYIr62I").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
