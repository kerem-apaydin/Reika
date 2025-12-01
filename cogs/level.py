import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import random
from helper import UI 

class LevelSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_dir = "data"
        self.data_file = "data/levels.json"
        
       
        self._cd = commands.CooldownMapping.from_cooldown(1, 60.0, commands.BucketType.member)
        
        self.check_data_file()
        self.users = self.load_data()

    def check_data_file(self):
        """Veri klasörü ve dosyasını kontrol eder, yoksa oluşturur."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        if not os.path.exists(self.data_file):
            with open(self.data_file, "w") as f:
                json.dump({}, f)

    def load_data(self):
        try:
            with open(self.data_file, "r") as f:
                return json.load(f)
        except Exception:
            return {}

    def save_data(self):
        with open(self.data_file, "w") as f:
            json.dump(self.users, f, indent=4)

    def get_xp_next_level(self, level):
        """Bir sonraki seviye için gereken XP miktarını hesaplar."""
        return 5 * (level ** 2) + 500 * level + 100

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        bucket = self._cd.get_bucket(message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            return

        user_id = str(message.author.id)

        if user_id not in self.users:
            self.users[user_id] = {"xp": 0, "level": 1, "total_xp": 0}

        xp_gain = random.randint(15, 25)
        self.users[user_id]["xp"] += xp_gain
        self.users[user_id]["total_xp"] += xp_gain


        current_lvl = self.users[user_id]["level"]
        needed_xp = self.get_xp_next_level(current_lvl)

        if self.users[user_id]["xp"] >= needed_xp:
            self.users[user_id]["level"] += 1
            self.users[user_id]["xp"] = 0
            
        
            embed = UI.create_embed(
                "Statü Güncellemesi", 
                f"> **{message.author.mention}** yeni bir seviyeye ayak bastın. Tebrikler!\n\n"
                f"**Yeni Seviye:** {current_lvl + 1}\n"
                f"**Toplam Puan:** {self.users[user_id]['total_xp']}",
                discord.Color.gold()
            )
            await message.channel.send(embed=embed)

        self.save_data()

    @app_commands.command(name="rank", description="Kullanıcı seviye ve tecrübe kartını görüntüler.")
    async def rank(self, interaction: discord.Interaction, member: discord.Member = None):
        target = member or interaction.user
        user_id = str(target.id)

        if user_id not in self.users:
            return await UI.info(interaction, "Veri Bulunamadı", f"{target.mention} sisteme henüz kayıtlı değil.")

        data = self.users[user_id]
        lvl = data["level"]
        xp = data["xp"]
        needed = self.get_xp_next_level(lvl)
        total = data.get("total_xp", 0)

   
        percent = xp / needed
        bar_len = 15
        filled = int(percent * bar_len)
        bar = "█" * filled + "░" * (bar_len - filled)

        embed = UI.create_embed("Personel Kartı", "", discord.Color.dark_theme())
        embed.set_thumbnail(url=target.display_avatar.url)
        embed.add_field(name="Kimlik", value=target.mention, inline=True)
        embed.add_field(name="Mevcut Seviye", value=f"**{lvl}**", inline=True)
        embed.add_field(name="Genel Puan", value=f"{total}", inline=True)
        
        embed.add_field(name="İlerleme Durumu", value=f"`|{bar}|` **%{int(percent * 100)}**", inline=False)
        embed.add_field(name="Hedef", value=f"{xp} / {needed} XP", inline=False)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="siralama", description="Sunucu genelindeki en yüksek seviyeli kullanıcıları listeler.")
    async def leaderboard(self, interaction: discord.Interaction):
        if not self.users:
            return await UI.info(interaction, "Liste Boş", "Henüz veri girişi yapılmamış.")

   
        sorted_users = sorted(
            self.users.items(), 
            key=lambda x: (x[1]['level'], x[1]['xp']), 
            reverse=True
        )

        top_10 = sorted_users[:10]
        desc_lines = []
        
        for idx, (uid, data) in enumerate(top_10, 1):
       
            user = self.bot.get_user(int(uid))
            name = user.name if user else "Bilinmeyen Kullanıcı"
            
            line = f"**#{idx}** `{name}` \n> Seviye: {data['level']} - Toplam Puan: {data.get('total_xp', 0)}"
            desc_lines.append(line)

        embed = UI.create_embed("Liderlik Tablosu", "\n\n".join(desc_lines), discord.Color.blurple())
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(LevelSystem(bot))