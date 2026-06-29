from dataclasses import dataclass


@dataclass
class Asset:
    symbol: str
    name: str | None
    asset_type: str