# CashFlow Game Engine

This repository contains a very small Python implementation of a game engine
for a board-game clone inspired by Robert Kiyosaki's **Cashflow**.

The engine is located in the `cashflow` package. A simple command-line runner
ftig7o-codex/create-game-engine-for-cashflow-clone
is provided in `run.py` to demonstrate gameplay. The default board now contains
48 spaces to better mirror the layout of the physical game.
=======
is provided in `run.py` to demonstrate gameplay.
main

## Installation

Install the package in editable mode using `pip`:

```bash
pip install -e .
```

This will make the `cashflow` package available on your system.

## Running the Example

Run the example game with:

```bash
python run.py
```

This will simulate turns for two sample players until one reaches
$50,000 in cash.

ftig7o-codex/create-game-engine-for-cashflow-clone
During play, landing on certain spaces draws from card decks that represent
deals, doodads, and market events. Deal cards may add new assets if you can
afford the purchase, doodad cards trigger immediate expenses, and market cards
can grant cash, add liabilities, or force you to lose an asset. These effects
combine with your existing assets and liabilities to modify your net cashflow
each turn. At each paycheck, the game will automatically attempt to pay off the
oldest liability if you have enough cash to cover its payoff amount. A player
wins when either their cash reaches $50,000 or their passive income from
assets meets or exceeds their total expenses.

You can customize the game using command-line options. For example:

```bash
python run.py --players Alice,Bob,Charlie --cash 1500 --rounds 30 --delay 0
```

This launches a 30-round game for three players starting with $1,500 each and
no delay between rounds.

### Command-Line Options

The runner accepts these arguments:

- `--players` comma-separated list of player names
- `--cash` starting cash for each player
- `--rounds` maximum number of rounds to play
- `--delay` seconds to pause between rounds
- `--show-scores` display the persistent scoreboard and exit
- `--scores` path to the scoreboard JSON file

The game keeps a persistent scoreboard in `scores.json` by default. To display
it without playing a game use:

```bash
python run.py --show-scores
```

During play the script prints a log message for every turn showing the dice
roll, new position and space type before displaying each player's updated cash
and assets.

=======
main
## Running Tests

The project uses `pytest` for its test suite. Execute the tests from the
repository root:

```bash
pytest
```
ftig7o-codex/create-game-engine-for-cashflow-clone

## Contributing

Install development dependencies and run the tests before submitting changes:

```bash
pip install -e .[dev]
pytest
```
=======
Main
