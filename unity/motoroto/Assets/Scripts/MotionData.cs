using System;

[Serializable]
public class MotionData
{
    public long timestamp;
    public PoseData pose;
}

[Serializable]
public class PoseData
{
    public float left_elbow;
    public float right_elbow;
    public float left_knee;
    public float right_knee;
}