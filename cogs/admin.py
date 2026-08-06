import discord
from discord import app_commands
from discord.ext import commands
from utils.permissions import is_admin
from utils.embeds import create_embed

class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="stats", description="Exibe estatísticas do servidor.")
    @is_admin()
    async def stats(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        guild = interaction.guild
        channels = len(guild.channels)
        categories = len(guild.categories)
        members = guild.member_count
        embed = create_embed(
            "📈 Estatísticas",
            fields=[
                ("Membros", str(members), True),
                ("Categorias", str(categories), True),
                ("Canais", str(channels), True),
            ],
            color=discord.Color.blurple()
        )
        await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(name="help", description="Lista todos os comandos disponíveis.")
    async def help_command(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        embed = discord.Embed(
            title="📚 Comandos do StudyBot",
            description="Aqui estão os comandos disponíveis:",
            color=discord.Color.green()
        )
        embed.add_field(name="/setup", value="Configura o servidor automaticamente.", inline=False)
        embed.add_field(name="/roadmap", value="Mostra o roadmap com status.", inline=False)
        embed.add_field(name="/progresso", value="Exibe seu progresso.", inline=False)
        embed.add_field(name="/proximo", value="Sugere o próximo tópico.", inline=False)
        embed.add_field(name="/concluir", value="Marca o tópico atual como concluído.", inline=False)
        embed.add_field(name="/reabrir", value="Remove a conclusão do tópico atual.", inline=False)
        embed.add_field(name="/topico", value="Cria um novo canal com template.", inline=False)
        embed.add_field(name="/hipotese", value="Cria uma thread de hipótese.", inline=False)
        embed.add_field(name="/lab", value="Cria uma thread de laboratório.", inline=False)
        embed.add_field(name="/writeup", value="Cria uma thread de writeup.", inline=False)
        embed.add_field(name="/nota", value="Salva uma nota.", inline=False)
        embed.add_field(name="/search", value="Pesquisa em notas e templates.", inline=False)
        embed.add_field(name="/stats", value="Estatísticas do servidor (admin).", inline=False)
        await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Admin(bot))