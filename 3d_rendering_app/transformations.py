import numpy as np
from config import ASPECT_RATIO as AR

"""
Class to create transformation matrices.

Methods can be chained like so:
custom_transform = Transform().add_scale_evenly(2).add_translation(x_amount=0.5).add_perspective()

Access the final matrix:
custom_transform.matrix
"""
class Transform:
    def __init__(self):
        self.matrix = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]], dtype=np.float32
        )  # identity matrix

    def add_rotation_x(self, degree):
        c = np.cos(np.radians(degree))
        s = np.sin(np.radians(degree))

        transform = np.array([
            [1, 0, 0, 0],
            [0, c, -s, 0],
            [0, s, c, 0],
            [0, 0, 0, 1]], dtype=np.float32
        )

        self.matrix = transform.dot(self.matrix)

        return self

    def add_rotation_y(self, degree):
        c = np.cos(np.radians(degree))
        s = np.sin(np.radians(degree))

        transform = np.array([
            [c, 0, s, 0],
            [0, 1, 0, 0],
            [-s, 0, c, 0],
            [0, 0, 0, 1]], dtype=np.float32
        )

        self.matrix = transform.dot(self.matrix)

        return self

    def add_rotation_z(self, degree):
        c = np.cos(np.radians(degree))
        s = np.sin(np.radians(degree))

        transform = np.array([
            [c, -s, 0, 0],
            [s, c, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]], dtype=np.float32
        )

        self.matrix = transform.dot(self.matrix)

        return self

    def add_translation(self, x_amount=0, y_amount=0, z_amount=0):
        transform = np.array([
            [1, 0, 0, x_amount],
            [0, 1, 0, y_amount],
            [0, 0, 1, z_amount],
            [0, 0, 0, 1]], dtype=np.float32
        )

        self.matrix = transform.dot(self.matrix)

        return self

    def add_scale(self, x_amount=1, y_amount=1, z_amount=1):
        transform = np.array([
            [x_amount, 0, 0, 0],
            [0, y_amount, 0, 0],
            [0, 0, z_amount, 0],
            [0, 0, 0, 1]], dtype=np.float32
        )

        self.matrix = transform.dot(self.matrix)

        return self

    def add_scale_evenly(self, amount):
        transform = np.array([
            [amount, 0, 0, 0],
            [0, amount, 0, 0],
            [0, 0, amount, 0],
            [0, 0, 0, 1]], dtype=np.float32
        )

        self.matrix = transform.dot(self.matrix)

        return self

    """
    Z Transform:
    Z values need to be mapped between -1 to 1 so OpenGL can correctly handle depth testing
    near_z and far_z are needed to determine the range of -1 to 1 (everything outside will be clipped)
    """

    def add_perspective(self, fov=90, near_z=1, far_z=10):
        tan_half_fov = np.tan(np.radians(fov / 2))
        d = 1 / tan_half_fov  # z distance from camera origin

        z_range = near_z - far_z
        a = (-far_z - near_z) / z_range
        b = (2 * far_z * near_z) / z_range

        transform = np.array([
            # dividing by the aspect ratio keeps the x coordinate from being stretched to the viewport
            [d / AR, 0, 0, 0],
            [0, d, 0, 0],
            [0, 0, a, b],
            [0, 0, 1, 0]], dtype=np.float32
        )

        self.matrix = transform.dot(self.matrix)

        return self
