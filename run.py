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
    parser.add_argument(
        "--delay",
        type=float,
        default=0.2,
        help="Seconds to wait between rounds",
    )
    args = parser.parse_args()

    names = [n.strip() for n in args.players.split(",") if n.strip()]
    players = [
        Player(name=n, cash=args.cash, income=1000, expenses=800) for n in names
    ]

    game = Game(players)

    def fmt_assets(p: Player) -> str:
        if not p.assets:
            return "none"
        return ", ".join(f"{a.name} (${a.income})" for a in p.assets)

    def fmt_liabs(p: Player) -> str:
        if not p.liabilities:
            return "none"
        return ", ".join(f"{l.name} (${l.expense})" for l in p.liabilities)

    print("Players:")
    for p in players:
        print(f"  {p.name} starting with ${p.cash}")

    round_counter = 0
    while not game.is_finished() and round_counter < args.rounds:
        print(f"\n=== Round {round_counter + 1} ===")
        logs = game.play_round()
        for log in logs:
            print(log)
        for p in players:
            print(
                f"{p.name}: cash=${p.cash}, pos={p.position}, assets={fmt_assets(p)}, liabilities={fmt_liabs(p)}"
            )
        round_counter += 1
        time.sleep(args.delay)

    winner = max(players, key=lambda p: p.cash)
    print(f"Winner is {winner.name} with cash {winner.cash}")


if __name__ == "__main__":
    main()
