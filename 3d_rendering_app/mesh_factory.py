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
                 GL_STATIC_DRAW)  # static draw = online one data upload intended
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

    return (position_buffer, color_buffer), vao


def build_triangle_mesh2():
    # translates by 0.5 to the right (positive x)
    transform = np.array([
        [1, 0, 0.5],
        [0, 1, 0],
        [0, 0, 1]], dtype=np.float32
    )

    vertices = [
        np.array([-0.3, -0.3, 1], dtype=np.float32),
        np.array([0.3, -0.3, 1], dtype=np.float32),
        np.array([0.0, 0.3, 1], dtype=np.float32)
    ]

    # transformed_vertices = [transform.dot(v) for v in vertices]
    transformed_vertices = vertices

    vertex_data = np.zeros(3, dtype=data_type_vertex)
    vertex_data[0] = (transformed_vertices[0][0], transformed_vertices[0][1], 0.0, 0)
    vertex_data[1] = (transformed_vertices[1][0], transformed_vertices[1][1], 0.0, 1)
    vertex_data[2] = (transformed_vertices[2][0], transformed_vertices[2][1], 0.0, 2)

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data,
                 GL_STATIC_DRAW)  # static draw = online one data upload intended

    glVertexAttribPointer(
        0,  # index of the attribute
        3,  # number of elements (x,y,z => 3)
        GL_FLOAT,  # data type of each number
        GL_FALSE,  # if floating point numbers should be normalized
        data_type_vertex.itemsize,
        # stride: number of bytes to go from one attribute to the next: 32 bits * 3 elements / 8 = 12 bytes
        ctypes.c_void_p(0)  # offset: where the first position is
    )
    glEnableVertexAttribArray(0)

    glVertexAttribIPointer(
        1,  # index of the attribute
        1,  # number of elements
        GL_UNSIGNED_INT,  # data type of each number
        data_type_vertex.itemsize,  # number of bytes to go from one attribute to the next: 32 bit = 4 byte
        ctypes.c_void_p(12)  # offset, where the first position is
    )
    glEnableVertexAttribArray(1)

    return vbo, vao


def build_cube_mesh():
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
