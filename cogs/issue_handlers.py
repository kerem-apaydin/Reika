import discord
from discord.ext import commands
from helper import UI

class IssueHandlers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
    
        if hasattr(ctx.command, 'on_error'):
            return

        embed = discord.Embed(color=discord.Color.red())
        
        if isinstance(error, commands.CommandNotFound):
            return # Sessiz kal
        
        elif isinstance(error, commands.MissingRequiredArgument):
            embed.title = "Eksik Parametre"
            embed.description = f"> Komut kullanımı hatalı. Lütfen eksik verileri girin."
        
        elif isinstance(error, commands.MissingPermissions):
            embed.title = "Yetki Sınırı"
            embed.description = f"> Bu işlemi gerçekleştirmek için gerekli izinlere sahip değilsiniz."
            
        elif isinstance(error, commands.CommandOnCooldown):
            embed.title = "Aşırı Yükleme"
            embed.description = f"> Lütfen tekrar denemeden önce **{error.retry_after:.1f}** saniye bekleyin."
            
        else:
            embed.title = "Sistem Hatası"
            embed.description = f"> Beklenmeyen bir durum oluştu: `{str(error)}`"

        try:
            await ctx.send(embed=embed, delete_after=10)
        except:
            pass

async def setup(bot):
    await bot.add_cog(IssueHandlers(bot))