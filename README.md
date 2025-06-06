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

## Running Tests

The project uses `pytest` for its test suite. Execute the tests from the
repository root:

```bash
pytest
```
