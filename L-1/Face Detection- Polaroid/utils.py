import os
import cv2
import time
import numpy as np
from datetime import datetime

class PhotoSaver:
    """Handles snapshot saving into the captures/ folder with formatted file names."""
    
    def __init__(self, output_dir="captures"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def save_polaroid(self, polaroid_image):
        """Saves Polaroid framed image to file and returns absolute path."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"polaroid_{timestamp}.png"
        filepath = os.path.abspath(os.path.join(self.output_dir, filename))
        
        cv2.imwrite(filepath, polaroid_image)
        return filepath, filename


class FlashEffect:
    """Visual camera flash effect triggered upon taking a snapshot."""
    
    def __init__(self, total_frames=4):
        self.total_frames = total_frames
        self.remaining_frames = 0

    def trigger(self):
        self.remaining_frames = self.total_frames

    def apply(self, frame):
        if self.remaining_frames <= 0:
            return frame
            
        alpha = self.remaining_frames / float(self.total_frames)
        white_overlay = np.full_like(frame, 255)
        flashed = cv2.addWeighted(frame, 1.0 - (alpha * 0.8), white_overlay, alpha * 0.8, 0)
        
        self.remaining_frames -= 1
        return flashed


class HUDOverlay:
    """Renders retro camera HUD status overlay and hotkey reference."""
    
    def __init__(self):
        self.show_hud = True
        self.notification_text = ""
        self.notification_expiry = 0
        
        # FPS tracker
        self.prev_time = time.time()
        self.fps = 0.0

    def update_fps(self):
        curr_time = time.time()
        delta = curr_time - self.prev_time
        if delta > 0:
            self.fps = (self.fps * 0.9) + (1.0 / delta * 0.1) # Smooth FPS
        self.prev_time = curr_time

    def set_notification(self, text, duration=2.5):
        self.notification_text = text
        self.notification_expiry = time.time() + duration

    def draw(self, frame, filter_mode, face_style, face_enabled, grain_on, vignette_on, caption):
        self.update_fps()
        
        if not self.show_hud and time.time() > self.notification_expiry:
            return frame

        output = frame.copy()
        h, w = output.shape[:2]
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        if self.show_hud:
            # Top-left HUD info bar
            lines = [
                f"MODE: {filter_mode}",
                f"FACES: {face_style if face_enabled else 'OFF'}",
                f"GRAIN: {'ON' if grain_on else 'OFF'} | VIGNETTE: {'ON' if vignette_on else 'OFF'}",
                f"FPS: {int(self.fps)}"
            ]
            
            hud_w = 260
            hud_h = len(lines) * 20 + 20
            
            # Semi-transparent background box
            overlay = output.copy()
            cv2.rectangle(overlay, (10, 10), (10 + hud_w, 10 + hud_h), (20, 20, 20), -1)
            cv2.addWeighted(overlay, 0.65, output, 0.35, 0, output)
            cv2.rectangle(output, (10, 10), (10 + hud_w, 10 + hud_h), (100, 100, 100), 1)

            y_offset = 30
            for line in lines:
                cv2.putText(output, line, (20, y_offset), font, 0.4, (220, 240, 255), 1, cv2.LINE_AA)
                y_offset += 20

            # Bottom hotkey help bar
            help_text = "[SPACE/P] Snap | [C] Color | [F] Faces | [G] Grain | [V] Vignette | [T] Text | [Q] Exit"
            (tw, th), _ = cv2.getTextSize(help_text, font, 0.38, 1)
            
            hx = (w - tw) // 2
            hy = h - 15
            
            # Background pill for hotkey help
            cv2.rectangle(output, (hx - 10, hy - th - 5), (hx + tw + 10, hy + 5), (15, 15, 15), -1)
            cv2.putText(output, help_text, (hx, hy), font, 0.38, (180, 220, 220), 1, cv2.LINE_AA)

        # Temporary Notification Banner (e.g. Photo Saved!)
        if time.time() < self.notification_expiry:
            (nw, nh), _ = cv2.getTextSize(self.notification_text, font, 0.6, 2)
            nx = (w - nw) // 2
            ny = h // 2
            
            # Banner background box
            cv2.rectangle(output, (nx - 18, ny - nh - 12), (nx + nw + 18, ny + 12), (0, 160, 80), -1)
            cv2.rectangle(output, (nx - 18, ny - nh - 12), (nx + nw + 18, ny + 12), (255, 255, 255), 2)
            cv2.putText(output, self.notification_text, (nx, ny), font, 0.6, (255, 255, 255), 2, cv2.LINE_AA)

        return output
