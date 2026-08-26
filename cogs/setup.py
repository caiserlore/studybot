import discord
from discord import app_commands
from discord.ext import commands
from config import load_json
from utils.helpers import send_and_pin
from utils.permissions import is_admin
from utils.logger import setup_logger
from utils.pendo import track as pendo_track

logger = setup_logger("Setup")

class Setup(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="setup", description="Cria automaticamente todas as categorias e canais do servidor.")
    @app_commands.default_permissions(administrator=True)
    @is_admin()
    async def setup(self, interaction: discord.Interaction):
        if not interaction.guild:
            return await interaction.response.send_message("Este comando só pode ser usado em servidores.", ephemeral=True)

        await interaction.response.defer(ephemeral=True)

        categories_data = load_json("categories.json")
        templates = load_json("templates.json")
        default_template = templates.get("default", "Template padrão não encontrado.")
        guild = interaction.guild

        created_categories = 0
        created_channels = 0
        skipped_categories = 0
        skipped_channels = 0

        existing_categories = {cat.name: cat for cat in guild.categories}

        for cat_info in categories_data:
            cat_name = cat_info["name"]
            if cat_name in existing_categories:
                category = existing_categories[cat_name]
                skipped_categories += 1
            else:
                category = await guild.create_category(cat_name)
                existing_categories[cat_name] = category
                created_categories += 1
                logger.info(f"Categoria criada: {cat_name}")

            for channel_name in cat_info["channels"]:
                existing_channel = discord.utils.get(category.text_channels, name=channel_name)
                if existing_channel:
                    skipped_channels += 1
                    continue

                try:
                    channel = await category.create_text_channel(channel_name)
                    created_channels += 1
                    template_content = templates.get(channel_name, default_template)
                    await send_and_pin(channel, template_content)
                except Exception as e:
                    logger.error(f"Erro ao criar canal {channel_name}: {e}")

        embed = discord.Embed(
            title="✅ Setup concluído",
            color=discord.Color.green(),
            description="Configuração automática do servidor finalizada."
        )
        embed.add_field(name="Categorias criadas", value=str(created_categories), inline=True)
        embed.add_field(name="Categorias já existentes", value=str(skipped_categories), inline=True)
        embed.add_field(name="Canais criados", value=str(created_channels), inline=True)
        embed.add_field(name="Canais já existentes", value=str(skipped_channels), inline=True)

        await pendo_track(
            "server_setup_completed",
            visitor_id=str(interaction.user.id),
            account_id=str(interaction.guild.id),
            properties={
                "guild_id": str(interaction.guild.id),
                "created_categories": created_categories,
                "skipped_categories": skipped_categories,
                "created_channels": created_channels,
                "skipped_channels": skipped_channels,
            },
        )

        await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Setup(bot))