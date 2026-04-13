import sys
import cv2
import mediapipe as mp
import numpy as np
import csv
import os
import subprocess
import tempfile

mp_pose = mp.solutions.pose

# ----------------------------------------
# EXTRACT LANDMARKS
# ----------------------------------------
def extract_landmarks(results):
    if not results.pose_landmarks:
        return None
    pts = []
    for lm in results.pose_landmarks.landmark:
        pts.extend([lm.x, lm.y, lm.z])
    return pts

# ----------------------------------------
# CALCULATE ANGLE
# ----------------------------------------
def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    ba = a - b
    bc = c - b
    cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
    return np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0)))

# ----------------------------------------
# GET ANGLES FROM LANDMARK VECTOR
# ----------------------------------------
def get_angles_from_landmarks(landmarks):
    pts = [(landmarks[i], landmarks[i+1], landmarks[i+2]) for i in range(0, len(landmarks), 3)]
    lm = mp_pose.PoseLandmark

    angles = {
        "right_elbow": calculate_angle(pts[lm.RIGHT_SHOULDER.value], pts[lm.RIGHT_ELBOW.value], pts[lm.RIGHT_WRIST.value]),
        "left_elbow": calculate_angle(pts[lm.LEFT_SHOULDER.value], pts[lm.LEFT_ELBOW.value], pts[lm.LEFT_WRIST.value]),
        "right_knee": calculate_angle(pts[lm.RIGHT_HIP.value], pts[lm.RIGHT_KNEE.value], pts[lm.RIGHT_ANKLE.value]),
        "left_knee": calculate_angle(pts[lm.LEFT_HIP.value], pts[lm.LEFT_KNEE.value], pts[lm.LEFT_ANKLE.value]),
    }

    return angles

# ----------------------------------------
# VIDEO SUPPORT
# ----------------------------------------
def convert_mov_to_mp4(mov_path):
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
            temp_path = tmp.name

        subprocess.run(
            ["ffmpeg", "-y", "-i", mov_path, "-c:v", "libx264", "-preset", "ultrafast", "-c:a", "aac", temp_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        return temp_path
    except (subprocess.CalledProcessError, FileNotFoundError):
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                pass
        return None


def open_video_capture(video_path):
    cap = cv2.VideoCapture(video_path)
    if cap.isOpened():
        return cap, None

    if video_path.lower().endswith(".mov"):
        temp_path = convert_mov_to_mp4(video_path)
        if temp_path:
            cap = cv2.VideoCapture(temp_path)
            if cap.isOpened():
                return cap, temp_path

    return cap, None

# ----------------------------------------
# PROCESS VIDEO → ANGLE CSV
# ----------------------------------------
def process_video_to_angle_csv(video_path, output_csv):
    pose = mp_pose.Pose()
    cap, temp_path = open_video_capture(video_path)

    if not cap.isOpened():
        raise ValueError(f"Cannot open video file: {video_path}")

    try:
        with open(output_csv, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["frame", "right_elbow", "left_elbow", "right_knee", "left_knee"])

            frame_idx = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                landmarks = extract_landmarks(results)

                if landmarks:
                    angles = get_angles_from_landmarks(landmarks)
                    writer.writerow([frame_idx] + list(angles.values()))

                frame_idx += 1
    finally:
        cap.release()
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                pass

    return output_csv

# ----------------------------------------
# COMPARE TWO ANGLE CSV FILES
# ----------------------------------------
def compare_angle_csvs(csv1, csv2):
    data1 = np.loadtxt(csv1, delimiter=",", skiprows=1)
    data2 = np.loadtxt(csv2, delimiter=",", skiprows=1)

    min_len = min(len(data1), len(data2))
    data1 = data1[:min_len, 1:]
    data2 = data2[:min_len, 1:]

    diff = np.abs(data1 - data2)
    mae = np.mean(diff)

    score = max(0, 100 - mae)
    return score

# ----------------------------------------
# MAIN (TERMINAL ARGUMENT MODE)
# ----------------------------------------
def main():
    if len(sys.argv) != 3:
        print("Usage: python3 main.py <video1.mp4|.mov> <video2.mp4|.mov>")
        sys.exit(1)

    video1 = sys.argv[1]
    video2 = sys.argv[2]

    print("\nProcessing videos...")
    # derive CSV filenames from input video basenames
    csv1 = os.path.splitext(os.path.basename(video1))[0] + ".csv"
    csv2 = os.path.splitext(os.path.basename(video2))[0] + ".csv"
    # avoid name collision if both inputs share the same basename
    if csv1 == csv2:
        csv1 = os.path.splitext(os.path.basename(video1))[0] + "_1.csv"
        csv2 = os.path.splitext(os.path.basename(video2))[0] + "_2.csv"

    process_video_to_angle_csv(video1, csv1)
    process_video_to_angle_csv(video2, csv2)

    print("Comparing angle data...")
    score = compare_angle_csvs(csv1, csv2)
    print(f"\nSimilarity Score: {score:.2f}/100\n")

    # write numeric score to a results file derived from the input filename
    base1 = os.path.splitext(os.path.basename(video1))[0]
    parts = base1.split('-')
    if len(parts) >= 2:
        results_name = '-'.join(parts[:-1]) + '-Results.txt'
    else:
        results_name = base1 + '-Results.txt'

    try:
        with open(results_name, 'w') as rf:
            rf.write(f"{score:.2f}\n")
    except OSError:
        # best-effort: ignore write failures but notify on stdout
        print(f"Warning: could not write results to {results_name}")

if __name__ == "__main__":
    main()
