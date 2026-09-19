import asyncio
import json

import cv2
import mediapipe as mp
import websockets

from motion import calculate_angle


# ============================================================
# Configuration
# ============================================================

WEBSOCKET_URI = "ws://localhost:8765"
MODEL_PATH = "ai/pose_landmarker_full.task"


# ============================================================
# MediaPipe setup
# ============================================================

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode


options = PoseLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path=MODEL_PATH
    ),
    running_mode=VisionRunningMode.VIDEO,
    num_poses=1,
)

landmarker = PoseLandmarker.create_from_options(options)


# ============================================================
# Camera
# ============================================================

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Could not open camera.")
    exit()


# ============================================================
# Motion capture
# ============================================================

async def capture_and_stream(websocket):

    frame_timestamp = 0

    print("Camera started.")
    print("MotionLens is streaming pose data...")
    print("Press Q to stop.\n")

    while cap.isOpened():

        success, frame = cap.read()

        if not success:
            print("Could not read camera.")
            break

        # OpenCV BGR → RGB
        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # Create MediaPipe image
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        frame_timestamp += 1

        # Run pose AI
        results = landmarker.detect_for_video(
            mp_image,
            frame_timestamp
        )

        # ----------------------------------------------------
        # If a person is detected
        # ----------------------------------------------------

        if results.pose_landmarks:

            landmarks = results.pose_landmarks[0]

            # Important joints

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


            # ------------------------------------------------
            # Calculate elbow angles
            # ------------------------------------------------

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


            # ------------------------------------------------
            # Calculate knee angles
            # ------------------------------------------------

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


            # ------------------------------------------------
            # Build motion packet
            # ------------------------------------------------

            motion_data = {
                "timestamp": frame_timestamp,

                "pose": {
                    "left_elbow": round(
                        float(left_elbow_angle), 2
                    ),

                    "right_elbow": round(
                        float(right_elbow_angle), 2
                    ),

                    "left_knee": round(
                        float(left_knee_angle), 2
                    ),

                    "right_knee": round(
                        float(right_knee_angle), 2
                    )
                }
            }


            # Convert dictionary → JSON
            message = json.dumps(motion_data)


            # Send to WebSocket server
            await websocket.send(message)


            # ------------------------------------------------
            # Draw pose
            # ------------------------------------------------

            h, w, _ = frame.shape

            for landmark in landmarks:

                x = int(landmark.x * w)
                y = int(landmark.y * h)

                if 0 <= x < w and 0 <= y < h:

                    cv2.circle(
                        frame,
                        (x, y),
                        5,
                        (0, 255, 0),
                        -1
                    )


            # Display current values

            cv2.putText(
                frame,
                f"L Elbow: {left_elbow_angle:.1f}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"R Elbow: {right_elbow_angle:.1f}",
                (20, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"L Knee: {left_knee_angle:.1f}",
                (20, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"R Knee: {right_knee_angle:.1f}",
                (20, 130),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )


        # ----------------------------------------------------
        # Display camera
        # ----------------------------------------------------

        cv2.imshow(
            "MotionLens - Live Motion Capture",
            frame
        )


        # Allow OpenCV to process events
        await asyncio.sleep(0.001)


        # Q = quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


# ============================================================
# Main
# ============================================================

async def main():

    print(
        f"Connecting to MotionLens server at "
        f"{WEBSOCKET_URI}..."
    )

    try:

        async with websockets.connect(
            WEBSOCKET_URI
        ) as websocket:

            print("Connected!")
            print("Starting motion capture...\n")

            await capture_and_stream(websocket)

    except ConnectionRefusedError:

        print(
            "\nERROR: Could not connect to WebSocket server."
        )

        print(
            "Make sure communication/server.py "
            "is running first."
        )

    except Exception as e:

        print(f"\nERROR: {e}")

    finally:

        cap.release()

        landmarker.close()

        cv2.destroyAllWindows()


if __name__ == "__main__":

    asyncio.run(main())