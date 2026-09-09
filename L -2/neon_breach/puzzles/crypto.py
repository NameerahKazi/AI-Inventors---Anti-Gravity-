import random
import base64
import hashlib
import string
try:
    from neon_breach.puzzles.base import Puzzle
except ModuleNotFoundError:
    from puzzles.base import Puzzle

CYBER_WORDS = [
    "NEON", "BREACH", "MATRIX", "FIREWALL", "MAINFRAME", "NETRUNNER", 
    "CYBER", "OVERRIDE", "PROTOCOL", "GRID", "QUANTUM", "TERMINAL",
    "DECRYPTION", "PAYLOAD", "KEYLOGGER", "BACKDOOR", "CIPHER"
]

class CryptoPuzzle(Puzzle):
    def __init__(self, difficulty: str = "CYBERPUNK"):
        super().__init__(difficulty)
        self.sub_type = ""
        self.ciphertext = ""
        self.extra_info = ""
        self.generate()

    def generate(self):
        modes = ["CAESAR", "BASE64", "HEX_CONVERT", "HASH_MATCH"]
        if self.difficulty == "NOVICE":
            modes = ["CAESAR", "BASE64", "HEX_CONVERT"]
            
        self.sub_type = random.choice(modes)
        
        if self.sub_type == "CAESAR":
            self.title = "CAESAR SHIFT CIPHER DECRYPTION"
            word = random.choice(CYBER_WORDS)
            shift = random.randint(1, 10)
            self.solution = word
            
            # Encrypt word with shift
            encrypted = []
            for ch in word:
                if ch in string.ascii_uppercase:
                    new_idx = (ord(ch) - ord('A') + shift) % 26
                    encrypted.append(chr(ord('A') + new_idx))
                else:
                    encrypted.append(ch)
            self.ciphertext = "".join(encrypted)
            self.extra_info = f"Shift Offset: +{shift}"
            
            self.hints = [
                f"Shift each letter BACKWARDS by {shift} positions in the alphabet.",
                f"First letter '{self.ciphertext[0]}' shifted back by {shift} becomes '{self.solution[0]}'.",
                f"Full plain-text keyword length is {len(self.solution)} letters."
            ]

        elif self.sub_type == "BASE64":
            self.title = "BASE64 PAYLOAD DECODE"
            word = random.choice(CYBER_WORDS)
            self.solution = word
            encoded_bytes = base64.b64encode(word.encode('ascii'))
            self.ciphertext = encoded_bytes.decode('ascii')
            self.extra_info = "Format: Standard ASCII Base64"
            
            self.hints = [
                "Base64 uses A-Z, a-z, 0-9, +, and / characters with '=' padding.",
                f"The decoded string is a common cyberpunk terms keyword starting with '{word[0]}'.",
                f"Word length: {len(word)} characters."
            ]

        elif self.sub_type == "HEX_CONVERT":
            self.title = "HEXADECIMAL TO DECIMAL DATA CONVERSION"
            val = random.randint(64, 4095)
            self.ciphertext = f"0x{val:X}"
            self.solution = str(val)
            self.extra_info = "Convert Hexadecimal value to Decimal integer."
            
            self.hints = [
                "Hexadecimal base 16: A=10, B=11, C=12, D=13, E=14, F=15.",
                f"Formula: Multiply first digit by power of 16. Higher byte = {val // 16}.",
                f"The number is between {val - 10} and {val + 10}."
            ]

        else: # HASH_MATCH
            self.title = "SHA-256 HASH CHECKSUM REVERSE SEARCH"
            candidates = random.sample(CYBER_WORDS, 4)
            target = random.choice(candidates)
            self.solution = target
            
            target_hash = hashlib.sha256(target.encode('utf-8')).hexdigest()[:16]
            self.ciphertext = target_hash.upper()
            self.candidates = candidates
            self.extra_info = f"Target SHA-256 Digest (truncated): {self.ciphertext}"
            
            self.hints = [
                f"Compute the SHA-256 hash prefix for each of the 4 candidate keywords.",
                f"The target keyword starts with letter '{target[0]}'.",
                f"Keyword length is {len(target)} characters."
            ]

    def get_prompt(self) -> str:
        lines = [
            f"=== SECURITY NODE: {self.title} ===",
            f"ENCRYPTED PAYLOAD : {self.ciphertext}",
            f"DIAGNOSTIC NOTICE : {self.extra_info}",
            ""
        ]
        if self.sub_type == "HASH_MATCH":
            lines.append("CANDIDATE KEYWORDS:")
            for idx, cand in enumerate(self.candidates, 1):
                lines.append(f"  [{idx}] {cand}")
            lines.append("")
            lines.append("COMMAND: Enter the matching keyword (or option 1-4).")
        else:
            lines.append("COMMAND: Enter the decrypted plain-text solution payload.")
        return "\n".join(lines)

    def evaluate(self, user_input: str) -> bool:
        cleaned = user_input.strip().upper()
        if self.sub_type == "HASH_MATCH":
            if cleaned.isdigit():
                idx = int(cleaned) - 1
                if 0 <= idx < len(self.candidates):
                    return self.candidates[idx] == self.solution
        return cleaned == self.solution.upper()
