import telebot
from telebot import types

# --- SOZLAMALAR ---
TOKEN = "8325286976:AAFZMLbMZZKsxicZIOK7_cKx00J3YqtZOXc"
ADMIN_ID = 7744385537
bot = telebot.TeleBot(TOKEN)

# --- VIDEO ID LAR UCHUN LUG'AT ---
# Bot sizga bergan ID raqamlarni shu yerga qo'yib chiqasiz
video_files = {
    "🇯🇵 Yaponiya": "BAACAgIAAxkBAAIB6Glnic2r0KAWYmJNQ7xE1_lqlGDUAAJ2iwACNhI4S3zijoY1GOXiOAQ",
    "🇬🇧 Angliya": "BAACAgIAAxkBAAIB5mlnibk7xquqwi_fVuz725OXftmOAAJziwACNhI4S9xA5aQxC0rcOAQ",
    "🇨🇦 Kanada": "BAACAgIAAxkBAAIBzGlnhblOFlvwp-4T8VfUXbAG7H5YAAJfiwACNhI4S-p10mhwH2ApOAQ",
    "🇺🇸 Amerika": "BAACAgIAAxkBAAIB5Glniaz8YJhe9uvfLTupStpgwdZTAAJyiwACNhI4S2ptgsHCfeINOAQ",
    "🇸🇦 Arabiston": "BAACAgIAAxkBAAIB4mlniZszd7NMm-0krg6OmFENPr4HAAJxiwACNhI4S6N7g4T8-XyTOAQ",
    "Fransiya": "BAACAgIAAxkBAAIB4GlniYBuU3IbKc9669XTI5K9guByAAJwiwACNhI4S-du9XRCJvmTOAQ",
    "Italiya": "BAACAgIAAxkBAAIB3mlniWyX5r-3quvyaNlGiQABkTKVogACbYsAAjYSOEsYcvnXHSurPTgE",
    "Germaniya": "BAACAgIAAxkBAAIB3GlniVhYheZ7BYPnODnAskhXpYwCAAJriwACNhI4SzaytBfbcgk9OAQ",
    "Ispaniya": "BAACAgIAAxkBAAIB2mlniUla9ZDrGquHLc0mMMAbRNfrAAJqiwACNhI4Sx9fCQOEnwf-OAQ",
    "Gretsiya": "BAACAgIAAxkBAAIB2GlniQftxPIGnjRDv8g4rbYzd99AAAJpiwACNhI4S_s4v4uIs5JyOAQ",
    "Shveytsariya": "BAACAgIAAxkBAAIB1mlniPPHoQp972kAAb_-aSgeyEHa3gACaIsAAjYSOEvQ72VoKaMlAjgE",
    "Niderlandiya": "BAACAgIAAxkBAAIB1GlniMRo7BLvf84iWCXwKmkjrGR7AAJniwACNhI4S2nehac_uquXOAQ",
    "Avstriya": "BAACAgIAAxkBAAIB0mlniKUK9npNFReB8QjHmWqlp-rKAAJliwACNhI4S0axPF6AslVJOAQ",
    "Chexiya": "BAACAgIAAxkBAAIB0GlniIxdZTBl1KHslqf62BnP-xlYAAJkiwACNhI4S8-auS7ofKGXOAQ",
    "Islandiya": "BAACAgIAAxkBAAIBzmlniHIkGOGhp-pT5F_tImFkH690AAJiiwACNhI4SxMbBZqI0cs9OAQ"
}

SHENGEN_TOP_10 = [
    "Fransiya", "Italiya", "Germaniya", "Ispaniya", "Gretsiya",
    "Shveytsariya", "Niderlandiya", "Avstriya", "Chexiya", "Islandiya"
]

# --- 1. TILNI TANLASH ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🇺🇿 Uzbek", "🇷🇺 Russian")
    bot.send_message(message.chat.id, "Tilni tanlang / Выберите язык:", reply_markup=markup)

