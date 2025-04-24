import re
from aiogram import F, Router
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import Optional

from datatypes.constants import Network

router = Router()

class MenuFactory(CallbackData, prefix="trade"):
    action: str
    process: Optional[str] = None
    subject: Optional[str] = None

def generate_menu():
    markup = InlineKeyboardBuilder()
    markup.button(text="----- Wallet -----", callback_data='filler')
    markup.button(text="💼 Create", callback_data="wallet_create")
    markup.button(text="📤 Import", callback_data="wallet_import")
    markup.button(text="🗑️ Delete", callback_data="wallet_delete")

    markup.adjust(1, 3)
    return markup.as_markup()

def generate_new_user_menu():
    markup = InlineKeyboardBuilder()
    markup.button(text="💼 Create", callback_data="wallet_create")
    markup.button(text="📤 Import", callback_data="wallet_import")
    markup.adjust(2)
    return markup.as_markup()

def view_on_bubblemaps(address: str, chain: Network):
    url = f"https://app.bubblemaps.io/{chain}/token/{address}?mode=0"
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔎 View on Bubblemaps", url=url)]
        ]
    )
    return markup