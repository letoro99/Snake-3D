#######################
# Modelos de Snake 3D #
#######################

# Modulos 
import glfw
import numpy as np
import random as rd
from OpenGL.GL import *
import OpenGL.GL.shaders
import basic_shapes as bs
import local_shapes as losh
import transformations as tr
import easy_shaders as es
import scene_graph as sg

def generar_esfera_unit(nTheta,nPhi,color):
    vertices = []
    indices = []

    theta_angs = np.linspace(0, np.pi, nTheta, endpoint=True)
    phi_angs = np.linspace(0, 2 * np.pi, nPhi, endpoint=True)

    start_index = 0

    for theta_ind in range(len(theta_angs)-1): # vertical
        cos_theta = np.cos(theta_angs[theta_ind]) # z_top
        cos_theta_next = np.cos(theta_angs[theta_ind + 1]) # z_bottom

        sin_theta = np.sin(theta_angs[theta_ind])
        sin_theta_next = np.sin(theta_angs[theta_ind + 1])


        for phi_ind in range(len(phi_angs)-1): # horizontal
            cos_phi = np.cos(phi_angs[phi_ind])
            cos_phi_next = np.cos(phi_angs[phi_ind + 1])
            sin_phi = np.sin(phi_angs[phi_ind])
            sin_phi_next = np.sin(phi_angs[phi_ind + 1])

             #                     X                             Y                          Z
            a = np.array([cos_phi      * sin_theta_next, sin_phi * sin_theta_next     , cos_theta_next])
            b = np.array([cos_phi_next * sin_theta_next, sin_phi_next * sin_theta_next, cos_theta_next])
            c = np.array([cos_phi_next * sin_theta     , sin_phi_next * sin_theta     , cos_theta])
            d = np.array([cos_phi * sin_theta          , sin_phi * sin_theta          , cos_theta])

            _vertex, _indices = losh.createColorQuadIndexation(
                start_index,
                a, b, c, d,
                color
                )
            vertices += _vertex
            indices  += _indices
            start_index += 4

    return bs.Shape(vertices, indices)
    pass

def generar_objeto(filename,color):
    vertices = []
    normals = []
    textCoords = []
    faces = []
    with open(filename,'r') as file:
        for line in file.readlines():
            aux = line.strip().split(' ')
        if aux[0] == 'v':
            vertices += [[float(coord) for coord in aux[1:]]]
        elif aux[0] == 'vn':
             normals += [[float(coord) for coord in aux[1:]]]
        elif aux[0] == 'vt':
            assert len(aux[1:]) == 2, "Texture coordinates with different than 2 dimensions are not supported"
            textCoords += [[float(coord) for coord in aux[1:]]]
        elif aux[0] == 'f':
            N = len(aux)                
            faces += [[readFaceVertex(faceVertex) for faceVertex in aux[1:4]]]
            for i in range(3, N-1):
                faces += [[readFaceVertex(faceVertex) for faceVertex in [aux[i], aux[i+1], aux[1]]]]

    vertexData = []
    indices = []
    index = 0

    # Per previous construction, each face is a triangle
    for face in faces:

        # Checking each of the triangle vertices
        for i in range(0,3):
            vertex = vertices[face[i][0]-1]
            normal = normals[face[i][2]-1]
            vertexData += [
                vertex[0], vertex[1], vertex[2],
                color[0], color[1], color[2],
                normal[0], normal[1], normal[2]
            ]

        # Connecting the 3 vertices to create a triangle
        indices += [index, index + 1, index + 2]
        index += 3        

    return bs.Shape(vertexData, indices)

