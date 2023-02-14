from pyrogram import Client, enums,filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests, time, csv, random, os, asyncio
from os import environ as env
from bs4 import BeautifulSoup
from kapaliyol import buttons

Markdown = enums.ParseMode.MARKDOWN

async def createCSV(csvList):
    fileID = random.randint(0,9999999999)
    with open(f'Arama_Sonuclari_{fileID}.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["İl", "Bölge", "Yol", "Bölge No", "Kontrol Kesim No", "Başlangıç KM", "Bitiş KM", "Nedeni", "Tarih", "Güncelleme Tarihi"])
        for item in csvList:
            writer.writerow(item)
      
async def closedRoadsFilter(city, message):
    matched = []
    csvList = []
    counter = 0
    m = await app.send_message(message.chat.id, f"**{city}** için yol durumu bilgisi aranıyor...", parse_mode=Markdown)
    for j in range(1,4):
        url = f"https://yoltest.kgm.gov.tr/arcgis/rest/services/Yol/YolDurumu/MapServer/{j}/query?where=1%3D1&outFields=*&outSR=4326&f=json"
        response = requests.get(url)
        data = response.json()
        totalRoad = len(data['features'])
        for i in range(totalRoad):
            bolgeadi = data['features'][i]['attributes']['bolgeadi'] if 'bolgeadi' in data['features'][i]['attributes'] else "-"
            bolgeno = data['features'][i]['attributes']['bolgeno'] if 'bolgeno' in data['features'][i]['attributes'] else "-"
            iladi = data['features'][i]['attributes']['iladi'] if 'iladi' in data['features'][i]['attributes'] else "-"
            kkno = data['features'][i]['attributes']['kkno'] if 'kkno' in data['features'][i]['attributes'] else "-"
            yolunadi = data['features'][i]['attributes']['yolunadi'] if 'yolunadi' in data['features'][i]['attributes'] else "-"
            baskm = data['features'][i]['attributes']['baskm'] if 'baskm' in data['features'][i]['attributes'] else "-"
            bitiskm = data['features'][i]['attributes']['bitiskm'] if 'bitiskm' in data['features'][i]['attributes'] else "-"
            nedeni = data['features'][i]['attributes']['nedeni'] if 'nedeni' in data['features'][i]['attributes'] else "-"
            tarih = data['features'][i]['attributes']['tarih'] if 'tarih' in data['features'][i]['attributes'] else "-"
            guncellemetarih = data['features'][i]['attributes']['gunceltarih'] if 'gunceltarih' in data['features'][i]['attributes'] else "-"
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
• --Güncelleme Tarihi--: **{guncellemetarih}**

"""
                csvList.append([iladi, bolgeadi, yolunadi, bolgeno, kkno, baskm, bitiskm, nedeni, tarih, guncellemetarih])
                counter += 1
                matched.append(base_txt)
                await m.edit(f"**{city}** için yol durumu bilgisi aranıyor... {counter} yol bulundu.")
    return matched, csvList

APP_ID = int(env.get('APP_ID', None))
APP_HASH = env.get('APP_HASH', None)
BOT_TOKEN = env.get('BOT_TOKEN', None)

app = Client('EarthquakeInfo', api_id=APP_ID, api_hash=APP_HASH, bot_token=BOT_TOKEN)

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
        reply_markup=buttons.START_BUTTONS)
    
@app.on_message(filters.command('yol'))
async def yolbilgisi(client, message):
    try:
        city = message.text.split(' ')[1]
        if not city.isupper():
            await app.send_message(message.chat.id,
                                   "**Lütfen şehir adının tamamını büyük harfle yazınız.** Örneğin: /yol GAZİANTEP. Mevcut il adları için /iller yazın.",
                                   parse_mode=Markdown)
        else:
            global csvList
            matched, csvList = await closedRoadsFilter(city, message)
            if matched == []:
                await app.send_message(message.chat.id, "❌ **Arama sonucu bulunamadı.**", parse_mode=Markdown)
            else:
                for road in matched:
                    await app.send_message(message.chat.id, road, parse_mode=Markdown, disable_web_page_preview=True)
                    time.sleep(0.75)
                await app.send_message(message.chat.id, "✅ **Arama Tamamlandı.**", parse_mode=Markdown, reply_markup=buttons.CSV_BUTTON)
    except IndexError:
        await app.send_message(message.chat.id, "**Lütfen şehir adını yazınız.** Örneğin: /yol GAZİANTEP. Mevcut il adları için /iller yazın.",parse_mode=Markdown)
        
@app.on_message(filters.command('iller'))
async def iller(client, message):
    cities = "Aramaya dahil şehirler: \n\n"
    for city in ilAdlari:
        cities += f"• `{city}`\n"
    await app.send_message(message.chat.id, cities, parse_mode=Markdown)
    
@app.on_message(filters.command('faydalilinkler'))
async def faydalilinkler(client, message):
    await app.send_message(message.chat.id,
                           "Faydalı Linkler. Lütfen paylaşalım.",
                           reply_markup=buttons.USEFUL_LINKS_BUTTONS)
    
    
@app.on_callback_query()
async def callback_data(client, callback_query):
    if callback_query.data == 'createcsv':
        if len(csvList) == 0:
            await callback_query.edit_message_text("❌ CSV Oluşturulamadı. Lütfen önce sorgulamanızdan sonuç aldığınızdan emin olun.")
        else:
            await callback_query.edit_message_text("CSV Oluşturuluyor...")
            fileID = await createCSV(csvList)
            await callback_query.edit_message_text("✅ CSV Oluşturuldu.")
            await asyncio.sleep(2)
            await client.send_document(callback_query.message.chat.id, open(f"Arama_Sonuclari_{fileID}.csv", "rb"))
            os.remove(f"./Arama_Sonuclari_{fileID}.csv")
    
app.run()