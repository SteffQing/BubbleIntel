from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, BotCommand, BotCommandScopeAllPrivateChats, FSInputFile

from keyboards.menu import generate_menu
from services.bubblemap import BubbleMap
from utils.constants import networks

router = Router()
router.message.filter(F.chat.type == "private")

bubblemap = BubbleMap()


async def set_bot_commands(bot: Bot):
    network_commands = list(map(lambda network: BotCommand(command=network, description=f"Query token bubblemap by the contract address on the {network} network"), networks))
    
    await bot.set_my_commands(commands=network_commands, scope=BotCommandScopeAllPrivateChats())
    
    return True
    

@router.message(Command(commands=networks))
async def cmd_start(message: Message, state: FSMContext):
    text = message.from_user
    pass
    

@router.message(Command(commands=["test"]))
async def send_bubblemap(message: Message):
    avbl = await bubblemap.isIframeAvailable("0x95ad61b0a150d79219dcf64e1e6cc01f0b64c4ce", "eth")
    print(avbl)
    photo = FSInputFile("bubblemap_0x95ad.png")
    await message.answer_photo(photo, caption="Here's the bubblemap 📈")