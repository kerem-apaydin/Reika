import discord
from discord.ext import commands
from discord import app_commands
import datetime
import re
from helper import UI

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.LOG_CHANNEL_ID = 123456789012345678 

    async def log_action(self, guild, title, fields):
        if not self.LOG_CHANNEL_ID: return
        channel = guild.get_channel(self.LOG_CHANNEL_ID)
        if channel:
            embed = discord.Embed(title=title, color=discord.Color.light_grey(), timestamp=discord.utils.utcnow())
            for name, value in fields.items():
                embed.add_field(name=name, value=value, inline=False)
            await channel.send(embed=embed)

    def parse_duration(self, time_str):
        pattern = re.compile(r"(\d+)([smhd])")
        match = pattern.match(time_string=time_str)
        if not match: return None
        amount, unit = match.groups()
        multipliers = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
        seconds = int(amount) * multipliers[unit]
        return seconds if seconds <= 2419200 else None

    @app_commands.command(name="ban", description="Kullanıcıyı sunucudan uzaklaştırır.")
    @app_commands.default_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "Belirtilmedi"):
        if member.top_role >= interaction.user.top_role:
            return await UI.error(interaction, "Bu kullanıcı üzerinde işlem yapma yetkiniz yok.")
        
        try:
            await member.ban(reason=reason)
            await UI.success(interaction, f"**{member}** kullanıcısı yasaklandı.\nSebep: `{reason}`")
            await self.log_action(interaction.guild, "BAN İŞLEMİ", {
                "Hedef": f"{member} ({member.id})", "Yetkili": interaction.user.mention, "Sebep": reason
            })
        except Exception as e:
            await UI.error(interaction, f"Sistem hatası: {e}")

    @app_commands.command(name="kick", description="Kullanıcıyı sunucudan atar.")
    @app_commands.default_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "Belirtilmedi"):
        if member.top_role >= interaction.user.top_role:
            return await UI.error(interaction, "Bu kullanıcı üzerinde işlem yapma yetkiniz yok.")
        
        await member.kick(reason=reason)
        await UI.success(interaction, f"**{member}** sunucudan atıldı.\nSebep: `{reason}`")

    @app_commands.command(name="timeout", description="Kullanıcıya geçici süreli susturma uygular.")
    @app_commands.default_permissions(mute_members=True)
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, duration: str, reason: str = "Belirtilmedi"):
        seconds = self.parse_duration(duration)
        if not seconds:
            return await UI.error(interaction, "Geçersiz süre formatı. Örnek: 10m, 1h, 1d")
        
        if member.top_role >= interaction.user.top_role:
            return await UI.error(interaction, "Bu kullanıcı üzerinde işlem yapma yetkiniz yok.")

        until = discord.utils.utcnow() + datetime.timedelta(seconds=seconds)
        await member.timeout(until, reason=reason)
        await UI.success(interaction, f"**{member}** susturuldu.\nSüre: `{duration}`\nSebep: `{reason}`")

    @app_commands.command(name="sil", description="Toplu mesaj silme işlemi.")
    @app_commands.default_permissions(manage_messages=True)
    async def purge(self, interaction: discord.Interaction, amount: int):
        if not (1 <= amount <= 100):
            return await UI.error(interaction, "Miktar 1 ile 100 arasında olmalıdır.")
        
        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=amount)
        await UI.success(interaction, f"**{len(deleted)}** adet mesaj veritabanından temizlendi.")

async def setup(bot):
    await bot.add_cog(Moderation(bot))