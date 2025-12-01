import os
import sys
import discord
import logging
from discord.ext import commands
from dotenv import load_dotenv

#UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()
TOKEN = os.getenv('TOKEN')
PREFIX = os.getenv('PREFIX', '.')

#Logging settings
logging.basicConfig(
    filename='system.log', 
    level=logging.ERROR, 
    format='%(asctime)s [%(levelname)s] %(message)s'
)

class ReikaBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        super().__init__(
            command_prefix=PREFIX, 
            intents=intents,
            help_command=None 
        )

    async def setup_hook(self):
        print("--- Modüller Yükleniyor ---")
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and not filename.startswith('__'):
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    print(f"[+] {filename[:-3]} yüklendi.")
                except Exception as e:
                    print(f"[-] {filename[:-3]} YÜKLENEMEDİ: {e}")

    async def on_ready(self):
        print("\n--- Sistem Hazır ---")
        print(f"Kullanıcı: {self.user}")
        print(f"ID: {self.user.id}")
        
        try:
            synced = await self.tree.sync()
            print(f"Slash Komutları: {len(synced)} adet senkronize edildi.")
        except Exception as e:
            print(f"Senkronizasyon Hatası: {e}")

if __name__ == '__main__':
    if not TOKEN:
        print("HATA: .env dosyasında TOKEN bulunamadı.")
    else:
        bot = ReikaBot()
        bot.run(TOKEN)