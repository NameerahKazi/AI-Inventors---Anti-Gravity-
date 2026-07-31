import cv2
import numpy as np
from datetime import datetime

class PolaroidFilter:
    """
    Applies authentic Polaroid film color grading, vignetting, 
    film grain, and iconic thick-bordered Polaroid paper frames.
    """
    
    MODES = ['Polaroid 600', 'Sepia Vintage', '70s Cool', 'B&W Instant', 'Original']
    CAPTIONS = ['POLAROID 600', 'SUMMER VIBES', 'RETRO SNAPSHOT', 'MEMORIES', 'VINTAGE MOOD']

    def __init__(self):
        self.mode_index = 0
        self.caption_index = 0
        self.enable_vignette = True
        self.enable_grain = True
        self.grain_intensity = 0.08
        
        # Cache for vignette mask to avoid recomputing every frame
        self._vignette_mask = None
        self._vignette_shape = None

    @property
    def current_mode(self):
        return self.MODES[self.mode_index]

    @property
    def current_caption(self):
        return self.CAPTIONS[self.caption_index]

    def cycle_mode(self):
        self.mode_index = (self.mode_index + 1) % len(self.MODES)
        return self.current_mode

    def cycle_caption(self):
        self.caption_index = (self.caption_index + 1) % len(self.CAPTIONS)
        return self.current_caption

    def apply_color_grading(self, frame):
        """Applies color transformation based on the active mode."""
        mode = self.current_mode
        
        if mode == 'Original':
            return frame.copy()
            
        b, g, r = cv2.split(frame.astype(np.float32))

        if mode == 'Polaroid 600':
            # Warm yellow-red cast in highlights, slightly lifted shadows, soft contrast
            r = cv2.add(r * 1.12, 12)
            g = cv2.add(g * 1.02, 5)
            b = cv2.add(b * 0.88, 10)
            
            # S-curve contrast tweak
            img_merged = cv2.merge([b, g, r])
            img_merged = np.clip(img_merged, 0, 255).astype(np.uint8)
            
            # Lift shadows slightly (vintage fade)
            img_merged = cv2.addWeighted(img_merged, 0.9, np.full_like(img_merged, 15), 0.1, 0)
            return img_merged

        elif mode == 'Sepia Vintage':
            # Classic warm golden sepia tones
            r_out = (r * 0.393) + (g * 0.769) + (b * 0.189)
            g_out = (r * 0.349) + (g * 0.686) + (b * 0.168)
            b_out = (r * 0.272) + (g * 0.534) + (b * 0.131)
            
            img_merged = cv2.merge([b_out, g_out, r_out])
            return np.clip(img_merged, 0, 255).astype(np.uint8)

        elif mode == '70s Cool':
            # Cool cyan blue cast, faded highlights
            r = cv2.add(r * 0.85, 5)
            g = cv2.add(g * 1.05, 10)
            b = cv2.add(b * 1.20, 20)
            
            img_merged = cv2.merge([b, g, r])
            return np.clip(img_merged, 0, 255).astype(np.uint8)

        elif mode == 'B&W Instant':
            # High-contrast monochrome film with soft midtones
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Boost contrast
            gray = cv2.equalizeHist(gray)
            gray_3ch = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            return cv2.addWeighted(gray_3ch, 0.85, np.full_like(gray_3ch, 20), 0.15, 0)

        return frame

    def generate_vignette_mask(self, h, w):
        """Creates a radial Gaussian vignette mask for vintage camera lens feel."""
        if self._vignette_mask is not None and self._vignette_shape == (h, w):
            return self._vignette_mask
            
        kernel_x = cv2.getGaussianKernel(w, w * 0.5)
        kernel_y = cv2.getGaussianKernel(h, h * 0.5)
        kernel = kernel_y * kernel_x.T
        mask = kernel / kernel.max()
        mask = np.power(mask, 0.6) # Soften vignette gradient
        
        self._vignette_mask = np.dstack([mask, mask, mask])
        self._vignette_shape = (h, w)
        return self._vignette_mask

    def apply_vignette(self, frame):
        """Darkens edges using radial mask."""
        if not self.enable_vignette:
            return frame
        h, w = frame.shape[:2]
        mask = self.generate_vignette_mask(h, w)
        vignetted = (frame.astype(np.float32) * mask).astype(np.uint8)
        return vignetted

    def apply_grain(self, frame):
        """Adds subtle analog film grain noise."""
        if not self.enable_grain:
            return frame
        h, w, c = frame.shape
        noise = np.random.normal(0, self.grain_intensity * 255, (h, w, c)).astype(np.float32)
        grained = cv2.add(frame.astype(np.float32), noise)
        return np.clip(grained, 0, 255).astype(np.uint8)

    def add_polaroid_frame(self, frame, custom_caption=None):
        """
        Embeds the video frame into an authentic Polaroid paper border:
        - Equal top/left/right margins
        - Extra thick bottom margin with drop shadow effect
        - Dynamic date timestamp and aesthetic caption text
        """
        h, w = frame.shape[:2]
        
        # Proportional border sizes
        top_margin = int(h * 0.06)
        side_margin = int(w * 0.06)
        bottom_margin = int(h * 0.22)
        
        frame_h = h + top_margin + bottom_margin
        frame_w = w + (side_margin * 2)
        
        # Off-white paper texture background (slightly warm #F8F6F0)
        polaroid = np.full((frame_h, frame_w, 3), (240, 246, 248), dtype=np.uint8)
        
        # Inner drop shadow behind photo cutout
        shadow = np.full((h + 8, w + 8, 3), (180, 185, 190), dtype=np.uint8)
        shadow_y = top_margin - 2
        shadow_x = side_margin - 2
        polaroid[shadow_y:shadow_y + h + 8, shadow_x:shadow_x + w + 8] = shadow
        
        # Place processed photo inside white border
        polaroid[top_margin:top_margin + h, side_margin:side_margin + w] = frame
        
        # Draw subtle inner frame border line around photo
        cv2.rectangle(polaroid, 
                      (side_margin, top_margin), 
                      (side_margin + w, top_margin + h), 
                      (200, 205, 210), 1)

        # Bottom text area
        caption = custom_caption if custom_caption else self.current_caption
        timestamp = datetime.now().strftime("%b %d, %Y • %H:%M")

        # Render vintage style text at the bottom
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale_caption = max(0.5, w / 900.0)
        font_scale_time = max(0.38, w / 1100.0)
        thickness = 1
        
        text_color = (60, 55, 50) # Dark charcoal vintage ink color

        # Bottom caption (Centered)
        caption_size = cv2.getTextSize(caption, font, font_scale_caption, thickness)[0]
        caption_x = (frame_w - caption_size[0]) // 2
        caption_y = top_margin + h + int(bottom_margin * 0.45)
        cv2.putText(polaroid, caption, (caption_x, caption_y), font, font_scale_caption, text_color, thickness, cv2.LINE_AA)

        # Date timestamp (Centered below caption)
        time_size = cv2.getTextSize(timestamp, font, font_scale_time, thickness)[0]
        time_x = (frame_w - time_size[0]) // 2
        time_y = caption_y + int(bottom_margin * 0.35)
        cv2.putText(polaroid, timestamp, (time_x, time_y), font, font_scale_time, (120, 115, 110), thickness, cv2.LINE_AA)

        return polaroid

    def process(self, frame):
        """Runs full filter pipeline on input video frame."""
        graded = self.apply_color_grading(frame)
        vignetted = self.apply_vignette(graded)
        grained = self.apply_grain(vignetted)
        return grained
