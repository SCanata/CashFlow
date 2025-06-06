import time
import argparse
from cashflow.engine import Game, Player


def main():
    parser = argparse.ArgumentParser(description="Run a CashFlow game")
    parser.add_argument(
        "--players",
        default="Alice,Bob",
        help="Comma-separated list of player names",
    )
    parser.add_argument(
        "--cash",
        type=int,
        default=1000,
        help="Starting cash for each player",
    )
    parser.add_argument(
        "--rounds",
        type=int,
        default=50,
        help="Maximum rounds to play",
    )
    args = parser.parse_args()

    names = [n.strip() for n in args.players.split(",") if n.strip()]
    players = [
        Player(name=n, cash=args.cash, income=1000, expenses=800) for n in names
    ]

    game = Game(players)

    round_counter = 0
    while not game.is_finished() and round_counter < args.rounds:
        game.play_round()
        round_counter += 1
        for p in players:
            print(
                f"{p.name}: cash={p.cash}, position={p.position}, assets={len(p.assets)}, liabilities={len(p.liabilities)}"
            )
        print("---")
        time.sleep(0.1)

    winner = max(players, key=lambda p: p.cash)
    print(f"Winner is {winner.name} with cash {winner.cash}")


if __name__ == "__main__":
    main()
