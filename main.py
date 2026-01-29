import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)  # Opens the default webcam

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

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
