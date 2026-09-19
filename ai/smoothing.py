class MotionSmoother:
    def __init__(self, alpha=0.35):
        self.alpha = alpha
        self.previous = {}

    def smooth(self, motion):
        smoothed = {}

        for joint, current_value in motion.items():

            if joint not in self.previous:
                smoothed_value = current_value

            else:
                previous_value = self.previous[joint]

                smoothed_value = (
                    self.alpha * current_value
                    + (1 - self.alpha) * previous_value
                )

            smoothed_value = round(smoothed_value, 2)

            smoothed[joint] = smoothed_value
            self.previous[joint] = smoothed_value

        return smoothed
    