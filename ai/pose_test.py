import cv2
import mediapipe as mp

from motion import calculate_angle


# ============================================================
# MediaPipe setup
# ============================================================

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode


# Path to our downloaded MediaPipe model
MODEL_PATH = "ai/pose_landmarker_full.task"


# Configure Pose Landmarker
options = PoseLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path=MODEL_PATH
    ),
    running_mode=VisionRunningMode.VIDEO,
    num_poses=1,
)


# Create the AI pose detector
landmarker = PoseLandmarker.create_from_options(options)


# ============================================================
# Camera setup
# ============================================================

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Could not open camera.")
    exit()


frame_timestamp = 0


# ============================================================
# Main loop
# ============================================================

while cap.isOpened():

    # Read frame from camera
    success, frame = cap.read()

    if not success:
        print("ERROR: Could not read camera.")
        break


    # --------------------------------------------------------
    # Convert OpenCV BGR → RGB
    # --------------------------------------------------------

    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )


    # Convert frame into MediaPipe image
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb
    )


    # Increase timestamp
    frame_timestamp += 1


    # --------------------------------------------------------
    # Run AI pose detection
    # --------------------------------------------------------

    results = landmarker.detect_for_video(
        mp_image,
        frame_timestamp
    )


    # --------------------------------------------------------
    # Process detected pose
    # --------------------------------------------------------

    if results.pose_landmarks:

        # Get first detected person
        landmarks = results.pose_landmarks[0]


        # ====================================================
        # Important body landmarks
        # ====================================================

        nose = landmarks[0]

        left_shoulder = landmarks[11]
        right_shoulder = landmarks[12]

        left_elbow = landmarks[13]
        right_elbow = landmarks[14]

        left_wrist = landmarks[15]
        right_wrist = landmarks[16]

        left_hip = landmarks[23]
        right_hip = landmarks[24]

        left_knee = landmarks[25]
        right_knee = landmarks[26]

        left_ankle = landmarks[27]
        right_ankle = landmarks[28]


        # ====================================================
        # Calculate LEFT ELBOW angle
        # ====================================================

        left_elbow_angle = calculate_angle(
            [
                left_shoulder.x,
                left_shoulder.y,
                left_shoulder.z
            ],

            [
                left_elbow.x,
                left_elbow.y,
                left_elbow.z
            ],

            [
                left_wrist.x,
                left_wrist.y,
                left_wrist.z
            ]
        )


        # ====================================================
        # Calculate RIGHT ELBOW angle
        # ====================================================

        right_elbow_angle = calculate_angle(
            [
                right_shoulder.x,
                right_shoulder.y,
                right_shoulder.z
            ],

            [
                right_elbow.x,
                right_elbow.y,
                right_elbow.z
            ],

            [
                right_wrist.x,
                right_wrist.y,
                right_wrist.z
            ]
        )


        # ====================================================
        # Calculate LEFT KNEE angle
        # ====================================================

        left_knee_angle = calculate_angle(
            [
                left_hip.x,
                left_hip.y,
                left_hip.z
            ],

            [
                left_knee.x,
                left_knee.y,
                left_knee.z
            ],

            [
                left_ankle.x,
                left_ankle.y,
                left_ankle.z
            ]
        )


        # ====================================================
        # Calculate RIGHT KNEE angle
        # ====================================================

        right_knee_angle = calculate_angle(
            [
                right_hip.x,
                right_hip.y,
                right_hip.z
            ],

            [
                right_knee.x,
                right_knee.y,
                right_knee.z
            ],

            [
                right_ankle.x,
                right_ankle.y,
                right_ankle.z
            ]
        )


        # ====================================================
        # Print motion information
        # ====================================================

        print(
            f"\r"
            f"Left Elbow: {left_elbow_angle:6.1f}° | "
            f"Right Elbow: {right_elbow_angle:6.1f}° | "
            f"Left Knee: {left_knee_angle:6.1f}° | "
            f"Right Knee: {right_knee_angle:6.1f}°",
            end=""
        )


        # ====================================================
        # Draw landmarks on camera
        # ====================================================

        h, w, _ = frame.shape

        for landmark in landmarks:

            x = int(landmark.x * w)
            y = int(landmark.y * h)

            # Only draw landmarks that are inside the frame
            if 0 <= x < w and 0 <= y < h:

                cv2.circle(
                    frame,
                    (x, y),
                    5,
                    (0, 255, 0),
                    -1
                )


        # ====================================================
        # Draw some text on the camera
        # ====================================================

        cv2.putText(
            frame,
            f"Left Elbow: {left_elbow_angle:.1f}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Right Elbow: {right_elbow_angle:.1f}",
            (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Left Knee: {left_knee_angle:.1f}",
            (20, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Right Knee: {right_knee_angle:.1f}",
            (20, 130),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )


    # ========================================================
    # Display camera
    # ========================================================

    cv2.imshow(
        "MotionLens - AI Motion Capture",
        frame
    )


    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ============================================================
# Cleanup
# ============================================================

cap.release()

landmarker.close()

cv2.destroyAllWindows()

print("\nMotionLens stopped.")