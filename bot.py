import telebot
from telebot import types

# -------------------
# TOKEN VA ADMIN ID
# -------------------
TOKEN = "8325286976:AAF5VY_C5GFWNijTUEAZtnX7lm3wDPhBIK0"
ADMIN_ID = 7744385537

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
    if lang == "🇺🇿 Uzbek":
        bot.send_message(message.chat.id, "Ism va familiyangizni kiriting:")
    else:
        bot.send_message(message.chat.id, "Введите ваше имя и фамилию:")
    bot.register_next_step_handler(message, get_name, lang)

# -------------------
# ISM/FAMILIYA
# -------------------
def get_name(message, lang):
    name = message.text
    if lang == "🇺🇿 Uzbek":
        msg = bot.send_message(message.chat.id, "Telefon raqamingizni kiriting:")
    else:
        msg = bot.send_message(message.chat.id, "Введите ваш номер телефона:")
    bot.register_next_step_handler(msg, get_phone, lang, name)

# -------------------
# TELEFON RAQAMI
# -------------------
def get_phone(message, lang, name):
    phone = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if lang == "🇺🇿 Uzbek":
        markup.add("🇯🇵 Yaponiya", "🇪🇺 Shengen", "🇬🇧 Angliya")
        markup.add("🇨🇦 Kanada", "🇺🇸 Amerika", "🇸🇦 Arabiston")
        bot.send_message(message.chat.id, "Qaysi davlatga sayohat qilishni istaysiz?", reply_markup=markup)
    else:
        markup.add("🇯🇵 Япония", "🇪🇺 Шенген", "🇬🇧 Англия")
        markup.add("🇨🇦 Канада", "🇺🇸 Америка", "🇸🇦 Саудовская Аравия")
        bot.send_message(message.chat.id, "В какую страну вы хотите поехать?", reply_markup=markup)
    bot.register_next_step_handler(message, get_country, lang, name, phone)

