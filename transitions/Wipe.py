import numpy as np


class Wipe(object):
    def __init__(self, sequence, other):
        """
        Creates a "wipe" effect where it looks like image A pushes image B off the screen either horizontally or
        vertically.

        :param sequence: image A
        :type sequence: list of height x width x channel numpy arrays
        :param other: image B
        :type other: list of height x width x channel numpy arrays
        """
        self.sequence = sequence
        self.other = other
        self.sequence_length = len(sequence)

    def hwipe(self, reverse=False):
        """
        Performs a horizontal "wipe."

        :param reverse: wipe from right to left (vs left to right)
        :type reverse: bool
        :return: a list of height x width x channel numpy arrays
        """
        w = self.sequence[0].shape[1]
        step = w/self.sequence_length
        slices_a = [self.sequence[x][:, int(step * (x + 1)):, :] for x in range(0, self.sequence_length)]
        slices_b = [self.other[x][:, w - int(step * (x + 1)):, :] for x in range(0, self.sequence_length)]
        sequence = []
        for x in range(self.sequence_length):
            if reverse:
                ac = slices_b[x]
                bc = slices_a[x]
            else:
                ac = slices_a[x]
                bc = slices_b[x]
            c = np.concatenate([bc, ac], axis=1)
            sequence.append(c)
        return sequence

    def vwipe(self, reverse=False):
        h = self.sequence[0].shape[0]
        step = h/self.sequence_length
        slices_a = [self.sequence[x][int(step * (x + 1)):, :, :] for x in range(0, self.sequence_length)]
        slices_b = [self.other[x][h - int(step * (x + 1)):, :, :] for x in range(0, self.sequence_length)]
        sequence = []
        for x in range(self.sequence_length):
            if reverse:
                ac = slices_b[x]
                bc = slices_a[x]
            else:
                ac = slices_a[x]
                bc = slices_b[x]
            c = np.concatenate([bc, ac], axis=0)
            sequence.append(c)
        return sequence
