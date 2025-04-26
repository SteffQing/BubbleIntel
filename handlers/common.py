from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, BotCommand, BotCommandScopeAllPrivateChats, BufferedInputFile, User
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
    user: User = message.from_user  # type: ignore
    welcome_message = (
        f"👋 Hello <b>{(user.first_name or user.username or 'there')}!</b>\n\n"
        f"<b>{('Welcome to the Bubblemap Intel Bot!')}</b>\n\n"
        f"This bot helps you visualize the token distribution of cryptocurrencies on various blockchain networks using Bubblemaps. Gain insights into token ownership, identify potential risks, and explore the flow of assets.\n\n"
        f"To get started, use the following commands:\n"
        f"➡️ /{networks[0]} [contract_address] - Explore the Bubblemap for a token on the <b>Ethereum</b> network. "
        f"(Replace `[contract_address]` with the actual contract address).\n"
        f"➡️ /{networks[8]} [contract_address] - Explore the Bubblemap for a token on the <b>Solana</b> network.\n"
        f"➡️ ... and so on for other networks.\n\n"
        f"For more detailed instructions and a list of all available commands, use /{('help')}.\n\n"
        f"Happy exploring! 🚀"
    )
    await message.answer(welcome_message, parse_mode="HTML")


@router.message(Command(commands=["help"]))
async def cmd_help(message: Message, state: FSMContext):
    help_text_mv2 = (
        "*Bubblemap Intel Bot \\- Help*\n\n"
        "*About:*\n"
        "This bot provides visualizations of cryptocurrency token distributions using Bubblemaps, offering insights into token ownership and potential risks\\.\n\n"
        "*Usage:*\n"
        "To explore a token's Bubblemap, use the network\\-specific commands followed by the token's contract address\\.\n\n"
        "*Available Commands:*\n"
        "\\➡️ /*start* \\- Displays the welcome message and basic instructions\\.\n"
        "\\➡️ /*help* \\- Shows this detailed help message\\.\n"
        f"{''.join(f'\\➡️ /*{network} \\[contract\\_address\\]* \\- Explore the Bubblemap for a token on the *{network.upper()}* network\\.\n' for network in networks)}\n\n"
        "*Example:*\n"
        "To see the Bubblemap for a token on Ethereum, you might use:\n"
        "`/eth 0xdAC17F958D2Ee523a2206206994597C13D831ec7` \\(This is the contract address for USDT on Ethereum\\)\n\n"
        "*How it Works:*\n"
        "The bot fetches Bubblemap data and relevant token information based on the contract address you provide\\. It then generates a visual representation and provides key details about the token's distribution and score \\(if available\\)\\.\n\n"
        "*Feedback and Support:*\n"
        "If you encounter any issues or have suggestions, please feel free to reach out to the [Bot developer](tg://user?id=976665869)\n\n"
        "Thank you for using the Bubblemap Intel Bot\\! 🌐"
    )
    await message.answer(help_text_mv2, parse_mode="MarkdownV2")


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
            await message.answer(f"Sorry 🫠 you need to pass in a contract address after the /{network} command.\n\n"
                                 f"Example: /{network} 0x...")
            return

        await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
        is_avbl_future = bubblemap.isIframeAvailable(asset, network)
        token_data_future = mobula.get_token_data(asset)

        is_avbl, tokenData = await promise_all([is_avbl_future, token_data_future])

        if is_avbl is False:
            return await message.answer(f"The contract address `{asset}` on {network.upper()} does not have bubblemap information. Please try another contract!", parse_mode="MarkdownV2")

        init_bm = await message.answer(f"Generating Bubblemaps for {tokenData['name']}({tokenData['symbol']})...")

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

    except Exception as e:
        print(e)
        await message.answer(f"An error occurred while processing your request.\nPlease view the bubblemap directly by clicking the button below", reply_markup=view_on_bubblemaps(asset, network))