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
from kivy.uix.textinput import TextInput
"""
Controller

The driver for the PyCamellia GUI. Main also assumes the
responsibility of reading and writing to the view (test.kv).
"""
class Controller(object):

    def __init__(self):
        self.model = Model()
        
    """
    Do this when refine is pressed.
    """
    def pressRefine(self, rType):
        Model.refine(self, rType)
        print(refineType)

    """
    Do this when plot is pressed.
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
        self.model.reset()
        pass

    """
    Do this when solve is pressed.
    """
    def pressSolve(self, data):
        self.model.solve(data)

    """
    Do this when load is pressed.
    """
    def pressLoad(self, filename):
        self.model.load(filename)

    """
    Do this when save is pressed.
    """
    def pressSave(self, filename):
        self.model.save(filename)



# Screen Accessors & Mutators ------------------------------------
   
    """
    Retrieve the text from the GUI.
    """
    def getText(self):
        pass

    """
    Retrieve the filename from the text box in the GUI
    """
    def getFilename(self):
        pass
    
    """
    Set the input errors on the GUI
    errors: A map from field to boolean, True if error, False if no error
    """
    def setErrors(self, errors):
        pass



"""
ViewApp

Design elements are contained in the PyCamellia.kv file
which kivy will look in when the program starts.

Kivy requires this class for interacting with view (PyCamellia.kv),
although it is somewhat redundant to Controller.
"""
class ViewApp(App):
    
    """
    Added this build function so we can maipulate viewApp when it is created. 
    We just need to specify which .kv file we are building from.
    """
    def build(self):
        self.controller = Controller()
        # Setting root as the instance variable needed to reference the GUI
        self.root = Builder.load_file('View.kv')
        return self.root

    def refine(self, input):
        self.controller.refine(input)
    def plot(self, input):
        self.controller.pressPlot(input)
    def reset(self):
        self.controller.pressReset()
    def solve(self):
        data = {}
        data["type"] = self.root.ids.probType.text
        data["state"] = self.root.ids.stateType.text
        data["polyOrder"] = self.root.ids.polyOrder.text
        data["numElements"] = self.root.ids.meshElems.text
        data["meshDimensions"] = self.root.ids.meshDim.text
        #data["inflow"] = [strings]
        #data["outflow"] = [strings]
        #self.controller.pressSolve(data)
    def getFilename(self):
        filename = self.root.ids.filename.text
        if filename == '':
            self.root.ids.filename.highlight()
        return filename
    def load(self):
        filename = self.getFilename()
        #self.controller.pressLoad(filename)
    def save(self):
        filename = self.getFilename()
        #self.controller.pressSave(filename)

class PyTextInput(TextInput):
    def highlight(self):
        self.background_color=(1,0,0,1)

if __name__ == '__main__':
    ViewApp().run()

