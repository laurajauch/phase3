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
        
    """
    This method is called when one of the refine choices is pressed
    """
    def pressRefine(self,rType, isAuto):
        Model.refine(self, rType, isAuto)
        print(refineType)

    """
    This method is called when one of the plot choices is pressed
    """
    def pressPlot(self, plotType):
        print(plotType)
        #self.fig = self.model.plot(plotType)
        #self.image = fig2png(self.fig)
        #Set the kivy image to self.image
        
    """
    Convert a matplotlib.Figure to PNG image.:returns: PNG image bytes
    """
    def fig2png(fig):
        data = StringIO.StringIO()
        canvas = FigureCanvasAgg(fig)
        canvas.print_png(data)
        return data.getvalue()
      
    """
    Do this when reset is pressed.
    """
    def pressReset(self):
        pass

    """
    Do this when solve is pressed.
    """
    def pressSolve(self):
        data = getText()


    """
    Retrieve the text from the GUI
    """
    def getText(self):
        # should be in this format 
        #data["state"] = string
        #data["polyOrder"] = string
        #data["numElements"] = string
        #data["meshDimensions"] = string
        #data["inflow"] = [strings]
        #data["outflow"] = [strings]
        pass

    """
    
    """
    def getFilename(self):
        pass
    
    """
    Set the input errors on the GUI
    """
    def setErrors(self):
        pass

    """
    Do this when load is pressed.
    """
    def pressLoad(self, filename):
        model.load(filename)

    """
    Do this when save is pressed.
    """
    def pressSave(self, filename):
        model.save(filename)


"""
Design elements are contained in the test.kv file
which kivy will look in when the program starts as
a result of this empty class.
"""
class viewApp(App):
    
    def refine(self, input):
        self.controller.refine(input)
    def plot(self, input):
        self.controller.pressPlot(input)
    """
    Added this build function so we can maipulate testApp when it is created. 
    We just need to specify which .kv file we are building from.
    """
    def build(self):
        self.controller = Controller()
        return Builder.load_file('View.kv')
        

if __name__ == '__main__':
    viewApp().run()

