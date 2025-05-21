import glfw
import numpy as np

from config import *
import mesh_factory
from transformations import Transform


def draw_rotating_triangle(uniform_location):
    transform1 = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, -0.3],
        [0, 0, 1, 0],
        [0, 0, 0, 1]], dtype=np.float32
    )

    c = np.cos(glfw.get_time())
    s = np.sin(glfw.get_time())
    transform2 = np.array([
        [c, -s, 0, 0],
        [s, c, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]], dtype=np.float32
    )

    transform = transform2.dot(transform1)

    glUniformMatrix4fv(uniform_location, 1, GL_TRUE, transform)

    glDrawArrays(GL_TRIANGLES, 0, 3)  # every three points are taken together as a single solid shape


def draw_rotating_cube(uniform_location):
    transform = (Transform()
                 .add_rotation_y(np.degrees(glfw.get_time()))
                 .add_translation(z_amount=2)
                 .add_perspective(fov=90, near_z=1, far_z=10)
                 )

    glUniformMatrix4fv(uniform_location, 1, GL_TRUE, transform.matrix)
    glDrawElements(GL_LINES, 24, GL_UNSIGNED_INT, None)  # count is the number of indices to connect with lines


class App:
    def __init__(self):
        self.initialize_glfw()
        self.initialize_opengl()

        # fields used for basic camera inputs
        self.rotate_x_input = 0
        self.rotate_y_input = 0
        self.translate_x_input = 0
        self.translate_y_input = 0
        self.translate_z_input = 2  # the scene needs some distance to the camera to be visible

    def initialize_glfw(self):
        glfw.init()
        glfw.window_hint(GLFW_CONSTANTS.GLFW_OPENGL_PROFILE, GLFW_CONSTANTS.GLFW_OPENGL_CORE_PROFILE)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_OPENGL_FORWARD_COMPAT, GLFW_CONSTANTS.GLFW_TRUE)  # necessary on Mac

        self.window = glfw.create_window(SCREEN_WIDTH, SCREEN_HEIGHT, "3D Rendering Program", None, None)
        glfw.make_context_current(self.window)

    def initialize_opengl(self):
        glClearColor(0.1, 0.1, 0.1, 1.0)  # set the displayed color of the window
        self.ebo, self.vbo, self.vao = mesh_factory.build_cube_mesh()
        # glBindVertexArray(self.triangle_vao)
        self.shader = create_shader_program("shaders/vertex.txt", "shaders/fragment.txt")

    def run(self):
        while not glfw.window_should_close(self.window):
            if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_ESCAPE) == GLFW_CONSTANTS.GLFW_PRESS:
                break  # close the window esc key

            self.add_basic_controls()

            glfw.poll_events()  # clears the event queue, otherwise the event buffer would overflow

            glClear(GL_COLOR_BUFFER_BIT)  # clears the color of the screen
            glUseProgram(self.shader)

            uniform_location = glGetUniformLocation(self.shader, "model")

            glUniformMatrix4fv(uniform_location, 1, GL_TRUE, self.get_basic_camera_matrix())
            glDrawElements(GL_LINES, 24, GL_UNSIGNED_INT, None)

            glfw.swap_buffers(self.window)

    """
    The functions adds basic inputs to mimic camera like controls.
    (Needs to be called from within the window loop)
    Control scheme:
    W/S – z translation (move front/back)
    A/D – x translation (move left/right)
    SPACE/LEFT_SHIFT – y translation (move up/down)
    UP/DOWN – x rotation (tilt up/down)
    LEFT/RIGHT – y rotation (tilt left/right)
    """
    def add_basic_controls(self):
        if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_RIGHT) == GLFW_CONSTANTS.GLFW_PRESS:
            self.rotate_y_input = self.rotate_y_input - 1

        if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_LEFT) == GLFW_CONSTANTS.GLFW_PRESS:
            self.rotate_y_input = self.rotate_y_input + 1

        if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_UP) == GLFW_CONSTANTS.GLFW_PRESS:
            self.rotate_x_input = self.rotate_x_input + 1

        if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_DOWN) == GLFW_CONSTANTS.GLFW_PRESS:
            self.rotate_x_input = self.rotate_x_input - 1

        if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_D) == GLFW_CONSTANTS.GLFW_PRESS:
            self.translate_x_input = self.translate_x_input - 0.05

        if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_A) == GLFW_CONSTANTS.GLFW_PRESS:
            self.translate_x_input = self.translate_x_input + 0.05

        if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_SPACE) == GLFW_CONSTANTS.GLFW_PRESS:
            self.translate_y_input = self.translate_y_input - 0.05

        if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_LEFT_SHIFT) == GLFW_CONSTANTS.GLFW_PRESS:
            self.translate_y_input = self.translate_y_input + 0.05

        if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_W) == GLFW_CONSTANTS.GLFW_PRESS:
            self.translate_z_input = self.translate_z_input - 0.05

        if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_S) == GLFW_CONSTANTS.GLFW_PRESS:
            self.translate_z_input = self.translate_z_input + 0.05

    """
    The function creates a transformation matrix based on the current inputs.
    (Needs to be called from within the window loop).
    The returned matrix can be uploaded to the vertex shader (vertex.txt) via a uniform. 
    """
    def get_basic_camera_matrix(self):
        return (Transform()
                .add_rotation_x(self.rotate_x_input)
                .add_rotation_y(self.rotate_y_input)
                .add_translation(x_amount=self.translate_x_input,
                                 y_amount=self.translate_y_input,
                                 z_amount=self.translate_z_input)
                .add_perspective(fov=90, near_z=1, far_z=10)).matrix

    def quit(self):
        glDeleteBuffers(2, (self.vbo, self.ebo))
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteProgram(self.shader)
        glfw.destroy_window(self.window)
        glfw.terminate()


if __name__ == '__main__':
    my_app = App()
    my_app.run()
    my_app.quit()
