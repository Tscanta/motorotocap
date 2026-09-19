import asyncio
import websockets

HOST = "localhost"
PORT = 8765

clients = set()


async def handle_client(websocket):
    print("Client connected!")

    clients.add(websocket)

    try:
        async for message in websocket:
            print(f"Received: {message}")

            # Forward the motion data to every other connected client
            for client in clients:
                if client != websocket:
                    await client.send(message)

    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected.")

    finally:
        clients.discard(websocket)


async def main():
    print(f"MotionLens WebSocket server running on ws://{HOST}:{PORT}")

    async with websockets.serve(handle_client, HOST, PORT):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())