import numpy as np


def calculate_angle(a, b, c):
    """
    Calculate the angle ABC.

    a = first point
    b = middle/joint point
    c = third point
    """

    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    c = np.array(c, dtype=float)

    # Vectors from the joint
    ba = a - b
    bc = c - b

    # Prevent division by zero
    ba_norm = np.linalg.norm(ba)
    bc_norm = np.linalg.norm(bc)

    if ba_norm == 0 or bc_norm == 0:
        return 0.0

    # Calculate cosine of the angle
    cosine_angle = np.dot(ba, bc) / (ba_norm * bc_norm)

    # Protect against floating-point errors
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)

    # Convert radians to degrees
    angle = np.degrees(np.arccos(cosine_angle))

    return angle