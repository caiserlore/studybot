from discord.ext import commands

class Progress(commands.Cog):
    """Placeholder para funcionalidades de progresso adicionais."""
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(Progress(bot))