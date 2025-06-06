"""Simple game engine for a Cashflow board game clone."""

from dataclasses import dataclass, field
from enum import Enum, auto
import random
from typing import List, Optional


class SpaceType(Enum):
    PAYCHECK = auto()
    DOODAD = auto()
    DEAL = auto()
    MARKET = auto()
    CHARITY = auto()
    DOWNSIZED = auto()
    BABY = auto()
    OPPORTUNITY = auto()


@dataclass
class Space:
    idx: int
    type: SpaceType


@dataclass
class Asset:
    name: str
    income: int


@dataclass
class Liability:
    name: str
    expense: int
    payoff: int = 0


@dataclass
class DealCard:
    """Card representing a potential investment."""
    name: str
    cost: int
    income: int


@dataclass
class DoodadCard:
    """Card representing an immediate expense."""
    name: str
    expense: int


@dataclass
class MarketCard:
    """Card representing a market event."""
    name: str
    effect: str  # 'lose_asset', 'gain_cash', or 'liability'
    amount: int = 0
    expense: int = 0


class Deck:
    """Simple deck that returns a random card when drawn."""
    def __init__(self, cards: List):
        self.cards = list(cards)

    def draw(self, rng: random.Random):
        return rng.choice(self.cards)


@dataclass
class Player:
    name: str
    cash: int = 0
    income: int = 0
    expenses: int = 0
    assets: List[Asset] = field(default_factory=list)
    liabilities: List[Liability] = field(default_factory=list)
    position: int = 0
    skip_turns: int = 0
    extra_dice_turns: int = 0

    def net_cashflow(self) -> int:
        asset_income = sum(a.income for a in self.assets)
        liability_cost = sum(l.expense for l in self.liabilities)
        return self.income + asset_income - (self.expenses + liability_cost)

    def passive_income(self) -> int:
        return sum(a.income for a in self.assets)

    def total_expenses(self) -> int:
        return self.expenses + sum(l.expense for l in self.liabilities)

    def pay_off_liability(self, index: int) -> bool:
        if 0 <= index < len(self.liabilities):
            liability = self.liabilities[index]
            if self.cash >= liability.payoff:
                self.cash -= liability.payoff
                self.liabilities.pop(index)
                return True
        return False


class Board:
    def __init__(self, spaces: Optional[List[Space]] = None):
        if spaces is None:
            spaces = self._default_board()
        self.spaces = spaces

    @staticmethod
    def _default_board() -> List[Space]:
        # This minimal prototype board has 48 spaces, mixing paychecks, deals, doodads, markets, etc.
        return [
            Space(0, SpaceType.PAYCHECK),
            Space(1, SpaceType.DEAL),
            Space(2, SpaceType.DOODAD),
            Space(3, SpaceType.MARKET),
            Space(4, SpaceType.DEAL),
            Space(5, SpaceType.PAYCHECK),
            Space(6, SpaceType.DOODAD),
            Space(7, SpaceType.CHARITY),
            Space(8, SpaceType.DEAL),
            Space(9, SpaceType.MARKET),
            Space(10, SpaceType.DOODAD),
            Space(11, SpaceType.PAYCHECK),
            Space(12, SpaceType.DEAL),
            Space(13, SpaceType.DOWNSIZED),
            Space(14, SpaceType.DEAL),
            Space(15, SpaceType.OPPORTUNITY),
            Space(16, SpaceType.PAYCHECK),
            Space(17, SpaceType.DEAL),
            Space(18, SpaceType.MARKET),
            Space(19, SpaceType.DOODAD),
            Space(20, SpaceType.DEAL),
            Space(21, SpaceType.BABY),
            Space(22, SpaceType.PAYCHECK),
            Space(23, SpaceType.DEAL),
            Space(24, SpaceType.DOODAD),
            Space(25, SpaceType.MARKET),
            Space(26, SpaceType.DEAL),
            Space(27, SpaceType.PAYCHECK),
            Space(28, SpaceType.DOODAD),
            Space(29, SpaceType.CHARITY),
            Space(30, SpaceType.DEAL),
            Space(31, SpaceType.MARKET),
            Space(32, SpaceType.DOODAD),
            Space(33, SpaceType.PAYCHECK),
            Space(34, SpaceType.DEAL),
            Space(35, SpaceType.DOWNSIZED),
            Space(36, SpaceType.DEAL),
            Space(37, SpaceType.OPPORTUNITY),
            Space(38, SpaceType.PAYCHECK),
            Space(39, SpaceType.DEAL),
            Space(40, SpaceType.MARKET),
            Space(41, SpaceType.DOODAD),
            Space(42, SpaceType.DEAL),
            Space(43, SpaceType.BABY),
            Space(44, SpaceType.DEAL),
            Space(45, SpaceType.PAYCHECK),
            Space(46, SpaceType.MARKET),
            Space(47, SpaceType.DOODAD),
        ]

    def space_count(self) -> int:
        return len(self.spaces)


