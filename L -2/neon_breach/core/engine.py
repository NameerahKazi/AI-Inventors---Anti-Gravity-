import time
import random
from typing import Tuple, Optional, Dict, Any

try:
    from neon_breach.puzzles.base import Puzzle
    from neon_breach.puzzles.logic import LogicPuzzle
    from neon_breach.puzzles.crypto import CryptoPuzzle
    from neon_breach.puzzles.pattern import PatternPuzzle
    from neon_breach.puzzles.sequence import SequencePuzzle
    from neon_breach.puzzles.codebreaker import CodebreakerPuzzle
except ModuleNotFoundError:
    from puzzles.base import Puzzle
    from puzzles.logic import LogicPuzzle
    from puzzles.crypto import CryptoPuzzle
    from puzzles.pattern import PatternPuzzle
    from puzzles.sequence import SequencePuzzle
    from puzzles.codebreaker import CodebreakerPuzzle

LAYER_TITLES = [
    ("LAYER 1: PERIMETER GATEWAY", "FIREWALL ICE INITIAL DEFENSE"),
    ("LAYER 2: NETWORK PROTOCOL MATRIX", "ENCRYPTED DATA ROUTING BUS"),
    ("LAYER 3: MAINFRAME RECURSIVE NODE", "NEURAL COGNITIVE MEMORY DUMP"),
    ("LAYER 4: AI SUB-ROUTINE CORE", "QUANTUM ALGORITHMIC LOCK"),
    ("LAYER 5: CENTRAL COMMAND BLACK-ICE", "SYSTEM ROOT EXECUTIVE KERNEL")
]

class GameEngine:
    def __init__(self):
        self.player_handle = "ANONYMOUS_RUNNER"
        self.difficulty = "CYBERPUNK"
        self.total_layers = 5
        self.current_layer_idx = 0
        
        self.integrity = 100
        self.trace_percent = 0
        self.score = 0
        self.time_limit_per_node = 60.0
        self.node_start_time = 0.0
        self.game_start_time = 0.0
        
        self.active_puzzle: Optional[Puzzle] = None
        self.hints_used_on_node = 0
        self.attempts_on_node = 0
        
        self.is_game_over = False
        self.is_victory = False

    def start_game(self, handle: str = "NETRUNNER_X", difficulty: str = "CYBERPUNK"):
        """Initialize new game state."""
        self.player_handle = handle if handle else "NETRUNNER_X"
        self.difficulty = difficulty.upper()
        self.current_layer_idx = 0
        self.integrity = 100
        self.trace_percent = 0
        self.score = 0
        self.is_game_over = False
        self.is_victory = False

        if self.difficulty == "NOVICE":
            self.total_layers = 4
            self.time_limit_per_node = 90.0
        elif self.difficulty == "BLACK_ICE":
            self.total_layers = 5
            self.time_limit_per_node = 45.0
        else: # CYBERPUNK
            self.total_layers = 5
            self.time_limit_per_node = 60.0

        self.game_start_time = time.time()
        self.load_layer_puzzle()

    def load_layer_puzzle(self):
        """Generate puzzle for the current security layer."""
        self.hints_used_on_node = 0
        self.attempts_on_node = 0
        self.node_start_time = time.time()

        # Map layer indices to puzzle classes, with randomization
        puzzle_classes = [LogicPuzzle, CryptoPuzzle, PatternPuzzle, SequencePuzzle, CodebreakerPuzzle]
        
        # Pick puzzle class based on layer index or shuffle for replayability
        puzzle_cls = puzzle_classes[self.current_layer_idx % len(puzzle_classes)]
        self.active_puzzle = puzzle_cls(difficulty=self.difficulty)

    def get_time_remaining(self) -> float:
        """Calculate seconds remaining for current node timer."""
        elapsed = time.time() - self.node_start_time
        remaining = self.time_limit_per_node - elapsed
        return max(0.0, remaining)

    def check_time_expiry(self) -> bool:
        """Check if time expired for current node."""
        if self.get_time_remaining() <= 0:
            self.trace_percent = 100
            self.is_game_over = True
            return True
        return False

    def submit_answer(self, user_input: str) -> Tuple[bool, str]:
        """Process player submission."""
        if self.is_game_over or not self.active_puzzle:
            return False, "SYSTEM OFFLINE."

        if self.check_time_expiry():
            return False, "TIME EXPIRED! SYSTEM TRACE REACHED 100%."

        self.attempts_on_node += 1
        is_correct = self.active_puzzle.evaluate(user_input)

        if is_correct:
            # Calculate node breach score
            time_left = self.get_time_remaining()
            time_bonus = int(time_left * 25)
            base_points = 1000 if self.difficulty == "NOVICE" else (1500 if self.difficulty == "CYBERPUNK" else 2500)
            hint_penalty = self.hints_used_on_node * 300
            
            node_score = max(200, base_points + time_bonus - hint_penalty)
            self.score += node_score
            
            # Reduce trace level slightly as reward
            self.trace_percent = max(0, self.trace_percent - 10)

            # Advance to next layer or trigger victory
            self.current_layer_idx += 1
            if self.current_layer_idx >= self.total_layers:
                self.is_victory = True
                self.is_game_over = True
                msg = f"BREACH SUCCESSFUL! Node pwned. Points earned: +{node_score}."
            else:
                self.load_layer_puzzle()
                msg = f"ACCESS GRANTED! Security Layer Breached. Points earned: +{node_score}."

            return True, msg
        else:
            # Wrong answer penalty
            trace_penalty = 15 if self.difficulty == "NOVICE" else (25 if self.difficulty == "CYBERPUNK" else 35)
            self.trace_percent += trace_penalty
            self.integrity -= 15

            if self.trace_percent >= 100 or self.integrity <= 0:
                self.trace_percent = 100
                self.integrity = 0
                self.is_game_over = True
                msg = f"ACCESS DENIED! Security countermeasure triggered. TRACE LEVEL: {self.trace_percent}%."
            else:
                msg = f"ACCESS DENIED! Invalid payload. TRACE INCREASED +{trace_penalty}% (Total: {self.trace_percent}%)."

            return False, msg

    def request_hint(self) -> Tuple[bool, str]:
        """Request a progressive hint."""
        if not self.active_puzzle:
            return False, "NO ACTIVE NODE."

        if self.hints_used_on_node >= 3:
            return False, "DIAGNOSTIC LIMIT REACHED: Maximum hints already used for this node."

        self.hints_used_on_node += 1
        hint_text = self.active_puzzle.get_hint(self.hints_used_on_node)
        
        # Hint penalty: slight trace increase
        self.trace_percent = min(99, self.trace_percent + 5)
        self.score = max(0, self.score - 150)
        
        return True, f"DIAGNOSTIC HINT #{self.hints_used_on_node}: {hint_text}"

    def get_layer_title(self) -> Tuple[str, str]:
        """Get title and subtitle for current layer."""
        if self.current_layer_idx < len(LAYER_TITLES):
            return LAYER_TITLES[self.current_layer_idx]
        return (f"LAYER {self.current_layer_idx + 1}: CORE NODE", "ICE DEFENSE MATRIX")
