import pygame,math
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
from scipy.spatial.transform import Rotation as R

class rotate():
    def startgame(self):
        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        glClearColor(0.2, 0.2, 0.2, 0.929)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
        glTranslatef(0, 0, -5)
        glMatrixMode(GL_MODELVIEW)
        

        self.axis_verts = (
                    (-7.5, 0.0, 0.0),
                    ( 7.5, 0.0, 0.0),
                    ( 0.0,-7.5, 0.0),
                    ( 0.0, 7.5, 0.0),
                    ( 0.0, 0.0,-7.5),
                    ( 0.0, 0.0, 7.5)
                    )

        self.axes = (
                    (0,1),
                    (2,3),
                    (4,5)
                    )

        self.axis_colors = (
                    (1.0,0.0,0.0), 
                    (0.0,1.0,0.0),
                    (0.0,0.0,1.0)  
                    )


    def draw_axes(self):
        glBegin(GL_LINES)
        for color,axis in zip(self.axis_colors,self.axes):
            glColor3fv(color)
            for point in axis:
                glVertex3fv(self.axis_verts[point])
        glEnd()

    def draw_cylinder(self, radius, height, sides, colour):
        glBegin(GL_QUAD_STRIP)
        for i in range(sides + 1):
            angle = 2 * 3.14159 * i / sides
            y = radius * math.cos(angle)
            z = radius * math.sin(angle)
            glColor3f(colour[0], colour[1], colour[2])  
            glVertex3f(height, y, z)
            glVertex3f(0, y, z)
        glEnd()

        glBegin(GL_POLYGON)
        for i in range(sides + 1):
            angle = 2 * 3.14159 * i / sides
            y = radius * math.cos(angle)
            z = radius * math.sin(angle)
            glColor3f(colour[0], colour[1], colour[2])  
            glVertex3f(0, y, z)
        glEnd()

        glBegin(GL_POLYGON)
        for i in range(sides + 1):
            angle = 2 * 3.14159 * i / sides
            y = radius * math.cos(angle)
            z = radius * math.sin(angle)
            glColor3f(colour[0], colour[1], colour[2])
            glVertex3f(height, y, z)
        glEnd()

    def rotationmatrix(self,q1):
        q_norm = np.linalg.norm(q1)
        q1 /= q_norm

        rotation_matrix1 = np.array([
            [1 - 2*q1[2]**2 - 2*q1[3]**2, 2*q1[1]*q1[2] - 2*q1[3]*q1[0], 2*q1[1]*q1[3] + 2*q1[2]*q1[0], 0.0],
            [2*q1[1]*q1[2] + 2*q1[3]*q1[0], 1 - 2*q1[1]**2 - 2*q1[3]**2, 2*q1[2]*q1[3] - 2*q1[1]*q1[0], 0.0],
            [2*q1[1]*q1[3] - 2*q1[2]*q1[0], 2*q1[2]*q1[3] + 2*q1[1]*q1[0], 1 - 2*q1[1]**2 - 2*q1[2]**2, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ], dtype=np.float32)
        return rotation_matrix1

    def quaternion_multiply(self,q1, q2):
            w1, x1, y1, z1 = q1
            w2, x2, y2, z2 = q2
            w = w1*w2 - x1*x2 - y1*y2 - z1*z2
            x = w1*x2 + x1*w2 + y1*z2 - z1*y2
            y = w1*y2 - x1*z2 + y1*w2 + z1*x2
            z = w1*z2 + x1*y2 - y1*x2 + z1*w2
            return [w, x, y, z]
    def conjugate_quaternion(self,q):
        w, x, y, z = q
        return [w, -x, -y, -z]
    
    def rotate_vector_by_quaternion(self,vector, q):
        p = [0, vector[0], vector[1], vector[2]]
        rotated_p = self.quaternion_multiply(self.quaternion_multiply(q, p), self.conjugate_quaternion(q))
        return [rotated_p[1], rotated_p[2], rotated_p[3]] 
    
    def arm1(self,q1=[1,0,0,0]):
        q_init=[1,0,0,0]
        position=[1,0,0]
        new_q=self.quaternion_multiply(q_init,q1)
        new_pos=self.rotate_vector_by_quaternion(position, new_q)
        return new_pos
    
    def arm2(self,q1=[1,0,0,0],q2=[1,0,0,0]):
        q_init=[1,0,0,0]
        position=[2,0,0]
        new_q1=self.quaternion_multiply(q_init,q2)
        new_q2=self.quaternion_multiply(q_init,q1)
        new_q=new_q2-new_q1
        new_pos=self.rotate_vector_by_quaternion(position, new_q)
        return new_pos
    




    def cube(self,q1=[1.0,0.0,1.0,0.0],q2=[1.0,0.0,1.0,0.0],q3=[1.0,0.0,1.0,0.0],q4=[1.0,0.0,1.0,0.0],q5=[1.0,0.0,1.0,0.0]):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.draw_axes()
        glLoadIdentity()
        glRotatef(-90,1,0,0)
        glRotatef(90,0,0,1)

        glPushMatrix()
        glMultMatrixf(self.rotationmatrix(q1).T)
        self.draw_cylinder(radius=0.1, height=1, sides=50,colour=(0.7,0.7,0.7))
        glTranslatef(1.0,0.0,0.0)
        glMultMatrixf(self.rotationmatrix(self.quaternion_multiply(q2,self.conjugate_quaternion(q1))).T)
        self.draw_cylinder(radius=0.1, height=1, sides=50,colour=(0.8,0.8,0.8))
        glPopMatrix()

        glPushMatrix()
        glMultMatrixf(self.rotationmatrix(q3).T)
        self.draw_cylinder(radius=0.1, height=1, sides=50,colour=(0.7,0.7,0.7))
        glTranslatef(1.0,0.0,0.0)
        glMultMatrixf(self.rotationmatrix(self.quaternion_multiply(q4,self.conjugate_quaternion(q3))).T)
        self.draw_cylinder(radius=0.1, height=1, sides=50,colour=(0.8,0.8,0.8))
        glPopMatrix()
        # print(f"Position of Right Arm Joint 1: {self.arm1(q1)} Joint 2: {self.arm2(q1,q2)} | Position of Left Arm Joint 1: {self.arm1(q3)} Joint 2: {self.arm2(q3,q4)}")
        pygame.display.flip()
        pygame.time.wait(1)

    def endgame(self):
        pygame.quit()



