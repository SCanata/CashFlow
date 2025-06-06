import random
import pytest

from cashflow.engine import Game, Player, Board, Space, SpaceType, Asset, Liability


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
    assert players[1].position == 3
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
    player.liabilities.append(Liability("Loan", expense=75))
    assert player.net_cashflow() == 1000 + 200 - (500 + 75)


def test_baby_space_adds_liability():
    player = Player(name="Parent", cash=1000, income=1000, expenses=500)
    board = Board([Space(0, SpaceType.BABY)])
    game = Game([player], board)
    game.move_player(player, 1)
    assert len(player.liabilities) == 1
    assert player.liabilities[0].expense == 50
