import csv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "7885279501:AAFzKMmLZ6JLzpQHOuSKlE8SMsXN5pykz8k"  # Replace with your real bot token

motor_data = {}

# Load CSV data into dictionary
with open('data.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        kw = float(row['kW'])
        motor_data[kw] = row

def find_closest_kw(input_kw):
    kws = sorted(motor_data.keys())
    closest = min(kws, key=lambda x: abs(x - input_kw))
    return closest

async def motor_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide motor kW. Example: /motor 7.5")
        return

    try:
        input_kw = float(context.args[0])
    except ValueError:
        await update.message.reply_text("Invalid input. Please enter a valid motor kW number.")
        return

    closest_kw = find_closest_kw(input_kw)
    data = motor_data[closest_kw]

    reply = f"""Motor Details for {data['kW']} kW

Horsepower (HP): {data['HP']}
Full Load Current (Star): {data['FLC_star']} A
Full Load Current (Delta): {data['FLC_delta']} A

MPCB Ratings:
 - Primary: {data['MPCB_primary']}
 - Next: {data['MPCB_next']}

Contactor (Model & Amp):
 - Siemens: {data['Contactor_Siemens']} ({data['Contactor_Siemens_amp']}A)
 - ABB: {data['Contactor_ABB']} ({data['Contactor_ABB_amp']}A)
 - L&T: {data['Contactor_LT']} ({data['Contactor_LT_amp']}A)

MCCB: {data['MCCB']}

Cable Size:
 - Aluminum: {data['Cable_Al']}
 - Copper: {data['Cable_Cu']}

Cable Gland Size: {data['Cable_Gland']}

Bearing Numbers:
 - DE (ABB): {data['Bearing_DE_ABB']} | NDE (ABB): {data['Bearing_NDE_ABB']}
 - DE (Siemens): {data['Bearing_DE_Siemens']} | NDE (Siemens): {data['Bearing_NDE_Siemens']}
"""
    await update.message.reply_text(reply)

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("motor", motor_info))
    print("Bot started...")
    app.run_polling()
