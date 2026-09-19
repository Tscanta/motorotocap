from motion import calculate_angle


def point(landmark):
    """
    Convert a MediaPipe landmark into a simple XYZ list.
    """
    return [
        landmark.x,
        landmark.y,
        landmark.z
    ]


def process_pose(landmarks):
    """
    Convert MediaPipe pose landmarks into MotionLens motion data.

    Returns a dictionary containing joint angles.
    """

    # --------------------------------------------------------
    # Upper body
    # --------------------------------------------------------

    left_shoulder = landmarks[11]
    right_shoulder = landmarks[12]

    left_elbow = landmarks[13]
    right_elbow = landmarks[14]

    left_wrist = landmarks[15]
    right_wrist = landmarks[16]


    # --------------------------------------------------------
    # Lower body
    # --------------------------------------------------------

    left_hip = landmarks[23]
    right_hip = landmarks[24]

    left_knee = landmarks[25]
    right_knee = landmarks[26]

    left_ankle = landmarks[27]
    right_ankle = landmarks[28]


    # --------------------------------------------------------
    # Elbow angles
    # --------------------------------------------------------

    left_elbow_angle = calculate_angle(
        point(left_shoulder),
        point(left_elbow),
        point(left_wrist)
    )

    right_elbow_angle = calculate_angle(
        point(right_shoulder),
        point(right_elbow),
        point(right_wrist)
    )


    # --------------------------------------------------------
    # Knee angles
    # --------------------------------------------------------

    left_knee_angle = calculate_angle(
        point(left_hip),
        point(left_knee),
        point(left_ankle)
    )

    right_knee_angle = calculate_angle(
        point(right_hip),
        point(right_knee),
        point(right_ankle)
    )


    # --------------------------------------------------------
    # MotionLens output
    # --------------------------------------------------------

    motion = {
        "left_elbow": round(float(left_elbow_angle), 2),
        "right_elbow": round(float(right_elbow_angle), 2),
        "left_knee": round(float(left_knee_angle), 2),
        "right_knee": round(float(right_knee_angle), 2)
    }

    return motion