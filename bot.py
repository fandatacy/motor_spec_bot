import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"

with open("data.json") as f:
    motor_data = json.load(f)

def format_motor_data(data):
    return f"""
<b>Motor Details for {data['kW']} kW</b>

<b>Horsepower (HP):</b> {data['HP']}
<b>Full Load Current:</b>
 - Star: {data['FLC_Star']}
 - Delta: {data['FLC_Delta']}

<b>MPCB Ratings:</b>
 - ABB: {data['MPCB']['Primary']['ABB']} → {data['MPCB']['Next']['ABB']}
 - Siemens: {data['MPCB']['Primary']['Siemens']} → {data['MPCB']['Next']['Siemens']}
 - L&T: {data['MPCB']['Primary']['L&T']} → {data['MPCB']['Next']['L&T']}
 - Schneider: {data['MPCB']['Primary']['Schneider']} → {data['MPCB']['Next']['Schneider']}

<b>Contactor (Model & Amp):</b>
 - ABB: {data['Contactor']['ABB']}
 - Siemens: {data['Contactor']['Siemens']}
 - L&T: {data['Contactor']['L&T']}

<b>MCCB:</b> {data['MCCB']}

<b>Cable Size:</b>
 - Aluminium: {data['Cable']['Al']}
 - Copper: {data['Cable']['Cu']}

<b>Cable Gland:</b> {data['Cable_Gland']}

<b>Bearings:</b>
 - ABB: DE: {data['Bearing']['ABB']['DE']} | NDE: {data['Bearing']['ABB']['NDE']}
 - Siemens: DE: {data['Bearing']['Siemens']['DE']} | NDE: {data['Bearing']['Siemens']['NDE']}
"""

async def motor_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        kW = context.args[0]
        if kW in motor_data:
            message = format_motor_data(motor_data[kW])
        else:
            message = "Motor kW not found in database. Please try another value."
        await update.message.reply_text(message, parse_mode='HTML')
    except IndexError:
        await update.message.reply_text("Please provide motor kW. Usage: /motor 0.37", parse_mode='HTML')

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("motor", motor_info))
    app.run_polling()
