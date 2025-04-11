# 3d-rendering-project

This project is for the course WFP1 of Computer Science and Digital Communications at FH Campus Wien.

The goal is to create a program using PyOpenGL that can render a cube in real-time with camera movement via the mouse
and alongside learn about the theory of 3d computer graphics.

In here I will document the progress of my project.

### Initial State
I already did some trying out in a different project but I will start from mostly nothing in here. 
The initial commit only consists of some code that creates a window using GLFW.
(From this article: https://medium.com/@shashankdwivedi6386/pyopengl-creating-simple-window-in-python-9ae3b10f6355)

### 7th April: Python OpenGL Introduction Tutorial
As an intro to (Py)OpenGL I am watching this tutorial series and following along: 
https://www.youtube.com/watch?v=JOL-Ae0OkN8&list=PLn3eTxaOtL2N4-HCA6wFtHIYsu1NR-jqg

I will note all important information mentioned in the videos.

GLFW : windowing library, for opening windows and detecting user input
NumPy : numpy arrays are better suited for working with OpenGL than Python lists
Double Buffer System : one buffer is presented to the screen, the other buffer can be written to by the GPU
GLSL : GL Shading Language, c-like language that the shader programs (vertex.txt, fragment.txt) are written in
OpenGL coordinate system : values range from -1.0 to 1.0, x is right, y is top, z is front
Shaders : modules that are part of the pipeline, output an attribute and can take in an attribute
Vertex Buffer : memory allocation on the gpu but without any meaning attached
Attribute Pointer : how the GPU can interpret a vertex buffer
Vertex Array : "convenience object" that wraps up vertex buffers and attribute pointers

_vertex.txt_
writes to the in-built variable gl_Position, outputs a color to the fragmentColor attribute

_fragment.txt_
takes fragmentColor as an input and outputs screenColor to the screen