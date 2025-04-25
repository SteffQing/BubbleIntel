from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, BotCommand, BotCommandScopeAllPrivateChats, FSInputFile, BufferedInputFile
from aiogram.enums import ChatAction

from datatypes.constants import Network
from keyboards.menu import view_on_bubblemaps
from services.bubblemap import BubbleMap
from services.mobula import Mobula
from utils.constants import networks
from utils.index import promise_all
from utils.text import generate_token_caption

router = Router()
router.message.filter(F.chat.type == "private")

bubblemap = BubbleMap()


async def set_bot_commands(bot: Bot):
    network_commands = list(map(lambda network: BotCommand(command=network, description=f"Query token bubblemap and information by the contract address on the {network} network"), networks))
    start_command = BotCommand(command="start", description="Start the bot")
    help_command = BotCommand(command="help", description="Show help message")
    all_commands = [start_command, help_command] + network_commands

    await bot.set_my_commands(commands=all_commands, scope=BotCommandScopeAllPrivateChats())

    return True


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(
        "Hello! Welcome to the Bubblemap Explorer Bot.\n"
        "Use the network commands (e.g., /eth) followed by a contract address to explore bubblemaps.\n"
        "Example: /eth 0x... [contract address]\n\n"
        "Use /help for more information."
    )


@router.message(Command(commands=["help"]))
async def cmd_help(message: Message, state: FSMContext):
    await message.answer(
        "This bot allows you to visualize token distributions on various blockchain networks using Bubblemaps.\n\n"
        "Available commands:\n"
        "/start - Starts the bot and shows a welcome message.\n"
        f"/{' /'.join(networks)} [contract_address] - Query the bubblemap and token information for a given contract address on the specified network.\n"
        "/help - Shows this help message."
    )


@router.message(Command(commands=networks))
async def ntwrk_cmd(message: Message, command: CommandObject):
    network: Network = command.command  # type: ignore
    mobula = Mobula()
    bot = message.bot
    if bot is None:
        return

    try:
        if command.args:
            asset = command.args.split()[0]
        else:
            await message.answer(f"Sorry 🫠 you need to pass in an asset argument after the /{command.command} command")
            return

        await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
        is_avbl_future = bubblemap.isIframeAvailable(asset, network)
        token_data_future = mobula.get_token_data(asset)

        is_avbl, tokenData = await promise_all([is_avbl_future, token_data_future])

        if is_avbl is False:
            return await message.answer(f"The contract address passed in for {network} has no bubblemap information. Please try another!")

        init_bm = await message.answer(f"Generating Bubblemaps for {tokenData['name']}({tokenData['symbol']})")

        image_bytes_future = bubblemap.screenshot_bubblemap(asset, network)
        score_future = bubblemap.getScore(asset, network)
        bubblemap_data_future = bubblemap.getBubblemapData(asset, network)

        await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_PHOTO)
        image_bytes, score, bubblemap_data = await promise_all([image_bytes_future, score_future, bubblemap_data_future])

        await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
        await bot.delete_message(init_bm.chat.id, init_bm.message_id)
        image_bytes.seek(0)

        photo = BufferedInputFile(image_bytes.read(), filename=f"{tokenData['symbol']}.png")
        caption = generate_token_caption(tokenData, score, bubblemap_data)
        await message.answer_photo(photo, caption=caption, parse_mode="HTML", reply_markup=view_on_bubblemaps(asset, network))

    except:
        await message.answer(f"An error occurred while processing your request for {network}", reply_markup=view_on_bubblemaps(asset, network))