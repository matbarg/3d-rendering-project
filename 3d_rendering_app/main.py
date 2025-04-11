import glfw
import numpy as np

from config import *
import mesh_factory


class App:
    def __init__(self):
        self.initialize_glfw()
        self.initialize_opengl()

    def initialize_glfw(self):
        glfw.init()
        glfw.window_hint(GLFW_CONSTANTS.GLFW_OPENGL_PROFILE, GLFW_CONSTANTS.GLFW_OPENGL_CORE_PROFILE)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_OPENGL_FORWARD_COMPAT, GLFW_CONSTANTS.GLFW_TRUE)  # necessary on Mac

        self.window = glfw.create_window(SCREEN_WIDTH, SCREEN_HEIGHT, "3D Rendering Program", None, None)
        glfw.make_context_current(self.window)

    def initialize_opengl(self):
        glClearColor(0.1, 0.3, 0.4, 1.0)  # set the displayed color of the window
        self.triangle_vbo, self.triangle_vao = mesh_factory.build_triangle_mesh2()
        glBindVertexArray(self.triangle_vao)
        self.shader = create_shader_program("shaders/vertex.txt", "shaders/fragment.txt")

    def run(self):
        while not glfw.window_should_close(self.window):
            if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_ESCAPE) == GLFW_CONSTANTS.GLFW_PRESS:
                break  # close the window esc key
            glfw.poll_events()  # clears the event queue, otherwise the event buffer would overflow

            glClear(GL_COLOR_BUFFER_BIT)  # clears the color of the screen
            glUseProgram(self.shader)

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

            location = glGetUniformLocation(self.shader, "model")
            glUniformMatrix4fv(location, 1, GL_TRUE, transform)

            glDrawArrays(GL_TRIANGLES, 0, 3)  # every three points are taken together as a single solid shape
            glfw.swap_buffers(self.window)

    def quit(self):
        glDeleteBuffers(1, (self.triangle_vbo,))
        glDeleteVertexArrays(1, (self.triangle_vao,))
        glDeleteProgram(self.shader)
        glfw.destroy_window(self.window)
        glfw.terminate()


if __name__ == '__main__':
    my_app = App()
    my_app.run()
    my_app.quit()
