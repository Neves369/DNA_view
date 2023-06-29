import os
import pygame as pg
import numpy as np
from math import sin, cos

WIDTH = 800
HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)     

dic_cores = {
    'A': (255, 255, 0),
    'T': (255, 0, 0) ,
    'C': (0, 191, 255),
    'G': (0, 255, 0)
}

# listar arquivos da pasta data
caminhos = [os.path.join("data", nome) for nome in os.listdir("data")]
arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
fasta = [arq for arq in arquivos if arq.lower().endswith(".fasta")]

entrada = open(fasta[0]).read()
entrada = entrada.replace("\n", "")

pares = 0 

if (len(entrada) / 2) % 2 == 0:
    pares = int(len(entrada) / 2)
else:
    pares = int((len(entrada) / 2) - 1)


pg.init()

clock = pg.time.Clock()
screen = pg.display.set_mode((WIDTH, HEIGHT))


class Projection:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pg.display.set_mode((width, height))
        self.background = BLACK
        self.surfaces = {}

    def addSurface(self, name, surface):
        self.surfaces[name] = surface

    def drawCircle(self):
        for surface in self.surfaces.values():
            for node in surface.nodes:
                pg.draw.circle(self.screen, WHITE, (WIDTH / 2 + int(node[0]), int(node[2])), 5)

    def rotateZ(self, theta):
        for surface in self.surfaces.values():
            center = surface.findCentre()

            c = np.cos(theta)
            s = np.sin(theta)

            matrix = np.array([[c, -s, 0, 0],
                               [s, c, 0, 0],
                               [0, 0, 1, 0],
                               [0, 0, 0, 1]])

            surface.rotate(center, matrix)


class Object:
    def __init__(self):
        self.nodes = np.zeros((0, 4))

    def addNodes(self, node_array):
        ones_column = np.ones((len(node_array), 1))
        ones_added = np.hstack((node_array, ones_column))
        self.nodes = np.vstack((self.nodes, ones_added))

    def findCentre(self):
        mean = self.nodes.mean(axis=0)
        return mean

    def rotate(self, center, matrix):
        for i, node in enumerate(self.nodes):
            self.nodes[i] = center + np.matmul(matrix, node - center)

        for m in range(0, pares, 4):
            drawLine(m, m + 1, self.nodes, dic_cores[entrada[m]], dic_cores[entrada[m+1]])

        for m in range(2, pares, 4):
            drawLine(m, m + 1, self.nodes, dic_cores[entrada[m]], dic_cores[entrada[m+1]])


def drawLine(i, j, k, color1, color2):
    a = k[i]
    b = k[j]
    c = (a[0] + b[0]) / 2
    pg.draw.line(screen, color1, (WIDTH / 2 + a[0], a[2]), (WIDTH / 2 + c, b[2] - 6), 3)
    pg.draw.line(screen, color2, (WIDTH / 2 + c, a[2] + 6), (WIDTH / 2 + b[0], b[2]), 3)


helix = []

for t in range(pares):
    x = round(60 * cos(3 * t), 0)
    y = round(60 * sin(3 * t), 0)
    z = 12 * t
    helix.append((x, y, z))

spin = 0

running = True
while running:

    clock.tick(10)

    pv = Projection(WIDTH, HEIGHT)

    dna = Object()
    dna_nodes = [i for i in helix]
    dna.addNodes(np.array(dna_nodes))

    pv.addSurface('DNA', dna)
    pv.rotateZ(spin)
    pv.drawCircle()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    pg.display.update()
    spin += 0.02