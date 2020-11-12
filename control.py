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
        self.last_button = "a"
    
    def set_model(self,model):
        self.model = model
    
    def set_apple(self,apple):
        self.apple = apple

    def set_dif(self,d):
        self.dif = d
    
    def on_key(self,window, key, scancode, action, mods):
        if action != glfw.PRESS:
            return
        
        elif (key == glfw.KEY_LEFT or key == glfw.KEY_A) and action == glfw.PRESS:
            if self.model.jugando == False and self.model.dx != 1:
                self.model.dx = -1
                self.model.dy = 0
                self.model.jugando = True
        
        elif (key == glfw.KEY_RIGHT or key == glfw.KEY_D) and action == glfw.PRESS:
            if self.model.jugando == False and self.model.dx != -1:
                self.model.dx = 1
                self.model.dy = 0
                self.model.jugando = True

        elif (key == glfw.KEY_UP or key == glfw.KEY_W) and action == glfw.PRESS:
            if self.model.jugando == False and self.model.dy != -1:
                self.model.dy = 1
                self.model.dx = 0
                self.model.jugando = True

        elif (key == glfw.KEY_DOWN or key == glfw.KEY_S) and action == glfw.PRESS:
            if self.model.jugando == False and self.model.dy != 1:
                self.model.dy = -1
                self.model.dx = 0
                self.model.jugando = True

        