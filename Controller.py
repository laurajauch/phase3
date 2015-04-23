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
from kivy.uix.button import Button
from kivy.properties import *
import re
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
    #self.root.status = "running"
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
        self.root.status = "Refining..."
        self.controller.pressRefine(input)
        self.root.status  = "Refined."
    def plot(self, input):
        self.root.status = "Plotting..."
        self.controller.pressPlot(input)
        self.root.status = "Plotted."
    def reset(self):
        # So we don't write out self.root.ids each time:
        r = self.root.ids
        r.probType.clear()
        r.stateType.clear()
        r.refine.clear()
        r.refine.disabled=True
        r.plot.clear()
        r.plot.disabled=True
        r.polyOrder.clear()
        r.meshElems.clear()
        r.meshDim.clear()
        r.reynolds.clear()
        r.out1.clear()
        r.out2.clear()
        r.out3.clear()
        r.out4.clear()
        r.inf1.clear()
        r.inf1_x.clear()
        r.inf1_y.clear()
        r.inf2.clear()
        r.inf2_x.clear()
        r.inf2_y.clear()
        r.inf3.clear()
        r.inf3_x.clear()
        r.inf3_y.clear()
        r.inf4.clear()
        r.inf4_x.clear()
        r.inf4_y.clear()
        r.save.clear()
        r.save.disabled=True
        #self.controller.pressReset()
    def solve(self):
        self.root.status = "Solving..."
        missingEntry = False # Set to true if an important field is left blank
        data = {}
        data["type"] = self.root.ids.probType.text
        # Still says 'Problem Type' so nothing was selected
        if data["type"][:1] == 'P': 
            missingEntry = True
            self.root.ids.probType.highlight()
        data["reynolds"] = self.root.ids.reynolds.text
        # If no Reynolds number specified AND problem type is NOT Stokes
        if ((data["reynolds"] == '') and not(data["type"][:1] == 'S')):
            missingEntry = True
            self.root.ids.reynolds.highlight()
        data["state"] = self.root.ids.stateType.text
        # Still says 'State' so nothing was selected
        if data["state"][:3] == 'Sta':
            missingEntry = True
            self.root.ids.stateType.highlight()
        data["polyOrder"] = self.root.ids.polyOrder.text
        # Is empty so no value was given
        if data["polyOrder"] == '':
            missingEntry = True
            self.root.ids.polyOrder.highlight()
        data["numElements"] = self.root.ids.meshElems.text
        # Is empty so no value was given
        if data["numElements"] == '':
            missingEntry = True
            self.root.ids.meshElems.highlight()
        data["meshDimensions"] = self.root.ids.meshDim.text
        # Is empty so no value was given
        if data["meshDimensions"] == '':
            missingEntry = True
            self.root.ids.meshDim.highlight()
        #data["inflow"] = [strings]
        #data["outflow"] = [strings]
        # don't solve unless we have all necessary entries
        if not(missingEntry):
            self.root.ids.save.disabled=False
            self.root.ids.plot.disabled=False
            self.root.ids.refine.disabled=False
            #self.controller.pressSolve(data)
            pass
        #
        self.root.status = "Solved."


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
    reset_text = StringProperty("")
    def highlight(self):
        self.background_color=(.7,0,.15,.9)
    def clear(self):
        self.background_color=(1,1,1,1)
        self.text=self.reset_text

class PyButton(Button):
    reset_text = StringProperty("")
    def highlight(self):
        self.background_color=(1,0,0,1)
    def clear(self):
        self.background_color=(1,1,1,1)
        self.text=self.reset_text

if __name__ == '__main__':
    ViewApp().run()

