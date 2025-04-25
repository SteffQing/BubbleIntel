import re
import asyncio
from typing import Coroutine, List

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
            
            
async def promise_all(coroutines: List[Coroutine]):
    return await asyncio.gather(*coroutines)


def truncate_address(address, start_length=6, end_length=5):
    if not address.startswith("0x"):
        return address  # Return original if it doesn't look like an address

    return address[:start_length] + "..." + address[-end_length:]

def format_small_number(n) -> str:
    try:
        price_value = float(n)

        if price_value >= 1:
            return f"{price_value:.2f}"
        elif price_value > 0:
            s = f"{price_value:.8f}"
            decimal_index = s.find('.')
            if decimal_index != -1:
                first_digit_index = -1
                for i in range(decimal_index + 1, len(s)):
                    if s[i] != '0':
                        first_digit_index = i
                        break

                if first_digit_index != -1:
                    return f"{price_value:.{first_digit_index + 2 - decimal_index}f}"
                else:
                    return "0.00" 
            else:
                return f"{price_value:.2f}" 
        else:
            return "0.00"
    except ValueError:
        return "0.00"
    
def format_large_number(n):
    if n < 1_000:
        return format_small_number(n)
    elif n < 1_000_000:
        return f"{n / 1_000:.1f}k".rstrip('0').rstrip('.')
    elif n < 1_000_000_000:
        return f"{n / 1_000_000:.1f}m".rstrip('0').rstrip('.')
    elif n < 1_000_000_000_000:
        return f"{n / 1_000_000_000:.1f}b".rstrip('0').rstrip('.')
    else:
        return f"{n / 1_000_000_000_000:.1f}t".rstrip('0').rstrip('.')
    