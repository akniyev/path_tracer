
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random

def f(x, y):
    return math.sin(x) * math.cos(y)

def surface():
    glBegin(GL_QUADS)

    x = 0

    glColor3fv((0, 1, 0))

    delta_x = 0.2
    delta_y = 0.2

    while x < 2 * math.pi:
        y = 0
        while y < 2 * math.pi:
            (x0, y0) = (x,y)
            z = f(x0, y0)
            glColor3f(1, z, 0)
            glVertex3f(x0, z, y0)

            (x0, y0) = (x+delta_x,y)
            z = f(x0, y0)
            glColor3f(1, z, 0)
            glVertex3f(x0, z, y0)

            (x0, y0) = (x+delta_x,y+delta_y)
            z = f(x0, y0)
            glColor3f(1, z, 0)
            glVertex3f(x0, z, y0)

            (x0, y0) = (x,y+delta_y)
            z = f(x0, y0)
            glColor3f(1, z, 0)
            glVertex3f(x0, z, y0)

            y += delta_y
        x += delta_x

    p = False;
    glEnd()


def main():
    pygame.init()
    display = (1024, 768)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    #glEnable(GL_NORMALIZE)

    glLightfv(GL_LIGHT0, GL_AMBIENT, (0, 0, 0, 0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1, 1, 1, 0))

    light_y = 0
    light_y_direction = 1
    light_y_step = 0.01
    glLightfv(GL_LIGHT0, GL_POSITION, (0, light_y, 0))

    glTranslatef(0.0, 0.0, -5.0)

    #glRotate(25, 2, 1, 0)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    glTranslatef(-0.5, 0, 0)
                if event.key == pygame.K_RIGHT:
                    glTranslatef(0.5, 0, 0)
                if event.key == pygame.K_UP:
                    glTranslatef(0, 0.5, 0)
                if event.key == pygame.K_DOWN:
                    glTranslatef(0, -0.5, 0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    glTranslatef(0, 0, 1.0)

                if event.button == 5:
                    glTranslatef(0, 0, -1.0)

        #glRotate(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLightfv(GL_LIGHT0, GL_POSITION, (0, light_y, -3))
        light_y += light_y_direction * light_y_step
        if (math.fabs(light_y) > 2):
            light_y_direction *= -1

        delta = 0.2

        glBegin(GL_QUADS)
        for x in range(0,100):
            for y in range(0,100):
                glVertex3f(delta * x, -2, delta * y)
                glVertex3f(delta * (x+1), -2, delta * y)
                glVertex3f(delta * (x+1), -2, delta * (y+1))
                glVertex3f(delta * x, -2, delta * (y+1))


        glNormal3f(0, 0, -1)
        glVertex3f(1, 1, -2)
        glVertex3f(-1, 1, -2)
        glVertex3f(-1, -1, -2)
        glVertex3f(1, -1, -2)
        glEnd()

        pygame.display.flip()
        pygame.time.wait(10)

main()
