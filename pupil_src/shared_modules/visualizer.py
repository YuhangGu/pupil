'''
(*)~----------------------------------------------------------------------------------
 Pupil - eye tracking platform
 Copyright (C) 2012-2016  Pupil Labs

 Distributed under the terms of the GNU Lesser General Public License (LGPL v3.0).
 License details are in the file license.txt, distributed as part of this software.
----------------------------------------------------------------------------------~(*)
'''

from glfw import *
from OpenGL.GL import *
from OpenGL.GLU import gluOrtho2D


from pyglui.cygl.utils import init
from pyglui.cygl.utils import RGBA
from pyglui.cygl.utils import *
from pyglui.cygl import utils as glutils
from pyglui.pyfontstash import fontstash as fs
from pyglui.ui import get_opensans_font_path
import math


class Visualizer(object):
    """docstring for Visualizer
    Visualizer is a base class for all visualizations in new windows
    """


    def __init__(self, name = "Visualizer", run_independently = False):

        self.name = name
        self.window_size = (640,480)
        self.window = None
        self.input = None
        self.run_independently = run_independently

    ########### Open, update, close #####################


    def open_window(self):
        if not self.window:
            self.input = {'button':None, 'mouse':(0,0)}

            # get glfw started
            if self.run_independently:
                glfwInit()
                self.window = glfwCreateWindow(self.window_size[0], self.window_size[1], self.name, None  )
            else:
                self.window = glfwCreateWindow(self.window_size[0], self.window_size[1], self.name, None, share=self.g_pool.main_window )

            active_window = glfwGetCurrentContext();
            glfwMakeContextCurrent(self.window)

            glfwSetWindowPos(self.window,0,0)
            # Register callbacks window
            glfwSetFramebufferSizeCallback(self.window,self.on_resize)
            glfwSetWindowIconifyCallback(self.window,self.on_iconify)
            glfwSetKeyCallback(self.window,self.on_key)
            glfwSetCharCallback(self.window,self.on_char)
            glfwSetMouseButtonCallback(self.window,self.on_button)
            glfwSetCursorPosCallback(self.window,self.on_pos)
            glfwSetScrollCallback(self.window,self.on_scroll)

            # get glfw started
            if self.run_independently:
                init()
            self.basic_gl_setup()

            self.glfont = fs.Context()
            self.glfont.add_font('opensans',get_opensans_font_path())
            self.glfont.set_size(22)
            self.glfont.set_color_float((0.2,0.5,0.9,1.0))
            self.on_resize(self.window,*glfwGetFramebufferSize(self.window))
            glfwMakeContextCurrent(active_window)


    def begin_update_window(self ):
        if self.window:
            if glfwWindowShouldClose(self.window):
                self.close_window()
                return

            active_window = glfwGetCurrentContext()
            glfwMakeContextCurrent(self.window)


    def update_window(self):
        pass

    def end_update_window(self ):
            glfwSwapBuffers(self.window)
            glfwPollEvents()
            glfwMakeContextCurrent(active_window)


    ############## DRAWING FUNCTIONS ##############################

    def draw_frustum(self, width, height , length):

        W = width/2.0
        H = height/2.0
        Z = length
        # draw it
        glLineWidth(1)
        glColor4f( 1, 0.5, 0, 0.5 )
        glBegin( GL_LINE_LOOP )
        glVertex3f( 0, 0, 0 )
        glVertex3f( -W, H, Z )
        glVertex3f( W, H, Z )
        glVertex3f( 0, 0, 0 )
        glVertex3f( W, H, Z )
        glVertex3f( W, -H, Z )
        glVertex3f( 0, 0, 0 )
        glVertex3f( W, -H, Z )
        glVertex3f( -W, -H, Z )
        glVertex3f( 0, 0, 0 )
        glVertex3f( -W, -H, Z )
        glVertex3f( -W, H, Z )
        glEnd( )

    def draw_coordinate_system(self,l=1):
        # Draw x-axis line. RED
        glLineWidth(2)
        glColor3f( 1, 0, 0 )
        glBegin( GL_LINES )
        glVertex3f( 0, 0, 0 )
        glVertex3f( l, 0, 0 )
        glEnd( )

        # Draw y-axis line. GREEN.
        glColor3f( 0, 1, 0 )
        glBegin( GL_LINES )
        glVertex3f( 0, 0, 0 )
        glVertex3f( 0, l, 0 )
        glEnd( )

        # Draw z-axis line. BLUE
        glColor3f( 0, 0, 1 )
        glBegin( GL_LINES )
        glVertex3f( 0, 0, 0 )
        glVertex3f( 0, 0, l )
        glEnd( )

    def basic_gl_setup(self):
        glEnable(GL_POINT_SPRITE )
        glEnable(GL_VERTEX_PROGRAM_POINT_SIZE) # overwrite pointsize
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)
        glClearColor(.8,.8,.8,1.)
        glEnable(GL_LINE_SMOOTH)
        # glEnable(GL_POINT_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_POLYGON_SMOOTH)
        glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)

    def adjust_gl_view(self,w,h):
        """
        adjust view onto our scene.
        """
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, w, h, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def clear_gl_screen(self):
        glClearColor(.9,.9,0.9,1.)
        glClear(GL_COLOR_BUFFER_BIT)

    def close_window(self):
        if self.window:
            glfwDestroyWindow(self.window)
            self.window = None

    ############ window callbacks #################
    def on_resize(self,window,w, h):
        h = max(h,1)
        w = max(w,1)

        self.window_size = (w,h)
        active_window = glfwGetCurrentContext()
        glfwMakeContextCurrent(window)
        self.adjust_gl_view(w,h)
        glfwMakeContextCurrent(active_window)

    def on_char(self,window,char):
        pass

    def on_button(self,window,button, action, mods):
        pass

    def on_pos(self,window,x, y):
        pass

    def on_scroll(self,window,x,y):
        pass

    def on_iconify(self,window,iconified):
        pass

    def on_key(self,window, key, scancode, action, mods):
        pass