# -------------------
# DAVLAT TANLASH VA QIZIQTIRUVI MALUMOT
# -------------------
def get_country(message, lang, name, phone):
    country = message.text

    prices_uz = {
        "🇯🇵 Yaponiya": 200,
        "🇪🇺 Shengen": 300,
        "🇬🇧 Angliya": 350,
        "🇨🇦 Kanada": 400,
        "🇺🇸 Amerika": 500,
        "🇸🇦 Arabiston": 80
    }

    prices_ru = {
        "🇯🇵 Япония": 200,
        "🇪🇺 Шенген": 300,
        "🇬🇧 Англия": 350,
        "🇨🇦 Канада": 400,
        "🇺🇸 Америка": 500,
        "🇸🇦 Саудовская Аравия": 80
    }

    info_uz = {
        "🇯🇵 Yaponiya": """Siz oldin Yaponiyaga bormaganmisiz? Tasavvur qiling, Shibuya Sky maydoniga chiqib, butun Tokio shahrini yuqoridan tomosha qilasiz. Bahor kelib, Sakura gullash davrida bu shahar juda rang-barang va romantik bo‘ladi. Qadimiy ibodatxonalar, zamonaviy arxitektura va texnologiyalar uyg‘unlashgan, har bir burchak suratga tushish uchun ajoyib. Shuningdek, Osiyo oshxonalarini tatib ko‘rish, mahalliy madaniyatni o‘rganish va festivallarda qatnashish imkoniyati mavjud. Yaponiya sayohatingiz sizni hayratga soladi va unutilmas taassurot qoldiradi.\n\nXizmat haqi: 200$""",
        "🇪🇺 Shengen": """Shengen hududidagi Evropaning go‘zal shaharlarini kashf qilmoqchimisiz? Har bir mamlakat o‘zining noyob arxitekturasi, tarixiy qasrlari va madaniy merosi bilan mashhur. Shahar bo‘ylab sayr qilish, diqqatga sazovor joylarni tomosha qilish va mahalliy an’analarni o‘rganish ajoyib tajriba beradi. Tabiat bog‘lari va go‘zal manzaralar sayohatingizni yanada boyitadi.\n\nXizmat haqi: 300$""",
        "🇬🇧 Angliya": """Angliyaga tashrif buyurib, Londonning tarixiy diqqatga sazovor joylarini kashf qilishni xohlaysizmi? Big Ben, London ko‘prigi, ajoyib muzeylar va teatrlari bilan mashhur. Shahar boy madaniy hayoti, klassik arxitektura va go‘zal bog‘lar sayohatingizni unutilmas qiladi.\n\nXizmat haqi: 350$""",
"🇨🇦 Kanada": """Kanadaga sayohat qilmoqchimisiz? Niagarа sharsharasi va keng tabiat bog‘lari sizni hayratda qoldiradi. Tabiatning rang-barangligi, hayvonot dunyosi va tog‘lar sizni o‘ziga jalb qiladi. Foto va dam olish imkoniyatlari juda ko‘p.\n\nXizmat haqi: 400$""",
        "🇺🇸 Amerika": """Amerikaga sayohat qilmoqchimisiz? Nyu-York baland binolari, Grand Canyon va Las-Vegasning yorqin ko‘chalari sizni kutmoqda. Har bir shahar o‘ziga xos madaniyat va hayratlanarli tajriba beradi. Sayohatingiz unutilmas va rang-barang bo‘ladi.\n\nXizmat haqi: 500$""",
        "🇸🇦 Arabiston": """Saudiya Arabistoniga borib, tarixiy masjidlar va qadimiy joylarni kashf qilmoqchimisiz? Riyad va boshqa shaharlarda sizni noyob madaniy tajribalar kutmoqda. Sahro sayohati va yulduzli tunlar sayohatingizni unutilmas qiladi.\n\nXizmat haqi: 80$"""
    }

    info_ru = {
        "🇯🇵 Япония": """Вы раньше не были в Японии? Представьте, что вы поднимаетесь на Shibuya Sky и наблюдаете весь Токио сверху. Во время цветения сакуры город выглядит особенно красочным и романтичным. Древние храмы, современная архитектура и технологии сочетаются, каждый уголок подходит для фото. Вы сможете попробовать местную кухню, познакомиться с культурой и принять участие в фестивалях. Поездка в Японию оставит незабываемые впечатления.\n\nСтоимость услуги: 200$""",
        "🇪🇺 Шенген": """Вы хотите открыть для себя красивые города Европы в Шенгенской зоне? Каждая страна славится своей уникальной архитектурой, историческими замками и культурным наследием. Прогулки по городу, осмотр достопримечательностей и изучение местных традиций подарят незабываемый опыт. Природные парки и живописные пейзажи делают поездку ещё более впечатляющей.\n\nСтоимость услуги: 300$""",
        "🇬🇧 Англия": """Хотите посетить Англию и увидеть исторические достопримечательности Лондона? Биг Бен, Лондонский мост, музеи и театры делают город уникальным. Культурная жизнь, классическая архитектура и красивые парки делают поездку незабываемой.\n\nСтоимость услуги: 350$""",
        "🇨🇦 Канада": """Хотите поехать в Канаду? Ниагарский водопад и национальные парки впечатляют своим величием. Природные красоты, дикая флора и фауна, горы и озёра создают незабываемые впечатления. Множество возможностей для фото и отдыха.\n\nСтоимость услуги: 400$""",
        "🇺🇸 Америка": """Планируете поездку в Америку? Высотные здания Нью-Йорка, грандиозный Гранд-Каньон и яркие улицы Лас-Вегаса ждут вас. Каждый город предлагает уникальную культуру и массу удивительных впечатлений. Поездка будет незабываемой и яркой.\n\nСтоимость услуги: 500$""",
        "🇸🇦 Саудовская Аравия": """Хотите посетить Саудовскую Аравию? Исторические мечети и древние достопримечательности вас ждут. В Эр-Рияде и других городах можно погрузиться в уникальную культуру страны. Путешествие по пустыне и звездное небо создают незабываемые впечатления.\n\nСтоимость услуги: 80$"""
    }

    price = prices_uz.get(country) if lang=="🇺🇿 Uzbek" else prices_ru.get(country)
    info = info_uz.get(country) if lang=="🇺🇿 Uzbek" else info_ru.get(country)

    # Foydalanuvchiga xabar yuborish
    bot.send_message(message.chat.id, f"{info}")

    # Ha/Yo‘q tugmalari
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if lang == "🇺🇿 Uzbek":
        markup.add("Ha", "Yo‘q")
        bot.send_message(message.chat.id, "Viza bo’yicha mutaxassisimiz sizga tez orada bog‘lanishini xohlaysizmi?", reply_markup=markup)
    else:
        markup.add("Да", "Нет")
        bot.send_message(message.chat.id, "Хотите, чтобы наш специалист по визам связался с вами?", reply_markup=markup)

    bot.register_next_step_handler(message, get_interest, lang, name, phone, country, price)

# -------------------
# QIZIQISH BO‘YICHA JAVOB VA SAVOL
# -------------------
def get_interest(message, lang, name, phone, country, price):
    text = message.text
    interest = False

    if text in ["Ha", "Да"]:
        interest = True
        bot.send_message(message.chat.id, "✅ Tez orada mutaxassis siz bilan bog‘lanadi!" if lang=="🇺🇿 Uzbek" else "✅ Наш специалист свяжется с вами в ближайшее время!")
    else:
        prompt = "Qiziqqan savollaringiz bo‘lsa, iltimos ularni shu yerga yozing:" if lang=="🇺🇿 Uzbek" else "Если у вас есть вопросы, пожалуйста, напишите их здесь:"
        msg = bot.send_message(message.chat.id, prompt)
        bot.register_next_step_handler(msg, handle_questions, lang)

    # Adminga xabar
    admin_text = f"📝 Yangi ariza!\n\n👤 Ism: {name}\n📞 Telefon: {phone}\n🌍 Davlat: {country}\n💰 Xizmat haqi: {price}$\n"
    admin_text += "💡 Qiziqish bildirdi ✅" if interest else "💡 Qiziqish bildirmadi ❌"
    bot.send_message(ADMIN_ID, admin_text)

# -------------------
# SAVOLLARNI QABUL QILISH
# -------------------
def handle_questions(message, lang="uz"):
    user_question = message.text
    bot.send_message(ADMIN_ID, f"📩 Foydalanuvchi savoli ({lang}): {user_question}")
    reply = "Savolingiz qabul qilindi, tez orada javob beramiz!" if lang=="🇺🇿 Uzbek" else "Ваш вопрос принят, мы ответим вам в ближайшее время!"
    bot.send_message(message.chat.id, reply)

# -------------------
# BOTNI ISHGA TUSHIRISH
# -------------------
bot.polling()