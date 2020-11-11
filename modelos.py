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

# Clase para dibujar la serpiente (cuerpo y cabeza)
class Serpiente:

    def __init__(self):
        self.pos_x = 0
        self.pos_y = 0
        self.largo = 3
        self.dx = 0 # Tiene que ser el minimo valor de avance
        self.dy = 0 # Tiene que ser el minimo valor de avance
        self.theta = 0 # Tiene que ser el valor donde incia la serpiente a mirar


    def generar_cabeza(self,color):
        nTheta = 5
        nPhi = 7
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
    
    def generar_cuerpo(self,color):
        nTheta = 5
        nPhi = 7
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

# Clase para dibujar el objeto premio
class Premio:

    def __init__(self):
        self.pos_x = 0
        self.pos_y = 0
    
    def generar_objeto(self,filename,color):
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
    
    def cambiar_pos(self):
        def randomPos(self):
            self.fruta.pos_x = self.rango[rd.randint(0,len(self.rango)-1)]
            self.fruta.pos_y = self.rango[rd.randint(0,len(self.rango)-1)]


# Clase para dibujar el escenario del juego (suelo y pared)
class Escenario:

    def __init__(self,n):
        self.n = n
        temp = bs.createColorCube(0.2,1,1)
        temp = es.toGPUShape(temp)
        self.pared = temp
        temp = bs.createColorQuad(0.8,0.8,0)
        temp = es.toGPUShape(temp)
        self.suelo = temp
        self.transform = tr.uniformScale(self.n)
    
    # generamos el suelo
    def generar_suelo(self):
        base = bs.createColorQuad(0.8,0.8,0)
        base = es.toGPUShape(base)
        self.suelo = base
    
    def generar_pared(self):
        pared = bs.createColorCube(0.2,1,1)
        pared = es.toGPUShape(pared)
        self.pared = pared
    
    def draw_suelo(self,pipeline,projection,view):
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, self.transform )
        pipeline.drawShape(self.suelo)
    
    def draw_pared(self,pipeline,projection,view):
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.uniformScale(4*self.n) )
        pipeline.drawShape(self.pared)
    
    def draw_escenario(self,pipeline,pipeline_texture,view,projection):
        self.draw_pared(pipeline_texture,projection,view)
        self.draw_suelo(pipeline,projection,view)




