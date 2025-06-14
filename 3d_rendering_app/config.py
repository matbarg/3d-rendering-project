import glfw
import glfw.GLFW as GLFW_CONSTANTS
import numpy as np
from OpenGL.GL import *
import ctypes
from OpenGL.GL.shaders import compileProgram, compileShader


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
ASPECT_RATIO = SCREEN_WIDTH / SCREEN_HEIGHT  # / operator always returns floats in python

vertex_datatype = np.dtype({
    "names": ["x", "y", "z", "color"],
    "formats": [np.float32, np.float32, np.float32, np.uint32],
    "offsets": [0, 4, 8, 12],
    "itemsize": 16
})


def create_shader_program(vertex_filepath, fragment_filepath):
    vertex_module = create_shader_module(vertex_filepath, GL_VERTEX_SHADER)
    fragment_module = create_shader_module(fragment_filepath, GL_FRAGMENT_SHADER)

    shader = compileProgram(vertex_module, fragment_module)
    """
    In the tutorial, the two shader modules are deleted with glDeleteShader() 
    to save performance, but this caused an error for me.
    """
    return shader


def create_shader_module(filepath, module_type):
    with open(filepath, "r") as file:
        source_code = file.readlines()

    # takes in the source code as string and an int indicating the shader type, e.g. GL_VERTEX_SHADER
    return compileShader(source_code, module_type)
