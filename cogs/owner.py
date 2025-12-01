import os
import discord
from discord.ext import commands
from discord import app_commands
from helper import UI

OWNER_ID = os.getenv('OWNER_ID')

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != OWNER_ID:
            await UI.error(interaction, "Erişim reddedildi. Yetkili kimliği doğrulanamadı.")
            return False
        return True

    @app_commands.command(name="sistem", description="Bot modüllerini yönet.")
    @app_commands.choices(islem=[
        app_commands.Choice(name="Yenile (Reload)", value="reload"),
        app_commands.Choice(name="Senkronize Et (Sync)", value="sync")
    ])
    async def system_manage(self, interaction: discord.Interaction, islem: str, modul: str = None):
        if islem == "reload":
            if not modul: return await UI.error(interaction, "Modül adı belirtilmedi.")
            try:
                await self.bot.reload_extension(f"cogs.{modul}")
                await UI.success(interaction, f"Modül yeniden başlatıldı: **{modul}**")
            except Exception as e:
                await UI.error(interaction, f"Modül hatası: {e}")
        
        elif islem == "sync":
            await interaction.response.defer(ephemeral=True)
            synced = await self.bot.tree.sync()
            await UI.success(interaction, f"**{len(synced)}** komut sunuculara dağıtıldı.")

    @app_commands.command(name="profil", description="Bot kimliğini güncelle.")
    async def reika_identity(self, interaction: discord.Interaction, isim: str = None, avatar: discord.Attachment = None):
        await interaction.response.defer(ephemeral=True)
        try:
            if isim: await self.bot.user.edit(username=isim)
            if avatar: await self.bot.user.edit(avatar=await avatar.read())
            await UI.success(interaction, "Kimlik bilgileri veritabanında güncellendi.")
        except Exception as e:
            await UI.error(interaction, f"Discord API Hatası: {e}")

async def setup(bot):
    await bot.add_cog(Owner(bot))