def _default_deal_cards() -> List[DealCard]:
    return [
        DealCard("Condo", cost=1000, income=100),
        DealCard("Car Wash", cost=2000, income=150),
        DealCard("Retail Shop", cost=3000, income=250),
    ]


def _default_big_deal_cards() -> List[DealCard]:
    return [
        DealCard("Apartment Building", cost=6000, income=600),
        DealCard("Storage Units", cost=8000, income=750),
    ]


def _default_doodad_cards() -> List[DoodadCard]:
    return [
        DoodadCard("New Phone", expense=100),
        DoodadCard("Vacation", expense=400),
        DoodadCard("Gadget", expense=250),
    ]


def _default_market_cards() -> List[MarketCard]:
    return [
        MarketCard("Economic Boom", effect="gain_cash", amount=500),
        MarketCard("Property Tax", effect="liability", expense=150),
        MarketCard("Storm Damage", effect="lose_asset"),
    ]


class Game:
    def __init__(
        self,
        players: List[Player],
        board: Optional[Board] = None,
        die_sides: int = 6,
        deal_deck: Optional[Deck] = None,
        big_deal_deck: Optional[Deck] = None,
        doodad_deck: Optional[Deck] = None,
        market_deck: Optional[Deck] = None,
    ):
        self.players = players
        self.board = board or Board()
        self.die_sides = die_sides
        self.current_player_idx = 0
        self.random = random.Random()
        self.deal_deck = deal_deck or Deck(_default_deal_cards())
        self.big_deal_deck = big_deal_deck or Deck(_default_big_deal_cards())
        self.doodad_deck = doodad_deck or Deck(_default_doodad_cards())
        self.market_deck = market_deck or Deck(_default_market_cards())

    def roll_die(self, player: Player) -> int:
        """Roll one or two dice depending on player's bonus state."""
        if player.extra_dice_turns > 0:
            player.extra_dice_turns -= 1
            return self.random.randint(1, self.die_sides) + self.random.randint(1, self.die_sides)
        return self.random.randint(1, self.die_sides)

    def move_player(self, player: Player, steps: int) -> Space:
        """Move player forward `steps` spaces and handle the landing space."""
        player.position = (player.position + steps) % self.board.space_count()
        space = self.board.spaces[player.position]
        self.handle_space(player, space)
        return space

    def handle_space(self, player: Player, space: Space):
        if space.type == SpaceType.PAYCHECK:
            player.cash += player.net_cashflow()
            if player.liabilities:
                # Attempt to pay off the first liability if affordable
                player.pay_off_liability(0)

        elif space.type == SpaceType.DOODAD:
            card = self.doodad_deck.draw(self.random)
            player.cash -= card.expense

        elif space.type == SpaceType.DEAL:
            card = self.deal_deck.draw(self.random)
            if player.cash >= card.cost:
                player.cash -= card.cost
                player.assets.append(Asset(card.name, card.income))

        elif space.type == SpaceType.MARKET:
            card = self.market_deck.draw(self.random)
            if card.effect == "lose_asset":
                if player.assets:
                    player.assets.pop()
            elif card.effect == "gain_cash":
                player.cash += card.amount
            elif card.effect == "liability":
                payoff = card.expense * 10
                player.liabilities.append(Liability(card.name, card.expense, payoff))

        elif space.type == SpaceType.CHARITY:
            donation = min(100, player.cash)
            player.cash -= donation
            player.extra_dice_turns = 3

        elif space.type == SpaceType.DOWNSIZED:
            player.cash -= player.expenses * 2
            player.skip_turns = 2

        elif space.type == SpaceType.BABY:
            player.liabilities.append(Liability("Baby", 50, payoff=500))

        elif space.type == SpaceType.OPPORTUNITY:
            card = self.big_deal_deck.draw(self.random)
            if player.cash >= card.cost:
                player.cash -= card.cost
                player.assets.append(Asset(card.name, card.income))

    def next_turn(self) -> str:
        """Advance the game by one turn for the current player."""
        player = self.players[self.current_player_idx]
        description = ""
        if player.skip_turns > 0:
            player.skip_turns -= 1
            description = f"{player.name} is downsized and must skip a turn."
        else:
            steps = self.roll_die(player)
            start_pos = player.position
            space = self.move_player(player, steps)
            description = (
                f"{player.name} rolled {steps}, moving from {start_pos} to "
                f"{player.position} ({space.type.name})."
            )
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
        return description

    def is_finished(self) -> bool:
        return any(
            p.cash >= 50000 or p.passive_income() >= p.total_expenses()
            for p in self.players
        )

    def play_round(self) -> List[str]:
        """Play a complete round and return log messages for each turn."""
        logs: List[str] = []
        for _ in range(len(self.players)):
            logs.append(self.next_turn())
        return logs
