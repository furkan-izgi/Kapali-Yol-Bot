from pyrogram import Client, enums,filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests, time
from os import environ as env
from bs4 import BeautifulSoup

Markdown = enums.ParseMode.MARKDOWN
        
async def closedRoadsFilter(city, message):
    matched = []
    counter = 0
    m = await app.send_message(message.chat.id, f"**{city}** için yol durumu bilgisi aranıyor...", parse_mode=Markdown)
    for j in range(1,4):
        url = f"https://yoltest.kgm.gov.tr/arcgis/rest/services/Yol/YolDurumu/MapServer/{j}/query?where=1%3D1&outFields=*&outSR=4326&f=json"
        response = requests.get(url)
        data = response.json()
        totalRoad = len(data['features'])
        for i in range(totalRoad):
            bolgeadi = data['features'][i]['attributes']['bolgeadi']
            bolgeno = data['features'][i]['attributes']['bolgeno']
            iladi = data['features'][i]['attributes']['iladi']
            kkno = data['features'][i]['attributes']['kkno']
            yolunadi = data['features'][i]['attributes']['yolunadi']
            baskm = data['features'][i]['attributes']['baskm']
            bitiskm = data['features'][i]['attributes']['bitiskm']
            nedeni = data['features'][i]['attributes']['nedeni']
            tarih = data['features'][i]['attributes']['tarih']
            gunceltarih = data['features'][i]['attributes']['gunceltarih']
            try:
                y = data['features'][i]['geometry']['y']
                x = data['features'][i]['geometry']['x']
                maps = f"https://www.google.com/maps/search/?api=1&query={y},{x}"
            except:
                maps = "Konum bilgisi bulunamadı."
            if iladi in city:
                base_txt = f"""
                ⚠️ Yol Durumu ⚠️
                
📌 Konum: {maps}
                
• --İl Adı--: **{iladi}**
• --Bölge Adı--: **{bolgeadi}**
• --Yolun Adı--: **{yolunadi}**
• --Bölge No--: **{bolgeno}**
• --Kontrol Kesim No--: **{kkno}**
• --Başlangıç Km--: **{int(baskm)/1000} km**
• --Bitiş Km--: **{int(bitiskm)/1000} km**
• --Nedeni--: **{nedeni}**
• --Tarih--: **{tarih}**
• --Güncelleme Tarihi--: **{gunceltarih}**

"""
                counter += 1
                matched.append(base_txt)
                await m.edit(f"**{city}** için yol durumu bilgisi aranıyor... {counter} yol bulundu.")
    return matched

APP_ID = int(env.get('APP_ID', None))
APP_HASH = env.get('APP_HASH', None)
BOT_TOKEN = env.get('BOT_TOKEN', None)

app = Client('EarthquakeInfo', api_id=APP_ID, api_hash=APP_HASH, bot_token=BOT_TOKEN)

START_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('📢 Son Depremler', url='https://t.me/sondepremlerkandilli'),
            InlineKeyboardButton('📢 Deprem.io', url='https://t.me/deprem.io')
        ],
        [
            InlineKeyboardButton('📢 Güvenli Bölgeler', url='https://www.google.com/maps/d/u/0/viewer?mid=1aQ0TJi4q_46XAZiSLggkbTjPzLGkTzQ&g_ep=CAESCTExLjY0LjcwMRgAQgJUUg%3D%3D&shorturl=1&ll=37.47264354077547%2C37.85919325518651&z=7'),
        ]
    ]
    )

