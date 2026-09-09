import json
import os
from typing import List, Dict, Any

SCORE_FILE = "high_scores.json"

class HighScoreManager:
    def __init__(self, file_path: str = SCORE_FILE):
        self.file_path = file_path

    def load_scores(self) -> List[Dict[str, Any]]:
        """Load high scores from JSON storage."""
        if not os.path.exists(self.file_path):
            return self._default_scores()
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return sorted(data, key=lambda x: x.get("score", 0), reverse=True)
        except Exception:
            return self._default_scores()

    def save_score(self, handle: str, score: int, layers_breached: int, difficulty: str, time_taken: float) -> bool:
        """Save a new score entry."""
        scores = self.load_scores()
        entry = {
            "handle": handle[:16] if handle else "UNKNOWN_RUNNER",
            "score": score,
            "layers": layers_breached,
            "difficulty": difficulty,
            "time_taken": round(time_taken, 1)
        }
        scores.append(entry)
        # Keep top 10 scores
        scores = sorted(scores, key=lambda x: x.get("score", 0), reverse=True)[:10]
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(scores, f, indent=2)
            return True
        except Exception:
            return False

    def _default_scores(self) -> List[Dict[str, Any]]:
        """Return dummy leaderboard if no file exists yet."""
        return [
            {"handle": "NEO_GHOST", "score": 9500, "layers": 5, "difficulty": "BLACK_ICE", "time_taken": 184.2},
            {"handle": "CYBER_VIXEN", "score": 7800, "layers": 5, "difficulty": "CYBERPUNK", "time_taken": 210.5},
            {"handle": "NULL_POINTER", "score": 6200, "layers": 4, "difficulty": "CYBERPUNK", "time_taken": 195.0},
            {"handle": "ZERO_COOL", "score": 4500, "layers": 3, "difficulty": "NOVICE", "time_taken": 140.8},
            {"handle": "ACID_BURN", "score": 3100, "layers": 2, "difficulty": "NOVICE", "time_taken": 90.0}
        ]
