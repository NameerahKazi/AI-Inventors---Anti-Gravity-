import sys
import argparse
import cv2
import numpy as np

from filters import PolaroidFilter
from detector import FaceDetector
from utils import PhotoSaver, FlashEffect, HUDOverlay

def main():
    parser = argparse.ArgumentParser(description="Real-Time OpenCV Polaroid Camera with Face Detection")
    parser.add_argument("--camera", type=int, default=0, help="Camera index (default: 0)")
    parser.add_argument("--test", action="store_true", help="Run self-test mode without opening video window")
    args = parser.parse_args()

    print("==================================================")
    print("  INSTANT POLAROID CAMERA & FACE DETECTOR ")
    print("==================================================")
    print("Controls:")
    print("  [SPACE] / [P] : Take Polaroid Snapshot")
    print("  [C]           : Cycle Color Modes (Polaroid 600, Sepia, 70s Cool, B&W, Original)")
    print("  [F]           : Cycle Face Tracking Box Styles (Retro Corner, Classic, Hidden)")
    print("  [G]           : Toggle Film Grain")
    print("  [V]           : Toggle Lens Vignette")
    print("  [T]           : Cycle Bottom Polaroid Caption")
    print("  [S]           : Toggle HUD Info Overlay")
    print("  [Q] / [ESC]   : Exit")
    print("==================================================\n")

    # Initialize modules
    polaroid = PolaroidFilter()
    detector = FaceDetector()
    saver = PhotoSaver(output_dir="captures")
    flash = FlashEffect(total_frames=5)
    hud = HUDOverlay()

    if args.test:
        print("[TEST MODE] Running module verification on synthetic frame...")
        test_frame = np.full((480, 640, 3), (120, 160, 200), dtype=np.uint8)
        
        # Test detection
        faces = detector.detect(test_frame)
        print(f"-> Detection complete. Faces found: {len(faces)}")
        
        # Test filter pipeline
        processed = polaroid.process(test_frame)
        framed = polaroid.add_polaroid_frame(processed)
        print(f"-> Filter processing complete. Output frame size: {framed.shape}")
        
        # Test photo saving
        filepath, filename = saver.save_polaroid(framed)
        print("-> Polaroid photo saved successfully to: " + filepath)
        print("[SUCCESS] Self-test completed successfully!")
        return

    # Open webcam
    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        print(f"[WARNING] Could not open camera {args.camera}. Trying fallback camera indices (1, 2)...")
        for fallback_idx in [1, 2]:
            cap = cv2.VideoCapture(fallback_idx)
            if cap.isOpened():
                print(f"[OK] Successfully opened camera index {fallback_idx}")
                break
                
    if not cap.isOpened():
        print("[ERROR] No accessible webcam found. Please check your camera connection or permissions.")
        print("Hint: You can test the project processing with: python main.py --test")
        sys.exit(1)

    # Set camera resolution (720p preferred for smooth real-time performance)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    window_name = "Polaroid Real-Time Face Detector"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 960, 720)

    try:
        while True:
            ret, frame = cap.read()
            if not ret or frame is None:
                print("[WARNING] Video frame read failed. Retrying...")
                continue

            # Mirror frame for intuitive webcam view
            frame = cv2.flip(frame, 1)

            # 1. Detect faces on raw frame
            faces = detector.detect(frame)

            # 2. Apply Polaroid color grading, vignette, and grain
            filtered_frame = polaroid.process(frame)

            # 3. Draw face bounding boxes and count badge
            framed_with_faces = detector.draw_faces(filtered_frame, faces)
            framed_with_faces = detector.draw_face_count_badge(framed_with_faces, len(faces))

            # 4. Apply shutter flash effect if active
            flashed_frame = flash.apply(framed_with_faces)

            # 5. Embed inside thick Polaroid paper frame
            polaroid_framed = polaroid.add_polaroid_frame(flashed_frame)

            # 6. Apply HUD info overlay
            final_display = hud.draw(
                polaroid_framed,
                filter_mode=polaroid.current_mode,
                face_style=detector.current_style,
                face_enabled=detector.enabled,
                grain_on=polaroid.enable_grain,
                vignette_on=polaroid.enable_vignette,
                caption=polaroid.current_caption
            )

            # Render live window
            cv2.imshow(window_name, final_display)

            # Process keyboard events
            key = cv2.waitKey(1) & 0xFF

            if key in [ord('q'), ord('Q'), 27]: # 27 = ESC
                print("\nExiting Polaroid Camera application...")
                break

            elif key in [ord(' '), ord('p'), ord('P')]: # Snap photo
                flash.trigger()
                # Save high-res framed Polaroid photo
                filepath, filename = saver.save_polaroid(polaroid_framed)
                hud.set_notification(f"PHOTO SAVED! ({filename})", duration=2.5)
                print(f"[SNAP] Captured Polaroid! Saved to: {filepath}")

            elif key in [ord('c'), ord('C')]: # Cycle color filter
                new_mode = polaroid.cycle_mode()
                hud.set_notification(f"FILTER: {new_mode.upper()}", duration=1.5)

            elif key in [ord('f'), ord('F')]: # Cycle face box style
                new_style = detector.cycle_style()
                hud.set_notification(f"FACE TRACKING: {new_style}", duration=1.5)

            elif key in [ord('g'), ord('G')]: # Toggle film grain
                polaroid.enable_grain = not polaroid.enable_grain
                status = "ON" if polaroid.enable_grain else "OFF"
                hud.set_notification(f"FILM GRAIN: {status}", duration=1.5)

            elif key in [ord('v'), ord('V')]: # Toggle vignette
                polaroid.enable_vignette = not polaroid.enable_vignette
                status = "ON" if polaroid.enable_vignette else "OFF"
                hud.set_notification(f"LENS VIGNETTE: {status}", duration=1.5)

            elif key in [ord('t'), ord('T')]: # Cycle bottom caption
                new_caption = polaroid.cycle_caption()
                hud.set_notification(f"CAPTION: '{new_caption}'", duration=1.5)

            elif key in [ord('s'), ord('S')]: # Toggle HUD
                hud.show_hud = not hud.show_hud

    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Camera resource released cleanly.")

if __name__ == "__main__":
    main()
