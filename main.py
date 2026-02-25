import cv2
import mediapipe as mp
import csv
import numpy as np

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

# -----------------------------
# LANDMARK EXTRACTION
# -----------------------------
def extract_landmarks(results):
    if not results.pose_landmarks:
        return None
    landmarks = []
    for lm in results.pose_landmarks.landmark:
        landmarks.extend([lm.x, lm.y, lm.z])
    return landmarks

# -----------------------------
# SAVE LANDMARKS TO CSV
# -----------------------------
def save_to_csv(csv_writer, frame_idx, landmarks):
    row = [frame_idx] + landmarks
    csv_writer.writerow(row)

# -----------------------------
# ANGLE CALCULATION
# -----------------------------
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    ba = a - b
    bc = c - b

    cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
    angle = np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0)))
    return angle

POSE_LANDMARKS = mp_pose.PoseLandmark

# -----------------------------
# ANGLES FROM LANDMARK VECTOR
# -----------------------------
def get_angles_from_landmarks(landmarks):
    pts = [(landmarks[i], landmarks[i+1], landmarks[i+2]) for i in range(0, len(landmarks), 3)]
    angles = {}

    angles["right_elbow"] = calculate_angle(
        pts[POSE_LANDMARKS.RIGHT_SHOULDER.value],
        pts[POSE_LANDMARKS.RIGHT_ELBOW.value],
        pts[POSE_LANDMARKS.RIGHT_WRIST.value]
    )

    angles["left_elbow"] = calculate_angle(
        pts[POSE_LANDMARKS.LEFT_SHOULDER.value],
        pts[POSE_LANDMARKS.LEFT_ELBOW.value],
        pts[POSE_LANDMARKS.LEFT_WRIST.value]
    )

    angles["right_knee"] = calculate_angle(
        pts[POSE_LANDMARKS.RIGHT_HIP.value],
        pts[POSE_LANDMARKS.RIGHT_KNEE.value],
        pts[POSE_LANDMARKS.RIGHT_ANKLE.value]
    )

    angles["left_knee"] = calculate_angle(
        pts[POSE_LANDMARKS.LEFT_HIP.value],
        pts[POSE_LANDMARKS.LEFT_KNEE.value],
        pts[POSE_LANDMARKS.LEFT_ANKLE.value]
    )

    return angles

# -----------------------------
# COMPARE TWO CSV FILES
# -----------------------------
def compare_csvs(csv1, csv2):
    data1 = np.loadtxt(csv1, delimiter=",", skiprows=1)
    data2 = np.loadtxt(csv2, delimiter=",", skiprows=1)

    min_len = min(len(data1), len(data2))
    data1 = data1[:min_len]
    data2 = data2[:min_len]

    diff = np.abs(data1[:, 1:] - data2[:, 1:])
    mae = np.mean(diff)

    score = max(0, 100 - mae * 10)
    return score

# -----------------------------
# MAIN VIDEO PROCESSING
# -----------------------------
video_path = input("Enter a video file path, or press Enter to use webcam: ").strip()

if video_path:
    cap = cv2.VideoCapture(video_path)
else:
    cap = cv2.VideoCapture(0)

print("Press 'q' to quit the test.")

csv_file = open("output_landmarks.csv", "w", newline="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["frame"] + [f"lm{i}" for i in range(99)])

frame_idx = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    if results.pose_landmarks:
        mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        landmarks = extract_landmarks(results)
        if landmarks:
            save_to_csv(csv_writer, frame_idx, landmarks)

            # Optional: compute angles live
            # angles = get_angles_from_landmarks(landmarks)
            # print(angles)

    cv2.imshow("Environment Check - The Dan Gap", frame)

    key = cv2.waitKey(1 if not video_path else 30) & 0xFF
    if key == ord('q'):
        break

    frame_idx += 1

csv_file.close()
cap.release()
cv2.destroyAllWindows()
