import asyncio
import websockets


HOST = "localhost"
PORT = 8765


async def handle_client(websocket):
    print("Client connected!")

    try:
        async for message in websocket:
            print(f"Received: {message}")

    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected.")


async def main():
    print(f"MotionLens WebSocket server running on ws://{HOST}:{PORT}")

    async with websockets.serve(
        handle_client,
        HOST,
        PORT
    ):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())