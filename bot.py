import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, ChatJoinRequestHandler
from telegram.request import HTTPXRequest

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user
    chat = update.chat_join_request.chat
    
    print(f"Join request aayi hai: {user.first_name} ki taraf se channel {chat.title} ke liye.")
    
    # Aapka direct image link jo bot ke andar chalega
    photo_url = "https://i.postimg.cc/Pvt9mWMg/image.jpg" # (Agar direct image load na ho toh direct direct link yahan ayega)
    
    # Aapka chota, pyara aur copy hone wala text 3 links ke sath
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
    
    # Neechye aane wala clickable button
    keyboard = [
        [InlineKeyboardButton("🚀 JOIN VIP CHANNEL 🚀", url="https://t.me/+neTu5arl0spkNjFk")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        # Yeh function image, text aur button aik sath user ko bhejega
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
    # Apna Bot Token yahan dalein
    TOKEN = "8881957837:AAE6HXQLzFhWvk82CLu4Z1j2ZP1euB9Tdb0"

    custom_request = HTTPXRequest(connect_timeout=30.0, read_timeout=30.0)
    application = ApplicationBuilder().token(TOKEN).request(custom_request).build()

    application.add_handler(ChatJoinRequestHandler(handle_join_request))

    print("M.K TRADER Bot successfully start ho gaya hai aur requests sun raha hai...")
    application.run_polling()

if __name__ == '__main__':
    main()
