from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, BotCommand, BotCommandScopeAllPrivateChats, FSInputFile
from aiogram.enums import ChatAction

from datatypes.constants import Network
from keyboards.menu import generate_menu, view_on_bubblemaps
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
    
    await bot.set_my_commands(commands=network_commands, scope=BotCommandScopeAllPrivateChats())
    
    return True
    

@router.message(Command(commands=networks))
async def ntwrk_cmd(message: Message, command: CommandObject, state: FSMContext):
    network: Network = command.command # type: ignore
    mobula = Mobula()
    if command.args:
        asset = command.args.split()[0]
    else:
        await message.answer(f"Sorry 🫠 you need to pass in an asset argument after the {command.command} command")
        return
    
    bot = message.bot
    if bot is None:
        return
    
    await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
    is_avbl = await bubblemap.isIframeAvailable(asset, network)
    if is_avbl is False:
        return await message.answer(f"The contract address passed in for {network} has no bubblemap information. Please try another!")
    
    tokenData = await mobula.get_token_data(asset)
    await message.answer(f"Generating Bubblemaps for {tokenData['name']}({tokenData['symbol']})")
    
    # await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_PHOTO)
    # await bubblemap.screenshot_bubblemap(asset, network)
    
    await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
    score = await bubblemap.getScore(asset, network)
    bubblemap_data = await bubblemap.getBubblemapData(asset, network)
    
    photo = FSInputFile(f"bubblemap/{asset}.png")
    caption = generate_token_caption(tokenData, score, bubblemap_data)
    await message.answer_photo(photo, caption, parse_mode="HTML", reply_markup=view_on_bubblemaps(asset, network))
    

text = """
<b>bold</b>, <strong>bold</strong>
<i>italic</i>, <em>italic</em>
<u>underline</u>, <ins>underline</ins>
<s>strikethrough</s>, <strike>strikethrough</strike>, <del>strikethrough</del>
<span class="tg-spoiler">spoiler</span>, <tg-spoiler>spoiler</tg-spoiler>
<b>bold <i>italic bold <s>italic bold strikethrough <span class="tg-spoiler">italic bold strikethrough spoiler</span></s> <u>underline italic bold</u></i> bold</b>
<a href="http://www.example.com/">inline URL</a>
<a href="tg://user?id=123456789">inline mention of a user</a>
<tg-emoji emoji-id="5368324170671202286">👍</tg-emoji>
<code>inline fixed-width code</code>
<pre>pre-formatted fixed-width code block</pre>
<pre><code class="language-python">pre-formatted fixed-width code block written in the Python programming language</code></pre>
<blockquote>Block quotation started\nBlock quotation continued\nThe last line of the block quotation</blockquote>
<blockquote expandable>Expandable block quotation started\nExpandable block quotation continued\nExpandable block quotation continued\nHidden by default part of the block quotation started\nExpandable block quotation continued\nThe last line of the block quotation</blockquote>
"""

@router.message(Command(commands=["test"]))
async def send_bubblemap(message: Message):
    avbl = await bubblemap.isIframeAvailable("0x95ad61b0a150d79219dcf64e1e6cc01f0b64c4ce", "eth")
    print(avbl)
    photo = FSInputFile("bubblemap_0x95ad.png")
    await message.answer_photo(photo, caption=text, parse_mode="HTML")