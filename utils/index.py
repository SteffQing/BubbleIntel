import re

def is_address_valid(wallet_address:str) -> bool:
    return bool(re.match(r"^(0x)?[0-9a-fA-F]{40}$", wallet_address))

async def process_long_message(message: str, find: str, res):
    max_message_length = 4096
    while len(message) > max_message_length or len(message) > 0:
        if len(message) < max_message_length:
            await res(message, parse_mode='Markdown')
            # message = []
        else:
            index = message[:max_message_length].rfind(find)
            sliced_message = message[:index]
            await res(sliced_message, parse_mode='Markdown')
            message = message[index:]