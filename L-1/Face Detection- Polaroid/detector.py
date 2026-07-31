import os
import urllib.request
import cv2
import numpy as np

class FaceDetector:
    """
    Real-time face detector powered by OpenCV YuNet Deep Neural Network model.
    Includes automatic model downloading, fallback skin-geometry detector,
    and aesthetic bounding box styles (Retro Corner Brackets, Classic Box, or Hidden).
    """
    
    BOX_STYLES = ['RETRO_CORNER', 'CLASSIC_BOX', 'HIDDEN']
    YUNET_MODEL_FILENAME = 'face_detection_yunet.onnx'
    YUNET_MODEL_URL = 'https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx'

    def __init__(self):
        self.enabled = True
        self.style_index = 0
        self.detected_faces = []
        self.detector_type = "YuNet DNN"
        self.yunet = None
        self._current_input_size = None

        self._init_yunet()

    def _init_yunet(self):
        """Initializes OpenCV FaceDetectorYN model."""
        try:
            model_path = os.path.abspath(self.YUNET_MODEL_FILENAME)
            if not os.path.exists(model_path):
                print(f"[INFO] Downloading YuNet Face Detector model to {model_path}...")
                urllib.request.urlretrieve(self.YUNET_MODEL_URL, model_path)
                print("[SUCCESS] YuNet model downloaded successfully.")

            # Create FaceDetectorYN
            self.yunet = cv2.FaceDetectorYN.create(
                model_path,
                "",
                (320, 320),
                score_threshold=0.6,
                nms_threshold=0.3,
                top_k=5000
            )
            print("[INFO] FaceDetectorYN (YuNet DNN) initialized successfully.")
        except Exception as e:
            print(f"[WARNING] Failed to initialize YuNet: {e}. Falling back to Skin-Geometry Detector.")
            self.yunet = None
            self.detector_type = "Skin-Geometry Fallback"

    @property
    def current_style(self):
        return self.BOX_STYLES[self.style_index]

    def cycle_style(self):
        self.style_index = (self.style_index + 1) % len(self.BOX_STYLES)
        return self.current_style

    def toggle(self):
        self.enabled = not self.enabled
        return self.enabled

    def detect(self, frame):
        """
        Detects faces in frame and returns list of (x, y, w, h) bounding boxes.
        """
        if not self.enabled or frame is None:
            self.detected_faces = []
            return []

        h, w = frame.shape[:2]

        if self.yunet is not None:
            try:
                # Update input size if frame dimensions changed
                if self._current_input_size != (w, h):
                    self.yunet.setInputSize((w, h))
                    self._current_input_size = (w, h)

                _, results = self.yunet.detect(frame)

                faces = []
                if results is not None:
                    for det in results:
                        # det format: [x, y, w, h, x_re, y_re, x_le, y_le, x_n, y_n, x_rm, y_rm, x_lm, y_lm, score]
                        fx, fy, fw, fh = det[:4].astype(int)
                        # Ensure bounds remain inside frame
                        fx, fy = max(0, fx), max(0, fy)
                        fw, fh = min(w - fx, fw), min(h - fy, fh)
                        if fw > 20 and fh > 20:
                            faces.append((fx, fy, fw, fh))

                self.detected_faces = faces
                return faces

            except Exception as e:
                print(f"[WARNING] YuNet detection error: {e}. Using fallback.")

        # Fallback skin-contour geometry detector
        return self._detect_fallback(frame)

    def _detect_fallback(self, frame):
        """Fallback skin-color and head aspect-ratio detector."""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # Skin color HSV threshold range
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.erode(mask, kernel, iterations=2)
        mask = cv2.dilate(mask, kernel, iterations=2)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        faces = []
        for c in contours:
            area = cv2.contourArea(c)
            if area > 3000:
                x, y, w, h = cv2.boundingRect(c)
                aspect_ratio = float(h) / w
                if 1.0 <= aspect_ratio <= 2.2: # Typical face aspect ratio
                    faces.append((x, y, w, h))

        self.detected_faces = faces
        return faces

    def draw_faces(self, frame, faces):
        """
        Draws bounding box tracking overlays on the frame.
        """
        if not self.enabled or len(faces) == 0 or self.current_style == 'HIDDEN':
            return frame

        output = frame.copy()
        
        for (x, y, w, h) in faces:
            if self.current_style == 'RETRO_CORNER':
                # Retro Viewfinder Corner Brackets
                length = int(min(w, h) * 0.22)
                thickness = 2
                color = (0, 230, 255) # Vintage Gold / Cyan highlight
                
                # Top-Left Corner
                cv2.line(output, (x, y), (x + length, y), color, thickness)
                cv2.line(output, (x, y), (x, y + length), color, thickness)
                
                # Top-Right Corner
                cv2.line(output, (x + w, y), (x + w - length, y), color, thickness)
                cv2.line(output, (x + w, y), (x + w, y + length), color, thickness)
                
                # Bottom-Left Corner
                cv2.line(output, (x, y + h), (x + length, y + h), color, thickness)
                cv2.line(output, (x, y + h), (x, y + h - length), color, thickness)
                
                # Bottom-Right Corner
                cv2.line(output, (x + w, y + h), (x + w - length, y + h), color, thickness)
                cv2.line(output, (x + w, y + h), (x + w, y + h - length), color, thickness)

                # Central viewfinder crosshair
                cx, cy = x + w // 2, y + h // 2
                cv2.line(output, (cx - 6, cy), (cx + 6, cy), (0, 200, 255), 1)
                cv2.line(output, (cx, cy - 6), (cx, cy + 6), (0, 200, 255), 1)

            elif self.current_style == 'CLASSIC_BOX':
                # Classic bounding rectangle with target label
                cv2.rectangle(output, (x, y), (x + w, y + h), (50, 200, 255), 2)
                cv2.putText(output, "FACE", (x, y - 8), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (50, 200, 255), 1, cv2.LINE_AA)

        return output

    def draw_face_count_badge(self, frame, count):
        """Draws aesthetic face counter pill badge at top right."""
        if not self.enabled:
            return frame
            
        h, w = frame.shape[:2]
        text = f"FACES: {count}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 0.45
        thickness = 1
        
        (tw, th), _ = cv2.getTextSize(text, font, scale, thickness)
        px, py = w - tw - 25, 25
        
        # Pill background
        cv2.rectangle(frame, (px - 10, py - th - 6), (px + tw + 10, py + 6), (30, 30, 30), -1)
        cv2.rectangle(frame, (px - 10, py - th - 6), (px + tw + 10, py + 6), (0, 220, 255), 1)
        
        # Pill text
        cv2.putText(frame, text, (px, py), font, scale, (240, 240, 240), thickness, cv2.LINE_AA)
        return frame
