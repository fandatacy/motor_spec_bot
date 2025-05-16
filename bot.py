import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "7885279501:AAFU7y-RsZ9S3OGNp1ekh1KIX1fBibbtchI"

with open("data.json") as f:
    motor_data = json.load(f)

def find_closest_kw(requested_kw):
    requested_kw = float(requested_kw)
    available_kws = [float(k) for k in motor_data.keys()]
    closest = min(available_kws, key=lambda x: abs(x - requested_kw))
    return str(closest)

async def motor_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide motor kW like: `/motor 15`")
        return
    
    try:
        requested_kw = float(context.args[0])
        kw_key = find_closest_kw(requested_kw)
        data = motor_data.get(kw_key)

        if not data:
            await update.message.reply_text("Motor kW not found in database.")
            return

        reply = f"""<b>Motor Details for {kw_key} kW</b>\n
<b>Horsepower (HP):</b> {data['hp']} HP
<b>Full Load Current:</b>
- <b>Star:</b> {data['flc_star']} A
- <b>Delta:</b> {data['flc_delta']} A

<b>MPCB Rating:</b>
- ABB: {data['mpcb']['abb']} ({data['mpcb']['abb_range']})
- Siemens: {data['mpcb']['siemens']} ({data['mpcb']['siemens_range']})
- L&T: {data['mpcb']['lt']} ({data['mpcb']['lt_range']})
- Schneider: {data['mpcb']['schneider']} ({data['mpcb']['schneider_range']})

<b>Contactor:</b>
- ABB: {data['contactor']['abb']} ({data['contactor']['abb_amp']} A)
- Siemens: {data['contactor']['siemens']} ({data['contactor']['siemens_amp']} A)
- L&T: {data['contactor']['lt']} ({data['contactor']['lt_amp']} A)

<b>MCCB:</b> {data['mccb']}

<b>Cable Size:</b>
- Aluminium: {data['cable']['al']}
- Copper: {data['cable']['cu']}

<b>Cable Gland:</b> {data['cable_gland']}

<b>Bearings:</b>
- ABB: DE: {data['bearing']['abb_de']} | NDE: {data['bearing']['abb_nde']}
- Siemens: DE: {data['bearing']['siemens_de']} | NDE: {data['bearing']['siemens_nde']}
"""
        await update.message.reply_text(reply, parse_mode="HTML")

    except ValueError:
        await update.message.reply_text("Please provide a valid number like: `/motor 7.5`")

# Setup Application
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("motor", motor_info))
app.run_polling()
