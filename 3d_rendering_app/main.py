import glfw
import numpy as np

from config import *
import mesh_factory
from transformation import Transform
from camera import Camera


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
        self.camera = Camera()

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

            self.query_camera_controls()

            glfw.poll_events()  # clears the event queue, otherwise the event buffer would overflow

            glClear(GL_COLOR_BUFFER_BIT)  # clears the color of the screen
            glUseProgram(self.shader)

            trans = (Transform()
                     # .add_rotation_y(np.degrees(glfw.get_time()))
                     .add_translation(z_amount=2)
                     .add_matrix(matrix=self.camera.get_matrix())
                     .add_perspective()
                     )

            uniform_location = glGetUniformLocation(self.shader, "model")
            glUniformMatrix4fv(uniform_location, 1, GL_TRUE, trans.matrix)
            glDrawElements(GL_LINES, 24, GL_UNSIGNED_INT, None)

            glfw.swap_buffers(self.window)

    """
    The functions queries for keyboard input to trigger camera positioning/rotation.
    (Needs to be called from within the window loop)
    Control scheme:
    W/S – move front/back
    A/D – move left/right
    SPACE/LEFT_SHIFT – move up/down
    LEFT/RIGHT – tilt left/right
    UP/DOWN – tilt up/down
    """

    def query_camera_controls(self):
        if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_W) == GLFW_CONSTANTS.GLFW_PRESS:
            self.camera.move_forward()

        if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_S) == GLFW_CONSTANTS.GLFW_PRESS:
            self.camera.move_backward()

        if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_A) == GLFW_CONSTANTS.GLFW_PRESS:
            self.camera.move_left()

        if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_D) == GLFW_CONSTANTS.GLFW_PRESS:
            self.camera.move_right()

        if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_SPACE) == GLFW_CONSTANTS.GLFW_PRESS:
            self.camera.move_up()

        if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_LEFT_SHIFT) == GLFW_CONSTANTS.GLFW_PRESS:
            self.camera.move_down()

        if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_LEFT) == GLFW_CONSTANTS.GLFW_PRESS:
            self.camera.rotate_left()

        if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_RIGHT) == GLFW_CONSTANTS.GLFW_PRESS:
            self.camera.rotate_right()

        if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_UP) == GLFW_CONSTANTS.GLFW_PRESS:
            self.camera.rotate_up()

        if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_DOWN) == GLFW_CONSTANTS.GLFW_PRESS:
            self.camera.rotate_down()

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
