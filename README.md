# Video Frame Sharpness Analyzer 📹✨

This project analyzes the sharpness (or focus) of frames in a video using two methods:
1. **Variance of Absolute Values of the Laplacian (VAVOL)**
2. **Sum of Modified Laplacian (SML)**

It identifies and displays the frames with the maximum sharpness using these methods, making it useful for applications like autofocus testing or video quality analysis.

---

## 🚀 Features
- Detects the sharpest frames in a video.
- Implements two focus-measurement techniques: VAVOL and SML.
- Crops regions of interest (ROI) to focus the sharpness analysis on specific areas.
- Displays the sharpest frames for comparison.

---

## 📂 File Structure
- `dataPath.py`: File containing the `DATA_PATH` variable (adjust as needed).
- `focus-test.mp4`: Input video file to be analyzed.
- `sharpness_analyzer.py`: Main script for running the analysis.

---


