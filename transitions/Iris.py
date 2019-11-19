import cv2
import numpy as np


class Iris(object):
    def __init__(self, sequence):
        """
        Creates an "iris" effect mimicking the opening and closing of a film camera lens.

        :param sequence: the images to perform the iris effect on
        :type sequence: list of height x width x channel numpy arrays
        """
        self.sequence = sequence
        self.sequence_length = len(sequence)

    def iris(self, iris_in=False):
        """
        TODO: currently the iris effect stops when the diameter is larger than the shortest side (height) rather than
            all the way to the longest side (width).

        Creates the iris.

        :param iris_in: whether to "iris in" rather than "iris out"
        :type iris_in: bool
        :return: a list of height x width x channel numpy arrays representing an "iris" effect
        """
        height, width = self.sequence[0].shape[:2]
        s = min(width, height)
        center_x = int(width/2)
        center_y = int(height/2)
        mask_template = np.zeros(self.sequence[0].shape, dtype='uint8')

        step = 1/self.sequence_length
        radii = [(step * x) for x in range(self.sequence_length + 1)]
        sequence = []
        for x in range(self.sequence_length):
            if iris_in:
                radius = int((s * radii[x])/2)
            else:
                radius = int((s * radii[-(x + 1)])/2)

            mask = mask_template.copy()
            cv2.circle(mask, (center_x, center_y), radius, color=(255, 255, 255), thickness=-1)
            img = self.sequence[x]
            c = cv2.bitwise_and(img, mask)
            sequence.append(c)
        return sequence
