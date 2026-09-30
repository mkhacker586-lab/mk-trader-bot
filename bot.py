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

# Common function jo dono posts bhejayega
async def send_welcome_posts(chat_id, user_first_name, context):
    # 1st Post: Photo aur Welcome Message (Sirf isme channel join ka button hoga)
    photo_url = "https://i.postimg.cc/Pvt9mWMg/image.jpg"
    caption_text_1 = (
        f"👑 **M.K TRADER** mein Khush Amdeed, {user_first_name}!\n\n"
        "⚡ **READY FOR PROFITABLE TRADING?**\n\n"
        "📊 **Daily Updates:**\n"
        "• High Accuracy Signals\n"
        "• Smart Market Analysis\n"
        "• VIP Setup & Guidance\n\n"
        "🔗 **Official Channel Links:**\n"
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

    # Thoda sa gap dono messages ke darmiyan
    await asyncio.sleep(1)

    # 2nd Post: Quotex Signals, $30 Deposit aur Broker link wala button
    caption_text_2 = (
        "🔥📈 **WANT 10 FREE NON-MTG BUG QUOTEX SIGNALS?**\n\n"
        "👑 Hi guys, ready ho jao profit banane ke liye!\n\n"
        "💎 **JOIN VIP IN 3 EASY STEPS:**\n\n"
        "⭐️ **1ST:** Create New Account using our official link:\n"
        "🔗 https://broker-qx.pro/?lid=1614511\n\n"
        "⭐️ **2ND:** Deposit Minimum $30 💵\n\n"
        "⭐️ **3RD:** Send your Trader ID for confirmation and get added to M.K VIP Group! 🚀\n\n"
        "⏰ **Signals Starting in 5 Minutes!**"
    )
    
    # Yahan button change kar diya hai taake broker link khule
    keyboard_2 = [
        [InlineKeyboardButton("⭐ CLICK HERE AND JOIN VIP ⭐", url="https://broker-qx.pro/?lid=1614511")],
        [InlineKeyboardButton("💬 CONTACT ADMIN", url="https://t.me/MK_TRADER586")]
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

# Jab koi channel join request bheje
async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user
    chat = update.chat_join_request.chat
    print(f"Join request aayi hai: {user.first_name} ki taraf se channel {chat.title} ke liye.")
    await send_welcome_posts(user.id, user.first_name, context)

# Jab koi /start dabaye
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    print(f"/start command aayi hai: {user.first_name} ki taraf se.")
    await send_welcome_posts(user.id, user.first_name, context)

async def main_bot():
    TOKEN = "8881957837:AAE6HXQLzFhWvk82CLu4Z1j2ZP1euB9Tdb0"

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
