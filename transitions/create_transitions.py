import cv2
import numpy as np

from transitions import Cut, Wipe, Fade, Dissolve, Iris


def cut(sequence, other, frame):
    """
    Creates a simple "cut" between two image sequences.

    :param sequence: the first sequence of images
    :type sequence: list of height x width x channel numpy arrays
    :param other: the second sequence of images
    :type other:  list of height x width x channel numpy arrays
    :param frame: position in frames at which to combine the first and second sequences
    :type frame: int
    :return: a list of height x width x channel numpy arrays of the combined sequence
    """
    sequence = sequence[:frame] + other[frame:]
    cut = Cut(sequence)
    return cut


def dissolve(sequence, other, gamma=0):
    """
    Creates a "dissolve" effect from two image sequences.

    :param sequence: the first sequence of images
    :type sequence: list of height x width x channel numpy arrays
    :param other: the second sequence of images
    :type other:  list of height x width x channel numpy arrays
    :param gamma: cv2.addWeighted parameter
    :type gamma: float
    :return: a list of height x width x channel numpy arrays representing a "dissolve" effect
    """
    duration = len(sequence)
    step = 1 / duration
    alphas = [1 - (step * x) for x in range(0, duration)]
    s = []
    for x in range(duration):
        a = sequence[x]
        b = other[x]
        alpha = alphas[x]
        beta = 1 - alpha
        dissolved = cv2.addWeighted(a, alpha, b, beta, gamma)
        s.append(dissolved)
    dissolve = Dissolve(s)
    return dissolve


def fade(sequence, gamma=0, fade_in=False):
    """
    Creates a fade from a list of numpy arrays.

    :param gamma: cv2.addWeighted parameter
    :type gamma: float
    :param fade_in: fade in rather than fade out
    :type fade_in: bool
    :return: a list of numpy arrays representing a fade
    """
    duration = len(sequence)
    mask = np.zeros(sequence[0].shape, dtype='uint8')
    step = 1/duration
    alphas = [x * step for x in range(1, duration + 1)]
    s = []
    for x in range(duration):
        img = sequence[x]
        if fade_in:
            alpha = alphas[x]
            beta = alphas[-x]
        else:
            alpha = alphas[-x]
            beta = alphas[x]
        combined = cv2.addWeighted(img, alpha, mask.copy(), beta, gamma)
        s.append(combined)
    fade = Fade(s)
    return fade


def hwipe(sequence, other, reverse=False):
    """
    Performs a horizontal "wipe."

    :param reverse: wipe from right to left (vs left to right)
    :type reverse: bool
    :return: a list of height x width x channel numpy arrays
    """
    duration = len(sequence)
    w = sequence[0].shape[1]
    step = w/duration
    slices_a = [sequence[x][:, int(step * (x + 1)):, :] for x in range(0, duration)]
    slices_b = [other[x][:, w - int(step * (x + 1)):, :] for x in range(0, duration)]
    s = []
    for x in range(duration):
        if reverse:
            ac = slices_b[x]
            bc = slices_a[x]
        else:
            ac = slices_a[x]
            bc = slices_b[x]
        c = np.concatenate([bc, ac], axis=1)
        s.append(c)
    wipe = Wipe([sequence[0]] + s[1:], type='horizontal')
    return wipe


def vwipe(sequence, other, reverse=False):
    duration = len(sequence)
    h = sequence[0].shape[0]
    step = h/duration
    slices_a = [sequence[x][int(step * (x + 1)):, :, :] for x in range(0, duration)]
    slices_b = [other[x][h - int(step * (x + 1)):, :, :] for x in range(0, duration)]
    s = []
    for x in range(duration):
        if reverse:
            ac = slices_b[x]
            bc = slices_a[x]
        else:
            ac = slices_a[x]
            bc = slices_b[x]
        c = np.concatenate([bc, ac], axis=0)
        s.append(c)
    wipe = Wipe(s, type='vertical')
    return wipe


def iris(sequence, iris_in=False):
    """
    TODO: currently the iris effect stops when the diameter is larger than the shortest side (height) rather than
        all the way to the longest side (width).

    Creates the iris.

    :param iris_in: whether to "iris in" rather than "iris out"
    :type iris_in: bool
    :return: a list of height x width x channel numpy arrays representing an "iris" effect
    """
    duration = len(sequence)
    height, width = sequence[0].shape[:2]
    s = min(width, height)
    center_x = int(width/2)
    center_y = int(height/2)
    mask_template = np.zeros(sequence[0].shape, dtype='uint8')

    step = 1/duration
    radii = [(step * x) for x in range(duration + 1)]
    s = []
    for x in range(duration):
        if iris_in:
            radius = int((s * radii[x])/2)
        else:
            radius = int((s * radii[-(x + 1)])/2)

        mask = mask_template.copy()
        cv2.circle(mask, (center_x, center_y), radius, color=(255, 255, 255), thickness=-1)
        img = sequence[x]
        c = cv2.bitwise_and(img, mask)
        c = cv2.GaussianBlur(c, (5, 5), 0)
        s.append(c)
    iris = Iris(s)
    return iris
