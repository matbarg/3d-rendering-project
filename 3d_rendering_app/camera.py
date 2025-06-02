import numpy as np
from transformation import Transform


class Camera:
    def __init__(self, initial_x=0, initial_y=0, initial_z=0):
        self.__camera_pos = np.array([initial_x, initial_y, initial_z], dtype=np.float32)
        self.__target_vec = np.array([0, 0, 1], dtype=np.float32)  # points towards positive z-axis
        self.__up_vec = np.array([0, 1, 0], dtype=np.float32)  # aligned with the y-axis
        self.__move_speed = 0.1  # scaling factor of movement added per frame
        self.__camera_speed = 1.5  # degrees of turning per frame

    def move_forward(self):
        # the target vector is used to move forward, scaled by the movement speed
        self.__camera_pos += self.__target_vec * self.__move_speed

    def move_backward(self):
        # the target vector is used to move backward, scaled by the movement speed
        self.__camera_pos -= self.__target_vec * self.__move_speed

    def move_left(self):
        # the target vector is used to move backward, scaled by the movement speed
        left_vec = np.linalg.cross(self.__target_vec, self.__up_vec)
        left_vec = left_vec / np.linalg.norm(left_vec)  # normalized vector
        self.__camera_pos += left_vec * self.__move_speed

    def move_right(self):
        # the target vector is used to move backward, scaled by the movement speed
        left_vec = np.linalg.cross(self.__up_vec, self.__target_vec)
        left_vec = left_vec / np.linalg.norm(left_vec)  # normalized vector
        self.__camera_pos += left_vec * self.__move_speed

    def move_up(self):
        self.__camera_pos += self.__up_vec * self.__move_speed

    def move_down(self):
        self.__camera_pos -= self.__up_vec * self.__move_speed

    def rotate_left(self):
        self.__target_vec = (Transform()
                             .add_rotation_y(-self.__camera_speed)
                             .mult_vec3_from_right(self.__target_vec))

    def rotate_right(self):
        self.__target_vec = (Transform()
                             .add_rotation_y(self.__camera_speed)
                             .mult_vec3_from_right(self.__target_vec))

    def rotate_up(self):
        target_x = self.__target_vec[0]
        target_y = self.__target_vec[1]
        target_z = self.__target_vec[2]

        # x angle between the z axis and the current target vector
        alpha = np.degrees(np.atan2(target_x, target_z))

        self.__target_vec = (Transform()
                             .add_rotation_y(-alpha)
                             .add_rotation_x(-self.__camera_speed)
                             .add_rotation_y(alpha)
                             .mult_vec3_from_right(self.__target_vec))

    def rotate_down(self):
        target_x = self.__target_vec[0]
        target_y = self.__target_vec[1]
        target_z = self.__target_vec[2]

        # x angle between the z axis and the current target vector
        alpha = np.degrees(np.atan2(target_x, target_z))

        self.__target_vec = (Transform()
                             .add_rotation_y(-alpha)
                             .add_rotation_x(self.__camera_speed)
                             .add_rotation_y(alpha)
                             .mult_vec3_from_right(self.__target_vec))

    def get_matrix(self):
        n_vec = self.__target_vec
        u_vec = np.linalg.cross(self.__up_vec, n_vec)
        v_vec = np.linalg.cross(n_vec, u_vec)

        u_vec = u_vec / np.linalg.norm(u_vec)
        v_vec = v_vec / np.linalg.norm(v_vec)
        n_vec = n_vec / np.linalg.norm(n_vec)

        camera_rotation = np.array([
            [u_vec[0], u_vec[1], u_vec[2], 0],
            [v_vec[0], v_vec[1], v_vec[2], 0],
            [n_vec[0], n_vec[1], n_vec[2], 0],
            [0, 0, 0, 1]], dtype=np.float32
        )

        camera_translation = np.array([
            [1, 0, 0, -self.__camera_pos[0]],
            [0, 1, 0, -self.__camera_pos[1]],
            [0, 0, 1, -self.__camera_pos[2]],
            [0, 0, 0, 1]], dtype=np.float32
        )

        return camera_rotation.dot(camera_translation)
