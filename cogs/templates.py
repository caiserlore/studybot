import discord
from discord import app_commands
from discord.ext import commands
from config import load_json
from utils.helpers import send_and_pin
from utils.permissions import is_admin
from utils.logger import setup_logger
from utils.pendo import track as pendo_track

logger = setup_logger("Templates")

class Templates(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="topico", description="Cria um novo canal com template.")
    @app_commands.describe(
        categoria="Categoria onde o canal será criado",
        nome="Nome do canal",
        template="Template a ser usado (opcional, padrão conforme o nome)"
    )
    @app_commands.default_permissions(manage_channels=True)
    @is_admin()
    async def topico(
        self,
        interaction: discord.Interaction,
        categoria: discord.CategoryChannel,
        nome: str,
        template: str = None
    ):
        await interaction.response.defer(ephemeral=True)
        guild = interaction.guild
        existing = discord.utils.get(categoria.text_channels, name=nome)
        if existing:
            return await interaction.followup.send(f"O canal `{nome}` já existe na categoria {categoria.name}.", ephemeral=True)

        channel = await categoria.create_text_channel(nome)
        templates = load_json("templates.json")
        content = templates.get(template or nome) or templates.get(nome) or load_json("config.json").get("default_template", "## Tópico")
        msg = await send_and_pin(channel, content)
        await pendo_track(
            "topic_channel_created",
            visitor_id=str(interaction.user.id),
            account_id=str(interaction.guild.id),
            properties={
                "guild_id": str(interaction.guild.id),
                "channel_name": nome,
                "category_name": categoria.name,
                "template_used": template or nome,
            },
        )
        embed = discord.Embed(
            title="✅ Canal criado",
            description=f"Canal {channel.mention} criado em **{categoria.name}** com o template selecionado.",
            color=discord.Color.green()
        )
        await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(name="hipotese", description="Cria uma thread para registrar uma hipótese.")
    async def hipotese(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        guild_id = interaction.guild.id
        user_id = interaction.user.id
        number = self.bot.db.get_next_counter(guild_id, "hypothesis")
        thread_name = f"Hipótese #{number:03d}"
        thread = await interaction.channel.create_thread(name=thread_name, type=discord.ChannelType.public_thread)
        self.bot.db.conn.execute(
            "INSERT INTO hypotheses (guild_id, user_id, thread_id, number) VALUES (?, ?, ?, ?)",
            (guild_id, user_id, thread.id, number)
        )
        self.bot.db.conn.commit()
        await pendo_track(
            "hypothesis_created",
            visitor_id=str(user_id),
            account_id=str(guild_id),
            properties={
                "guild_id": str(guild_id),
                "user_id": str(user_id),
                "hypothesis_number": number,
                "channel_name": interaction.channel.name,
                "thread_id": str(thread.id),
            },
        )
        await thread.send("## Hipótese\n\nDescreva aqui sua hipótese e os testes planejados.")
        embed = discord.Embed(
            title="💡 Hipótese criada",
            description=f"Thread {thread.mention} registrada como `{thread_name}`.",
            color=discord.Color.purple()
        )
        await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(name="lab", description="Cria uma thread para um laboratório prático.")
    async def lab(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        guild_id = interaction.guild.id
        user_id = interaction.user.id
        number = self.bot.db.get_next_counter(guild_id, "lab")
        thread_name = f"Lab #{number:03d}"
        thread = await interaction.channel.create_thread(name=thread_name, type=discord.ChannelType.public_thread)
        self.bot.db.conn.execute(
            "INSERT INTO labs (guild_id, user_id, thread_id, number) VALUES (?, ?, ?, ?)",
            (guild_id, user_id, thread.id, number)
        )
        self.bot.db.conn.commit()
        await pendo_track(
            "lab_created",
            visitor_id=str(user_id),
            account_id=str(guild_id),
            properties={
                "guild_id": str(guild_id),
                "user_id": str(user_id),
                "lab_number": number,
                "channel_name": interaction.channel.name,
                "thread_id": str(thread.id),
            },
        )
        template = (
            "## Objetivo\n\n"
            "## Aplicação\n\n"
            "## Payload\n\n"
            "## Resultado\n\n"
            "## Impacto\n\n"
            "## Conclusão"
        )
        await thread.send(template)
        embed = discord.Embed(
            title="🧪 Lab criado",
            description=f"Thread {thread.mention} registrada como `{thread_name}`.",
            color=discord.Color.teal()
        )
        await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(name="writeup", description="Cria uma thread para um writeup.")
    async def writeup(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        guild_id = interaction.guild.id
        user_id = interaction.user.id
        number = self.bot.db.get_next_counter(guild_id, "writeup")
        thread_name = f"Writeup #{number:03d}"
        thread = await interaction.channel.create_thread(name=thread_name, type=discord.ChannelType.public_thread)
        self.bot.db.conn.execute(
            "INSERT INTO writeups (guild_id, user_id, thread_id, number) VALUES (?, ?, ?, ?)",
            (guild_id, user_id, thread.id, number)
        )
        self.bot.db.conn.commit()
        await pendo_track(
            "writeup_created",
            visitor_id=str(user_id),
            account_id=str(guild_id),
            properties={
                "guild_id": str(guild_id),
                "user_id": str(user_id),
                "writeup_number": number,
                "channel_name": interaction.channel.name,
                "thread_id": str(thread.id),
            },
        )
        template = (
            "## Empresa\n\n"
            "## Programa\n\n"
            "## Vulnerabilidade\n\n"
            "## Impacto\n\n"
            "## PoC\n\n"
            "## Root Cause\n\n"
            "## Mitigação\n\n"
            "## Lições Aprendidas"
        )
        await thread.send(template)
        embed = discord.Embed(
            title="📝 Writeup criado",
            description=f"Thread {thread.mention} registrada como `{thread_name}`.",
            color=discord.Color.orange()
        )
        await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Templates(bot))