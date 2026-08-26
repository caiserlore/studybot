import discord
from discord import app_commands
from discord.ext import commands
from config import load_json
from database import Database
from utils.embeds import create_embed
from utils.logger import setup_logger
from utils.pendo import track as pendo_track

logger = setup_logger("Roadmap")

class Roadmap(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db: Database = bot.db

    def get_roadmap(self):
        return load_json("roadmap.json")

    @app_commands.command(name="progresso", description="Mostra seu progresso no roadmap.")
    async def progress(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        user_id = interaction.user.id
        guild_id = interaction.guild.id
        roadmap = self.get_roadmap()
        completed = self.db.get_user_progress(guild_id, user_id)
        completed_count = len(set(roadmap) & set(completed))
        total = len(roadmap)
        percent = (completed_count / total) * 100 if total > 0 else 0

        bar_length = 10
        filled = int(bar_length * completed_count // total) if total > 0 else 0
        bar = "█" * filled + "░" * (bar_length - filled)

        embed = create_embed(
            title="📊 Seu Progresso",
            description=f"**{completed_count}/{total}** tópicos concluídos\n\n[{bar}] {percent:.1f}%",
            color=discord.Color.blurple()
        )
        await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(name="proximo", description="Sugere o próximo tópico a estudar.")
    async def proximo(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        user_id = interaction.user.id
        guild_id = interaction.guild.id
        roadmap = self.get_roadmap()
        completed = self.db.get_user_progress(guild_id, user_id)
        next_topic = None
        for topic in roadmap:
            if topic not in completed:
                next_topic = topic
                break
        if next_topic:
            embed = create_embed("👉 Próximo tópico", f"**{next_topic}**", discord.Color.green())
        else:
            await pendo_track(
                "roadmap_fully_completed",
                visitor_id=str(interaction.user.id),
                account_id=str(interaction.guild.id),
                properties={
                    "guild_id": str(interaction.guild.id),
                    "user_id": str(interaction.user.id),
                    "total_topics_completed": len(completed),
                },
            )
            embed = create_embed("🎉 Parabéns!", "Você concluiu todos os tópicos do roadmap!", discord.Color.gold())
        await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(name="concluir", description="Marca o tópico do canal atual como concluído.")
    async def concluir(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        channel_name = interaction.channel.name
        roadmap = self.get_roadmap()
        if channel_name not in roadmap:
            return await interaction.followup.send("Este canal não é um tópico do roadmap.", ephemeral=True)
        success = self.db.mark_completed(interaction.guild.id, interaction.user.id, channel_name)
        if success:
            await pendo_track(
                "topic_completed",
                visitor_id=str(interaction.user.id),
                account_id=str(interaction.guild.id),
                properties={
                    "guild_id": str(interaction.guild.id),
                    "user_id": str(interaction.user.id),
                    "topic_name": channel_name,
                },
            )
            embed = create_embed("✅ Tópico concluído", f"**{channel_name}** marcado como concluído.", discord.Color.green())
        else:
            embed = create_embed("⚠️ Já concluído", "Este tópico já estava marcado como concluído.", discord.Color.orange())
        await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(name="reabrir", description="Remove a conclusão do tópico atual.")
    async def reabrir(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        channel_name = interaction.channel.name
        roadmap = self.get_roadmap()
        if channel_name not in roadmap:
            return await interaction.followup.send("Este canal não é um tópico do roadmap.", ephemeral=True)
        self.db.unmark_completed(interaction.guild.id, interaction.user.id, channel_name)
        await pendo_track(
            "topic_reopened",
            visitor_id=str(interaction.user.id),
            account_id=str(interaction.guild.id),
            properties={
                "guild_id": str(interaction.guild.id),
                "user_id": str(interaction.user.id),
                "topic_name": channel_name,
            },
        )
        embed = create_embed("🔓 Tópico reaberto", f"**{channel_name}** foi reaberto.", discord.Color.blue())
        await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(name="roadmap", description="Lista todos os tópicos do roadmap com status.")
    async def show_roadmap(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        roadmap = self.get_roadmap()
        completed = self.db.get_user_progress(interaction.guild.id, interaction.user.id)
        lines = []
        for topic in roadmap:
            status = "✅" if topic in completed else "⬜"
            lines.append(f"{status} {topic}")
        text = "\n".join(lines)
        embed = create_embed("🗺️ Roadmap", text[:4000] or "Nenhum tópico.", discord.Color.purple())
        await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Roadmap(bot))