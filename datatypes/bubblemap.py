from typing import TypedDict, Literal, List, Optional, Dict

from datatypes.constants import Network

class AvailabilityResponse(TypedDict):
    availability: bool
    status: Literal["OK", "KO"]

class IdentifiedSupply(TypedDict):
    percent_in_cexs: float
    percent_in_contracts: float

class ScoreResponse(TypedDict):
    decentralisation_score: float
    identified_supply: IdentifiedSupply
    dt_update: str
    ts_update: int
    status: Literal["OK", "KO"]
    message: str


class Node(TypedDict):
    address: str
    amount: float
    is_contract: bool
    name: Optional[str]
    percentage: float
    transaction_count: int
    transfer_X721_count: Optional[int]
    transfer_count: int

class Link(TypedDict):
    backward: float
    forward: float
    source: int
    target: int

class TokenLink(TypedDict):
    address: str
    decimals: int
    name: str
    symbol: str
    links: List[Link]
    
class Metadata(TypedDict):
    max_amount: float
    min_amount: float

class BubbleMapData(TypedDict):
    version: int
    chain: Network
    token_address: str
    dt_update: str
    full_name: str
    symbol: str
    is_X721: bool
    metadata: Metadata
    nodes: List[Node]
    links: List[Link]
    token_links: List[TokenLink]
