import discord
from discord import app_commands
from discord.ext import commands
from helper import UI

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Sistem gecikme sürelerini görüntüler.")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        await UI.info(interaction, "Sistem Durumu", f"Ağ Gecikmesi: **{latency}ms**\nAPI Bağlantısı: **Stabil**")

    @app_commands.command(name="kullanici", description="Belirtilen kullanıcının kayıtlarını getirir.")
    async def user_info(self, interaction: discord.Interaction, member: discord.Member = None):
        target = member or interaction.user
        
        roles = [role.mention for role in target.roles if role.name != "@everyone"]
        created_at = target.created_at.strftime("%d.%m.%Y")
        joined_at = target.joined_at.strftime("%d.%m.%Y")
        
        embed = UI.create_embed("Kullanıcı Kaydı", "", target.color)
        embed.set_thumbnail(url=target.display_avatar.url)
        embed.add_field(name="Kimlik", value=target.mention, inline=True)
        embed.add_field(name="ID", value=f"`{target.id}`", inline=True)
        embed.add_field(name="Hesap Tarihi", value=created_at, inline=True)
        embed.add_field(name="Katılım Tarihi", value=joined_at, inline=True)
        embed.add_field(name="Roller", value=" ".join(roles) if roles else "Yok", inline=False)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Utilities(bot))