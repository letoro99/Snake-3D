
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
    glfw.set_key_callback(window, controlador.on_key)

    pipeline = es.SimpleModelViewProjectionShaderProgram()
    pipeline_pantalla = es.SimpleTextureTransformShaderProgram()
    pipeline_texture = es.SimpleTextureModelViewProjectionShaderProgram()
    
    glUseProgram(pipeline.shaderProgram)

    glClearColor(0.85, 0.85, 0.85, 1.0)

    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    scene = Escenario(22)
    snake = Serpiente()
    premio = Premio()
    premio.update(snake)
    camera = Camera()
    camera.cambiar_pos_camera(snake)

    controlador.set_model(snake)
    controlador.set_dif(1)
    controlador.set_apple(premio)
    controlador.set_camera(camera)
    
    t0 = 0
    dt = 0
    rot = 0

    while not glfw.window_should_close(window):
        
        ti = glfw.get_time()
        dt = ti - t0

        if dt > 0.3 and not snake.gameOver:
            snake.update()
            camera.cambiar_pos_camera(snake)
            snake.colision(premio)
            dt = 0
            t0 = ti
        
        elif camera.rotando == True:
            pass
        
        premio.posicionar_rotar(ti)

        glfw.poll_events()

        camera.drawCamera(pipeline,width,height)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        if snake.gameOver:
            glClearColor(0,0,0,1)
            if rot < (np.pi/15):
                scene.update(rot)
                rot += 0.00008
            scene.draw_go(pipeline_pantalla,2)
            glfw.swap_buffers(window)

        else:
            scene.draw(pipeline)
            snake.draw(pipeline)
            premio.draw(pipeline)
            glfw.swap_buffers(window)

    glfw.terminate()
