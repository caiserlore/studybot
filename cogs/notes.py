import discord
from discord import app_commands
from discord.ext import commands
from utils.embeds import create_embed
from utils.logger import setup_logger

logger = setup_logger("Notes")

class Notes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="nota", description="Salva uma nota estruturada.")
    @app_commands.describe(conteudo="Conteúdo da nota")
    async def nota(self, interaction: discord.Interaction, conteudo: str):
        await interaction.response.defer(ephemeral=True)
        self.bot.db.add_note(interaction.guild.id, interaction.user.id, conteudo)
        embed = create_embed("📌 Nota salva", "Sua nota foi armazenada com sucesso.", discord.Color.green())
        await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Notes(bot))