# --- 2. ISM VA FAMILIYA ---
@bot.message_handler(func=lambda message: message.text in ["🇺🇿 Uzbek", "🇷🇺 Russian"])
def choose_language(message):
    lang = message.text
    text = "Ism va familiyangizni kiriting:" if lang == "🇺🇿 Uzbek" else "Введите ваше имя и фамилию:"
    msg = bot.send_message(message.chat.id, text, reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, get_name, lang)

def get_name(message, lang):
    name = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_text = "📞 Raqamni yuborish" if lang == "🇺🇿 Uzbek" else "📞 Отправить номер"
    markup.add(types.KeyboardButton(btn_text, request_contact=True))
    
    text = "Telefon raqamingizni yuboring:" if lang == "🇺🇿 Uzbek" else "Отправьте ваш номер телефона:"
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, get_phone, lang, name)

# --- 3. TELEFON RAQAM VA ASOSIY MENYU ---
def get_phone(message, lang, name):
    phone = message.contact.phone_number if message.contact else message.text
    show_main_menu(message, lang, name, phone)

def show_main_menu(message, lang, name, phone):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🇯🇵 Yaponiya", "🇪🇺 Shengen", "🇬🇧 Angliya", "🇨🇦 Kanada", "🇺🇸 Amerika", "🇸🇦 Arabiston")
    
    text = "Davlatni tanlang:" if lang == "🇺🇿 Uzbek" else "Выберите страну:"
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, handle_country_choice, lang, name, phone)

# --- 4. SHENGEN VA BOSHQA DAVLATLAR ---
def handle_country_choice(message, lang, name, phone):
    choice = message.text
    if choice == "🇪🇺 Shengen":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        buttons = [types.KeyboardButton(d) for d in SHENGEN_TOP_10]
        markup.add(*buttons)
        markup.add("⬅️ Ortga")
        
        text = "Shengen hududidagi top 10 sayohat davlati:" if lang == "🇺🇿 Uzbek" else "Топ 10 стран Шенгена:"
        msg = bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(msg, handle_shengen_choice, lang, name, phone)
    else:
        process_final(message, lang, name, phone, choice)

def handle_shengen_choice(message, lang, name, phone):
    if message.text == "⬅️ Ortga":
        return show_main_menu(message, lang, name, phone)
    process_final(message, lang, name, phone, message.text, is_shengen=True)

# --- 5. YAKUNIY BOSQICH: VIDEO VA ADMIN ---
def process_final(message, lang, name, phone, country, is_shengen=False):
    # Video yuborish
    video_id = video_files.get(country)
    caption = f"{country} uchun viza va sayohat xizmatlari haqida ma'lumot."
    
    if video_id and "ID_" not in video_id:
        try:
            bot.send_video(message.chat.id, video_id, caption=caption)
        except:
            bot.send_message(message.chat.id, caption)
    else:
        bot.send_message(message.chat.id, caption)

    # Adminga ma'lumot yuborish
    admin_msg = (
        f"🔔 YANGI ARIZA!\n\n"
        f"👤 Ism: {name}\n"
        f"📞 Tel: {phone}\n"
        f"🌍 Davlat: {country} {'(Shengen)' if is_shengen else ''}\n"
        f"✅ Qiziqish bildirdi."
    )
    bot.send_message(ADMIN_ID, admin_msg)
    
    thanks = "Raxmat! Ma'lumotlaringiz qabul qilindi." if lang == "🇺🇿 Uzbek" else "Спасибо! Данные приняты."
    bot.send_message(message.chat.id, thanks, reply_markup=types.ReplyKeyboardRemove())

# --- VIDEO ID RAQAMINI ANIQLASH UCHUN YORDAMCHI ---
@bot.message_handler(content_types=['video'])
def get_file_id(message):
    bot.reply_to(message, f"Ushbu videoning ID raqami:\n\n`{message.video.file_id}`", parse_mode="Markdown")

print("Bot @iamdarkhanovbot ishga tushdi...")
bot.polling()
