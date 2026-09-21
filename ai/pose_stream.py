import asyncio
import json

import cv2
import mediapipe as mp
import websockets

from smoothing import MotionSmoother
from motion_processor import process_pose, extract_landmarks

# ============================================================
# Configuration
# ============================================================

WEBSOCKET_URI = "ws://localhost:8765"
MODEL_PATH = "ai/pose_landmarker_full.task"

smoother = MotionSmoother(alpha=0.35)

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

            raw_motion = process_pose(landmarks)

            motion = smoother.smooth(raw_motion)

            body_landmarks = extract_landmarks(landmarks)
            # ------------------------------------------------
            # Build motion packet
            # ------------------------------------------------

            motion_data = {
                "timestamp": frame_timestamp,
                "pose": motion,
                "landmarks": body_landmarks
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
                f"L Elbow: {motion['left_elbow']:.1f}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"R Elbow: {motion['right_elbow']:.1f}",
                (20, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"L Knee: {motion['left_knee']:.1f}",
                (20, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"R Knee: {motion['right_knee']:.1f}",
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