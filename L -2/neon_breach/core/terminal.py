import sys
import os
import time
import random

def enable_ansi():
    """Enable Virtual Terminal Processing on Windows OS for ANSI escape codes."""
    if sys.platform == "win32":
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            # 0x0004 is ENABLE_VIRTUAL_TERMINAL_PROCESSING
            # 0x0001 is ENABLE_PROCESSED_OUTPUT
            mode = ctypes.c_ulong()
            stdout_handle = kernel32.GetStdHandle(-11)
            kernel32.GetConsoleMode(stdout_handle, ctypes.byref(mode))
            mode.value |= 0x0004 | 0x0001
            kernel32.SetConsoleMode(stdout_handle, mode)
        except Exception:
            os.system("") # Fallback: calling os.system("") activates ANSI in Windows cmd/powershell

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    REVERSE = "\033[7m"
    
    # Standard Foregrounds
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Bright Foregrounds (Cyberpunk Neon Palette)
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    # Backgrounds
    BG_DARK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_CYAN = "\033[46m"
    BG_MAGENTA = "\033[45m"

class Terminal:
    def __init__(self, anim_speed: float = 0.012):
        enable_ansi()
        self.anim_speed = anim_speed
        self.fast_mode = False

    def clear(self):
        """Clear the terminal screen."""
        os.system("cls" if os.name == "nt" else "clear")

    def print(self, text: str = "", color: str = ""):
        """Standard formatted print."""
        if color:
            print(f"{color}{text}{Colors.RESET}")
        else:
            print(text)

    def print_typed(self, text: str, color: str = "", delay: float = None):
        """Print text with animated typewriter effect."""
        speed = delay if delay is not None else self.anim_speed
        if self.fast_mode or speed <= 0:
            self.print(text, color)
            return

        prefix = color if color else ""
        sys.stdout.write(prefix)
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            if char in ".!?\n":
                time.sleep(speed * 3)
            elif char in ",;:":
                time.sleep(speed * 2)
            else:
                time.sleep(speed)
        if color:
            sys.stdout.write(Colors.RESET)
        sys.stdout.write("\n")
        sys.stdout.flush()

    def glitch_effect(self, text: str, duration: float = 0.4):
        """Display a simulated terminal glitch line."""
        glitch_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?/~`"
        steps = 8
        step_delay = duration / steps
        for _ in range(steps):
            corrupted = "".join(
                c if random.random() > 0.4 else random.choice(glitch_chars)
                for c in text
            )
            color = random.choice([Colors.BRIGHT_RED, Colors.BRIGHT_MAGENTA, Colors.BRIGHT_CYAN])
            sys.stdout.write(f"\r{color}{corrupted}{Colors.RESET}")
            sys.stdout.flush()
            time.sleep(step_delay)
        sys.stdout.write(f"\r{Colors.BRIGHT_GREEN}{text}{Colors.RESET}\n")

    def sound_fx(self, fx_type: str):
        """Simulate cyberpunk sound effects via visual indicators and audio beeps."""
        if fx_type == "BEEP":
            sys.stdout.write("\a") # ASCII Bell
            sys.stdout.flush()
        elif fx_type == "WARNING":
            sys.stdout.write("\a")
            sys.stdout.flush()
            self.print(f"{Colors.BRIGHT_RED}{Colors.BLINK}<<< ALERT: TRACE DETECTED >>>{Colors.RESET}")
        elif fx_type == "SUCCESS":
            self.print(f"{Colors.BRIGHT_GREEN}<<< NODE BREACHED >>>{Colors.RESET}")

    def draw_box(self, title: str, content_lines: list, width: int = 70, color: str = Colors.BRIGHT_CYAN):
        """Render stylized cyberpunk terminal box."""
        top_border = f"┌─[ {Colors.BOLD}{title}{Colors.RESET}{color} ]" + "─" * max(0, width - len(title) - 6) + "┐"
        bottom_border = "└" + "─" * (width - 2) + "┘"
        
        self.print(top_border, color)
        for line in content_lines:
            # Padding calculation considering clean ANSI strip length would be complex, so format clean string
            padding = " " * max(0, width - len(self._strip_ansi(line)) - 4)
            self.print(f"│ {line}{padding} │", color)
        self.print(bottom_border, color)

    def _strip_ansi(self, text: str) -> str:
        """Internal helper to strip ANSI escape codes for width calculation."""
        import re
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)

    def print_header(self):
        """Display NEON BREACH title art."""
        banner = f"""{Colors.BRIGHT_CYAN}{Colors.BOLD}
 █▄  █ █▀▀▀ █▀▀█ █▄  █    █▀▀█ █▀▀█ █▀▀▀ █▀▀█ █▀▀█ █  █
 █ █ █ █▀▀▀ █  █ █ █ █    █▀▀▄ █▄▄▀ █▀▀▀ █▄▄█ █    █▀▀█
 █  ▀█ ▀▀▀▀ ▀▀▀▀ █  ▀█    █▄▄█ █  █ ▀▀▀▀ █  █ █▄▄█ █  █
{Colors.BRIGHT_MAGENTA}=======================================================
   SYSTEM BREACH SIMULATOR // NEURAL TERMINAL v3.0.9
======================================================={Colors.RESET}"""
        print(banner)

    def print_victory_banner(self):
        """Display Breach Success art."""
        banner = f"""{Colors.BRIGHT_GREEN}{Colors.BOLD}
 █▀▀█ █▀▀█ █▀▀▀ █▀▀█ █  █    █▀▀▀ █  █ █▀▀▀ █▀▀▀ █▀▀▀ █▀▀▀ █▀▀▀ █
 █▀▀▄ █▄▄▀ █▀▀▀ █▄▄█ █  █    ▀▀▀█ █  █ █  █ █  █ █▀▀▀ ▀▀▀█ ▀▀▀█ ▀
 █▄▄█ █  █ ▀▀▀▀ █  █ ▀▀▀▀    ▀▀▀▀ ▀▀▀▀ ▀▀▀▀ ▀▀▀▀ ▀▀▀▀ ▀▀▀▀ ▀▀▀▀ ▄
=================================================================
       CYBERSPACE PROTOCOL ACQUIRED // MAINFRAME PWNED
================================================================={Colors.RESET}"""
        print(banner)

    def print_game_over_banner(self):
        """Display Flatlined art."""
        banner = f"""{Colors.BRIGHT_RED}{Colors.BOLD}
 █▀▀ █    █▀▀█ █▀▀█ █  █ █   █ █  █ █  █ █▀▀▀ █▀▀█ █ 
 █▀▀ █    █▄▄█ █  █ █  █ █   █ █▀▀█ █▀▀█ █▀▀▀ █  █ ▀ 
 ▀   ▀▀▀▀ ▀  ▀ ▀▀▀█ ▀▀▀▀ ▀▀▀▀▀ ▀  ▀ ▀  ▀ ▀▀▀▀ ▀▀▀█ ▄ 
======================================================
      NEURAL LINK SEVERED // SYSTEM TRACE 100%
======================================================{Colors.RESET}"""
        print(banner)
