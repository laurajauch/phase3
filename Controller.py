import kivy
kivy.require('1.0.7')
from kivy.app import App
from Model import *
import StringIO
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import numpy as np
from kivy.core.image.img_pygame import ImageLoaderPygame
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.lang import Builder
"""
Controller

The driver for the PyCamellia GUI. Main also assumes the
responsibility of reading and writing to the view (test.kv).
"""
class Controller(object):


    def __init__(self):
        self.model = Model()
        """This method is called when one of the plot choices is pressed"""
    def plot(self, plotType):
       

        print(plotType)
        #self.fig = self.model.plot(plotType)
        #self.image = fig2png(self.fig)
        #Set the kivy image to self.image
        


        """Convert a matplotlib.Figure to PNG image.:returns: PNG image bytes"""
    def fig2png(fig):
  
        data = StringIO.StringIO()
        canvas = FigureCanvasAgg(fig)
        canvas.print_png(data)
        return data.getvalue()


    
    
    """This method is called when one of the refine choices is pressed"""
    def refine(self,refineType):
        print(refineType)





"""
Design elements are contained in the test.kv file
which kivy will look in when the program starts as
a result of this empty class.
"""
class testApp(App):
    
    def refine(self, input):
        self.controller.refine(input)
    def plot(self, input):
        self.controller.plot(input)
    """
    Added this build function so we can maipulate testApp when it is created. 
    We just need to specify which .kv file we are building from.
    """
    def build(self):
        self.controller = Controller()
        return Builder.load_file('test.kv')
        




if __name__ == '__main__':
    testApp().run()

