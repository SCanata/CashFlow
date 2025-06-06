import os
import sys
import random
import pytest

# Ensure the project root is on sys.path so that cashflow can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from cashflow.engine import (
    Game,
    Player,
    Board,
    Space,
    SpaceType,
    Asset,
    Liability,
    Deck,
    DealCard,
    DoodadCard,
    MarketCard,
)
from cashflow.scoreboard import ScoreBoard


def test_default_board_setup():
    board = Board()
    assert board.space_count() == 48


def test_play_round_updates_state():
    players = [
        Player(name="Alice", cash=1000, income=1000, expenses=800),
        Player(name="Bob", cash=1000, income=1500, expenses=1200),
    ]
    game = Game(players)
    game.random.seed(0)
    game.play_round()
    assert players[0].position == 4
    assert players[1].position == 1
    assert players[0].cash == 1000
    assert players[1].cash == 1000


def test_winning_condition():
    players = [
        Player(name="Alice", cash=51000, income=0, expenses=0),
        Player(name="Bob", cash=0, income=0, expenses=0),
    ]
    game = Game(players)
    assert game.is_finished()


def test_asset_income_and_liability_expense():
    player = Player(name="Test", income=1000, expenses=500)
    player.assets.append(Asset("House", income=200))
    player.liabilities.append(Liability("Loan", expense=75, payoff=500))
    assert player.net_cashflow() == 1000 + 200 - (500 + 75)


def test_baby_space_adds_liability():
    player = Player(name="Parent", cash=1000, income=1000, expenses=500)
    board = Board([Space(0, SpaceType.BABY)])
    game = Game([player], board)
    game.move_player(player, 1)
    assert len(player.liabilities) == 1
    assert player.liabilities[0].expense == 50


def test_deal_card_adds_asset():
    player = Player(name="Investor", cash=2000)
    deal_deck = Deck([DealCard("Test Deal", cost=1000, income=100)])
    board = Board([Space(0, SpaceType.DEAL)])
    game = Game([player], board, deal_deck=deal_deck)
    game.move_player(player, 1)
    assert player.cash == 1000
    assert len(player.assets) == 1
    assert player.assets[0].income == 100


def test_doodad_card_reduces_cash():
    player = Player(name="Shopper", cash=1000)
    doodad_deck = Deck([DoodadCard("Test Doodad", expense=300)])
    board = Board([Space(0, SpaceType.DOODAD)])
    game = Game([player], board, doodad_deck=doodad_deck)
    game.move_player(player, 1)
    assert player.cash == 700


def test_market_card_grants_cash():
    player = Player(name="Trader", cash=500)
    market_deck = Deck([MarketCard("Bonus", effect="gain_cash", amount=200)])
    board = Board([Space(0, SpaceType.MARKET)])
    game = Game([player], board, market_deck=market_deck)
    game.move_player(player, 1)
    assert player.cash == 700


def test_pay_off_liability():
    player = Player(name="Debtor", cash=1000, income=0, expenses=0)
    player.liabilities.append(Liability("Car Loan", expense=50, payoff=300))
    board = Board([Space(0, SpaceType.PAYCHECK)])
    game = Game([player], board)
    game.move_player(player, 1)
    # net_cashflow = income + asset_income - (expenses + liability_expense)
    # Here income = 0, no assets, expenses = 0, liability_expense = 50
    # During PAYCHECK, player.cash += net_cashflow (0 - 50 = -50) => cash = 950
    # Then pay_off_liability pops that liability for 300 => cash = 650
    assert player.cash == 650
    assert not player.liabilities


def test_winning_condition_passive_income():
    player = Player(name="Investor", cash=0, income=0, expenses=500)
    player.assets.append(Asset("Rental", income=600))
    game = Game([player])
    assert game.is_finished()


def test_charity_grants_extra_dice():
    player = Player(name="Charitable", cash=1000)
    board = Board([Space(0, SpaceType.CHARITY), Space(1, SpaceType.PAYCHECK)])
    game = Game([player], board)
    game.random.seed(0)
    # First turn: land on CHARITY
    msg = game.next_turn()
    assert player.cash == 900
    assert player.extra_dice_turns == 3
    # Second turn: should roll two dice (seeded to 4 + 1 = 5)
    game.next_turn()
    assert player.position == 1
    assert player.extra_dice_turns == 2


def test_downsized_skips_turns():
    player = Player(name="Worker", cash=1000, income=1000, expenses=500)
    board = Board([Space(0, SpaceType.DOWNSIZED), Space(1, SpaceType.PAYCHECK)])
    game = Game([player], board)
    game.random.seed(0)
    # First turn: land on DOWNSIZED
    game.next_turn()
    # downsized: cash -= expenses*2 => 1000 - 1000 = 0
    assert player.cash == 0
    assert player.skip_turns == 2
    # Next two turns should be skipped
    game.next_turn()
    assert player.position == 0
    assert player.skip_turns == 1
    game.next_turn()
    assert player.position == 0
    assert player.skip_turns == 0


def test_scoreboard_records_wins(tmp_path):
    sb_path = tmp_path / "scores.json"
    board = ScoreBoard(str(sb_path))
    board.record_win("Alice")
    board.record_win("Bob")
    board.record_win("Alice")
    reloaded = ScoreBoard(str(sb_path))
    assert reloaded.scores == {"Alice": 2, "Bob": 1}


def test_scoreboard_str(tmp_path):
    path = tmp_path / "scores.json"
    sb = ScoreBoard(str(path))
    sb.record_win("Alice")
    sb.record_win("Bob")
    sb.record_win("Alice")
    # Scores should be sorted by key for deterministic string
    assert str(sb) == "Alice: 2, Bob: 1"


def test_scoreboard_handles_invalid_json(tmp_path):
    path = tmp_path / "scores.json"
    path.write_text("not json")
    sb = ScoreBoard(str(path))
    assert sb.scores == {}


def test_roll_die_two_dice_and_single():
    player = Player(name="Roller")
    game = Game([player])
    game.random.seed(0)
    single = game.roll_die(player)
    assert 1 <= single <= 6
    player.extra_dice_turns = 1
    game.random.seed(0)
    double = game.roll_die(player)
    assert 2 <= double <= 12


def test_next_turn_log_message():
    player = Player(name="Logger", cash=1000, income=1000, expenses=800)
    board = Board([Space(i, SpaceType.PAYCHECK) for i in range(6)])
    game = Game([player], board)
    game.random.seed(0)
    msg = game.next_turn()
    assert "Logger rolled 4" in msg
    assert "to 4 (PAYCHECK)" in msg


def test_play_round_returns_logs():
    players = [Player(name="A"), Player(name="B")]
    board = Board([Space(i, SpaceType.PAYCHECK) for i in range(6)])
    game = Game(players, board)
    game.random.seed(0)
    logs = game.play_round()
    assert len(logs) == 2
    assert all(isinstance(log, str) for log in logs)