USEFUL_LINKS_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('📢 Son Depremler', url='https://t.me/sondepremlerkandilli'),
            InlineKeyboardButton('📢 Deprem.io', url='https://t.me/deprem.io'),
            InlineKeyboardButton('📢 Güvenli Bölgeler', url='https://www.google.com/maps/d/u/0/viewer?mid=1aQ0TJi4q_46XAZiSLggkbTjPzLGkTzQ&g_ep=CAESCTExLjY0LjcwMRgAQgJUUg%3D%3D&shorturl=1&ll=37.47264354077547%2C37.85919325518651&z=7'),
        ],
        [
            InlineKeyboardButton('📌 Enkaz Dinleme Uygulaması', url='https://web.itu.edu.tr/sariero/dinleme.html?fbclid=PAAaZToiVKz15Yxc-1Vq8aMhn2ycuY3MWospPGPVtv0QrCzKFHNIJyMmrOs2c'),
            InlineKeyboardButton('📌 Deprem Yardım', url='https://depremyardim.com/'),
            InlineKeyboardButton('📌 Ben İyiyim', url='https://beniyiyim.com')
        ],
        [
            InlineKeyboardButton('💵 Resmi Bağış Hesapları', url='https://earthquake.enessahin.dev/docs/Deprem%20Kaynaklar%20-%20Resmi%20Ba%C4%9F%C4%B1%C5%9F%20Hesaplar%C4%B1%20(Yeni).pdf'),
            InlineKeyboardButton('💵 Yardım Toplama Merkezleri', url='https://play.google.com/store/apps/details?id=com.deprem'),
            InlineKeyboardButton('💵 Resmi Afad Twitter Hesabı', url='https://twitter.com/AFADBaskanlik')
        ]
    ]
    )

ilAdlari = [
    'GAZİANTEP',
    'MALATYA',
    'BATMAN',
    'BİNGÖL',
    'ELAZIĞ',
    'KİLİS',
    'DİYARBAKIR',
    'MARDİN',
    'SİİRT',
    'ŞIRNAK',
    'VAN',
    'MUŞ',
    'BİTLİS',
    'HAKKARİ',
    'ADANA',
    'OSMANİYE',
    'HATAY',
    'KAHRAMANMARAŞ'
    ]


@app.on_message(filters.command('start'))
async def start(client, message):
    await message.reply_text(
        f"Merhaba {message.from_user.first_name}!\n\nBen Yol Durumu Botuyum. Yol durumunu öğrenmek için /yol (BÜYÜK HAFRLERLE Şehir adı) komutunu kullanabilirsin. Örneğin: /yol GAZİANTEP",
        reply_markup=START_BUTTONS
        )
@app.on_message(filters.command('yol'))
async def yolbilgisi(client, message):
    try:
        city = message.text.split(' ')[1]
        if not city.isupper():
            await app.send_message(message.chat.id, "**Lütfen şehir adının tamamını büyük harfle yazınız.** Örneğin: /yol GAZİANTEP. Mevcut il adları için /iller yazın.", parse_mode=Markdown)
        else:
            matched = await closedRoadsFilter(city, message)
            if matched == []:
                await app.send_message(message.chat.id, "❌ **Arama sonucu bulunamadı.**", parse_mode=Markdown)
            else:
                for road in matched:
                    await app.send_message(message.chat.id, road, parse_mode=Markdown, disable_web_page_preview=True)
                    time.sleep(0.75)
                await app.send_message(message.chat.id, "✅ **Arama Tamamlandı.**", parse_mode=Markdown)
    except IndexError:
        await app.send_message(message.chat.id, "**Lütfen şehir adını yazınız.** Örneğin: /yol GAZİANTEP. Mevcut il adları için /iller yazın.", parse_mode=Markdown)
@app.on_message(filters.command('iller'))
async def iller(client, message):
    cities = "Aramaya dahil şehirler: \n\n"
    for city in ilAdlari:
        cities += f"• `{city}`\n"
    await app.send_message(message.chat.id, cities, parse_mode=Markdown)
    
@app.on_message(filters.command('faydalilinkler'))
async def faydalilinkler(client, message):
    await app.send_message(message.chat.id, "Faydalı Linkler. Lütfen paylaşalım.", reply_markup=USEFUL_LINKS_BUTTONS),
    
app.run()