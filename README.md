# CashFlow Game Engine

This repository contains a very small Python implementation of a game engine
for a board-game clone inspired by Robert Kiyosaki's **Cashflow**.

The engine is located in the `cashflow` package. A simple command-line runner
is provided in `run.py` to demonstrate gameplay.

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

During play, landing on certain spaces may grant assets that provide extra
income each turn or liabilities that increase a player's expenses.

You can customize the game using command-line options. For example:

```bash
python run.py --players Alice,Bob,Charlie --cash 1500 --rounds 30
```

This launches a 30-round game for three players starting with $1,500 each.

## Running Tests

The project uses `pytest` for its test suite. Execute the tests from the
repository root:

```bash
pytest
```

## Contributing

Install development dependencies and run the tests before submitting changes:

```bash
pip install -e .[dev]
pytest
```
