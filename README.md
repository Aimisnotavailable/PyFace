# PyFace

A small experimental Python VTubing prototype that uses MediaPipe for face and hand tracking and Pygame (or another renderer) for simple rendering. This project demonstrates capture, landmark processing, smoothing, projection, and drawing in a modular structure.

---

## Overview

PyFace captures webcam input, extracts facial and hand landmarks with MediaPipe, applies smoothing and projection, and renders shapes or sprites driven by those landmarks. The code is organized so tracking, math, and rendering can be inspected and modified independently.

**Status:** experimental prototype — not production ready.

---

## Features

- Real-time face and hand landmark capture using MediaPipe.  
- Smoothing filters to reduce jitter.  
- Projection utilities for mapping 3D landmarks to 2D render coordinates.  
- Simple rendering pipeline suitable for Pygame or similar libraries.  
- JSON-based shape assets for configurable visuals.

---

## Requirements

- **Python 3.8+**  
- **MediaPipe**  
- **Pygame** (or another rendering library if you replace the renderer)  
- Install dependencies with `pip` using the included `requirements.txt`.

---

## Quick Start

1. Create and activate a virtual environment:
```bash
python -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the demo:
```bash
python main.py
```

4. If camera access fails, check OS camera permissions and ensure no other application is using the camera.

---

## Configuration

- **Shapes and assets:** JSON files and assets are stored in the `shapes/` directory.  
- **Smoothing and projection:** Parameters are defined in `smooth.py` and `projection.py`. Adjust values there to change responsiveness and mapping.  
- **Camera settings:** Camera capture and MediaPipe configuration are in `camera.py`.

---

## Project Structure

```
PyFace/
├─ main.py
├─ app.py
├─ camera.py
├─ engine.py
├─ draw.py
├─ projection.py
├─ smooth.py
├─ shapes/
├─ requirements.txt
```

- **main.py** — primary entry point.  
- **app.py** — application orchestration and runtime loop.  
- **camera.py** — webcam capture and MediaPipe integration.  
- **engine.py** — core update loop and transform management.  
- **draw.py** — rendering routines.  
- **projection.py** — 3D-to-2D projection math.  
- **smooth.py** — smoothing filters and utilities.  
- **shapes/** — JSON shape definitions and visual assets.  
- **requirements.txt** — Python dependencies.

---

## Usage Notes

- The code is modular; you can replace the renderer or adjust smoothing and projection without changing capture logic.  
- Expect tuning of smoothing and projection parameters for different cameras, lighting, and face orientations.

---

## Contributing

Fork the repository and submit pull requests for bug fixes, improvements to tracking or rendering, or additional shape assets. Include clear, minimal changes per PR.

---

## License

No license file is included in the repository. Add an appropriate license before redistributing or reusing the code.
