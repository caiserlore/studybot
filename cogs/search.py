import discord
from discord import app_commands
from discord.ext import commands
from config import load_json
from utils.embeds import create_embed
from utils.logger import setup_logger
from utils.pendo import track as pendo_track

logger = setup_logger("Search")

class Search(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="search", description="Pesquisa em notas e templates.")
    @app_commands.describe(termo="Termo a ser pesquisado")
    async def search(self, interaction: discord.Interaction, termo: str):
        await interaction.response.defer(ephemeral=True)
        guild_id = interaction.guild.id

        # Pesquisar notas
        notes = self.bot.db.search_notes(guild_id, termo)
        templates = load_json("templates.json")
        matching_templates = {k: v for k, v in templates.items() if termo.lower() in k.lower() or termo.lower() in v.lower()}

        notes_count = len(notes) if notes else 0
        templates_count = len(matching_templates) if matching_templates else 0

        await pendo_track(
            "search_executed",
            visitor_id=str(interaction.user.id),
            account_id=str(interaction.guild.id),
            properties={
                "guild_id": str(interaction.guild.id),
                "user_id": str(interaction.user.id),
                "search_term": termo[:100],
                "notes_result_count": notes_count,
                "templates_result_count": templates_count,
                "total_result_count": notes_count + templates_count,
                "has_results": bool(notes or matching_templates),
            },
        )

        embed = discord.Embed(title=f"🔍 Resultados para: '{termo}'", color=discord.Color.blue())

        if notes:
            text = ""
            for note in notes[:3]:
                text += f"**Nota {note['id']}** ({note['created_at']}): {note['content'][:200]}...\n\n"
            embed.add_field(name="📝 Notas", value=text, inline=False)

        if matching_templates:
            items = list(matching_templates.keys())[:5]
            embed.add_field(name="📋 Templates", value=", ".join(f"`{t}`" for t in items), inline=False)

        if not notes and not matching_templates:
            embed.description = "Nenhum resultado encontrado."

        await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Search(bot))