import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

# --- NEW: Ask for video file path ---
video_path = input("Enter a video file path, or press Enter to use webcam: ").strip()

if video_path:
    cap = cv2.VideoCapture(video_path)
else:
    cap = cv2.VideoCapture(0)  # default webcam

print("Press 'q' to quit the test.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Process the frame
    results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # Draw landmarks
    if results.pose_landmarks:
        mp_draw.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

    cv2.imshow("Environment Check - The Dan Gap", frame)

    # For video files, slow down playback to real-time
    key = cv2.waitKey(1 if not video_path else 30) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
