# 🥋📉 tkd-drift-analyzer
### Quantifying Biomechanical Performance Decay         in Martial Arts

**tkd-drift-analyzer** is a computer‑vision research tool designed to measure **Technical Drift** — the measurable deviation from “perfect form” caused by physical exhaustion.  
Using **MediaPipe** for pose estimation and **NumPy** for kinematic analysis, the system computes an objective **Drift Score** by comparing a baseline performance to a fatigued performance.

---

## 🔬 Research Objective

In traditional Taekwondo training, it is hypothesized that even expert practitioners (2nd/3rd Dan) experience an **80–90% effort gap** during the final stages of a training session.

This project aims to:

- **Establish a Baseline:** Capture “fresh” biomechanical markers (Velocity, Extension, Stability).  
- **Detect Drift:** Quantify performance loss after high‑intensity training.  
- **Analyze Precision:** Identify which joints or movements degrade the most under fatigue.  

---

## 🛠 Tech Stack

- **Language:** Python 3.11  
- **Computer Vision:** MediaPipe, OpenCV  
- **Data Science:** Pandas (logging), NumPy (kinematics)  
- **Version Control:** Git  

---

## ▶️ How to Run the Project

This project includes a `main.py` script which now operates as a **command-line comparator**. When you supply two recorded video files, the program automatically converts them to angle CSV logs and produces a **Similarity Score** reflecting how closely the two performances match.

### **1. Clone the repository**
```bash
git clone [https://github.com/ymodak25/tkd-drift-analyzer.git](https://github.com/ymodak25/tkd-drift-analyzer.git)
cd tkd-drift-analyzer
```

### **2. Create and activate a virtual environment**

```bash
python3.11 -m venv venv
source venv/bin/activate
```

### **3. Install dependencies**

```bash
pip install -r requirements.txt
```

### **4. Run the Analyzer**

Provide two video file paths as positional arguments:

```bash
python3.11 main.py <video1.mp4> <video2.mp4>
```

The script will:

* process each MP4 with MediaPipe and write `angles_1.csv` and `angles_2.csv` to the working directory
* compare the angle data frame‑by‑frame
* print a similarity score on a 0–100 scale

Example:

```bash
python3.11 main.py videos/baseline.mp4 videos/fatigued.mp4
```

> **Tip:** you can inspect or re‑use the generated CSV files later, or call `compare_angle_csvs()` directly from other Python code. Legacy webcam/live‑tracking mode has been removed in favor of the batch comparison workflow.

---

## 📐 Key Metrics Tracked

The analyzer extracts three primary signals to calculate drift:

| Metric | Calculation | Significance |
| --- | --- | --- |
| Terminal Velocity | Δ Distance / Δ Time | Measures “snap” and power generation. |
| Extension Angle | Law of Cosines (H-K-A) | Detects if the student is short‑changing kicks. |
| Stability Variance | Std. Dev. of Center of Mass | Measures balance degradation under stress. |
| **Similarity Score** | 100 - Mean Absolute Error of corresponding angles | Indicates how closely two video sessions match; higher means more similar. |

---

## 🚀 Analysis Workflow (Abstract)

The system operates through a multi‑stage pipeline designed to minimize human bias:

### 1. **Baseline Ingestion** User provides a video (or live feed) of standardized movements performed in a peak‑energy state to establish “Gold Standard” coordinates.

### 2. **Fatigue Ingestion** User provides a second video/feed of the same movements performed after a controlled training load.

### 3. **Automated Feature Extraction** The script processes the input, extracting high‑frequency spatial data via MediaPipe and logging performance metrics into structured files.

### 4. **Drift Comparison / Similarity** A comparative module calculates the frame‑by‑frame variance between the two generated logs and converts it into a **Similarity Score** (0–100) rather than a raw percentage decay. A higher score means the performances are more alike.
---

## 🗂️ tkd-drift-analyzer Change-Log

### January - 2026
- I had an idea to do some research in the two fields that I love using computer vision (TaeKwonDo & Computer Science)
- Created a python program to do basic video and motion tracking.
- Used mediapipe to track joints of the body

---

### February - 2026
- Added ability to track motion through video files additional to the webcam.

---

### March - 2026
- Implemented CLI mode: comparing two MP4 recordings.
- Videos are auto‑converted to `angles_*.csv`; a similarity score (0‑100) is computed from mean joint-angle error.
- Removed legacy webcam/live tracking; workflow now focuses on pairwise video comparison.

---