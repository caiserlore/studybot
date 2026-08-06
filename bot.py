import asyncio
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from utils.logger import setup_logger
from database import Database

load_dotenv()
logger = setup_logger("StudyBot")

class StudyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.guilds = True
        super().__init__(command_prefix=None, intents=intents)
        self.db = Database()

    async def setup_hook(self):
        await self.load_cogs()
        await self.tree.sync()
        logger.info("Comandos sincronizados globalmente.")

    async def load_cogs(self):
        cogs = [
            "cogs.setup",
            "cogs.roadmap",
            "cogs.progress",
            "cogs.templates",
            "cogs.notes",
            "cogs.search",
            "cogs.admin",
            "cogs.stats",
        ]
        for cog in cogs:
            try:
                await self.load_extension(cog)
                logger.info(f"Cog carregado: {cog}")
            except Exception as e:
                logger.error(f"Erro ao carregar {cog}: {e}")

    async def on_ready(self):
        logger.info(f"Bot conectado como {self.user}")

async def main():
    bot = StudyBot()
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        logger.critical("Token não encontrado. Defina DISCORD_TOKEN no .env")
        return
    await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())