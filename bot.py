import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, ChatJoinRequestHandler
from telegram.request import HTTPXRequest
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Render ke liye chota sa dummy web server taake port ka error na aaye
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

def main():
    # Web server ko background mein chalane ke liye thread start kar rahe hain
    server_thread = threading.Thread(target=run_web_server, daemon=True)
    server_thread.start()

    TOKEN = "8881957837:AAE6HXQLzFhWvk82CLu4Z1j2ZP1euB9Tdb0"

    custom_request = HTTPXRequest(connect_timeout=30.0, read_timeout=30.0)
    application = ApplicationBuilder().token(TOKEN).request(custom_request).build()

    application.add_handler(ChatJoinRequestHandler(handle_join_request))

    print("M.K TRADER Bot successfully start ho gaya hai aur requests sun raha hai...")
    application.run_polling()

if __name__ == '__main__':
    main()
