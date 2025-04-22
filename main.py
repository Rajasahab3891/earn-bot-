import telebot
import sqlite3
from telebot import types

# BotFather से टोकन (यहाँ अपना टोकन डाल, भाई!)
TOKEN = 'YOUR_BOT_TOKEN_HERE'
bot = telebot.TeleBot(TOKEN)

# टेलीग्राम ग्रुप लिंक (यहाँ अपना ग्रुप लिंक डाल)
GROUP_LINK = 'https://t.me/kingotp_payous'
# यूट्यूब गेमिंग चैनल लिंक (यहाँ अपना चैनल लिंक डाल)
YOUTUBE_CHANNEL = 'https://www.youtube.com/@Expiredgamer0090'

# डेटाबेस सेटअप
conn = sqlite3.connect('referrals.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                 (user_id INTEGER PRIMARY KEY, referrals INTEGER, balance REAL, ref_code TEXT, language TEXT)''')
conn.commit()

# लैंग्वेज डिक्शनरी (हर लैंग्वेज में नॉटी मैसेज)
MESSAGES = {
    'hindi': {
        'welcome': "अरे भाई, मस्ती की दुनिया में स्वागत! 😎 पहले {group} ग्रुप जॉइन कर, फिर 10 दोस्त बुला, ₹1 झटक! 🤑\nमेरे गेमिंग चैनल {youtube} पर भी जॉइन कर, PUBG की धूम मचा! 🎮",
        'choose_lang': "भाई, पहले लैंग्वेज चुन ले, ताकि मस्ती फुल ऑन हो! 😜",
        'group_join': "अरे नौटंकीबाज, पहले {group} ग्रुप जॉइन कर, फिर मस्ती शुरू! 😈",
        'ref_link': "तेरा तगड़ा रेफरल लिंक: {link}\n10 दोस्त बुला, ₹1 तेरी जेब में! 💸 {youtube} पर भी आजा, गेमिंग का बॉस बन! 🎮",
        'reward': "वाह भाई, तू तो छा गया! 🎉 10 रेफरल्स पूरे, ₹1 तेरे खाते में! और ला, अमीर बन जा! 😎",
        'balance': "तेरा खजाना: ₹{balance} 💰\nरेफरल्स: {refs} 😎\nऔर दोस्त बुला, {youtube} पर गेमिंग मस्ती कर! 🚀",
        'leaderboard': "🏆 टॉप मस्ती बाजार 🏆\n{list}\nतू भी बन जा गेमिंग का बादशाह, और रेफर कर! 😈"
    },
    'tamil': {
        'welcome': "மச்சி, மஸ்தி உலகத்துக்கு வாங்க! 😎 முதல்ல {group} குரூப்ப ஜாயின் பண்ணு, பிறகு 10 நண்பர்கள கூட்டிட்டு வா, ₹1 அள்ளு! 🤑 என் கேமிங் சேனல் {youtube}லயும் ஜாயின் பண்ணு, PUBG மஜா பண்ணு! 🎮",
        'choose_lang': "மச்சி, முதல்ல லாங்குவேஜ் செலக்ட் பண்ணு, மஸ்தி ஃபுல் ஆன் ஆகும்! 😜",
        'group_join': "ஏய், முதல்ல {group} குரூப்ப ஜாயின் பண்ணு, அப்புறம் மஸ்தி ஆரம்பம்! 😈",
        'ref_link': "உன் தகதக ரெஃபரல் லிங்க்: {link}\n10 நண்பர்கள கூட்டு, ₹1 உன் பாக்கெட்டுல! 💸 {youtube}லயும் வா, கேமிங் பாஸ் ஆகு! 🎮",
        'reward': "வாவ் மச்சி, நீ தூள் கிளப்பிட்ட! 🎉 10 ரெஃபரல்ஸ் முடிச்ச, ₹1 உன் அக்கவுண்ட்ல! இன்னும் கூட்டு, பணக்காரன் ஆகு! 😎",
        'balance': "உன் பணப்பெட்டி: ₹{balance} 💰\nரெஃபரல்ஸ்: {refs} 😎\nஇன்னும் நண்பர்கள கூட்டு, {youtube}ல கேமிங் மஜா பண்ணு! 🚀",
        'leaderboard': "🏆 டாப் மஸ்தி கிங்ஸ் 🏆\n{list}\nநீயும் கேமிங் கிங் ஆகு, ரெஃபர் பண்ணு! 😈"
    },
    'telugu': {
        'welcome': "బ్రో, మస్తీ వరల్డ్‌కి స్వాగతం! 😎 ముందు {group} గ్రూప్‌లో జాయిన్ అవ్వు, తర్వాత 10 మంది ఫ్రెండ్స్‌ని తీసుకొచ్చి ₹1 సంపాదించు! 🤑 నా గేమింగ్ ఛానల్ {youtube}లో కూడా జాయిన్ అవ్వు, PUBG జోష్ చూపించు! 🎮",
        'choose_lang': "బ్రో, ముందు లాంగ్వేజ్ సెలెక్ట్ చేయి, మస్తీ ఫుల్ ఆన్ అవుతుంది! 😜",
        'group_join': "ఏయ్, ముందు {group} గ్రూప్‌లో జాయిన్ అవ్వు, తర్వాత మస్తీ స్టార్ట్! 😈",
        'ref_link': "నీ ధమాకా రెఫరల్ లింక్: {link}\n10 మంది ఫ్రెండ్స్‌ని తీసుకొచ్చు, ₹1 నీ జేబులో! 💸 {youtube}లో కూడా రా, గేమింగ్ బాస్ అవ్వు! 🎮",
        'reward': "వామ్మో బ్రో, నీవు సూపర్ హీరోలా రాక్ చేశావు! 🎉 10 రెఫరల్స్ కంప్లీట్, ₹1 నీ అకౌంట్‌లో! ఇంకా తీసుకొచ్చు, కోటీశ్వరుడివి అవ్వు! 😎",
        'balance': "నీ ఖజానా: ₹{balance} 💰\nరెఫరల్స్: {refs} 😎\nఇంకా ఫ్రెండ్స్‌ని తీసుకొచ్చు, {youtube}లో గేమింగ్ మస్తీ చేయి! 🚀",
        'leaderboard': "🏆 టాప్ మస్తీ హీరోలు 🏆\n{list}\nనీవు కూడా గేమింగ్ కింగ్ అవ్వు, రెఫర్ చేయి! 😈"
    }
    # और लैंग्वेज (बंगाली, मराठी, आदि) बाद में ऐड कर सकते हैं
}

