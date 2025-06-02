import numpy as np

from config import *


def build_triangle_mesh():
    position_data = np.array(
        (-0.75, -0.75, 0.0,
         0.75, -0.75, 0.0,
         0.00, 0.75, 0.0), dtype=np.float32
    )

    color_data = np.array(
        (0, 1, 2), dtype=np.uint32  # unsigned integer
    )

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    position_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, position_buffer)
    glBufferData(GL_ARRAY_BUFFER, position_data.nbytes, position_data,
                 GL_STATIC_DRAW)  # static draw = only one data upload intended
    glVertexAttribPointer(
        0,  # index of the attribute
        3,  # number of elements (x,y,z => 3)
        GL_FLOAT,  # data type of each number
        GL_FALSE,  # if floating point numbers should be normalized
        12,  # stride: number of bytes to go from one attribute to the next: 32 bits * 3 elements / 8 = 12 bytes
        ctypes.c_void_p(0)  # offset: where the first position is
    )
    glEnableVertexAttribArray(0)

    color_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, color_buffer)
    glBufferData(GL_ARRAY_BUFFER, color_data.nbytes, color_data,
                 GL_STATIC_DRAW)  # static draw = online one data upload intended
    glVertexAttribIPointer(
        1,  # index of the attribute
        1,  # number of elements
        GL_UNSIGNED_INT,  # data type of each number
        4,  # number of bytes to go from one attribute to the next: 32 bit = 4 byte
        ctypes.c_void_p(0)  # offset, where the first position is
    )
    glEnableVertexAttribArray(1)

    return position_buffer, color_buffer, vao


def build_colored_cube_mesh():
    vertices = np.array([
        # front
        (-0.5, 0.5, 0.5, 0),  # top left
        (0.5, 0.5, 0.5, 1),  # top right
        (0.5, -0.5, 0.5, 2),  # bottom right
        (-0.5, -0.5, 0.5, 3),  # bottom left
        # back
        (-0.5, 0.5, -0.5, 2),  # top left
        (0.5, 0.5, -0.5, 3),  # top right
        (0.5, -0.5, -0.5, 0),  # bottom right
        (-0.5, -0.5, -0.5, 1)  # bottom left
    ], dtype=vertex_datatype)

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    glVertexAttribPointer(
        0,
        3,
        GL_FLOAT,
        GL_FALSE,
        vertex_datatype.itemsize,
        ctypes.c_void_p(0)
    )

    glVertexAttribIPointer(
        1,
        1,
        GL_UNSIGNED_INT,
        vertex_datatype.itemsize,
        ctypes.c_void_p(12)
    )

    glEnableVertexAttribArray(0)
    glEnableVertexAttribArray(1)

    indices = np.array([
        0, 1, 2, 0, 2, 3,  # front face
        1, 5, 6, 1, 6, 2,  # right face
        5, 4, 7, 5, 7, 6,  # back face
        4, 0, 3, 4, 3, 7,  # left face
        4, 5, 1, 4, 1, 0,  # top face
        3, 2, 6, 3, 6, 7  # bottom face
    ], dtype=np.uint32)

    ebo = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    return ebo, vbo, vao


def build_line_cube_mesh():
    vertices = np.array((
        -0.5, 0.5, 0.5,  # 0 front top left
        0.5, 0.5, 0.5,  # 1 front top right
        0.5, -0.5, 0.5,  # 2 front bottom right
        -0.5, -0.5, 0.5,  # 3 front bottom left
        -0.5, 0.5, -0.5,  # 4 back top left
        0.5, 0.5, -0.5,  # 5 back top right
        0.5, -0.5, -0.5,  # 6 back bottom right
        -0.5, -0.5, -0.5,  # 7 back bottom left
    ), dtype=np.float32)

    # define the edges between the vertices
    indices = np.array((
        0, 1, 1, 2, 2, 3, 3, 0,  # front face
        4, 5, 5, 6, 6, 7, 7, 4,  # back face
        0, 4, 1, 5, 2, 6, 3, 7  # sides
    ), np.uint32)

    return build_line_mesh(vertices, indices)


def build_pyramid_mesh():
    vertices = np.array((
        -0.0, 0.0, -0.1,
        0.3, 0.0, -0.0,
        0.0, 0.0, 0.1,
        -0.3, 0.0, 0.0,
        0.0, 0.5, 0.0,
        0.0, -0.5, 0.0,
        -0.0, -0.8, -0.1,
        0.3, -0.8, 0.0,
        0.0, -0.8, 0.1,
        -0.3, -0.8, 0.0,
    ), np.float32)

    indices = np.array((
        0, 1, 1, 2, 2, 3, 3, 0,  # bottom face
        0, 4, 1, 4, 2, 4, 3, 4,  # connections to top
        0, 5, 1, 5, 2, 5, 3, 5,
        6, 7, 7, 8, 8, 9, 9, 6,
        6, 5, 7, 5, 8, 5, 9, 5
    ), np.uint32)

    return build_line_mesh(vertices, indices)


def build_line_mesh(vertices, indices):
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    ebo = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    glVertexAttribPointer(
        0,
        3,
        GL_FLOAT,
        GL_FALSE,
        12,
        ctypes.c_void_p(0)
    )
    glEnableVertexAttribArray(0)

    return ebo, vbo, vao
