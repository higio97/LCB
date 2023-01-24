import os

# [ API HASH ] OR [ API ID ] OR [ BOT TOKEN ]
API_ID = int(os.environ.get("API_ID", ""))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# OWNER ID
OWNER_ID = int(os.environ.get("OWNER_ID", ""))

# [ ID CHANNEL ]
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", ""))
CHANNEL_USERNAME = os.environ.get("CHANNEL_USERNAME", "") #Boleh diisi atau ga
# Tulis angka 0 agar pesan tidak diforward ke gc
GROUP = int(os.environ.get("GROUP", "0")) 
# atau masukkan id gc

# DATABASE MONGO
MONGO_DB_URL = os.environ.get("MONGO_DB_URL", "")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", "livegram")
MONGO_DB_TABLE = os.environ.get("MONGO_DB_TABLE", "user")
MONGO_DB_TABLE_2 = os.environ.get("MONGO_DB_TABLE", "chat")

IMG_START = os.environ.get("IMG_START", "https://telegra.ph/file/7e7b8a5abd9e3c6dd73d5.jpg")
IMG_CAPTION = os.environ.get("IMG_CAPTION", """
Hai Sayang 😘, Terima Kasih Telah Menggunakan Bot Ini

•╼════════════════╾•
🆔  Kamu : {id}
╟◈ Nama : {mention}
╟◈ Username : {username}
╟◈ Bahasa : {lang}
╟◈ DC ID:  {dc_id}
╟◈ Tipe Chat : {type}
╰╼════════════════╾•
""")