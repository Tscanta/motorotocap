using TMPro;
using UnityEngine;

public class MotionUI : MonoBehaviour
{
    public TMP_Text leftElbowText;
    public TMP_Text rightElbowText;
    public TMP_Text leftKneeText;
    public TMP_Text rightKneeText;

    public void UpdateMotion(MotionData motion)
    {
        leftElbowText.text = $"Left Elbow: {motion.pose.left_elbow:F1}°";
        rightElbowText.text = $"Right Elbow: {motion.pose.right_elbow:F1}°";
        leftKneeText.text = $"Left Knee: {motion.pose.left_knee:F1}°";
        rightKneeText.text = $"Right Knee: {motion.pose.right_knee:F1}°";
    }
}