import json
import os
from typing import Dict


class ScoreBoard:
    """Simple persistent scoreboard stored as JSON."""

    def __init__(self, path: str = "scores.json"):
        self.path = path
        self.scores: Dict[str, int] = self._load()

    def _load(self) -> Dict[str, int]:
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def record_win(self, player: str) -> None:
        self.scores[player] = self.scores.get(player, 0) + 1
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.scores, f)

    def __str__(self) -> str:
        if not self.scores:
            return "No games played yet."
        parts = [f"{p}: {w}" for p, w in sorted(self.scores.items(), key=lambda x: -x[1])]
        return ", ".join(parts)
