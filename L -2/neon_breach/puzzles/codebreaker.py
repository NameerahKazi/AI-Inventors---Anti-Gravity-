import random
try:
    from neon_breach.puzzles.base import Puzzle
except ModuleNotFoundError:
    from puzzles.base import Puzzle

class CodebreakerPuzzle(Puzzle):
    def __init__(self, difficulty: str = "CYBERPUNK"):
        super().__init__(difficulty)
        self.code_length = 4
        self.secret_code = ""
        self.attempts_history = []
        self.max_guesses = 6
        self.generate()

    def generate(self):
        self.title = "BLACK-ICE HEURISTIC PIN CODEBREAKER"
        if self.difficulty == "NOVICE":
            # 4 numeric digits
            digits = [str(i) for i in range(10)]
            self.secret_code = "".join(random.sample(digits, 4))
            char_set_desc = "Digits 0-9"
        elif self.difficulty == "CYBERPUNK":
            # 4 Hex characters
            hex_chars = "0123456789ABCDEF"
            self.secret_code = "".join(random.choices(hex_chars, k=4))
            char_set_desc = "Hexadecimal 0-9, A-F"
        else: # BLACK_ICE
            # 5 Hex characters
            self.code_length = 5
            hex_chars = "0123456789ABCDEF"
            self.secret_code = "".join(random.choices(hex_chars, k=5))
            char_set_desc = "Hexadecimal 0-9, A-F (5 Chars)"

        self.solution = self.secret_code

        self.hints = [
            f"Allowed characters: {char_set_desc}. Code length: {self.code_length} characters.",
            f"The secret code starts with character '{self.secret_code[0]}'.",
            f"The secret code ends with character '{self.secret_code[-1]}'."
        ]

    def get_prompt(self) -> str:
        lines = [
            f"=== SECURITY NODE: {self.title} ===",
            f"TARGET PIN LENGTH: {self.code_length} Characters",
            f"ATTEMPTS LOGGED  : {len(self.attempts_history)} / {self.max_guesses}",
            ""
        ]

        if self.attempts_history:
            lines.append("PREVIOUS HACK ATTEMPTS & FEEDBACK:")
            for idx, (guess, exact, partial) in enumerate(self.attempts_history, 1):
                lines.append(f"  [{idx}] Guess: {guess}  -> [ EXACT: {exact} | PARTIAL: {partial} ]")
            lines.append("")

        lines.append("COMMAND: Enter your 4-character PIN guess (or type 'hint').")
        return "\n".join(lines)

    def evaluate(self, user_input: str) -> bool:
        cleaned = user_input.strip().upper()
        if len(cleaned) != self.code_length:
            return False

        # Calculate exact and partial matches
        exact = 0
        partial = 0

        secret_unmatched = []
        guess_unmatched = []

        for g, s in zip(cleaned, self.secret_code):
            if g == s:
                exact += 1
            else:
                guess_unmatched.append(g)
                secret_unmatched.append(s)

        for g in guess_unmatched:
            if g in secret_unmatched:
                partial += 1
                secret_unmatched.remove(g)

        self.attempts_history.append((cleaned, exact, partial))
        return cleaned == self.secret_code