# Clase para dibujar la cabeza de la serpiente 
class Cabeza:
    def __init__(self,x,y,z):
        gpu_cabeza = es.toGPUShape(generar_esfera_unit(5,7,[1,0,0]))

        cabeza = sg.SceneGraphNode('cabeza')
        cabeza.transform = tr.uniformScale(1)
        cabeza.childs += [gpu_cabeza]
        
        transform_cabeza = sg.SceneGraphNode('cabezaTR')
        transform_cabeza.childs += [cabeza]

        self.model = transform_cabeza
        self.posx = x
        self.posy = y
        self.posz = z

    def draw(self,pipeline):
        glUseProgram(pipeline.shaderProgram)
        sg.drawSceneGraphNode(self.model,pipeline,'model')
    
    def posicionar(self,pos):
        self.posx, self.posy , self.posz = pos[0],pos[1],pos[2]
        self.model.transform = tr.translate(self.posx,self.posy,self.posz)

# Clase para dibujar el cuepro de la serpiente 
class Cuerpo:
    def __init__(self,x,y,z):
        gpu_cuerpo = es.toGPUShape(generar_esfera_unit(5,7,[0.5,0.1,0]))

        cuerpo = sg.SceneGraphNode('cuerpo')
        cuerpo.transform = tr.uniformScale(1)
        cuerpo.childs += [gpu_cuerpo]
        
        transform_cuerpo = sg.SceneGraphNode('cuerpoTR')
        transform_cuerpo.childs += [cuerpo]

        self.model = transform_cuerpo
        self.posx = x
        self.posy = y
        self.posz = z

    def draw(self,pipeline):
        glUseProgram(pipeline.shaderProgram)
        sg.drawSceneGraphNode(self.model,pipeline,'model')

    def posicionar(self,pos):
        self.posx,self.posy,self.posz = pos[0],pos[1],pos[2]
        self.model.transform = tr.translate(self.posx,self.posy,self.posz)

# Clase para dibujar la serpiente 
class Serpiente:

    def __init__(self):
        self.cabeza = Cabeza(0,0,0)
        self.largo = 3
        self.cola = [Cuerpo(0,1,0),Cuerpo(0,2,0),Cuerpo(0,3,0)]
        self.dx = 1 # Tiene que ser el minimo valor de avance
        self.dy = 0 # Tiene que ser el minimo valor de avance
        self.theta = 0 # Tiene que ser el valor donde incia la serpiente a mirar
        self.jugando = False

    def update(self):
        for i in range(len(self.cola)-1,-1,-1):
            self.cola[i].posicionar([self.cola[i-1].posx,self.cola[i-1].posy,self.cola[i-1].posz])
        self.cola[0].posicionar([self.cabeza.posx,self.cabeza.posy,self.cabeza.posz])
        self.cabeza.posicionar([self.cabeza.posx + self.dx, self.cabeza.posy + self.dy, self.cabeza.posz])
        self.jugando = False
    
    def draw(self,pipeline):
        self.cabeza.draw(pipeline)
        for i in range(len(self.cola)):
            self.cola[i].draw(pipeline)

# Clase para dibujar el objeto premio
class Premio:

    def __init__(self):
        self.pos_x = 0
        self.pos_y = 0
    
    def cambiar_pos(self):
        def randomPos(self):
            self.fruta.pos_x = self.rango[rd.randint(0,len(self.rango)-1)]
            self.fruta.pos_y = self.rango[rd.randint(0,len(self.rango)-1)]

# Clase para dibujar el escenario del juego (suelo y pared)
class Escenario:

    def __init__(self,n):
        # Creamos pard
        gpu_pared = es.toGPUShape(bs.createColorCube(0.2,1,1))
        gpu_base = es.toGPUShape(bs.createColorQuad(0.8,0.8,0))

        paredes = sg.SceneGraphNode('paredes')
        paredes.transform = tr.uniformScale(4*n)
        paredes.childs += [gpu_pared]

        suelo = sg.SceneGraphNode('suelo')
        suelo.transform = tr.uniformScale(n)
        suelo.childs += [gpu_base]

        transform_escenario = sg.SceneGraphNode('escenario')
        transform_escenario.childs += [suelo,paredes] 
        
        self.model = transform_escenario
    
    def draw(self,pipeline):
        glUseProgram(pipeline.shaderProgram)
        sg.drawSceneGraphNode(self.model,pipeline,'model')
    




