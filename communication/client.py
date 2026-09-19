import asyncio
import websockets
import json


URI = "ws://localhost:8765"


async def main():

    async with websockets.connect(URI) as websocket:

        print("Connected to MotionLens server!")

        motion_data = {
            "timestamp": 123456,
            "pose": {
                "left_elbow": 93.4,
                "right_elbow": 102.1,
                "left_knee": 157.2,
                "right_knee": 160.4
            }
        }

        message = json.dumps(motion_data)

        await websocket.send(message)

        print("Sent:")
        print(message)


if __name__ == "__main__":
    asyncio.run(main())