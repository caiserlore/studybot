import discord
from discord import app_commands

def is_admin():
    async def predicate(interaction: discord.Interaction) -> bool:
        if not interaction.guild:
            return False
        member = interaction.user
        return member.guild_permissions.administrator
    return app_commands.check(predicate)