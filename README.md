```markdown
# 🥋📉 tkd-drift-analyzer
### Quantifying Biomechanical Performance Decay         qin Martial Arts

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

This project includes a `main.py` script that supports both live webcam tracking and pre-recorded video file analysis.

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

```bash
python3.11 main.py

```

Upon launch, the program will prompt you to:

* **Enter a file path** (e.g., `videos/baseline.mp4`) to analyze a recorded session.
* **Press Enter** to launch the tracker using your default webcam.

---

## 📐 Key Metrics Tracked

The analyzer extracts three primary signals to calculate drift:

| Metric | Calculation | Significance |
| --- | --- | --- |
| Terminal Velocity | Δ Distance / Δ Time | Measures “snap” and power generation. |
| Extension Angle | Law of Cosines (H-K-A) | Detects if the student is short‑changing kicks. |
| Stability Variance | Std. Dev. of Center of Mass | Measures balance degradation under stress. |

---

## 🚀 Analysis Workflow (Abstract)

The system operates through a multi‑stage pipeline designed to minimize human bias:

### 1. **Baseline Ingestion** User provides a video (or live feed) of standardized movements performed in a peak‑energy state to establish “Gold Standard” coordinates.

### 2. **Fatigue Ingestion** User provides a second video/feed of the same movements performed after a controlled training load.

### 3. **Automated Feature Extraction** The script processes the input, extracting high‑frequency spatial data via MediaPipe and logging performance metrics into structured files.

### 4. **Drift Comparison** A comparative module calculates the variance between the two logs, outputting a **Drift Coefficient** representing percentage performance decay.

