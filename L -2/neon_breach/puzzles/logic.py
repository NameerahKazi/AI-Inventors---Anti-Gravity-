import random
try:
    from neon_breach.puzzles.base import Puzzle
except ModuleNotFoundError:
    from puzzles.base import Puzzle

class LogicPuzzle(Puzzle):
    def __init__(self, difficulty: str = "CYBERPUNK"):
        super().__init__(difficulty)
        self.title = "LOGIC GATE CIRCUIT EVALUATION"
        self.inputs = {}
        self.expression_str = ""
        self.solution_bool = False
        self.generate()

    def generate(self):
        # Choose difficulty parameters
        gate_depth = 2 if self.difficulty == "NOVICE" else (3 if self.difficulty == "CYBERPUNK" else 4)
        
        # Available variables
        var_names = ["SIG_A", "SIG_B", "SIG_C", "SIG_D", "SIG_E"][:gate_depth + 1]
        self.inputs = {var: random.choice([True, False]) for var in var_names}

        # Operators
        ops = ["AND", "OR", "XOR", "NAND", "NOR"]

        # Build random expression tree
        if gate_depth == 2:
            op1 = random.choice(["AND", "OR", "XOR"])
            op2 = random.choice(["AND", "OR", "XOR"])
            v1, v2, v3 = var_names[:3]
            self.expression_str = f"({v1} {op1} {v2}) {op2} {v3}"
        elif gate_depth == 3:
            op1 = random.choice(ops)
            op2 = random.choice(ops)
            op3 = random.choice(ops)
            v1, v2, v3, v4 = var_names[:4]
            self.expression_str = f"({v1} {op1} {v2}) {op3} ({v3} {op2} {v4})"
        else: # BLACK_ICE
            op1 = random.choice(ops)
            op2 = random.choice(ops)
            op3 = random.choice(ops)
            op4 = random.choice(ops)
            v1, v2, v3, v4, v5 = var_names[:5]
            self.expression_str = f"((NOT {v1} {op1} {v2}) {op2} {v3}) {op3} ({v4} {op4} {v5})"

        # Evaluate expression
        self.solution_bool = self._eval_expr(self.expression_str, self.inputs)
        self.solution = "1" if self.solution_bool else "0"

        # Hints
        input_desc = ", ".join([f"{k}={'1' if v else '0'}" for k, v in self.inputs.items()])
        self.hints = [
            f"Input signals detected: {input_desc}.",
            f"Remember boolean rules: XOR is true ONLY when inputs differ. NAND is NOT(AND).",
            f"Break expression into sub-gates first before combining with outer operator."
        ]

    def _eval_expr(self, expr: str, vals: dict) -> bool:
        """Safe evaluation of boolean gate string."""
        s = expr
        for k, v in vals.items():
            s = s.replace(k, str(v))
        
        # Replace custom logic operators with Python equivalents
        # Need to handle NAND and NOR specially
        # To avoid partial string collisions, replace NAND/NOR first
        s = s.replace("NAND", "nand_op")
        s = s.replace("NOR", "nor_op")
        s = s.replace("XOR", "^")
        s = s.replace("AND", "and")
        s = s.replace("OR", "or")
        s = s.replace("NOT", "not ")
        
        # We can implement helper functions in scope for eval
        def nand_op(a, b):
            return not (a and b)
        def nor_op(a, b):
            return not (a or b)

        eval_scope = {"True": True, "False": False, "nand_op": nand_op, "nor_op": nor_op}
        try:
            res = eval(s, {"__builtins__": None}, eval_scope)
            return bool(res)
        except Exception:
            return False

    def get_prompt(self) -> str:
        prompt_lines = [
            f"=== SECURITY NODE: {self.title} ===",
            "Analyze the signal input lines and compute the FINAL GATE OUTPUT (1 or 0).",
            "",
            "INPUT SIGNALS:"
        ]
        for k, v in self.inputs.items():
            val_str = "1 (HIGH)" if v else "0 (LOW)"
            prompt_lines.append(f"  └─ {k:<8} : {val_str}")
        
        prompt_lines.append("")
        prompt_lines.append(f"CIRCUIT LOGIC EXPR : {self.expression_str}")
        prompt_lines.append("")
        prompt_lines.append("COMMAND: Submit final output as '1' or '0' (or TRUE / FALSE).")
        return "\n".join(prompt_lines)

    def evaluate(self, user_input: str) -> bool:
        cleaned = user_input.strip().upper()
        if cleaned in ["1", "TRUE", "HIGH", "T"]:
            ans = "1"
        elif cleaned in ["0", "FALSE", "LOW", "F"]:
            ans = "0"
        else:
            ans = cleaned
        return ans == self.solution
