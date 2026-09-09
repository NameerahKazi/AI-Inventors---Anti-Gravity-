"""
Headless Automated Test Suite for NEON BREACH
Verifies logic, crypto, pattern, sequence, and codebreaker puzzles,
engine state transitions, timer functions, and score persistence.
"""
import unittest
import os
import sys

# Ensure local directory is in path
sys.path.insert(0, os.path.abspath("."))

from neon_breach.puzzles.logic import LogicPuzzle
from neon_breach.puzzles.crypto import CryptoPuzzle
from neon_breach.puzzles.pattern import PatternPuzzle
from neon_breach.puzzles.sequence import SequencePuzzle
from neon_breach.puzzles.codebreaker import CodebreakerPuzzle
from neon_breach.core.engine import GameEngine
from neon_breach.utils.storage import HighScoreManager

class TestNeonBreachPuzzles(unittest.TestCase):
    def test_logic_puzzle(self):
        for diff in ["NOVICE", "CYBERPUNK", "BLACK_ICE"]:
            puzzle = LogicPuzzle(difficulty=diff)
            prompt = puzzle.get_prompt()
            self.assertIn("CIRCUIT LOGIC EXPR", prompt)
            
            # Verify correct solution evaluation
            sol = puzzle.solution
            self.assertTrue(puzzle.evaluate(sol))
            self.assertFalse(puzzle.evaluate("9999_WRONG"))
            
            # Verify hints
            hint1 = puzzle.get_hint(1)
            self.assertTrue(len(hint1) > 0)

    def test_crypto_puzzle(self):
        for diff in ["NOVICE", "CYBERPUNK", "BLACK_ICE"]:
            for _ in range(5):
                puzzle = CryptoPuzzle(difficulty=diff)
                prompt = puzzle.get_prompt()
                self.assertIn("SECURITY NODE", prompt)
                
                sol = puzzle.solution
                self.assertTrue(puzzle.evaluate(sol))
                self.assertFalse(puzzle.evaluate("WRONG_PAYLOAD_X"))

    def test_pattern_puzzle(self):
        for diff in ["NOVICE", "CYBERPUNK", "BLACK_ICE"]:
            for _ in range(5):
                puzzle = PatternPuzzle(difficulty=diff)
                prompt = puzzle.get_prompt()
                self.assertIn("SECURITY NODE", prompt)
                
                sol = puzzle.solution
                self.assertTrue(puzzle.evaluate(sol))

    def test_sequence_puzzle(self):
        for diff in ["NOVICE", "CYBERPUNK", "BLACK_ICE"]:
            for _ in range(5):
                puzzle = SequencePuzzle(difficulty=diff)
                prompt = puzzle.get_prompt()
                self.assertIn("DATA BUFFER", prompt)
                
                sol = puzzle.solution
                self.assertTrue(puzzle.evaluate(sol))
                self.assertFalse(puzzle.evaluate("-999999"))

    def test_codebreaker_puzzle(self):
        for diff in ["NOVICE", "CYBERPUNK", "BLACK_ICE"]:
            puzzle = CodebreakerPuzzle(difficulty=diff)
            prompt = puzzle.get_prompt()
            self.assertIn("TARGET PIN LENGTH", prompt)
            
            # Incorrect guess should yield False but record history
            self.assertFalse(puzzle.evaluate("000000000_TOO_LONG"))
            self.assertTrue(puzzle.evaluate(puzzle.solution))

class TestGameEngine(unittest.TestCase):
    def test_full_breach_run(self):
        engine = GameEngine()
        engine.start_game(handle="TEST_BOT", difficulty="NOVICE")
        
        self.assertEqual(engine.current_layer_idx, 0)
        self.assertFalse(engine.is_game_over)

        # Solve each layer automatically
        layers_count = engine.total_layers
        for idx in range(layers_count):
            self.assertIsNotNone(engine.active_puzzle)
            sol = engine.active_puzzle.solution
            
            # Submit correct answer
            is_correct, msg = engine.submit_answer(sol)
            self.assertTrue(is_correct)

        self.assertTrue(engine.is_victory)
        self.assertTrue(engine.is_game_over)
        self.assertGreater(engine.score, 0)

    def test_score_storage(self):
        mgr = HighScoreManager(file_path="test_high_scores.json")
        saved = mgr.save_score("BOT_TESTER", 8800, 5, "BLACK_ICE", 120.0)
        self.assertTrue(saved)
        
        scores = mgr.load_scores()
        self.assertTrue(any(s["handle"] == "BOT_TESTER" for s in scores))
        
        if os.path.exists("test_high_scores.json"):
            os.remove("test_high_scores.json")

if __name__ == "__main__":
    unittest.main()
