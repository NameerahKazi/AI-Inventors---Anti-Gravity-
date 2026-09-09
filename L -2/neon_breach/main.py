import sys
import os

# Add parent directory to sys.path so 'neon_breach' package is always importable
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import time
try:
    from neon_breach.core.terminal import Terminal, Colors
    from neon_breach.core.engine import GameEngine
    from neon_breach.utils.storage import HighScoreManager
except ModuleNotFoundError:
    from core.terminal import Terminal, Colors
    from core.engine import GameEngine
    from utils.storage import HighScoreManager

class NeonBreachApp:
    def __init__(self):
        self.term = Terminal(anim_speed=0.012)
        self.engine = GameEngine()
        self.scores_mgr = HighScoreManager()
        self.player_handle = "NETRUNNER_X"
        self.difficulty = "CYBERPUNK"

    def run(self):
        """Main application lifecycle loop."""
        while True:
            self.term.clear()
            self.term.print_header()
            self.show_main_menu()

            choice = input(f"{Colors.BRIGHT_CYAN}SYSTEM_SELECT> {Colors.RESET}").strip()

            if choice == "1":
                self.configure_runner_handle()
                self.play_game_loop()
            elif choice == "2":
                self.show_intel_briefing()
            elif choice == "3":
                self.show_leaderboard()
            elif choice == "4":
                self.configure_difficulty()
            elif choice == "5":
                self.toggle_text_speed()
            elif choice in ["6", "exit", "quit", "q"]:
                self.term.print_typed("TERMINATING NEURAL LINK... GOODBYE RUNNER.", Colors.BRIGHT_RED)
                break
            else:
                self.term.print("INVALID SYSTEM COMMAND.", Colors.BRIGHT_RED)
                time.sleep(0.8)

    def show_main_menu(self):
        """Render main terminal menu options."""
        menu_lines = [
            f"{Colors.BOLD}[1] INFILTRATE MAINFRAME{Colors.RESET}   : Initiate System Breach Run",
            f"{Colors.BOLD}[2] INTEL BRIEFING{Colors.RESET}        : Operations Manual & Lore",
            f"{Colors.BOLD}[3] HALL OF FAME{Colors.RESET}          : High Breach Records",
            f"{Colors.BOLD}[4] SECURITY SEVERITY{Colors.RESET}     : [{Colors.BRIGHT_YELLOW}{self.difficulty}{Colors.RESET}]",
            f"{Colors.BOLD}[5] TERMINAL SPEED{Colors.RESET}        : [{'FAST' if self.term.fast_mode else 'ANIMATED'}]",
            f"{Colors.BOLD}[6] TERMINATE LINK{Colors.RESET}        : Disconnect Neural Deck"
        ]
        self.term.draw_box("NEON BREACH // MAIN INTERFACE", menu_lines, width=68, color=Colors.BRIGHT_CYAN)
        self.term.print()

    def configure_runner_handle(self):
        """Prompt runner for callsign handle."""
        self.term.clear()
        self.term.print_header()
        self.term.print_typed("IDENTIFICATION REQUIRED FOR NETWORK ACCESS LOGS.", Colors.BRIGHT_CYAN)
        val = input(f"{Colors.BRIGHT_YELLOW}ENTER NETRUNNER CALLSIGN [{self.player_handle}]: {Colors.RESET}").strip().upper()
        if val:
            self.player_handle = val.replace(" ", "_")[:16]

    def configure_difficulty(self):
        """Difficulty selection interface."""
        self.term.clear()
        self.term.print_header()
        lines = [
            f"[1] NOVICE    : 4 Security Layers | 90s Timer | Low Trace Penalties",
            f"[2] CYBERPUNK : 5 Security Layers | 60s Timer | Standard Penalties (Recommended)",
            f"[3] BLACK_ICE : 5 Security Layers | 45s Timer | Extreme Trace & Hard Puzzles"
        ]
        self.term.draw_box("SELECT SECURITY MATRIX SEVERITY", lines, width=72, color=Colors.BRIGHT_YELLOW)
        sel = input(f"{Colors.BRIGHT_YELLOW}SELECT SEVERITY (1-3): {Colors.RESET}").strip()
        if sel == "1":
            self.difficulty = "NOVICE"
        elif sel == "3":
            self.difficulty = "BLACK_ICE"
        else:
            self.difficulty = "CYBERPUNK"
        self.term.print_typed(f"SECURITY SEVERITY SET TO: {self.difficulty}", Colors.BRIGHT_GREEN)
        time.sleep(1)

    def toggle_text_speed(self):
        """Toggle fast mode typing animations."""
        self.term.fast_mode = not self.term.fast_mode
        status = "FAST INSTANT MODE" if self.term.fast_mode else "CYBERPUNK ANIMATED TYPEWRITER"
        self.term.print_typed(f"TERMINAL DISPLAY MODE SWITCHED TO: {status}", Colors.BRIGHT_GREEN)
        time.sleep(1)

    def show_intel_briefing(self):
        """Display game lore & instructions."""
        self.term.clear()
        self.term.print_header()
        lore = [
            "OPERATION: NEON BREACH",
            "----------------------",
            "You are a rogue Netrunner attempting to breach Arasaka-Orbital's central ICE.",
            "Each security node presents a procedurally generated cipher or logic challenge.",
            "",
            "SYSTEM STATUS METRICS:",
            "  • TRACE LEVEL  : If trace reaches 100%, Black-ICE will locate and fry your neural deck.",
            "  • INTEGRITY    : Represents system stability. Incorrect hack payloads degrade integrity.",
            "  • TIMER        : Each node is monitored by an automated countdown sequence.",
            "",
            "AVAILABLE IN-GAME COMMANDS:",
            "  • <payload>    : Type your hack payload solution directly to submit.",
            "  • hint / diag  : Request a diagnostic hint (cost: slight score/trace penalty).",
            "  • scan         : Re-examine current node status and puzzle prompt.",
            "  • status       : View runner statistics.",
            "  • abort        : Sever neural connection and escape run."
        ]
        self.term.draw_box("NETRUNNER INTEL MANUAL", lore, width=76, color=Colors.BRIGHT_CYAN)
        input(f"\n{Colors.BRIGHT_CYAN}PRESS ENTER TO RETURN TO MAIN TERMINAL...{Colors.RESET}")

    def show_leaderboard(self):
        """Display high score record tables."""
        self.term.clear()
        self.term.print_header()
        scores = self.scores_mgr.load_scores()
        lines = [
            f"{'RANK':<5} | {'RUNNER HANDLE':<16} | {'SCORE':<8} | {'LAYERS':<6} | {'DIFFICULTY':<10} | {'TIME'}"
        ]
        lines.append("─" * 68)
        for idx, entry in enumerate(scores, 1):
            line = f"#{idx:<4} | {entry['handle']:<16} | {entry['score']:<8} | {entry['layers']:<6} | {entry['difficulty']:<10} | {entry['time_taken']}s"
            lines.append(line)
        self.term.draw_box("MAINFRAME BREACH HALL OF FAME", lines, width=74, color=Colors.BRIGHT_MAGENTA)
        input(f"\n{Colors.BRIGHT_CYAN}PRESS ENTER TO RETURN TO MAIN TERMINAL...{Colors.RESET}")

    def render_hud(self):
        """Render top status bar frame."""
        time_rem = self.engine.get_time_remaining()
        time_color = Colors.BRIGHT_GREEN if time_rem > 20 else (Colors.BRIGHT_YELLOW if time_rem > 10 else Colors.BRIGHT_RED)
        trace_color = Colors.BRIGHT_GREEN if self.engine.trace_percent < 50 else (Colors.BRIGHT_YELLOW if self.engine.trace_percent < 85 else Colors.BRIGHT_RED)
        
        hud_str = (
            f"RUNNER: {Colors.BRIGHT_CYAN}{self.engine.player_handle:<12}{Colors.RESET} | "
            f"LAYER: {Colors.BOLD}{self.engine.current_layer_idx + 1}/{self.engine.total_layers}{Colors.RESET} | "
            f"TRACE: {trace_color}{self.engine.trace_percent:>3}%{Colors.RESET} | "
            f"TIME: {time_color}{time_rem:>4.1f}s{Colors.RESET} | "
            f"SCORE: {Colors.BRIGHT_YELLOW}{self.engine.score}{Colors.RESET}"
        )
        print(f"\n┌─[ {Colors.BOLD}SYSTEM MONITOR HUD{Colors.RESET} ]" + "─" * 45 + "┐")
        print(f"│ {hud_str} │")
        print("└" + "─" * 68 + "┘\n")

    def play_game_loop(self):
        """Primary interactive gameplay loop."""
        self.engine.start_game(handle=self.player_handle, difficulty=self.difficulty)
        
        self.term.clear()
        self.term.print_typed("INITIATING NEURAL INTERFACE LINK...", Colors.BRIGHT_CYAN)
        self.term.glitch_effect("CONNECTING TO PERIMETER GATEWAY ICE...", duration=0.3)
        time.sleep(0.5)

        while not self.engine.is_game_over:
            self.term.clear()
            self.render_hud()
            
            layer_title, layer_sub = self.engine.get_layer_title()
            self.term.print(f"[{Colors.BRIGHT_MAGENTA}{layer_title}{Colors.RESET} // {layer_sub}]")
            self.term.print("-" * 70, Colors.BRIGHT_CYAN)

            # Check time expiry before rendering
            if self.engine.check_time_expiry():
                break

            # Render active puzzle prompt
            prompt_text = self.engine.active_puzzle.get_prompt()
            print(prompt_text)
            print("-" * 70)

            user_cmd = input(f"\n{Colors.BRIGHT_GREEN}NEON-SHELL> {Colors.RESET}").strip()

            if not user_cmd:
                continue

            cmd_lower = user_cmd.lower()

            if cmd_lower in ["hint", "diag", "diagnostic"]:
                success, hint_msg = self.engine.request_hint()
                if success:
                    self.term.print(f"\n[DIAGNOSTIC OUTPUT] {hint_msg}", Colors.BRIGHT_YELLOW)
                else:
                    self.term.print(f"\n[DIAGNOSTIC ERROR] {hint_msg}", Colors.BRIGHT_RED)
                input("\nPRESS ENTER TO CONTINUE...")

            elif cmd_lower in ["scan", "status"]:
                continue # Loop re-renders screen

            elif cmd_lower in ["help", "?"]:
                self.term.print("\nCOMMAND HELP: Type your solution payload directly, or 'hint', 'scan', 'abort'.", Colors.BRIGHT_CYAN)
                input("\nPRESS ENTER TO CONTINUE...")

            elif cmd_lower in ["abort", "exit", "quit"]:
                self.term.print_typed("ABORTING BREACH RUN. CONNECTION SEVERED.", Colors.BRIGHT_RED)
                self.engine.is_game_over = True
                break

            else:
                # Treat command input as hack submission
                # Strip 'hack ' prefix if user typed 'hack <answer>'
                if cmd_lower.startswith("hack "):
                    payload = user_cmd[5:].strip()
                else:
                    payload = user_cmd

                is_correct, feedback = self.engine.submit_answer(payload)
                
                if is_correct:
                    self.term.sound_fx("SUCCESS")
                    self.term.print_typed(feedback, Colors.BRIGHT_GREEN)
                    time.sleep(1.2)
                else:
                    self.term.sound_fx("WARNING")
                    self.term.print_typed(feedback, Colors.BRIGHT_RED)
                    time.sleep(1.5)

        # Game Over / Victory Handling
        self.handle_game_completion()

    def handle_game_completion(self):
        """Display victory or defeat screens and process high scores."""
        self.term.clear()
        total_time = time.time() - self.engine.game_start_time

        if self.engine.is_victory:
            self.term.print_victory_banner()
            self.term.print_typed(f"\nCONGRATULATIONS RUNNER {self.engine.player_handle}!", Colors.BRIGHT_GREEN)
            self.term.print_typed(f"ALL SECURITY LAYERS PWNED IN {total_time:.1f} SECONDS.", Colors.BRIGHT_CYAN)
            self.term.print_typed(f"FINAL OVERRIDE SCORE: {self.engine.score} PTS", Colors.BRIGHT_YELLOW)
            
            # Save score
            saved = self.scores_mgr.save_score(
                handle=self.engine.player_handle,
                score=self.engine.score,
                layers_breached=self.engine.current_layer_idx,
                difficulty=self.difficulty,
                time_taken=total_time
            )
            if saved:
                self.term.print("\n>>> RECORD LOGGED TO MAINFRAME HALL OF FAME <<<", Colors.BRIGHT_MAGENTA)

        else:
            self.term.print_game_over_banner()
            self.term.print_typed(f"\nLINK FLATLINED! TRACE LEVEL REACHED {self.engine.trace_percent}%.", Colors.BRIGHT_RED)
            self.term.print_typed(f"LAYERS BREACHED: {self.engine.current_layer_idx} / {self.engine.total_layers}", Colors.BRIGHT_YELLOW)
            self.term.print_typed(f"ACCUMULATED SCORE: {self.engine.score} PTS", Colors.BRIGHT_CYAN)

        input(f"\n{Colors.BRIGHT_CYAN}PRESS ENTER TO RETURN TO MAIN TERMINAL MENU...{Colors.RESET}")

def main():
    app = NeonBreachApp()
    app.run()

if __name__ == "__main__":
    main()
