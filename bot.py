import telebot

TOKEN = "8325286976:AAF5VY_C5GFWNijTUEAZtnX7lm3wDPhBIK0"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['video'])
def get_id(message):
    file_id = message.video.file_id
    bot.reply_to(message, f"Video ID raqami:\n\n`{file_id}`", parse_mode="Markdown")

print("Bot yoqildi. Endi botga video yuboring...")
bot.polling()
