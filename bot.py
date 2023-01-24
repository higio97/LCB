import pyrogram, sys, config

figlet_start = """
BOT LiveGram IS ACTIVED
"""

class Bot(pyrogram.Client):
    def __init__(self):
        super().__init__(
            'LiveGramBot',
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            plugins={
                "root": "plugins"
            },
        )
    async def start(self):
        await super().start()
        bot_me = await self.get_me()

        print(f"[!] LINK MONGO DB  : {config.MONGO_DB_URL}")
        print(f"[!] MONGO DB NAME  : {config.MONGO_DB_NAME}")
        print(f"[!] MONGO DB TABLE : {config.MONGO_DB_TABLE} - {config.MONGO_DB_TABLE_2}")
        print("=========================")
        if config.CHANNEL_ID:
            try:
                await self.export_chat_invite_link(config.CHANNEL_ID)
            except:
                print(f'Harap periksa kembali ID [ {config.CHANNEL_ID} ] pada CHANNEL 1')
                print(f'Pastikan bot telah dimasukan kedalam channel dan menjadi admin')
                print('-> Bot terpaksa dihentikan')
                sys.exit()
        if config.GROUP:
            try:
                await self.export_chat_invite_link(config.GROUP)
            except:
                print(f'Harap periksa kembali ID [ {config.GROUP} ] pada GROUP')
                print(f'Pastikan bot telah dimasukan kedalam channel dan menjadi admin')
                print('-> Bot terpaksa dihentikan')
                sys.exit()

        self.username = bot_me.username
        
        print(figlet_start)
    
    async def stop(self):
        await super().stop()
        print("BOT STOPPED")