import telebot
from telebot import types

TOKEN = "8325286976:AAF5VY_C5GFWNijTUEAZtnX7lm3wDPhBIK0"
ADMIN_ID = 7744385537

bot = telebot.TeleBot(TOKEN)

# ---------------------------------------------------------
# VIDEOLAR UCHUN FILE_ID LAR (Buni o'zingiznikiga almashtirasiz)
# ---------------------------------------------------------
video_files = {
    # Asosiy davlatlar
    "🇯🇵 Yaponiya": "https://t.me/c/3667231673/16",
    "🇬🇧 Angliya": "https://t.me/c/3667231673/15",
    "🇨🇦 Kanada": "https://t.me/c/3667231673/18",
    "🇺🇸 Amerika": "https://t.me/c/3667231673/12",
    "🇸🇦 Arabiston": "https://t.me/c/3667231673/11",
    
    # Shengen Top 10 davlatlari uchun alohida videolar
    "Fransiya": "https://t.me/c/3667231673/6",
    "Italiya": "https://t.me/c/3667231673/10",
    "Germaniya": "https://t.me/c/3667231673/9",
    "Ispaniya": "https://t.me/c/3667231673/5",
    "Gretsiya": "https://t.me/c/3667231673/7",
    "Shveytsariya": "https://t.me/c/3667231673/8",
    "Niderlandiya": "https://t.me/c/3667231673/4",
    "Avstriya": "https://t.me/c/3667231673/3",
    "Chexiya": "https://t.me/c/3667231673/17",
    "Islandiya": "https://t.me/c/3667231673/2"
}

SHENGEN_TOP_10 = [
    "Fransiya", "Italiya", "Germaniya", "Ispaniya", "Gretsiya",
    "Shveytsariya", "Niderlandiya", "Avstriya", "Chexiya", "Islandiya"
]

# --- 1. START ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🇺🇿 Uzbek", "🇷🇺 Russian")
    bot.send_message(message.chat.id, "Tilni tanlang / Выберите язык:", reply_markup=markup)

# --- 2. ISM VA RAQAM (Ketma-ketlik siz aytgandek) ---
@bot.message_handler(func=lambda message: message.text in ["🇺🇿 Uzbek", "🇷🇺 Russian"])
def choose_language(message):
    lang = message.text
    text = "Ism va familiyangizni kiriting:" if lang == "🇺🇿 Uzbek" else "Введите имя и фамилию:"
    msg = bot.send_message(message.chat.id, text, reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, get_name, lang)

def get_name(message, lang):
    name = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("📞 Raqamni yuborish" if lang == "🇺🇿 Uzbek" else "📞 Отправить номер", request_contact=True)
    markup.add(btn)
    msg = bot.send_message(message.chat.id, "Raqamni yuboring:", reply_markup=markup)
    bot.register_next_step_handler(msg, get_phone, lang, name)

def get_phone(message, lang, name):
    phone = message.contact.phone_number if message.contact else message.text
    show_main_menu(message, lang, name, phone)

# --- 3. ASOSIY MENYU ---
def show_main_menu(message, lang, name, phone):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🇯🇵 Yaponiya", "🇪🇺 Shengen", "🇬🇧 Angliya", "🇨🇦 Kanada", "🇺🇸 Amerika", "🇸🇦 Arabiston")
    bot.send_message(message.chat.id, "Davlatni tanlang:", reply_markup=markup)
    bot.register_next_step_handler(message, get_country, lang, name, phone)

# --- 4. SHENGEN TANLANGANDA ---
def get_country(message, lang, name, phone):
    country = message.text
    if country == "🇪🇺 Shengen":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        buttons = [types.KeyboardButton(d) for d in SHENGEN_TOP_10]
        markup.add(*buttons)
        markup.add("⬅️ Ortga")
        msg = bot.send_message(message.chat.id, "Shengen davlatini tanlang:", reply_markup=markup)
        bot.register_next_step_handler(msg, get_shengen_detail, lang, name, phone)
        return
    process_final(message, lang, name, phone, country)

def get_shengen_detail(message, lang, name, phone):
    if message.text == "⬅️ Ortga":
        return show_main_menu(message, lang, name, phone)
    process_final(message, lang, name, phone, message.text, is_shengen=True)

# --- 5. YAKUNIY BOSQICH (Video + Info + Admin) ---
def process_final(message, lang, name, phone, country, is_shengen=False):
    # Har bir davlat uchun info (Namuna)
    info_texts = {
        "Fransiya": "Eyfel minorasi va Parij ko'chalariga sayohat!",
        "Italiya": "Rim, Venetsiya va eng mazali pitsalar yurti!",
        "🇯🇵 Yaponiya": "Kunchiqar mamlakatga viza va sayohat xizmatlari."
    }
    
    info = info_texts.get(country, f"{country} uchun viza va sayohat ma'lumotlari.")
    video_id = video_files.get(country)

    # Videoni yuborish
    if video_id and video_id.startswith("ID_") == False: # ID o'zgartirilgan bo'lsa
        bot.send_video(message.chat.id, video_id, caption=info)
    else:
        bot.send_message(message.chat.id, info)

    # Adminga arizani yuborish
    price = 300 if is_shengen else 0 # Narxlarni o'zingiz sozlashingiz mumkin
    admin_text = (
        f"📝 Yangi ariza!\n\n👤 Ism: {name}\n📞 Tel: {phone}\n"
        f"🌍 Davlat: {'Shengen ('+country+')' if is_shengen else country}\n"
        f"💰 Xizmat haqi: {price if price > 0 else '350'}$ \n💡 Qiziqish bildirdi ✅"
    )
    bot.send_message(ADMIN_ID, admin_text)
    bot.send_message(message.chat.id, "Raxmat! Ma'lumotlaringiz qabul qilindi.", reply_markup=types.ReplyKeyboardRemove())

# --- FILE_ID larni olish uchun yordamchi funksiya ---
@bot.message_handler(content_types=['video'])
def capture_video_id(message):
    bot.reply_to(message, f"Ushbu videoning ID raqami:\n\n`{message.video.file_id}`", parse_mode="Markdown")

@bot.message_handler(content_types=['video'])
def get_video_id(message):
    # Bu kod botga video yuborsangiz, uning ID raqamini sizga qaytaradi
    bot.reply_to(message, f"Siz yuborgan videoning ID raqami:\n\n`{message.video.file_id}`", parse_mode="Markdown")
bot.polling()
