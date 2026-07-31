# 📸 Real-Time OpenCV Polaroid Camera & Face Detector

An interactive computer vision project built with Python and OpenCV that captures real-time video from your webcam, detects faces, and transforms the live feed into an authentic **Polaroid Instant Photo** experience with analog color grading, vignetting, film grain, and iconic thick-bordered framing.

---

## ✨ Features

- **Real-Time Face Detection**: Powered by OpenCV Haar Cascade classifiers (`haarcascade_frontalface_default.xml`).
- **Multiple Face Bounding Box Styles**:
  - `RETRO_CORNER`: Camera viewfinder corner brackets.
  - `CLASSIC_BOX`: Golden vintage highlight box.
  - `HIDDEN`: Clean view without boxes.
- **Authentic Polaroid Color Filters**:
  - 🎞️ **Polaroid 600**: Classic warm highlights, lifted blacks, soft vintage fade.
  - 🟡 **Sepia Vintage**: Golden monochrome tone.
  - 🧊 **70s Cool**: Cyan/blue tint with faded highlights.
  - 🎬 **B&W Instant**: High-contrast black and white instant film.
  - 📷 **Original**: Clean raw webcam feed with Polaroid framing.
- **Analog Lens Effects**:
  - Radial Gaussian lens vignetting.
  - Dynamic analog film grain / noise overlay.
- **Instant Photo Snapshot**:
  - Press `[SPACE]` or `[P]` to snap a high-resolution Polaroid photo.
  - Realistic camera shutter flash animation.
  - Photos automatically saved to `captures/` with timestamped filename and Polaroid frame.
- **Dynamic Captions & Date Stamp**:
  - Bottom frame features real-time date timestamp and customizable retro captions (`POLAROID 600`, `SUMMER VIBES`, `RETRO SNAPSHOT`, etc.).

---

## 🎮 Keyboard Controls

| Key | Action |
| :--- | :--- |
| `[SPACE]` or `[P]` | 📸 **Snap Polaroid Photo** (saves to `captures/` folder) |
| `[C]` | 🎨 **Cycle Color Filter** (Polaroid 600 -> Sepia -> 70s Cool -> B&W -> Original) |
| `[F]` | 👤 **Cycle Face Box Style** (Retro Corner -> Classic Box -> Hidden) |
| `[G]` | 🌾 **Toggle Analog Film Grain** |
| `[V]` | 🌑 **Toggle Lens Vignette Darkening** |
| `[T]` | ✍️ **Cycle Bottom Polaroid Caption** |
| `[S]` | 📊 **Toggle HUD Info Overlay** |
| `[Q]` or `[ESC]` | ❌ **Exit Application** |

---

## 📁 Project Architecture

```
.
├── main.py           # Main application loop and keyboard event controller
├── filters.py        # Polaroid color grading, vignette, grain, & photo frame rendering
├── detector.py       # Haar Cascade face detector & retro bounding box overlay engine
├── utils.py          # Camera HUD overlay, flash animation, and photo saving utilities
├── requirements.txt  # Project dependencies list
└── captures/         # Saved high-resolution Polaroid snapshots (auto-created)
```

---

## 🚀 Getting Started

### 1. Requirements

Make sure you have Python 3.8+ installed. OpenCV and NumPy are required:

```bash
pip install -r requirements.txt
```

### 2. Launch the Polaroid Camera

Run the main application script:

```bash
python main.py
```

### 3. Verification / Self-Test Mode

To verify all filter pipelines and photo saving without opening an interactive camera window:

```bash
python main.py --test
```

---

## 🛠️ Customization

- **Add Custom Captions**: Edit `self.CAPTIONS` in [`filters.py`](file:///c:/Users/Nameerah%20Kazi/Desktop/JETLEARN-%20NAMEE/AI%20Inventors/filters.py) to add your own handwritten retro texts.
- **Tweak Grain & Vignette**: Modify `self.grain_intensity` or vignette Gaussian multipliers in `PolaroidFilter` in `filters.py`.
- **Change Face Detection Sensitivity**: Adjust `scaleFactor` and `minNeighbors` in `FaceDetector.detect()` inside [`detector.py`](file:///c:/Users/Nameerah%20Kazi/Desktop/JETLEARN-%20NAMEE/AI%20Inventors/detector.py).
