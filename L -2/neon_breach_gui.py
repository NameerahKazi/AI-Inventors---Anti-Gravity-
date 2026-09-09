"""
=========================================================
 NEON BREACH // Python Cyberpunk Escape-Room Visual GUI
 Standard Library Tkinter Graphical Application
=========================================================
"""
import sys
import os
import time
import random
import json
import tkinter as tk
from tkinter import messagebox

# Add local path for engine & puzzles import
sys.path.insert(0, os.path.abspath("."))

try:
    from neon_breach.core.engine import GameEngine
    from neon_breach.utils.storage import HighScoreManager
except ModuleNotFoundError:
    from core.engine import GameEngine
    from utils.storage import HighScoreManager

COLOR_BG = "#080911"
COLOR_PANEL = "#0d111e"
COLOR_CYAN = "#00f3ff"
COLOR_MAGENTA = "#ff0055"
COLOR_GREEN = "#00ff66"
COLOR_YELLOW = "#ffb700"
COLOR_RED = "#ff2a2a"
COLOR_TEXT = "#e0f7fc"
COLOR_DIM = "#7a8b9e"

class NeonBreachGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NEON BREACH // Cyberpunk Graphical Escape-Room")
        self.geometry("1024x720")
        self.configure(bg=COLOR_BG)
        self.resizable(True, True)

        self.engine = GameEngine()
        self.scores_mgr = HighScoreManager()
        self.runner_handle = "NEO_RUNNER"
        self.difficulty = "CYBERPUNK"
        self.timer_active = False

        self.create_widgets()
        self.show_start_screen()

    def create_widgets(self):
        # Top HUD Status Bar
        self.hud_frame = tk.Frame(self, bg=COLOR_PANEL, bd=1, relief="ridge", highlightbackground=COLOR_CYAN, highlightthickness=1)
        self.hud_frame.pack(fill="x", padx=12, pady=10)

        self.lbl_title = tk.Label(self.hud_frame, text="NEON BREACH", font=("Orbitron", 18, "bold"), fg=COLOR_CYAN, bg=COLOR_PANEL)
        self.lbl_title.pack(side="left", padx=15, pady=8)

        self.metrics_frame = tk.Frame(self.hud_frame, bg=COLOR_PANEL)
        self.metrics_frame.pack(side="right", padx=15)

        self.lbl_runner = tk.Label(self.metrics_frame, text="RUNNER: NEO_RUNNER", font=("Consolas", 10, "bold"), fg=COLOR_CYAN, bg=COLOR_PANEL)
        self.lbl_runner.grid(row=0, column=0, padx=10)

        self.lbl_integrity = tk.Label(self.metrics_frame, text="INTEGRITY: 100 HP", font=("Consolas", 10, "bold"), fg=COLOR_GREEN, bg=COLOR_PANEL)
        self.lbl_integrity.grid(row=0, column=1, padx=10)

        self.lbl_trace = tk.Label(self.metrics_frame, text="TRACE: 0%", font=("Consolas", 10, "bold"), fg=COLOR_RED, bg=COLOR_PANEL)
        self.lbl_trace.grid(row=0, column=2, padx=10)

        self.lbl_timer = tk.Label(self.metrics_frame, text="TIME: 60.0s", font=("Consolas", 10, "bold"), fg=COLOR_YELLOW, bg=COLOR_PANEL)
        self.lbl_timer.grid(row=0, column=3, padx=10)

        self.lbl_score = tk.Label(self.metrics_frame, text="SCORE: 0", font=("Consolas", 10, "bold"), fg=COLOR_MAGENTA, bg=COLOR_PANEL)
        self.lbl_score.grid(row=0, column=4, padx=10)

        # Node Navigation Bar
        self.nodes_frame = tk.Frame(self, bg=COLOR_PANEL, bd=1, relief="ridge")
        self.nodes_frame.pack(fill="x", padx=12, pady=5)
        self.node_labels = []
        for i in range(5):
            lbl = tk.Label(self.nodes_frame, text=f" NODE 0{i+1} ", font=("Orbitron", 9, "bold"), fg=COLOR_DIM, bg=COLOR_PANEL, relief="flat", padx=15, pady=6)
            lbl.pack(side="left", expand=True)
            self.node_labels.append(lbl)

        # Main Stage Container
        self.stage_frame = tk.Frame(self, bg=COLOR_PANEL, bd=1, relief="ridge", highlightbackground=COLOR_CYAN, highlightthickness=1)
        self.stage_frame.pack(fill="both", expand=True, padx=12, pady=10)

        self.lbl_puzzle_title = tk.Label(self.stage_frame, text="SYSTEM READY", font=("Orbitron", 14, "bold"), fg=COLOR_CYAN, bg=COLOR_PANEL)
        self.lbl_puzzle_title.pack(pady=10)

        self.lbl_puzzle_sub = tk.Label(self.stage_frame, text="Initiate neural infiltration sequence.", font=("Consolas", 10), fg=COLOR_DIM, bg=COLOR_PANEL)
        self.lbl_puzzle_sub.pack(pady=2)

        # Interactive Content Area
        self.content_area = tk.Frame(self.stage_frame, bg="#04060c", bd=1, relief="sunken")
        self.content_area.pack(fill="both", expand=True, padx=20, pady=15)

        # Control Buttons Bar
        self.controls_frame = tk.Frame(self.stage_frame, bg=COLOR_PANEL)
        self.controls_frame.pack(fill="x", padx=20, pady=10)

        self.btn_submit = tk.Button(self.controls_frame, text="SUBMIT PAYLOAD", font=("Orbitron", 10, "bold"), fg=COLOR_BG, bg=COLOR_CYAN, activebackground=COLOR_GREEN, command=self.on_submit)
        self.btn_submit.pack(side="left", expand=True, fill="x", padx=5)

        self.btn_hint = tk.Button(self.controls_frame, text="DIAGNOSTIC HINT", font=("Orbitron", 10, "bold"), fg=COLOR_BG, bg=COLOR_YELLOW, command=self.on_hint)
        self.btn_hint.pack(side="left", expand=True, fill="x", padx=5)

        self.btn_abort = tk.Button(self.controls_frame, text="ABORT RUN", font=("Orbitron", 10, "bold"), fg="#ffffff", bg=COLOR_RED, command=self.show_start_screen)
        self.btn_abort.pack(side="left", expand=True, fill="x", padx=5)

    def show_start_screen(self):
        self.timer_active = False
        self.clear_content_area()

        lbl_welcome = tk.Label(self.content_area, text="NEON BREACH // GRAPHICAL INTERFACE", font=("Orbitron", 16, "bold"), fg=COLOR_CYAN, bg="#04060c")
        lbl_welcome.pack(pady=20)

        # Handle entry
        frame_form = tk.Frame(self.content_area, bg="#04060c")
        frame_form.pack(pady=10)

        tk.Label(frame_form, text="NETRUNNER CALLSIGN: ", font=("Consolas", 11, "bold"), fg=COLOR_TEXT, bg="#04060c").grid(row=0, column=0, pady=5)
        self.ent_handle = tk.Entry(frame_form, font=("Consolas", 11), bg="#000", fg=COLOR_CYAN, insertbackground=COLOR_CYAN)
        self.ent_handle.insert(0, "NEO_RUNNER")
        self.ent_handle.grid(row=0, column=1, pady=5)

        tk.Label(frame_form, text="SECURITY SEVERITY: ", font=("Consolas", 11, "bold"), fg=COLOR_TEXT, bg="#04060c").grid(row=1, column=0, pady=5)
        self.var_diff = tk.StringVar(value="CYBERPUNK")
        opt_diff = tk.OptionMenu(frame_form, self.var_diff, "NOVICE", "CYBERPUNK", "BLACK_ICE")
        opt_diff.config(font=("Consolas", 10, "bold"), bg=COLOR_PANEL, fg=COLOR_YELLOW)
        opt_diff.grid(row=1, column=1, pady=5)

        btn_start = tk.Button(self.content_area, text="INITIATE SYSTEM BREACH", font=("Orbitron", 12, "bold"), fg=COLOR_BG, bg=COLOR_GREEN, padx=20, pady=10, command=self.start_game)
        btn_start.pack(pady=25)

    def start_game(self):
        self.runner_handle = self.ent_handle.get().strip() or "NETRUNNER_X"
        self.difficulty = self.var_diff.get()
        self.engine.start_game(handle=self.runner_handle, difficulty=self.difficulty)
        
        self.timer_active = True
        self.update_gui_loop()
        self.render_active_node()

    def update_gui_loop(self):
        if not self.timer_active:
            return

        if self.engine.check_time_expiry():
            self.timer_active = False
            messagebox.showerror("LINK FLATLINED", "SYSTEM TRACE REACHED 100%! Black-ICE detected your neural deck.")
            self.show_start_screen()
            return

        # Update HUD Metrics
        self.lbl_runner.config(text=f"RUNNER: {self.engine.player_handle}")
        self.lbl_integrity.config(text=f"INTEGRITY: {max(0, self.engine.integrity)} HP")
        self.lbl_trace.config(text=f"TRACE: {min(100, self.engine.trace_percent)}%")
        self.lbl_timer.config(text=f"TIME: {self.engine.get_time_remaining():.1f}s")
        self.lbl_score.config(text=f"SCORE: {self.engine.score}")

        # Update Node Progress Labels
        for idx, lbl in enumerate(self.node_labels):
            if idx < self.engine.current_layer_idx:
                lbl.config(fg=COLOR_BG, bg=COLOR_GREEN)
            elif idx == self.engine.current_layer_idx:
                lbl.config(fg=COLOR_BG, bg=COLOR_CYAN)
            else:
                lbl.config(fg=COLOR_DIM, bg=COLOR_PANEL)

        self.after(100, self.update_gui_loop)

    def render_active_node(self):
        self.clear_content_area()
        p = self.engine.active_puzzle
        if not p:
            return

        self.lbl_puzzle_title.config(text=f"NODE 0{self.engine.current_layer_idx + 1}: {p.title}")
        self.lbl_puzzle_sub.config(text="Solve the diagnostic payload puzzle to pwn this security layer.")

        # Render puzzle prompt
        prompt_box = tk.Text(self.content_area, font=("Consolas", 10), bg="#000", fg=COLOR_CYAN, height=12, bd=1, relief="sunken")
        prompt_box.insert("1.0", p.get_prompt())
        prompt_box.config(state="disabled")
        prompt_box.pack(fill="both", expand=True, padx=15, pady=10)

        # Input Frame
        frame_in = tk.Frame(self.content_area, bg="#04060c")
        frame_in.pack(pady=10)

        tk.Label(frame_in, text="HACK PAYLOAD: ", font=("Consolas", 11, "bold"), fg=COLOR_YELLOW, bg="#04060c").pack(side="left")
        self.ent_payload = tk.Entry(frame_in, font=("Consolas", 12, "bold"), bg="#000", fg=COLOR_GREEN, insertbackground=COLOR_GREEN, width=24)
        self.ent_payload.pack(side="left", padx=10)
        self.ent_payload.focus_set()
        self.ent_payload.bind("<Return>", lambda e: self.on_submit())

    def on_submit(self):
        if not self.engine.active_puzzle or self.engine.is_game_over:
            return
        payload = self.ent_payload.get().strip() if hasattr(self, 'ent_payload') else ""
        is_correct, feedback = self.engine.submit_answer(payload)

        if is_correct:
            if self.engine.is_victory:
                self.timer_active = False
                messagebox.showinfo("MAINFRAME BREACHED", f"VICTORY! All security nodes overridden.\nFinal Score: {self.engine.score} PTS")
                self.scores_mgr.save_score(self.engine.player_handle, self.engine.score, self.engine.total_layers, self.difficulty, 60.0)
                self.show_start_screen()
            else:
                messagebox.showinfo("NODE BREACHED", feedback)
                self.render_active_node()
        else:
            if self.engine.is_game_over:
                self.timer_active = False
                messagebox.showerror("FLATLINED", feedback)
                self.show_start_screen()
            else:
                messagebox.showwarning("ACCESS DENIED", feedback)

    def on_hint(self):
        success, hint_msg = self.engine.request_hint()
        if success:
            messagebox.showinfo("DIAGNOSTIC HINT", hint_msg)
        else:
            messagebox.showwarning("DIAGNOSTIC ERROR", hint_msg)

    def clear_content_area(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()

def main():
    app = NeonBreachGUI()
    app.mainloop()

if __name__ == "__main__":
    main()
