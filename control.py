# Condigo para controlar snake version final

from modelos import *
import glfw
import sys
from typing import Union

class Controller:
    def __init__(self):
        self.model = None
        self.apple = None
        self.dif = None
        self.last_button = "a"
    
    def set_model(self,model):
        self.model = model
    
    def set_apple(self,apple):
        self.apple = apple

    def set_dif(self,d):
        self.dif = d
    
    def on_key(window, key, scancode, action, mods):

        if action != glfw.PRESS:
            return