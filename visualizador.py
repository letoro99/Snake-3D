
# Modulos
import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys

from modelos import *
from control import Controller

import transformations as tr
import lighting_shaders as ls
import easy_shaders as es
import basic_shapes as bs

if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Snake 3D", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    controlador = Controller()

    pipeline = es.SimpleModelViewProjectionShaderProgram()
    texture_pipeline = es.SimpleTextureModelViewProjectionShaderProgram()
    
    glUseProgram(pipeline.shaderProgram)

    glClearColor(0.85, 0.85, 0.85, 1.0)

    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    projection = tr.perspective(45, float(width)/float(height), 0.1, 100)

    static_view = tr.lookAt(
            np.array([10,0,5]), # eye
            np.array([0,0,0]), # at
            np.array([0,0,1])  # up
        )

    suelo = Escenario(5)
    suelo.generar_suelo()
    suelo.generar_pared()

    while not glfw.window_should_close(window):
        
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        suelo.draw_suelo(pipeline,projection,static_view)
        suelo.draw_pared(pipeline,projection,static_view)

        glfw.swap_buffers(window)

    glfw.terminate()
