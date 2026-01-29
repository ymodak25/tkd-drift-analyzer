# 🥋📉 tkd-drift-analyzer
### Quantifying Biomechanical Performance Decay in Martial Arts

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

- **Language:** Python 3.x  
- **Computer Vision:** MediaPipe, OpenCV  
- **Data Science:** Pandas (logging), NumPy (kinematics)  
- **Version Control:** Git  

---

## 📐 Key Metrics Tracked

The analyzer extracts three primary signals to calculate drift:

| Metric             | Calculation                 | Significance                                      |
|--------------------|-----------------------------|---------------------------------------------------|
| Terminal Velocity  | Δ Distance / Δ Time         | Measures “snap” and power generation.             |
| Extension Angle    | Law of Cosines (H-K-A)      | Detects if the student is short‑changing kicks.   |
| Stability Variance | Std. Dev. of Center of Mass | Measures balance degradation under stress.        |

---

## 🚀 Analysis Workflow (Abstract)

The system operates through a multi‑stage pipeline designed to minimize human bias:

### 1. **Baseline Ingestion**  
User provides a video of standardized movements performed in a peak‑energy state to establish “Gold Standard” coordinates.

### 2. **Fatigue Ingestion**  
User provides a second video of the same movements performed after a controlled training load.

### 3. **Automated Feature Extraction**  
The script processes both streams, extracting high‑frequency spatial data and logging performance metrics into structured files.

### 4. **Drift Comparison**  
A comparative module calculates the variance between the two logs, outputting a **Drift Coefficient** representing percentage performance decay.
