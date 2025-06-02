import glfw
import numpy as np

from config import *
import mesh_factory
from transformation import Transform
from camera import Camera


class App:
    def __init__(self):
        self.initialize_glfw()
        self.initialize_opengl()
        self.camera = Camera(initial_z=-2)

    def initialize_glfw(self):
        glfw.init()
        glfw.window_hint(GLFW_CONSTANTS.GLFW_OPENGL_PROFILE, GLFW_CONSTANTS.GLFW_OPENGL_CORE_PROFILE)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_OPENGL_FORWARD_COMPAT, GLFW_CONSTANTS.GLFW_TRUE)  # necessary on Mac

        self.window = glfw.create_window(SCREEN_WIDTH, SCREEN_HEIGHT, "3D Rendering Program", None, None)
        glfw.make_context_current(self.window)

    def initialize_opengl(self):
        glClearColor(0.2, 0.2, 0.3, 1.0)  # set the displayed color of the window

        # Enable depth testing
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)

        self.ebo, self.vbo, self.vao = mesh_factory.build_colored_cube_mesh()
        # glBindVertexArray(self.triangle_vao)
        self.shader = create_shader_program("shaders/vertex.txt", "shaders/fragment.txt")

    def render(self):
        while not glfw.window_should_close(self.window):
            if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_ESCAPE) == GLFW_CONSTANTS.GLFW_PRESS:
                break  # close the window on esc key

            self.query_camera_controls()

            glfw.poll_events()  # clears the event queue, otherwise the event buffer would overflow

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # clears the color of the screen
            glUseProgram(self.shader)

            trans = (Transform()
                     # .add_rotation_y(np.degrees(glfw.get_time()))
                     # .add_translation(z_amount=0)
                     # .add_scale(z_amount=3)
                     # .add_rotation_z(90)
                     # .add_rotation_y(np.degrees(glfw.get_time()))
                     .add_matrix(matrix=self.camera.get_matrix())
                     .add_perspective()
                     )

            uniform_location = glGetUniformLocation(self.shader, "model")
            glUniformMatrix4fv(uniform_location, 1, GL_TRUE, trans.matrix)
            # glDrawElements(GL_LINES, 24, GL_UNSIGNED_INT, None)
            glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, None)

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


def main() -> None:
    my_app = App()
    my_app.render()
    my_app.quit()


if __name__ == '__main__':
    main()
