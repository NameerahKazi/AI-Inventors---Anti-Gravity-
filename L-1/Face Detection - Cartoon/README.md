# 📸 Premium Real-Time Cartoon Camera (OpenCV)

A high-performance, real-time Python camera application featuring Snapchat/Instagram style cartoon filters, cinematic color grading, smooth vignette falloff, and a modern semi-transparent DSLR/Mirrorless HUD viewfinder UI.

---

## ✨ Features

- **🚀 Real-Time Full HD Performance**: Optimized bilateral filtering using resolution downscaling pyramid passes for high FPS real-time rendering.
- **🎨 5 Premium Filter Presets**:
  1. **Snapchat Vibrant Cartoon**: Ultra-smooth skin tone colors, high HSV vibrance, and clean adaptive threshold black ink outlines.
  2. **Comic Book Pop-Art**: Posterized 5-level color palette with bold graphic novel Canny ink lines.
  3. **Pastel Soft Sketch**: Soft color blending with delicate sketch outlines and warm tones.
  4. **Noir Graphite Pencil Sketch**: Inverted monochrome graphite shading and texture drawing.
  5. **DSLR Pro Clean Feed**: Clean HD camera feed with subtle clarity boost and skin smoothing.
- **🎞️ Cinematic Effects**:
  - **Radial Vignette**: Pre-calculated smooth Gaussian gradient matrix for rich edge shading.
  - **Cinematic LUT Grade**: Custom S-curve contrast boost with warm midtone split toning.
- **🖥️ Semi-Transparent DSLR HUD Overlay**:
  - Blinking `● REC` live status dot.
  - Viewfinder framing corner brackets and center targeting reticle.
  - Live FPS gauge (color-coded green/yellow/red).
  - Active Filter Badge, Resolution Tag, Vignette & Color Grade Toggles.
  - Animated **Toast Notification** when snapshots are saved.
  - Interactive on-screen Help Modal (toggle with `H`).

---

## 🛠️ Installation & Setup

### Requirements
- Python 3.8 or higher
- OpenCV (`opencv-python`)
- NumPy (`numpy`)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Application
```bash
python cartoon_camera.py
```

---

## 🎮 Keyboard Controls & Hotkeys

| Key | Action |
|---|---|
| **`1` - `5`** | Switch Filter Presets (Snapchat, Comic, Pastel, Noir, DSLR Pro) |
| **`V`** | Toggle Cinematic Vignette Effect (On / Off) |
| **`C`** | Toggle Color Grading & Vibrance Boost (On / Off) |
| **`S`** | Take High-Resolution Snapshot (Saved in `snapshots/` folder) |
| **`H`** | Toggle On-Screen Help Overlay |
| **`Q` / `ESC`** | Quit Application |

---

## 📁 Snapshot Storage

When pressing **`S`**, snapshots are saved automatically to the `snapshots/` directory with a timestamped filename:
`snapshots/snapshot_YYYYMMDD_HHMMSS.jpg`
The saved snapshots preserve the full resolution processed filter without UI overlay elements for maximum image quality.
