import random
try:
    from neon_breach.puzzles.base import Puzzle
except ModuleNotFoundError:
    from puzzles.base import Puzzle

SYMBOLS = ["▲", "■", "◆", "●", "★", "✦"]
SYMBOL_NAMES = {
    "▲": "TRIANGLE",
    "■": "SQUARE",
    "◆": "DIAMOND",
    "●": "CIRCLE",
    "★": "STAR",
    "✦": "SPARK"
}

class PatternPuzzle(Puzzle):
    def __init__(self, difficulty: str = "CYBERPUNK"):
        super().__init__(difficulty)
        self.grid = []
        self.sub_type = ""
        self.anomaly_coord = (0, 0)
        self.missing_symbol = ""
        self.generate()

    def generate(self):
        self.sub_type = random.choice(["GRID_ANOMALY", "SYMBOL_MATRIX"])
        size = 3 if self.difficulty == "NOVICE" else 4

        if self.sub_type == "GRID_ANOMALY":
            self.title = "NEURAL MATRIX ANOMALY DETECTION"
            normal_sym = random.choice(SYMBOLS)
            anomaly_sym = random.choice([s for s in SYMBOLS if s != normal_sym])
            
            # Fill grid with normal symbol
            self.grid = [[normal_sym for _ in range(size)] for _ in range(size)]
            
            # Pick random anomaly row, col (0-indexed)
            r = random.randint(0, size - 1)
            c = random.randint(0, size - 1)
            self.grid[r][c] = anomaly_sym
            self.anomaly_coord = (r + 1, c + 1) # 1-indexed for user
            self.solution = f"{r + 1},{c + 1}"

            self.hints = [
                f"Scan each row from top to bottom. Find the coordinate with symbol '{anomaly_sym}'.",
                f"The corrupted signal is located in Row {self.anomaly_coord[0]}.",
                f"Format answer as 'Row,Col' e.g. '{self.anomaly_coord[0]},{self.anomaly_coord[1]}'."
            ]

        else: # SYMBOL_MATRIX
            self.title = "PATTERN RECOGNITION MATRIX SEQUENCER"
            seq_len = 3 if self.difficulty == "NOVICE" else 4
            pattern_syms = random.sample(SYMBOLS, seq_len)
            
            # Create repeating pattern grid
            flat_pattern = (pattern_syms * 5)[:size * size]
            missing_idx = random.randint(0, len(flat_pattern) - 1)
            self.missing_symbol = flat_pattern[missing_idx]
            
            flat_pattern[missing_idx] = "?"
            
            # Construct 2D grid
            self.grid = []
            for i in range(0, len(flat_pattern), size):
                self.grid.append(flat_pattern[i:i+size])

            self.solution = SYMBOL_NAMES.get(self.missing_symbol, self.missing_symbol)
            self.alt_solution = self.missing_symbol

            self.hints = [
                f"Observe the repeating symbol sequence: {' -> '.join(pattern_syms)}.",
                f"The missing symbol at '?' corresponds to '{self.solution}'.",
                f"Type the symbol character '{self.missing_symbol}' or name '{self.solution}'."
            ]

    def get_prompt(self) -> str:
        lines = [
            f"=== SECURITY NODE: {self.title} ===",
            "SCANNING NEURAL MATRIX NODES...",
            ""
        ]

        if self.sub_type == "GRID_ANOMALY":
            lines.append("  COLS ->  " + "  ".join([f"C{i+1}" for i in range(len(self.grid))]))
            for r_idx, row in enumerate(self.grid, 1):
                row_str = "   ".join(row)
                lines.append(f"  ROW R{r_idx} |  {row_str}")
            lines.append("")
            lines.append("COMMAND: Identify anomaly coordinate as 'ROW,COL' (e.g. '2,3').")

        else: # SYMBOL_MATRIX
            lines.append("  COLS ->  " + "  ".join([f"C{i+1}" for i in range(len(self.grid))]))
            for r_idx, row in enumerate(self.grid, 1):
                row_str = "   ".join(row)
                lines.append(f"  ROW R{r_idx} |  {row_str}")
            lines.append("")
            lines.append("AVAILABLE SYMBOLS: ▲ (TRIANGLE), ■ (SQUARE), ◆ (DIAMOND), ● (CIRCLE), ★ (STAR)")
            lines.append("COMMAND: Enter the missing symbol at '?' (symbol or name).")

        return "\n".join(lines)

    def evaluate(self, user_input: str) -> bool:
        cleaned = user_input.strip().upper().replace(" ", "")
        if self.sub_type == "GRID_ANOMALY":
            # Normalize user coordinate format (e.g. 2,3 or R2C3 or 2 3)
            cleaned = cleaned.replace("R", "").replace("C", "").replace(";", ",")
            return cleaned == self.solution
        else:
            sol_name = SYMBOL_NAMES.get(self.missing_symbol, "").upper()
            return cleaned == self.missing_symbol or cleaned == sol_name or cleaned == self.solution.upper()
