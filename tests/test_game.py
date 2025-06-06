import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import random
import pytest

from cashflow.engine import Game, Player, Board


def test_default_board_setup():
    board = Board()
    assert board.space_count() == 12

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
