import time
from cashflow.engine import Game, Player


def main():
    players = [
        Player(name="Alice", cash=1000, income=1000, expenses=800),
        Player(name="Bob", cash=1000, income=1500, expenses=1200),
    ]
    game = Game(players)

    round_counter = 0
    while not game.is_finished() and round_counter < 50:
        game.play_round()
        round_counter += 1
        for p in players:
            print(f"{p.name}: cash={p.cash}, position={p.position}, assets={len(p.assets)}")
        print("---")
        time.sleep(0.1)

    winner = max(players, key=lambda p: p.cash)
    print(f"Winner is {winner.name} with cash {winner.cash}")


if __name__ == "__main__":
    main()
