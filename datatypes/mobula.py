from typing import TypedDict, List

class Contract(TypedDict):
    address: str
    blockchainId: str
    blockchain: str
    decimals: int

class Native(TypedDict):
    name: str
    symbol: str
    address: str
    type: str
    decimals: int
    logo: str

class TokenData(TypedDict):
    id: int
    name: str
    symbol: str
    decimals: int
    logo: str
    rank: int
    price: float
    market_cap: float
    market_cap_diluted: float
    volume: float
    volume_change_24h: float
    volume_7d: float
    liquidity: float
    ath: float
    atl: float
    off_chain_volume: int
    is_listed: bool
    price_change_1h: float
    price_change_24h: float
    price_change_7d: float
    price_change_1m: float
    price_change_1y: float
    total_supply: float
    circulating_supply: float
    contracts: List[Contract]
    native: Native

class TokenDataApiRes(TypedDict):
    data: TokenData
