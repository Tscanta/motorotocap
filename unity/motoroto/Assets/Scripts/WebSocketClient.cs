using UnityEngine;
using NativeWebSocket;
using System.Text;

public class WebSocketClient : MonoBehaviour
{
    private WebSocket websocket;

    public MotionUI motionUI;

    public CharacterMotionController characterController;

    async void Start()
    {
        Debug.Log("Starting MotionLens WebSocket client...");

        websocket = new WebSocket("ws://localhost:8765");

        websocket.OnOpen += () =>
        {
            Debug.Log("MotionLens WebSocket CONNECTED!");
        };

        websocket.OnError += (error) =>
        {
            Debug.LogError("WebSocket Error: " + error);
        };

        websocket.OnClose += (closeCode) =>
        {
            Debug.Log("WebSocket CLOSED: " + closeCode);
        };

        websocket.OnMessage += (bytes) =>
        {
            string message = Encoding.UTF8.GetString(bytes);

            Debug.Log("RECEIVED FROM PYTHON:");
            Debug.Log(message);

            MotionData motion = JsonUtility.FromJson<MotionData>(message);

            Debug.Log("LEFT ELBOW: " + motion.pose.left_elbow);
            Debug.Log("RIGHT ELBOW: " + motion.pose.right_elbow);
            Debug.Log("LEFT KNEE: " + motion.pose.left_knee);
            Debug.Log("RIGHT KNEE: " + motion.pose.right_knee);

            if (motionUI != null)
            {
                motionUI.UpdateMotion(motion);
            }   
            if (characterController != null)
            {
                characterController.UpdateMotion(motion);
            }
        };

        await websocket.Connect();
    }

    void Update()
    {
#if !UNITY_WEBGL || UNITY_EDITOR
        websocket?.DispatchMessageQueue();
#endif
    }

    async void OnApplicationQuit()
    {
        if (websocket != null)
        {
            await websocket.Close();
        }
    }
}