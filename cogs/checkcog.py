import discord
from discord.ext import commands
from discord import app_commands
from helper import UI

class checkCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="kontrol", description="Sistem aktivite durumunu sorgular.")
    async def check_active(self, interaction: discord.Interaction):
        await UI.success(interaction, "Sistem aktif ve komutlara yanıt veriyor.\n")

async def setup(bot):
    await bot.add_cog(checkCog(bot))