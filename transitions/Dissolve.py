import cv2


class Dissolve(object):
    def __init__(self, sequence, other):
        """
        Creates a "dissolve" effect from two image sequences.

        :param sequence: the first sequence to dissolve
        :type sequence: list of height x width x channel numpy arrays
        :param other: the second sequence to dissolve
        :type other: list of height x width x channel numpy arrays
        """
        self.sequence = sequence
        self.other = other

        self.sequence_length = len(self.sequence)

    def dissolve(self, gamma=0):
        """
        Creates the dissolve.

        :param gamma: cv2.addWeighted parameter
        :type gamma: float
        :return: a list of height x width x channel numpy arrays representing a "dissolve" effect
        """
        step = 1/self.sequence_length
        alphas = [1 - (step * x) for x in range(0, self.sequence_length)]
        sequence = []
        for x in range(self.sequence_length):
            a = self.sequence[x]
            b = self.other[x]
            dissolved = cv2.addWeighted(a, alphas[x], b, alphas[-(x + 1)], gamma)
            sequence.append(dissolved)
        return sequence
