import random
try:
    from neon_breach.puzzles.base import Puzzle
except ModuleNotFoundError:
    from puzzles.base import Puzzle

class SequencePuzzle(Puzzle):
    def __init__(self, difficulty: str = "CYBERPUNK"):
        super().__init__(difficulty)
        self.sequence = []
        self.rule_desc = ""
        self.sub_type = ""
        self.generate()

    def generate(self):
        modes = ["MULTIPLIER", "ALTERNATING", "FIBONACCI_VAR", "PRIMES"]
        if self.difficulty == "NOVICE":
            modes = ["MULTIPLIER", "ALTERNATING"]
            
        self.sub_type = random.choice(modes)

        if self.sub_type == "MULTIPLIER":
            self.title = "NUMERICAL PROGRESSION FREQUENCY SYNC"
            start = random.randint(2, 7)
            mult = random.randint(2, 4)
            offset = random.randint(0, 3)
            
            seq = [start]
            for _ in range(4):
                seq.append(seq[-1] * mult + offset)
            
            self.sequence = seq
            self.solution = str(seq[-1] * mult + offset)
            self.rule_desc = f"Multiply by {mult} and add {offset}"
            
            self.hints = [
                f"Examine the ratio between consecutive numbers.",
                f"Rule: Each step is calculated as (Previous * {mult}) + {offset}.",
                f"Calculation: ({seq[-1]} * {mult}) + {offset} = {self.solution}."
            ]

        elif self.sub_type == "ALTERNATING":
            self.title = "DUAL-OPERATOR BUS SEQUENCE"
            start = random.randint(10, 30)
            op1 = random.randint(5, 12)
            op2 = random.randint(2, 6)
            
            seq = [start]
            for i in range(4):
                if i % 2 == 0:
                    seq.append(seq[-1] + op1)
                else:
                    seq.append(seq[-1] - op2)

            self.sequence = seq
            # Next operation alternates
            next_val = seq[-1] + op1 if len(seq) % 2 == 1 else seq[-1] - op2
            self.solution = str(next_val)
            self.rule_desc = f"Alternate (+{op1}) and (-{op2})"

            self.hints = [
                "Notice the alternating pattern: value increases, then decreases.",
                f"Step 1 adds +{op1}, Step 2 subtracts -{op2}.",
                f"Apply the next step operator to {seq[-1]}."
            ]

        elif self.sub_type == "FIBONACCI_VAR":
            self.title = "FIBONACCI RECURSIVE DATA BUFFER"
            a, b = random.randint(1, 4), random.randint(2, 5)
            seq = [a, b]
            for _ in range(4):
                seq.append(seq[-1] + seq[-2])
            
            self.sequence = seq
            self.solution = str(seq[-1] + seq[-2])
            self.rule_desc = "Each number is the sum of the preceding two numbers"

            self.hints = [
                "Each value is generated from the previous two terms.",
                f"Sum of last two terms: {seq[-2]} + {seq[-1]}.",
                f"Target value = {seq[-2] + seq[-1]}."
            ]

        else: # PRIMES
            self.title = "PRIME NUMBER CLUSTER DECRYPTION"
            primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59]
            start_idx = random.randint(0, len(primes) - 6)
            sub_primes = primes[start_idx : start_idx + 5]
            
            self.sequence = sub_primes
            self.solution = str(primes[start_idx + 5])
            self.rule_desc = "Sequential prime numbers"

            self.hints = [
                "These numbers cannot be divided evenly by any number except 1 and themselves.",
                "This is a sequence of consecutive prime numbers.",
                f"The next prime number after {sub_primes[-1]} is {self.solution}."
            ]

    def get_prompt(self) -> str:
        seq_str = ",  ".join([str(x) for x in self.sequence])
        lines = [
            f"=== SECURITY NODE: {self.title} ===",
            "ANALYZE DATA STREAM SEQUENCE:",
            "",
            f"  DATA BUFFER : [  {seq_str},  ???  ]",
            "",
            "COMMAND: Compute and enter the next missing number in the sequence."
        ]
        return "\n".join(lines)

    def evaluate(self, user_input: str) -> bool:
        cleaned = user_input.strip()
        return cleaned == self.solution
