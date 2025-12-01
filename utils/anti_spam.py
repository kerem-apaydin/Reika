import discord
from discord.ext import commands
import datetime
from helper import UI

class AntiSpam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
      
        self._cd = commands.CooldownMapping.from_cooldown(5, 5.0, commands.BucketType.member)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

  
        if message.author.guild_permissions.administrator:
            return

        bucket = self._cd.get_bucket(message)
        retry_after = bucket.update_rate_limit()

        if retry_after:
          
            try:
                until = discord.utils.utcnow() + datetime.timedelta(seconds=60)
                await message.author.timeout(until, reason="Otomatik: Spam Koruması")
                
                embed = UI.create_embed(
                    "Spam Tespit Edildi", 
                    f"> **{message.author.mention}** çok hızlı mesaj gönderdiği için 60 saniye susturuldu.", 
                    discord.Color.dark_grey()
                )
                await message.channel.send(embed=embed, delete_after=10)
            except Exception:
                pass 

async def setup(bot):
    await bot.add_cog(AntiSpam(bot))