# स्टार्ट कमांड
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    args = message.text.split()
    cursor.execute("SELECT language FROM users WHERE user_id=?", (user_id,))
    lang = cursor.fetchone()

    if not lang:
    # अगर लैंग्वेज नहीं चुना
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Hindi"), types.KeyboardButton("Tamil"), types.KeyboardButton("Telugu"))
    bot.reply_to(message, "अरे भाई, पहले लैंग्वेज चुन ले, मस्ती फुल औं होगी! 😎", reply_markup=markup)
    bot.register_next_step_handler(message, set_language)
    return

    lang = lang[0]
    ref_code = str(user_id)
    cursor.execute("INSERT OR IGNORE INTO users (user_id, referrals, balance, ref_code, language) VALUES (?, 0, 0.0, ?, ?)", (user_id, ref_code, lang))
    conn.commit()

    # ग्रुप जॉइन चेक
    try:
        status = bot.get_chat_member(chat_id="@kingotp_payous", user_id=user_id).status
        if status in ['member', 'administrator', 'creator']:
            # रेफरल हैंडल
            if len(args) > 1 and args[1] != str(user_id):
                ref_code = args[1]
                cursor.execute("SELECT user_id, language FROM users WHERE ref_code=?", (ref_code,))
                referrer = cursor.fetchone()
                if referrer and referrer[0] != user_id:
                    cursor.execute("UPDATE users SET referrals=referrals+1 WHERE user_id=?", (referrer[0],))
                    cursor.execute("SELECT referrals FROM users WHERE user_id=?", (referrer[0],))
                    refs = cursor.fetchone()[0]
                    if refs >= 10:
                        cursor.execute("UPDATE users SET balance=balance+1 WHERE user_id=?", (referrer[0],))
                        bot.send_message(referrer[0], MESSAGES[referrer[1]]['reward'])
                    conn.commit()

            # रेफरल लिंक
            ref_link = f"https://t.me/{bot.get_me().username}?start={ref_code}"
            bot.send_photo(message.chat.id, "https://envs.sh/CYA.jpg", caption=MESSAGES[lang]['ref_link'].format(link=ref_link, youtube=YOUTUBE_CHANNEL))
        else:
            bot.reply_to(message, MESSAGES[lang]['group_join'].format(group=GROUP_LINK))
    except:
        bot.reply_to(message, MESSAGES[lang]['group_join'].format(group=GROUP_LINK))

# लैंग्वेज सेट
def set_language(message):
    user_id = message.from_user.id
    lang = message.text.lower()
    if lang in ['hindi', 'tamil', 'telugu']:
        cursor.execute("INSERT OR IGNORE INTO users (user_id, referrals, balance, ref_code, language) VALUES (?, 0, 0.0, ?, ?)", (user_id, str(user_id), lang))
        cursor.execute("UPDATE users SET language=? WHERE user_id=?", (lang, user_id))
        conn.commit()
        bot.reply_to(message, MESSAGES[lang]['welcome'].format(group=GROUP_LINK, youtube=YOUTUBE_CHANNEL))
    else:
        bot.reply_to(message, "अरे भाई, सही लैंग्वेज चुन! 😜")
        bot.register_next_step_handler(message, set_language)

# बैलेंस चेक
@bot.message_handler(commands=['balance'])
def check_balance(message):
    user_id = message.from_user.id
    cursor.execute("SELECT balance, referrals, language FROM users WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    if result:
        bot.reply_to(message, MESSAGES[result[2]]['balance'].format(balance=result[0], refs=result[1], youtube=YOUTUBE_CHANNEL))
    else:
        bot.reply_to(message, "अरे नौटंकीबाज, पहले /start कर! 😜")

# लीडरबोर्ड
@bot.message_handler(commands=['leaderboard'])
def leaderboard(message):
    user_id = message.from_user.id
    cursor.execute("SELECT language FROM users WHERE user_id=?", (user_id,))
    lang = cursor.fetchone()[0] if cursor.fetchone() else 'hindi'
    cursor.execute("SELECT user_id, referrals FROM users ORDER BY referrals DESC LIMIT 5")
    top_users = cursor.fetchall()
    msg = ""
    for i, user in enumerate(top_users, 1):
        msg += f"{i}. भाई {user[0]}: {user[1]} रेफरल्स 🔥\n"
    bot.reply_to(message, MESSAGES[lang]['leaderboard'].format(list=msg))
