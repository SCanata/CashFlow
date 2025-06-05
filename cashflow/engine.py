"""Simple game engine for a Cashflow board game clone."""

from dataclasses import dataclass, field
from enum import Enum, auto
import random
from typing import List, Callable, Optional


class SpaceType(Enum):
    PAYCHECK = auto()
    DOODAD = auto()
    DEAL = auto()
    MARKET = auto()
    CHARITY = auto()


@dataclass
class Space:
    idx: int
    type: SpaceType


@dataclass
class Player:
    name: str
    cash: int = 0
    income: int = 0
    expenses: int = 0
    assets: List[str] = field(default_factory=list)
    liabilities: List[str] = field(default_factory=list)
    position: int = 0

    def net_cashflow(self) -> int:
        return self.income - self.expenses


class Board:
    def __init__(self, spaces: Optional[List[Space]] = None):
        if spaces is None:
            spaces = self._default_board()
        self.spaces = spaces

    @staticmethod
    def _default_board() -> List[Space]:
        layout = [
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
        ]
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
            if player.cash >= investment:
                player.cash -= investment
                player.assets.append(f"Deal worth {investment}")
        elif space.type == SpaceType.MARKET:
            if player.assets:
                player.assets.pop()
        elif space.type == SpaceType.CHARITY:
            donation = min(100, player.cash)
            player.cash -= donation

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

