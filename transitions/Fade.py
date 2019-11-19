import cv2
import numpy as np


class Fade(object):
    def __init__(self, sequence):
        """
        Creates a "fade in" or "fade out."

        :param sequence: images to perform fade effect on
        :type sequence: list of height x width x channel numpy arrays
        """
        self.sequence = sequence
        self.sequence_length = len(self.sequence)

    def fade(self, gamma=0, fade_in=False):
        """
        Creates a fade from a list of numpy arrays.

        :param gamma: cv2.addWeighted parameter
        :type gamma: float
        :param fade_in: fade in rather than fade out
        :type fade_in: bool
        :return: a list of numpy arrays representing a fade
        """
        mask = np.zeros(self.sequence[0].shape, dtype='uint8')
        step = 1/self.sequence_length
        alphas = [x * step for x in range(1, self.sequence_length + 1)]
        sequence = []
        for x in range(self.sequence_length):
            img = self.sequence[x]
            if fade_in:
                alpha = alphas[x]
                beta = alphas[-x]
            else:
                alpha = alphas[-x]
                beta = alphas[x]
            combined = cv2.addWeighted(img, alpha, mask.copy(), beta, gamma)
            sequence.append(combined)
        return sequence
