import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "7885279501:AAFU7y-RsZ9S3OGNp1ekh1KIX1fBibbtchI"

with open("data.json") as f:
    motor_data = json.load(f)

def normalize_kw(input_str):
    try:
        num = float(input_str)
        if num.is_integer():
            return str(int(num))
        return "{0:.10f}".format(num).rstrip('0').rstrip('.')
    except ValueError:
        return None

def format_motor_info(data, kw):
    # Format MPCB recommendations
    mpcb_recommend = "\nMPCB Recommendations:\n"
    for brand in ['abb', 'siemens', 'lt', 'schneider']:
        mpcb_recommend += f"- {brand.upper()}: `{data['mpcb'][brand]['recommend']}` ({data['mpcb'][brand]['range']})\n"

    # Format Contactor recommendations
    contactor_recommend = "\nContactor Recommendations:\n"
    for brand in ['abb', 'siemens', 'lt']:
        contactor_recommend += f"- {brand.upper()}: `{data['contactor'][brand]['recommend']}` ({data['contactor'][brand]['amp']}A)\n"

    # Format MCCB data
    mccb_info = "\nMCCB Ratings:\n"
    for brand in ['abb', 'siemens', 'lt', 'schneider']:
        mccb_info += f"- {brand.upper()}: `{data['mccb'][brand]}`\n"

    return f'''
Motor Details for {kw} kW

Horsepower (HP): `{data["hp"]}`
Full Load Current (Star): `{data["flc_star"]} A`
Full Load Current (Delta): `{data["flc_delta"]} A`
{mpcb_recommend}
{contactor_recommend}
{mccb_info}
Cable Size:
- Aluminium: `{data["cable"]["al"]}`
- Copper: `{data["cable"]["cu"]}`
Cable Gland: `{data["cable_gland"]}`

Bearing Numbers:
- ABB: DE `{data["bearing"]["abb_de"]}`, NDE `{data["bearing"]["abb_nde"]}`
- Siemens: DE `{data["bearing"]["siemens_de"]}`, NDE `{data["bearing"]["siemens_nde"]}`
'''

async def motor_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide motor kW. Example: /motor 5.5")
        return

    kw_input = context.args[0]
    normalized_kw = normalize_kw(kw_input)

    if normalized_kw is None:
        await update.message.reply_text("Invalid input. Please use a number (e.g., /motor 5.5)")
        return

    data = motor_data.get(normalized_kw)
    if data:
        reply = format_motor_info(data, normalized_kw)
        await update.message.reply_text(reply, parse_mode="Markdown")
    else:
        await update.message.reply_text(f"Data not found for {normalized_kw} kW. Available sizes: {', '.join(sorted(motor_data.keys()))}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("motor", motor_info))
app.run_polling()
