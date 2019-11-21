from pathlib import Path

import cv2


class Transition(object):
    def __init__(self, images):
        self.images = images
        self.duration = len(images)

    def show(self):
        for image in self.images:
            cv2.imshow('images', image)
            cv2.waitKey(24)

    def save(self, path):
        if not Path(path).exists():
            Path.mkdir(Path(path))
        for num, image in enumerate(self.images):
            save_path = f'{path}/{num}.jpg'
            cv2.imwrite(save_path, image)


class Wipe(Transition):
    def __init__(self, images, type='horizontal'):
        super().__init__(images)
        """
        Creates a "wipe" effect where it looks like image A pushes image B off the screen either horizontally or
        vertically.

        :param images: image A
        :type sequence: list of height x width x channel numpy arrays
        """
        self.images = images
        self.type = type
        self.duration = len(images)


class Fade(object):
    def __init__(self, images):
        """
        Creates a "fade in" or "fade out."

        :param images: images to perform fade effect on
        :type images: list of height x width x channel numpy arrays
        """
        self.images = images
        self.duration = len(self.images)


class Iris(object):
    def __init__(self, images):
        """
        Creates an "iris" effect mimicking the opening and closing of a film camera lens.

        :param images: the images to perform the iris effect on
        :type images: list of height x width x channel numpy arrays
        """
        self.images = images
        self.duration = len(images)


class Cut(object):
    def __init__(self, images):
        self.images = images
        self.duration = len(self.images)


class Dissolve(object):
    def __init__(self, images):
        """
        Creates a "dissolve" effect from two image sequences.

        :param images: the first sequence to dissolve
        :type images: list of height x width x channel numpy arrays
        """
        self.images = images
        self.duration = len(self.images)