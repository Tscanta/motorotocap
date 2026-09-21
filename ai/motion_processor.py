from motion import calculate_angle


def point(landmark):
    """
    Convert a MediaPipe landmark into an XYZ list.

    Used by calculate_angle().
    """
    return [
        landmark.x,
        landmark.y,
        landmark.z
    ]


def landmark_to_dict(landmark):
    """
    Convert a MediaPipe landmark into a JSON-friendly dictionary.

    x, y, z:
        Position of the landmark.

    visibility:
        MediaPipe's confidence that the landmark is visible.
    """
    return {
        "x": round(float(landmark.x), 4),
        "y": round(float(landmark.y), 4),
        "z": round(float(landmark.z), 4),
        "visibility": round(float(landmark.visibility), 4)
    }


def process_pose(landmarks):
    """
    Convert MediaPipe pose landmarks into MotionLens joint angles.

    Returns:
        {
            "left_elbow": ...,
            "right_elbow": ...,
            "left_knee": ...,
            "right_knee": ...
        }
    """

    # ========================================================
    # Upper body landmarks
    # ========================================================

    left_shoulder = landmarks[11]
    right_shoulder = landmarks[12]

    left_elbow = landmarks[13]
    right_elbow = landmarks[14]

    left_wrist = landmarks[15]
    right_wrist = landmarks[16]


    # ========================================================
    # Lower body landmarks
    # ========================================================

    left_hip = landmarks[23]
    right_hip = landmarks[24]

    left_knee = landmarks[25]
    right_knee = landmarks[26]

    left_ankle = landmarks[27]
    right_ankle = landmarks[28]


    # ========================================================
    # Elbow angles
    # ========================================================

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


    # ========================================================
    # Knee angles
    # ========================================================

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


    # ========================================================
    # MotionLens angle output
    # ========================================================

    motion = {
        "left_elbow": round(
            float(left_elbow_angle),
            2
        ),

        "right_elbow": round(
            float(right_elbow_angle),
            2
        ),

        "left_knee": round(
            float(left_knee_angle),
            2
        ),

        "right_knee": round(
            float(right_knee_angle),
            2
        )
    }

    return motion


def extract_landmarks(landmarks):
    """
    Extract the body landmarks that Unity needs.

    We don't send all 33 MediaPipe landmarks because the prototype
    currently only needs the major arm and leg joints.

    Returns JSON-friendly landmark data.
    """

    body_landmarks = {

        "nose": landmark_to_dict(
            landmarks[0]
        ),

        # ====================================================
        # Upper body
        # ====================================================

        "left_shoulder": landmark_to_dict(
            landmarks[11]
        ),

        "right_shoulder": landmark_to_dict(
            landmarks[12]
        ),

        "left_elbow": landmark_to_dict(
            landmarks[13]
        ),

        "right_elbow": landmark_to_dict(
            landmarks[14]
        ),

        "left_wrist": landmark_to_dict(
            landmarks[15]
        ),

        "right_wrist": landmark_to_dict(
            landmarks[16]
        ),


        # ====================================================
        # Lower body
        # ====================================================

        "left_hip": landmark_to_dict(
            landmarks[23]
        ),

        "right_hip": landmark_to_dict(
            landmarks[24]
        ),

        "left_knee": landmark_to_dict(
            landmarks[25]
        ),

        "right_knee": landmark_to_dict(
            landmarks[26]
        ),

        "left_ankle": landmark_to_dict(
            landmarks[27]
        ),

        "right_ankle": landmark_to_dict(
            landmarks[28]
        )
    }

    return body_landmarks