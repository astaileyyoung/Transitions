class Cut(object):
    def __init__(self, sequence, other):
        """
        Creates a simple "cut" between two image sequences.

        :param sequence: the first sequence of images
        :type sequence: list of height x width x channel numpy arrays
        :param other: the second sequence of images
        :type other:  list of height x width x channel numpy arrays
        """
        self.sequence = sequence
        self.other = other
        self.sequence_length = len(self.sequence)

    def cut(self, frame):
        """
        Creates the cut.

        :param frame: position in frames at which to combine the first and second sequences
        :type frame: int
        :return: a list of height x width x channel numpy arrays of the combined sequence
        """
        sequence = self.sequence[:frame] + self.other[frame:]
        return sequence
