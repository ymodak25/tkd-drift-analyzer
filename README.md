tkd-drift-analyzer 🥋📉

Quantifying Biomechanical Performance Decay in Martial Arts

tkd-drift-analyzer is a computer vision-based research tool designed to measure Technical Drift—the measurable deviation from "perfect form" caused by physical exhaustion. By utilizing MediaPipe for pose estimation and NumPy for kinematic analysis, this project provides an objective "Score" for martial arts movements, comparing a baseline state to a fatigued state.

🔬 The Research Objective

In traditional Taekwondo training, it is hypothesized that even expert practitioners (2nd/3rd Dan) experience an "80/90% effort gap" during the final stages of a training session. This project seeks to:

Establish a Baseline: Capture "Fresh" biomechanical markers (Velocity, Extension, Stability).

Detect Drift: Quantify the percentage of performance loss after high-intensity training.

Analyze Precision: Identify which specific joints or movements are most susceptible to fatigue.

🛠 Tech Stack

Language: Python 3.x

Computer Vision: MediaPipe, OpenCV

Data Science: Pandas (Logging), NumPy (Kinematics)

Version Control: Git

📐 Key Metrics Tracked

The analyzer extracts three primary signals to calculate "Drift":

Metric	Calculation	Significance
Terminal Velocity	Δ Distance / Δ Time	Measures "Snap" and power generation.
Extension Angle	Law of Cosines (Hip-Knee-Ankle)	Detects if the student is "short-changing" the move.
Stability Variance	Standard Deviation of Center of Mass	Measures balance degradation under stress.
Export to Sheets
🚀 Analysis Workflow (Abstract)

The system operates through a multi-stage pipeline designed to minimize human bias in marking:

Baseline Ingestion: The user provides a video of standardized movements performed in a peak-energy state to establish "Gold Standard" coordinates.

Fatigue Ingestion: The user provides a second video of the same movements performed after a controlled training load.

Automated Feature Extraction: The script processes both streams, extracting high-frequency spatial data and logging performance metrics into structured data files.

Drift Comparison: A comparative module calculates the variance between the two logs, outputting a "Drift Coefficient" that represents the percentage of performance decay.