@dataclass
class Trader:

    id: str

    broker: str

    nickname: str

    equity_curve: list[float]

    followers: int

    total_followers: int

    aum: float

    pnl: float

    pnl_ratio: float

    winrate: float

    lead_days: int

    leverage: float | None

    instruments: list[str]

    trades: list = field(default_factory=list)