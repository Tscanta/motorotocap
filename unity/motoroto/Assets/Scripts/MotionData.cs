using System;

[Serializable]
public class MotionData
{
    public long timestamp;
    public PoseData pose;
    public Landmarks landmarks;
}

[Serializable]
public class PoseData
{
    public float left_elbow;
    public float right_elbow;
    public float left_knee;
    public float right_knee;
}

[Serializable]
public class Landmarks
{
    public Landmark nose;
    public Landmark left_shoulder;
    public Landmark right_shoulder;
    public Landmark left_elbow;
    public Landmark right_elbow;
    public Landmark left_wrist;
    public Landmark right_wrist;
    public Landmark left_hip;
    public Landmark right_hip;
    public Landmark left_knee;
    public Landmark right_knee;
    public Landmark left_ankle;
    public Landmark right_ankle;
}

[Serializable]
public class Landmark
{
    public float x;
    public float y;
    public float z;
    public float visibility;
}