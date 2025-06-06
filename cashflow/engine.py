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


@dataclass
class Player:
    name: str
    cash: int = 0
    income: int = 0
    expenses: int = 0
    assets: List[Asset] = field(default_factory=list)
    liabilities: List[Liability] = field(default_factory=list)
    position: int = 0

    def net_cashflow(self) -> int:
        asset_income = sum(a.income for a in self.assets)
        liability_cost = sum(l.expense for l in self.liabilities)
        return self.income + asset_income - (self.expenses + liability_cost)


class Board:
    def __init__(self, spaces: Optional[List[Space]] = None):
        if spaces is None:
            spaces = self._default_board()
        self.spaces = spaces

    @staticmethod
    def _default_board() -> List[Space]:
        # The real Cashflow board contains many more spaces than the minimal
        # prototype, so here we expand the default layout to 48 spaces.  This
        # list loosely mirrors the distribution of special spaces found on the
        # actual board, providing a mix of paychecks, deals and random events.

        base_layout = [
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

        layout = base_layout
        return layout

    def space_count(self) -> int:
        return len(self.spaces)


class Game:
    def __init__(self, players: List[Player], board: Optional[Board] = None, die_sides: int = 6):
        self.players = players
        self.board = board or Board()
        self.die_sides = die_sides
        self.current_player_idx = 0
        self.random = random.Random()

    def roll_die(self) -> int:
        return self.random.randint(1, self.die_sides)

    def move_player(self, player: Player, steps: int):
        player.position = (player.position + steps) % self.board.space_count()
        space = self.board.spaces[player.position]
        self.handle_space(player, space)

    def handle_space(self, player: Player, space: Space):
        if space.type == SpaceType.PAYCHECK:
            player.cash += player.net_cashflow()
        elif space.type == SpaceType.DOODAD:
            cost = self.random.randint(100, 500)
            player.cash -= cost
        elif space.type == SpaceType.DEAL:
            investment = self.random.randint(1000, 4000)
            income = self.random.randint(100, 300)
            if player.cash >= investment:
                player.cash -= investment
                player.assets.append(Asset(f"Deal {investment}", income))
        elif space.type == SpaceType.MARKET:
            if player.assets:
                player.assets.pop()
        elif space.type == SpaceType.CHARITY:
            donation = min(100, player.cash)
            player.cash -= donation
        elif space.type == SpaceType.DOWNSIZED:
            player.cash -= player.expenses * 2
        elif space.type == SpaceType.BABY:
            player.liabilities.append(Liability("Baby", 50))
        elif space.type == SpaceType.OPPORTUNITY:
            investment = self.random.randint(2000, 6000)
            income = self.random.randint(200, 500)
            if player.cash >= investment:
                player.cash -= investment
                player.assets.append(Asset(f"Opportunity {investment}", income))

    def next_turn(self):
        player = self.players[self.current_player_idx]
        steps = self.roll_die()
        self.move_player(player, steps)
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)

    def is_finished(self) -> bool:
        return any(p.cash >= 50000 for p in self.players)

    def play_round(self):
        for _ in range(len(self.players)):
            self.next_turn()

