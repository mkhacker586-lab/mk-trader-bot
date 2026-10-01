import logging
import os
import asyncio
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, ChatJoinRequestHandler, CommandHandler

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Render port requirement ke liye dummy web server
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"M.K TRADER Bot is running 24/7!")

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

# Function 1: Sirf Pehli Post (Join Request ke liye)
async def send_first_post_only(chat_id, user_first_name, context):
    photo_url = "https://i.postimg.cc/Pvt9mWMg/image.jpg"
    caption_text_1 = (
        f"👑 **M.K TRADER** mein Khush Amdeed, {user_first_name}!\n\n"
        "⚡ **READY FOR PROFITABLE TRADING?**\n\n"
        "📊 **Daily Updates:**\n"
        "• High Accuracy Signals\n"
        "• Smart Market Analysis\n"
        "• VIP Setup & Guidance\n\n"
        "🔗 **Official Channel Links:**\n"
        "https://t.me/+neTu5arl0spkNjFk\n"
        "https://t.me/+neTu5arl0spkNjFk\n"
        "https://t.me/+neTu5arl0spkNjFk"
    )
    keyboard_1 = [
        [InlineKeyboardButton("🚀 JOIN VIP CHANNEL 🚀", url="https://t.me/+neTu5arl0spkNjFk")]
    ]
    
    try:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=photo_url,
            caption=caption_text_1,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard_1)
        )
    except Exception as e:
        print(f"Pehli post nahi gayi: {e}")

# Function 2: Dono Posts Ek Sath (/start dabane par)
async def send_both_posts(chat_id, user_first_name, context):
    # Pehle pehli post bhejo
    await send_first_post_only(chat_id, user_first_name, context)

    # Thoda sa gap dono messages ke darmiyan
    await asyncio.sleep(1)

    # Phir doosri (Personal Recovery Session) post bhejo
    caption_text_2 = (
        "⭐ WELCOME TO M.K TRADER ⭐\n\n"
        "🚨 **PERSONAL RECOVERY SESSION OPEN** 🚨\n\n"
        "📉 Losing trades again and again?\n"
        "🖤 Low balance? No proper strategy?\n"
        "⚡️ Time to recover with smart execution!\n\n"
        "🔥 **PERSONAL 1-on-1 LOSS RECOVERY SESSION** 🔥\n\n"
        "✅ Special OTC Trading Strategy\n"
        "✅ Accurate Entry Timing\n"
        "✅ Controlled Risk Management\n"
        "✅ Professional Account Handling 💼\n"
        "✅ Step-by-Step Recovery Plan\n\n"
        "💫 *Trade Smart — Recover Slowly & Safely* 🚀\n\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "🎯 **Create Your Account Here:**\n"
        "🔗 https://broker-qx.pro/?lid=1614510\n\n"
        "🏦 *Deposit & Send Your Trader ID For Access ✅*\n\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "🌹 **LIMITED SLOTS AVAILABLE** 💯\n"
        "💖 *Only Serious Traders Allowed* 💖"
    )
    
    keyboard_2 = [
        [InlineKeyboardButton("⭐ CLICK HERE AND JOIN VIP ⭐", url="https://broker-qx.pro/?lid=1614510")],
        [InlineKeyboardButton("💬 CONTACT FOR PERSONAL SESSION", url="https://t.me/MK_TRADER586")]
    ]

    try:
        await context.bot.send_message(
            chat_id=chat_id,
            text=caption_text_2,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard_2)
        )
    except Exception as e:
        print(f"Doosri post nahi gayi: {e}")

# Jab koi channel join request bheje (Sirf pehli post aayegi)
async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user
    chat = update.chat_join_request.chat
    print(f"Join request aayi hai: {user.first_name} ki taraf se channel {chat.title} ke liye.")
    await send_first_post_only(user.id, user.first_name, context)

# Jab koi /start dabaye (Dono posts ikathi aayengi)
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    print(f"/start command aayi hai: {user.first_name} ki taraf se.")
    await send_both_posts(user.id, user.first_name, context)

async def main_bot():
    TOKEN = "8567527528:AAHPavhyxDBFDFImZph7gyGvj9PvdVUAuZw"

    application = ApplicationBuilder().token(TOKEN).build()

    # Handlers add kar rahe hain
    application.add_handler(ChatJoinRequestHandler(handle_join_request))
    application.add_handler(CommandHandler("start", start_command))

    print("M.K TRADER Bot successfully start ho gaya hai aur sab kuch sun raha hai...")
    
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    while True:
        await asyncio.sleep(3600)

def run_async_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main_bot())

def main():
    server_thread = threading.Thread(target=run_web_server, daemon=True)
    server_thread.start()
    run_async_loop()

if __name__ == '__main__':
    main()
