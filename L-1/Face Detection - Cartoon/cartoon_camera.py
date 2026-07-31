import cv2
import numpy as np
import time
import os
import datetime

class FilterEngine:
    """
    High-performance real-time image processing engine providing multiple cartoon
    and artistic filter presets, cinematic color grading, and vignette effects.
    """

    PRESETS = {
        1: "1. SNAPCHAT VIBRANT CARTOON",
        2: "2. COMIC BOOK POP-ART",
        3: "3. PASTEL SOFT SKETCH",
        4: "4. NOIR GRAPHITE SKETCH",
        5: "5. DSLR CINEMATIC PRO"
    }

    def __init__(self):
        self.active_preset = 1
        self.vignette_enabled = True
        self.color_grade_enabled = True
        
        # Cache parameters for pre-computed operations
        self._vignette_mask = None
        self._cached_shape = None
        self._lut_cinematic = self._build_cinematic_lut()

    def set_preset(self, preset_id: int):
        if preset_id in self.PRESETS:
            self.active_preset = preset_id

    def toggle_vignette(self):
        self.vignette_enabled = not self.vignette_enabled

    def toggle_color_grade(self):
        self.color_grade_enabled = not self.color_grade_enabled

    def _build_cinematic_lut(self) -> np.ndarray:
        """Creates a smooth S-curve Color Lookup Table for cinematic contrast & warm midtones."""
        lut = np.zeros((256, 1, 3), dtype=np.uint8)
        for i in range(256):
            # S-curve contrast boost algorithm
            x = i / 255.0
            # S-curve expression: 3x^2 - 2x^3
            s_curve = 3 * (x ** 2) - 2 * (x ** 3)
            
            # Channel adjustments (B, G, R) - subtle warm split toning
            b_val = np.clip(s_curve * 245.0, 0, 255)
            g_val = np.clip(s_curve * 252.0, 0, 255)
            r_val = np.clip(s_curve * 255.0 + (x * 10), 0, 255)  # slightly warmer reds
            
            lut[i, 0] = [int(b_val), int(g_val), int(r_val)]
        return lut

    def _get_vignette_mask(self, shape: tuple) -> np.ndarray:
        """Generates and caches a high-quality smooth radial vignette gradient mask."""
        h, w = shape[:2]
        if self._vignette_mask is None or self._cached_shape != (h, w):
            self._cached_shape = (h, w)
            # Create coordinate grid centered at (w/2, h/2)
            kernel_x = cv2.getGaussianKernel(w, w * 0.45)
            kernel_y = cv2.getGaussianKernel(h, h * 0.45)
            kernel = kernel_y * kernel_x.T
            mask = kernel / kernel.max()
            
            # Adjust strength (smooth falloff from 1.0 center to 0.45 edges)
            mask = 0.45 + 0.55 * mask
            self._vignette_mask = np.dstack([mask] * 3).astype(np.float32)
            
        return self._vignette_mask

    def apply_vignette(self, frame: np.ndarray) -> np.ndarray:
        """Applies radial vignette mask to frame."""
        mask = self._get_vignette_mask(frame.shape)
        vignetted = (frame.astype(np.float32) * mask).astype(np.uint8)
        return vignetted

    def apply_color_grade(self, frame: np.ndarray) -> np.ndarray:
        """Applies cinematic LUT tone grading."""
        return cv2.LUT(frame, self._lut_cinematic)

    def _boost_vibrance(self, img_bgr: np.ndarray, factor: float = 1.35) -> np.ndarray:
        """Boosts HSV saturation channel for Instagram/Snapchat pop-out color."""
        hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * factor, 0, 255)
        hsv = hsv.astype(np.uint8)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    def _quantize_colors(self, img_bgr: np.ndarray, num_levels: int = 8) -> np.ndarray:
        """Fast color quantization via step bit-masking."""
        step = 256 // num_levels
        return (img_bgr // step) * step + step // 2

    # --- FILTER IMPLEMENTATIONS ---

    def _filter_snapchat_cartoon(self, frame: np.ndarray) -> np.ndarray:
        """
        Preset 1: Snapchat Vibrant Cartoon
        Smooth color regions via downsampled bilateral filtering, high vibrance,
        and clean dark adaptive threshold edge outlines.
        """
        # Step 1: Optimized downsampled bilateral filter for high FPS
        h, w = frame.shape[:2]
        small = cv2.resize(frame, (w // 2, h // 2), interpolation=cv2.INTER_LINEAR)
        
        # Apply multiple fast bilateral passes on small frame
        smooth_small = cv2.bilateralFilter(small, d=7, sigmaColor=65, sigmaSpace=65)
        smooth_small = cv2.bilateralFilter(smooth_small, d=7, sigmaColor=65, sigmaSpace=65)
        
        # Upscale back to full resolution
        color_smooth = cv2.resize(smooth_small, (w, h), interpolation=cv2.INTER_LINEAR)
        color_smooth = self._boost_vibrance(color_smooth, factor=1.4)
        color_quant = self._quantize_colors(color_smooth, num_levels=12)

        # Step 2: Edge map extraction at full resolution
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.medianBlur(gray, 7)
        edges = cv2.adaptiveThreshold(
            gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2
        )
        
        # Convert edges to 3-channel
        edges_3ch = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        # Combine smoothed vibrant colors with sharp black ink edges
        cartoon = cv2.bitwise_and(color_quant, edges_3ch)
        return cartoon

    def _filter_comic_pop_art(self, frame: np.ndarray) -> np.ndarray:
        """
        Preset 2: Comic Book Pop-Art
        High contrast, aggressive 5-level posterization, and bold Canny ink outlines.
        """
        # Posterized high vibrance color palette
        vibrant = self._boost_vibrance(frame, factor=1.6)
        color_quant = self._quantize_colors(vibrant, num_levels=5)
        
        # Bold Canny edge outlines
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.GaussianBlur(gray, (5, 5), 0)
        canny = cv2.Canny(gray_blur, 50, 140)
        
        # Dilate edges for bold graphic novel ink look
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        canny_bold = cv2.dilate(canny, kernel, iterations=1)
        
        # Invert edges (white -> black lines)
        edges_inv = cv2.bitwise_not(canny_bold)
        edges_3ch = cv2.cvtColor(edges_inv, cv2.COLOR_GRAY2BGR)

        return cv2.bitwise_and(color_quant, edges_3ch)

    def _filter_pastel_soft(self, frame: np.ndarray) -> np.ndarray:
        """
        Preset 3: Pastel Soft Sketch
        Soft color blending with delicate sketch outlines and warm tones.
        """
        h, w = frame.shape[:2]
        small = cv2.resize(frame, (w // 2, h // 2))
        smooth_small = cv2.pyrMeanShiftFiltering(small, 15, 30)
        color_smooth = cv2.resize(smooth_small, (w, h))

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.GaussianBlur(gray, (3, 3), 0)
        edges = cv2.adaptiveThreshold(
            gray_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 3
        )
        edges_3ch = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        # Blend colors gently with edges
        pastel = cv2.addWeighted(color_smooth, 0.85, edges_3ch, 0.15, 0)
        return pastel

    def _filter_noir_sketch(self, frame: np.ndarray) -> np.ndarray:
        """
        Preset 4: Noir Graphite Pencil Sketch
        Artistic monochrome line art and pencil shading.
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_inv = cv2.bitwise_not(gray)
        blur = cv2.GaussianBlur(gray_inv, (21, 21), 0)
        
        # Color dodge blend mode for realistic pencil sketch texture
        sketch = cv2.divide(gray, 255 - blur, scale=256)
        sketch = cv2.threshold(sketch, 240, 255, cv2.THRESH_TRUNC)[1]
        
        return cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)

    def _filter_dslr_pro(self, frame: np.ndarray) -> np.ndarray:
        """
        Preset 5: DSLR Pro Clean Feed
        Clean feed with subtle bilateral skin-smoothing and clarity boost.
        """
        h, w = frame.shape[:2]
        small = cv2.resize(frame, (w // 2, h // 2))
        smoothed_small = cv2.bilateralFilter(small, d=5, sigmaColor=35, sigmaSpace=35)
        smoothed = cv2.resize(smoothed_small, (w, h))
        return cv2.addWeighted(frame, 0.6, smoothed, 0.4, 0)

    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """Executes selected filter preset followed by optional color grading and vignette."""
        # 1. Apply selected Cartoon / Artistic Filter
        if self.active_preset == 1:
            processed = self._filter_snapchat_cartoon(frame)
        elif self.active_preset == 2:
            processed = self._filter_comic_pop_art(frame)
        elif self.active_preset == 3:
            processed = self._filter_pastel_soft(frame)
        elif self.active_preset == 4:
            processed = self._filter_noir_sketch(frame)
        elif self.active_preset == 5:
            processed = self._filter_dslr_pro(frame)
        else:
            processed = frame.copy()

        # 2. Apply Cinematic Color Grading (if enabled)
        if self.color_grade_enabled and self.active_preset != 4:
            processed = self.apply_color_grade(processed)

        # 3. Apply Cinematic Vignette (if enabled)
        if self.vignette_enabled:
            processed = self.apply_vignette(processed)

        return processed


class UIRenderer:
    """
    Renders a modern, semi-transparent DSLR/Mirrorless camera HUD overlay,
    including live telemetry, framing brackets, status bars, toast notifications,
    and interactive help modal.
    """

    COLOR_ACCENT = (0, 230, 255)     # Bright Neon Gold/Cyan
    COLOR_REC_RED = (40, 40, 255)    # REC Red Dot
    COLOR_WHITE = (255, 255, 255)
    COLOR_BG_DARK = (15, 18, 24)     # Dark Frosted Glass
    COLOR_GREEN = (50, 220, 100)
    COLOR_GRAY = (160, 165, 175)

    def __init__(self):
        self.show_help = False
        self.toast_message = ""
        self.toast_start_time = 0.0

    def show_toast(self, message: str, duration: float = 2.5):
        self.toast_message = message
        self.toast_start_time = time.time()

    def toggle_help(self):
        self.show_help = not self.show_help

    def _draw_rounded_rect(self, img: np.ndarray, pt1: tuple, pt2: tuple, color: tuple, alpha: float = 0.65, radius: int = 10):
        """Draws a semi-transparent rounded rectangle overlay."""
        x1, y1 = pt1
        x2, y2 = pt2
        
        # Create overlay layer
        overlay = img.copy()
        
        # Draw main rect and circles at corners for smooth rounded box
        cv2.rectangle(overlay, (x1 + radius, y1), (x2 - radius, y2), color, -1)
        cv2.rectangle(overlay, (x1, y1 + radius), (x2, y2 - radius), color, -1)
        cv2.circle(overlay, (x1 + radius, y1 + radius), radius, color, -1)
        cv2.circle(overlay, (x2 - radius, y1 + radius), radius, color, -1)
        cv2.circle(overlay, (x1 + radius, y2 - radius), radius, color, -1)
        cv2.circle(overlay, (x2 - radius, y2 - radius), radius, color, -1)

        # Alpha blend onto original image
        cv2.addWeighted(overlay, alpha, img, 1.0 - alpha, 0, img)

    def _draw_dslr_viewfinder_brackets(self, img: np.ndarray):
        """Renders subtle professional camera viewfinder corner brackets & center target."""
        h, w = img.shape[:2]
        margin = 35
        bracket_len = 30
        thickness = 2
        color = (220, 220, 220)

        # Top-Left Corner
        cv2.line(img, (margin, margin), (margin + bracket_len, margin), color, thickness)
        cv2.line(img, (margin, margin), (margin, margin + bracket_len), color, thickness)

        # Top-Right Corner
        cv2.line(img, (w - margin, margin), (w - margin - bracket_len, margin), color, thickness)
        cv2.line(img, (w - margin, margin), (w - margin, margin + bracket_len), color, thickness)

        # Bottom-Left Corner
        cv2.line(img, (margin, h - margin), (margin + bracket_len, h - margin), color, thickness)
        cv2.line(img, (margin, h - margin), (margin, h - margin - bracket_len), color, thickness)

        # Bottom-Right Corner
        cv2.line(img, (w - margin, h - margin), (w - margin - bracket_len, h - margin), color, thickness)
        cv2.line(img, (w - margin, h - margin), (w - margin, h - margin - bracket_len), color, thickness)

        # Center Crosshair target (subtle)
        cx, cy = w // 2, h // 2
        ch_size = 12
        cv2.line(img, (cx - ch_size, cy), (cx + ch_size, cy), (255, 255, 255), 1, cv2.LINE_AA)
        cv2.line(img, (cx, cy - ch_size), (cx, cy + ch_size), (255, 255, 255), 1, cv2.LINE_AA)
        cv2.circle(img, (cx, cy), 4, self.COLOR_ACCENT, 1, cv2.LINE_AA)

    def render_hud(self, frame: np.ndarray, fps: float, filter_engine: FilterEngine, resolution_str: str):
        """Renders complete top header bar, bottom telemetry bar, and framing elements."""
        h, w = frame.shape[:2]

        # 1. Viewfinder Framing Lines
        self._draw_dslr_viewfinder_brackets(frame)

        # 2. TOP HEADER BAR
        top_bar_height = 50
        self._draw_rounded_rect(frame, (20, 15), (w - 20, top_bar_height + 15), self.COLOR_BG_DARK, alpha=0.72, radius=8)

        # Blinking REC dot (toggles every 0.6 seconds)
        rec_dot_on = (int(time.time() * 1.6) % 2 == 0)
        dot_color = self.COLOR_REC_RED if rec_dot_on else (80, 80, 80)
        cv2.circle(frame, (45, 40), 7, dot_color, -1, cv2.LINE_AA)
        
        cv2.putText(frame, "LIVE", (60, 45), cv2.FONT_HERSHEY_DUPLEX, 0.55, self.COLOR_WHITE, 1, cv2.LINE_AA)
        cv2.putText(frame, "|  DSLR CARTOON CAMERA", (115, 45), cv2.FONT_HERSHEY_DUPLEX, 0.55, self.COLOR_ACCENT, 1, cv2.LINE_AA)

        # System Time & Camera Status right aligned
        curr_time = datetime.datetime.now().strftime("%H:%M:%S")
        status_text = f"SYS: ONLINE  |  {curr_time}"
        cv2.putText(frame, status_text, (w - 260, 45), cv2.FONT_HERSHEY_DUPLEX, 0.50, self.COLOR_GRAY, 1, cv2.LINE_AA)

        # 3. BOTTOM TELEMETRY BAR
        bottom_y1 = h - 65
        bottom_y2 = h - 15
        self._draw_rounded_rect(frame, (20, bottom_y1), (w - 20, bottom_y2), self.COLOR_BG_DARK, alpha=0.75, radius=8)

        # FPS Display with dynamic color coding
        fps_color = self.COLOR_GREEN if fps >= 25 else (0, 200, 255) if fps >= 15 else (50, 50, 255)
        cv2.putText(frame, f"FPS: {fps:4.1f}", (40, h - 32), cv2.FONT_HERSHEY_DUPLEX, 0.55, fps_color, 1, cv2.LINE_AA)

        # Active Filter Preset Title
        filter_name = filter_engine.PRESETS.get(filter_engine.active_preset, "CARTOON FILTER")
        cv2.putText(frame, f"FILTER: {filter_name}", (170, h - 32), cv2.FONT_HERSHEY_DUPLEX, 0.55, self.COLOR_WHITE, 1, cv2.LINE_AA)

        # Resolution Badge
        cv2.putText(frame, f"RES: {resolution_str}", (w - 430, h - 32), cv2.FONT_HERSHEY_DUPLEX, 0.50, self.COLOR_GRAY, 1, cv2.LINE_AA)

        # Feature Toggles (Vignette & Color Grade)
        vig_str = "VIG: ON" if filter_engine.vignette_enabled else "VIG: OFF"
        vig_col = self.COLOR_ACCENT if filter_engine.vignette_enabled else self.COLOR_GRAY
        cv2.putText(frame, vig_str, (w - 270, h - 32), cv2.FONT_HERSHEY_DUPLEX, 0.50, vig_col, 1, cv2.LINE_AA)

        grade_str = "GRADE: ON" if filter_engine.color_grade_enabled else "GRADE: OFF"
        grade_col = self.COLOR_ACCENT if filter_engine.color_grade_enabled else self.COLOR_GRAY
        cv2.putText(frame, grade_str, (w - 170, h - 32), cv2.FONT_HERSHEY_DUPLEX, 0.50, grade_col, 1, cv2.LINE_AA)

        # Help Hint Text rightmost
        cv2.putText(frame, "[H] Help", (w - 75, h - 32), cv2.FONT_HERSHEY_DUPLEX, 0.45, self.COLOR_ACCENT, 1, cv2.LINE_AA)

        # 4. RENDER TOAST NOTIFICATION (if active)
        if self.toast_message and (time.time() - self.toast_start_time < 2.8):
            self._render_toast(frame)

        # 5. RENDER HELP MODAL (if active)
        if self.show_help:
            self._render_help_modal(frame)

    def _render_toast(self, frame: np.ndarray):
        """Renders a modern toast banner popup notification near top center."""
        h, w = frame.shape[:2]
        box_w, box_h = 520, 45
        cx, cy = w // 2, 88
        
        pt1 = (cx - box_w // 2, cy - box_h // 2)
        pt2 = (cx + box_w // 2, cy + box_h // 2)
        
        self._draw_rounded_rect(frame, pt1, pt2, (20, 80, 20), alpha=0.88, radius=8)
        cv2.rectangle(frame, pt1, pt2, self.COLOR_GREEN, 1, cv2.LINE_AA)
        
        cv2.putText(
            frame, self.toast_message, (pt1[0] + 20, cy + 6),
            cv2.FONT_HERSHEY_DUPLEX, 0.50, self.COLOR_WHITE, 1, cv2.LINE_AA
        )

    def _render_help_modal(self, frame: np.ndarray):
        """Renders an overlay window detailing keyboard shortcuts and filter controls."""
        h, w = frame.shape[:2]
        modal_w, modal_h = 580, 360
        cx, cy = w // 2, h // 2
        
        pt1 = (cx - modal_w // 2, cy - modal_h // 2)
        pt2 = (cx + modal_w // 2, cy + modal_h // 2)

        # Dark frosted modal body
        self._draw_rounded_rect(frame, pt1, pt2, (10, 12, 18), alpha=0.92, radius=12)
        cv2.rectangle(frame, pt1, pt2, self.COLOR_ACCENT, 1, cv2.LINE_AA)

        # Modal Header
        cv2.putText(frame, "CARTOON CAMERA CONTROLS & SHORTCUTS", (pt1[0] + 35, pt1[1] + 45),
                    cv2.FONT_HERSHEY_DUPLEX, 0.65, self.COLOR_ACCENT, 1, cv2.LINE_AA)
        cv2.line(frame, (pt1[0] + 35, pt1[1] + 60), (pt2[0] - 35, pt1[1] + 60), (60, 65, 75), 1)

        shortcuts = [
            ("1 - 5", "Switch Filter Presets (Snapchat, Comic, Pastel, Noir, DSLR)"),
            ("V",     "Toggle Cinematic Vignette Effect (On / Off)"),
            ("C",     "Toggle Color Grading & Vibrance Boost (On / Off)"),
            ("S",     "Take High-Res Snapshot (Saved to snapshots/ directory)"),
            ("H",     "Toggle This Help Screen"),
            ("Q / ESC","Quit Cartoon Camera Application")
        ]

        y_offset = pt1[1] + 95
        for key, desc in shortcuts:
            # Key box badge
            cv2.rectangle(frame, (pt1[0] + 40, y_offset - 16), (pt1[0] + 130, y_offset + 6), (35, 40, 50), -1)
            cv2.rectangle(frame, (pt1[0] + 40, y_offset - 16), (pt1[0] + 130, y_offset + 6), self.COLOR_ACCENT, 1)
            cv2.putText(frame, key, (pt1[0] + 48, y_offset - 1), cv2.FONT_HERSHEY_DUPLEX, 0.45, self.COLOR_WHITE, 1, cv2.LINE_AA)

            # Description
            cv2.putText(frame, desc, (pt1[0] + 145, y_offset - 1), cv2.FONT_HERSHEY_DUPLEX, 0.48, self.COLOR_GRAY, 1, cv2.LINE_AA)
            y_offset += 38

        # Footer dismiss note
        cv2.putText(frame, "Press 'H' or 'ESC' to close this menu", (cx - 140, pt2[0] - 25 if False else pt2[1] - 20),
                    cv2.FONT_HERSHEY_DUPLEX, 0.45, self.COLOR_ACCENT, 1, cv2.LINE_AA)


class CartoonCameraApp:
    """
    Main application orchestrator handling webcam loop, user interactions,
    snapshot storage, and frame rate calculation.
    """

    def __init__(self, target_width: int = 1920, target_height: int = 1080):
        self.target_width = target_width
        self.target_height = target_height
        
        self.filter_engine = FilterEngine()
        self.ui_renderer = UIRenderer()

        self.snapshot_dir = "snapshots"
        os.makedirs(self.snapshot_dir, exist_ok=True)

        self.cap = None
        self.actual_width = 0
        self.actual_height = 0

    def init_camera(self) -> bool:
        """Initializes high-definition webcam feed."""
        print("[INFO] Initializing webcam feed...")
        
        # DirectShow backend on Windows for faster initialization & 1080p support
        if os.name == 'nt':
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        else:
            self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            # Fallback to default backend if DirectShow fails
            self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            print("[ERROR] Could not open webcam device. Please check hardware connection.")
            return False

        # Request Full HD resolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.target_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.target_height)
        self.cap.set(cv2.CAP_PROP_FPS, 60)

        # Query actual hardware resolution obtained
        self.actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        print(f"[SUCCESS] Webcam connected: {self.actual_width}x{self.actual_height}")
        return True

    def save_snapshot(self, frame: np.ndarray):
        """Saves current processed frame to disk with timestamp."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"snapshot_{timestamp}.jpg"
        filepath = os.path.join(self.snapshot_dir, filename)
        
        cv2.imwrite(filepath, frame)
        print(f"[SNAPSHOT] Saved: {filepath}")
        self.ui_renderer.show_toast(f"SNAPSHOT SAVED: {filename}")

    def run(self):
        """Main execution loop."""
        if not self.init_camera():
            return

        window_name = "Premium Cartoon Camera - Snapchat Filter"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, 1280, 720)

        resolution_str = f"{self.actual_width}x{self.actual_height}"

        # FPS calculation variables
        prev_frame_time = time.time()
        fps = 0.0

        print("\n" + "="*60)
        print(" CARTOON CAMERA STARTED SUCCESSFULLY!")
        print(" Hotkeys: [1-5] Filters | [V] Vignette | [C] Color Grade")
        print("          [S] Snapshot | [H] Help | [Q] Quit")
        print("="*60 + "\n")

        try:
            while True:
                ret, frame = self.cap.read()
                if not ret or frame is None:
                    print("[WARNING] Empty frame received from webcam. Retrying...")
                    time.sleep(0.01)
                    continue

                # Calculate smooth moving-average FPS
                curr_frame_time = time.time()
                time_delta = curr_frame_time - prev_frame_time
                prev_frame_time = curr_frame_time
                if time_delta > 0:
                    inst_fps = 1.0 / time_delta
                    fps = 0.9 * fps + 0.1 * inst_fps if fps > 0 else inst_fps

                # 1. Process frame with active cartoon filter engine
                processed_frame = self.filter_engine.process_frame(frame)

                # Create display frame copy for UI HUD rendering
                display_frame = processed_frame.copy()

                # 2. Render modern semi-transparent DSLR UI overlay
                self.ui_renderer.render_hud(display_frame, fps, self.filter_engine, resolution_str)

                # 3. Show composite result
                cv2.imshow(window_name, display_frame)

                # 4. Process Key Input
                key = cv2.waitKey(1) & 0xFF

                if key in [ord('q'), ord('Q'), 27]: # Q or ESC to quit
                    print("[INFO] Quit requested by user.")
                    break
                elif key in [ord('1'), ord('2'), ord('3'), ord('4'), ord('5')]:
                    preset_num = int(chr(key))
                    self.filter_engine.set_preset(preset_num)
                elif key in [ord('v'), ord('V')]:
                    self.filter_engine.toggle_vignette()
                elif key in [ord('c'), ord('C')]:
                    self.filter_engine.toggle_color_grade()
                elif key in [ord('s'), ord('S')]:
                    # Save clean processed frame (without HUD overlays) for high quality
                    self.save_snapshot(processed_frame)
                elif key in [ord('h'), ord('H')]:
                    self.ui_renderer.toggle_help()

                # Check if window was closed via X button
                if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                    print("[INFO] Window closed by user.")
                    break

        except KeyboardInterrupt:
            print("\n[INFO] Terminated by KeyboardInterrupt.")
        finally:
            self.cleanup(window_name)

    def cleanup(self, window_name: str):
        """Releases camera hardware and destroys OpenCV windows cleanly."""
        print("[INFO] Cleaning up resources...")
        if self.cap and self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
        print("[INFO] Shutdown complete. Goodbye!")


if __name__ == "__main__":
    app = CartoonCameraApp(target_width=1920, target_height=1080)
    app.run()
