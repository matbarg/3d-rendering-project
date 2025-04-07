import glfw
import numpy as np
from OpenGL.GL import *
import ctypes
from OpenGL.GL.shaders import compileProgram, compileShader


def main():
    glfw.init()
    window = glfw.create_window(1000, 800, "3D Rendering Program", None, None)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == '__main__':
    main()
