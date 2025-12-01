import discord
import datetime

class UI:
    @staticmethod
    def create_embed(title: str, description: str, color: discord.Color):
        embed = discord.Embed(
            title=title,
            description=description,
            color=color,
            timestamp=datetime.datetime.now()
        )
        return embed

    @staticmethod
    async def success(interaction: discord.Interaction, message: str):

        embed = UI.create_embed("İşlem Başarılı", f"> {message}", discord.Color.from_rgb(67, 181, 129))
        if not interaction.response.is_done():
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.followup.send(embed=embed, ephemeral=True)

    @staticmethod
    async def error(interaction: discord.Interaction, message: str):
        
        embed = UI.create_embed("Hata", f"> {message}", discord.Color.from_rgb(240, 71, 71))
        if not interaction.response.is_done():
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.followup.send(embed=embed, ephemeral=True)

    @staticmethod
    async def info(interaction: discord.Interaction, title: str, message: str):

        embed = UI.create_embed(title, message, discord.Color.from_rgb(52, 152, 219))
        await interaction.response.send_message(embed=embed)