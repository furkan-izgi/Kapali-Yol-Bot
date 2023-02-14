from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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
            InlineKeyboardButton('📢 Afet Harita', url='https://afetharita.com/tr'),
            InlineKeyboardButton('📢 Güvenli Bölgeler', url='https://www.google.com/maps/d/u/0/viewer?mid=1aQ0TJi4q_46XAZiSLggkbTjPzLGkTzQ&g_ep=CAESCTExLjY0LjcwMRgAQgJUUg%3D%3D&shorturl=1&ll=37.47264354077547%2C37.85919325518651&z=7'),
        ],
        [
            InlineKeyboardButton('📌 Enkaz Dinleme', url='https://web.itu.edu.tr/sariero/dinleme.html?fbclid=PAAaZToiVKz15Yxc-1Vq8aMhn2ycuY3MWospPGPVtv0QrCzKFHNIJyMmrOs2c'),
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

CSV_BUTTON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('📗 CSV Dosyası Oluştur', callback_data='createcsv')           
        ]
    ]
)