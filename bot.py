import telebot
from telebot import types

# -------------------
# TOKEN VA ADMIN ID
# -------------------
TOKEN = "8325286976:AAF5VY_C5GFWNijTUEAZtnX7lm3wDPhBIK0"
ADMIN_ID = 7744385537
ADMIN_LINK = "https://t.me/premium_vza"

bot = telebot.TeleBot(TOKEN)

# -------------------
# BOSHLANG'ICH /start
# -------------------
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🇺🇿 Uzbek", "🇷🇺 Russian")
    bot.send_message(message.chat.id, "Tilni tanlang / Выберите язык:", reply_markup=markup)

# -------------------
# TIL TANLASH
# -------------------
@bot.message_handler(func=lambda message: message.text in ["🇺🇿 Uzbek", "🇷🇺 Russian"])
def choose_language(message):
    lang = message.text
    markup = types.ReplyKeyboardRemove()
    
    text = "Ism va familiyangizni kiriting:" if lang == "🇺🇿 Uzbek" else "Введите ваше имя и фамилию:"
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, get_name, lang)

# -------------------
# ISM/FAMILIYA
# -------------------
def get_name(message, lang):
    name = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if lang == "🇺🇿 Uzbek":
        btn_phone = types.KeyboardButton("📞 Raqamni yuborish", request_contact=True)
        back, text = "⬅️ Ortga", "Telefon raqamingizni yuboring:"
    else:
        btn_phone = types.KeyboardButton("📞 Отправить номер", request_contact=True)
        back, text = "⬅️ Назад", "Отправьте ваш номер телефона:"
    
    markup.add(btn_phone)
    markup.add(back)
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, get_phone, lang, name)

# -------------------
# TELEFON RAQAMI
# -------------------
def get_phone(message, lang, name):
    if message.text in ["⬅️ Ortga", "⬅️ Назад"]:
        return choose_language(message)

    phone = message.contact.phone_number if message.contact else message.text

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if lang == "🇺🇿 Uzbek":
        markup.add("🇯🇵 Yaponiya", "🇪🇺 Shengen", "🇬🇧 Angliya")
        markup.add("🇨🇦 Kanada", "🇺🇸 Amerika", "🇸🇦 Arabiston")
        markup.add("⬅️ Ortga")
        bot.send_message(message.chat.id, "Qaysi davlatga sayohat qilishni istaysiz?", reply_markup=markup)
    else:
        markup.add("🇯🇵 Япония", "🇪🇺 Шенген", "🇬🇧 Англия")
        markup.add("🇨🇦 Канада", "🇺🇸 Америка", "🇸🇦 Саудовская Аравия")
        markup.add("⬅️ Назад")
        bot.send_message(message.chat.id, "В какую страну вы хотите поехать?", reply_markup=markup)
    
    bot.register_next_step_handler(message, get_country, lang, name, phone)

# -------------------
# DAVLAT TANLASH VA OXIRGI MENYULAR
# -------------------
def get_country(message, lang, name, phone):
    country = message.text
    if country in ["⬅️ Ortga", "⬅️ Назад"]:
        return get_name(message, lang)

    info_dict = {
        "uz": {
            "🇯🇵 Yaponiya": "Siz oldin Yaponiyaga bormaganmisiz?...",
            "🇪🇺 Shengen": "Shengen hududidagi Evropaning go‘zal shaharlarini...",
            "🇬🇧 Angliya": "Angliyaga tashrif buyurib, Londonning tarixiy...",
            "🇨🇦 Kanada": "Kanadaga sayohat qilmoqchimisiz?...",
            "🇺🇸 Amerika": "Amerikaga sayohat qilmoqchimisiz?...",
            "🇸🇦 Arabiston": "Saudiya Arabistoniga borib, tarixiy masjidlar..."
        },
        "ru": {
            "🇯🇵 Япония": "Вы раньше не были в Японии?...",
            "🇪🇺 Шенген": "Вы хотите открыть для себя красивые города...",
            "🇬🇧 Англия": "Хотите посетить Англию...",
            "🇨🇦 Канада": "Хотите поехать в Канаду?...",
            "🇺🇸 Америка": "Планируете поездку в Америку?...",
            "🇸🇦 Саудовская Аравия": "Хотите посетить Саудовскую Аравию?..."
        }
    }

    current_info = info_dict["uz"].get(country) if lang=="🇺🇿 Uzbek" else info_dict["ru"].get(country)
    if not current_info:
        return get_phone(message, lang, name)

    # Davlat haqida ma'lumot
    bot.send_message(message.chat.id, current_info)

    # Oxirgi menyu tugmalari
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    if lang == "🇺🇿 Uzbek":
        btn_price = "💰 Narxni bilish (Lichka)"
        btn_contact = "📞 Mutaxassis bog'lansin"
        back = "⬅️ Ortga"
        prompt = "Kerakli bo'limni tanlang:"
    else:
        btn_price = "💰 Узнать цену (Личка)"
        btn_contact = "📞 Связаться со специалистом"
        back = "⬅️ Назад"
        prompt = "Выберите нужный раздел:"

    markup.add(btn_price, btn_contact, back)
    msg = bot.send_message(message.chat.id, prompt, reply_markup=markup)
    bot.register_next_step_handler(msg, final_step, lang, name, phone, country)

# -------------------
# OXIRGI BOSQICH MANTIQI
# -------------------
def final_step(message, lang, name, phone, country):
    text = message.text

    if text in ["⬅️ Ortga", "⬅️ Назад"]:
        return get_phone(message, lang, name)

    if "💰 Narxni bilish" in text or "💰 Узнать цену" in text:
        # Inline tugma bilan lichkaga yuborish
        inline = types.InlineKeyboardMarkup()
        btn_text = "Yozish ✍️" if lang == "🇺🇿 Uzbek" else "Написать ✍️"
        inline.add(types.InlineKeyboardButton(text=btn_text, url=ADMIN_LINK))
        bot.send_message(message.chat.id, "Pastdagi tugmani bosing va bizga yozing:", reply_markup=inline)
        
        # Adminga xabar yuborish (shunchaki foydalanuvchi qiziqqanini bilish uchun)
        bot.send_message(ADMIN_ID, f"👀 Foydalanuvchi narxni bilish uchun lichkaga o'tdi:\n👤 {name}\n📞 {phone}")

    elif "📞 Mutaxassis" in text or "📞 Связаться" in text:
        bot.send_message(message.chat.id, "✅ So'rovingiz qabul qilindi. Mutaxassis tez orada bog'lanadi!", reply_markup=types.ReplyKeyboardRemove())
        bot.send_message(ADMIN_ID, f"🔔 YANGI ARIZA (Qayta aloqa):\n👤 Ism: {name}\n📞 Tel: {phone}\n🌍 Davlat: {country}")
    
    else:
        # Agar boshqa narsa yozsa, menyuni qayta ko'rsatish
        return get_country(message, lang, name, phone)

bot.polling()
