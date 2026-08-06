import discord
from utils.logger import setup_logger

logger = setup_logger("Helpers")

async def send_and_pin(channel: discord.TextChannel, content: str):
    try:
        msg = await channel.send(content)
        await msg.pin()
        logger.info(f"Mensagem fixada em #{channel.name}")
        return msg
    except discord.Forbidden:
        logger.error(f"Sem permissão para enviar/fixar em #{channel.name}")
        return None
    except Exception as e:
        logger.error(f"Erro em send_and_pin #{channel.name}: {e}")
        return None