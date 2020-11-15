# Condigo para controlar snake version final

from modelos import *
import glfw
import sys
from typing import Union

class Controller:
    def __init__(self):
        self.model = None
        self.apple = None
        self.dif = 1
        self.camera = None
    
    def set_model(self,model):
        self.model = model
    
    def set_apple(self,apple):
        self.apple = apple

    def set_dif(self,d):
        self.dif = d
    
    def set_camera(self,camera):
        self.camera = camera

    def on_key(self,window, key, scancode, action, mods):

        if action != glfw.PRESS:
            return
        
        elif key == glfw.KEY_R and action == glfw.PRESS:
            self.camera.cambiar_camera(1)

        elif key == glfw.KEY_E and action == glfw.PRESS:
            self.camera.cambiar_camera(2)

        elif key == glfw.KEY_T and action == glfw.PRESS:
            self.camera.cambiar_camera(3)

        elif self.camera.camera_activa == 2 or self.camera.camera_activa == 3 or self.camera.camera_activa <= 3:
            if (key == glfw.KEY_LEFT or key == glfw.KEY_A) and action == glfw.PRESS:
                if self.model.jugando == False and self.model.dx != 1:
                    self.model.dx = -1
                    self.model.dy = 0
                    self.model.theta = np.pi
                    self.model.jugando = True
            
            elif (key == glfw.KEY_RIGHT or key == glfw.KEY_D) and action == glfw.PRESS:
                if self.model.jugando == False and self.model.dx != -1:
                    self.model.dx = 1
                    self.model.dy = 0
                    self.model.theta = 0
                    self.model.jugando = True

            elif (key == glfw.KEY_UP or key == glfw.KEY_W) and action == glfw.PRESS:
                if self.model.jugando == False and self.model.dy != -1:
                    self.model.dy = 1
                    self.model.dx = 0
                    self.model.theta = 1*np.pi/2
                    self.model.jugando = True

            elif (key == glfw.KEY_DOWN or key == glfw.KEY_S) and action == glfw.PRESS:
                if self.model.jugando == False and self.model.dy != 1:
                    self.model.dy = -1
                    self.model.dx = 0
                    self.model.theta = -1*np.pi/2
                    self.model.jugando = True
        
        elif self.camera.camera_activa == 5:
            if (key == glfw.KEY_LEFT or key == glfw.KEY_A) and action == glfw.PRESS:
                if self.model.theta == 0:
                    self.model.dy = 1
                    self.model.dx = 0
                    self.model.theta = 1*np.pi/2
                    self.model.jugando = True

                elif self.model.theta == np.pi/2:
                    pass
                elif self.model.theta == np.pi:
                    pass
                elif self.model.theta == -1*np.pi/2:
                    pass
            if (key == glfw.KEY_RIGHT or key == glfw.KEY_D) and action == glfw.PRESS:
                if self.model.theta == 0:
                    pass
                elif self.model.theta == np.pi/2:
                    pass
                elif self.model.theta == np.pi:
                    pass
                elif self.model.theta == -1*np.pi/2:
                    pass
        