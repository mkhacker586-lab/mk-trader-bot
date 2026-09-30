import logging
import os
import asyncio
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, ChatJoinRequestHandler
from telegram.request import HTTPXRequest

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

async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user
    chat = update.chat_join_request.chat
    
    print(f"Join request aayi hai: {user.first_name} ki taraf se channel {chat.title} ke liye.")
    
    photo_url = "https://i.postimg.cc/Pvt9mWMg/image.jpg"
    
    caption_text = (
        f"👑 **M.K TRADER** mein Khush Amdeed, {user.first_name}!\n\n"
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
    
    keyboard = [
        [InlineKeyboardButton("🚀 JOIN VIP CHANNEL 🚀", url="https://t.me/+neTu5arl0spkNjFk")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await context.bot.send_photo(
            chat_id=user.id,
            photo=photo_url,
            caption=caption_text,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
        print(f"Professional post successfully sent to {user.first_name}")
    except Exception as e:
        print(f"Message nahi ja saka: {e}")

async def main_bot():
    TOKEN = "8881957837:AAE6HXQLzFhWvk82CLu4Z1j2ZP1euB9Tdb0"

    custom_request = HTTPXRequest(connect_timeout=30.0, read_timeout=30.0)
    application = ApplicationBuilder().token(TOKEN).request(custom_request).build()

    application.add_handler(ChatJoinRequestHandler(handle_join_request))

    print("M.K TRADER Bot successfully start ho gaya hai aur requests sun raha hai...")
    
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    # Bot ko chalate rakhne ke liye infinite sleep
    while True:
        await asyncio.sleep(3600)

def run_async_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main_bot())

def main():
    # Web server background thread mein start karo
    server_thread = threading.Thread(target=run_web_server, daemon=True)
    server_thread.start()

    # Bot event loop thread mein start karo
    run_async_loop()

if __name__ == '__main__':
    main()
