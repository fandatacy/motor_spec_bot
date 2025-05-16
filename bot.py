import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "7885279501:AAEaFgFlPVie986wExCO-8LEaljYcjECuyM"

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
    return f"""
⚡ *Motor Details for {kw} kW* ⚡

🏷️ *Horsepower (HP):* `{data["hp"]}`
⚡ *Full Load Current:*
   - Star: `{data["flc_star"]} A`
   - Delta: `{data["flc_delta"]} A`

🔧 *Protection Devices:*
   - MPCB Rating: `{data["mpcb"]["schneider"]}`
   - MCCB: `{data["mccb"]["abb"]}`

🔌 *Contactor:*
   - Siemens: `{data["contactor"]["siemens"]}`
   - ABB: `{data["contactor"]["abb"]}`
   - L&T: `{data["contactor"]["lt"]}`

🔗 *Cable Size:*
   - Aluminium: `{data["cable"]["al"]}`
   - Copper: `{data["cable"]["cu"]}`
   - Gland Size: `{data["cable_gland"]}`

🛠️ *Bearing Numbers:*
   - ABB: 
     - DE: `{data["bearing"]["abb_de"]}`
     - NDE: `{data["bearing"]["abb_nde"]}`
   - Siemens: 
     - DE: `{data["bearing"]["siemens_de"]}`
     - NDE: `{data["bearing"]["siemens_nde"]}`

📌 *Note:* All ratings are recommendations. Verify with actual load conditions.
"""

async def motor_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("🔍 Please provide motor kW. Example: /motor 5.5")
        return

    kw_input = context.args[0]
    normalized_kw = normalize_kw(kw_input)

    if normalized_kw is None:
        await update.message.reply_text("❌ Invalid input. Please use a number (e.g., /motor 5.5)")
        return

    data = motor_data.get(normalized_kw)
    if data:
        reply = format_motor_info(data, normalized_kw)
        await update.message.reply_text(reply, parse_mode="Markdown")
    else:
        await update.message.reply_text(
            f"⚠️ Data Will Available Soon for {normalized_kw} kW\n\n"
            f"Currently available sizes: {', '.join(sorted(motor_data.keys()))}",
            parse_mode="Markdown"
        )

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("motor", motor_info))
app.run_polling()
