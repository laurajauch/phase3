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
from kivy.core.image import Image as CoreImage
from kivy.animation import Animation
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
        self.model.refine(rType)


    """
    Convert a matplotlib.Figure to PNG image.:returns: PNG image bytes
    """
    #def fig2png(self, fig):
     #   data = StringIO.StringIO()
      #  canvas = FigureCanvasAgg(fig)
      #  canvas.print_png(data)
      #  return data.getvalue()




    """
    Do this when plot is pressed.
    """
    def pressPlot(self, plotType, numPlots):
        
        self.model.plot(plotType, numPlots)
       
  
        
 
      
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
        results = self.model.solve(data)
        print "what" + str((type(results)))
        return results # either a form or errors
            
    """
    Do this when load is pressed.
    """
    def pressLoad(self, filename):
        return self.model.load(filename)

    """
    Do this when save is pressed.
    """
    def pressSave(self, filename):
        self.model.save(filename)



# Screen Accessors & Mutators ------------------------------------
   

    
        



"""
ViewApp

Design elements are contained in the PyCamellia.kv file
which kivy will look in when the program starts.

Kivy requires this class for interacting with view (PyCamellia.kv),
although it is somewhat redundant to Controller.
"""
class ViewApp(App):
    #self.root.status = "running"
    title = 'PyCamellia Incompressible Flow Solver'
    """
    Added this build function so we can maipulate viewApp when it is created. 
    We just need to specify which .kv file we are building from.
    """
    def build(self):
        self.controller = Controller()
        self.numPlots = 0
        # Setting root as the instance variable needed to reference the GUI
        self.root = Builder.load_file('View.kv')
        return self.root

    """
    Refine the mesh of the current form
    """
    def refine(self, input):
        self.root.status = "Refining..."
        self.controller.pressRefine(input)
        self.root.status  = "Refined."
    def plot(self, input):
        self.root.status = "Plotting..."
        self.numPlots += 1
        self.controller.pressPlot(input, self.numPlots)
        self.root.plot_image = '/tmp/plot'+str(self.numPlots)+'.png'
    
        self.root.status = "Plotted."
    
    """
    Clear all fields on the screen
    """
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
        r.filename.clear()
        self.root.energyError = ""
        self.controller.pressReset()

    """
    Grab the input from the screen, then create and solve a form
    with that input. Be sure along the way that all necessary
    data is present and valid.
    """
    def solve(self):
        self.root.status = "Solving..."
        missingEntry = False # Set to true if an important field is left blank
        data = {}
        r = self.root.ids
        data["type"] = self.root.ids.probType.text
        # Still says 'Problem Type' so nothing was selected
        if data["type"][:1] == 'P': 
            missingEntry = True
            self.root.ids.probType.highlight()
        elif data["type"][:1] == 'S':
            data["stokes"] = True
        elif data["type"][:1] == 'N':
            data["stokes"] = False
        if data["type"][:3] == 'Nav':
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
        elif data["state"][:3] == 'Tra':
            data["transient"] = True
        elif data["state"][:3] == 'Ste':
            data["transient"] = False
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

        data["inflows"] = []

        if r.inf1.text != "" and r.inf1_x.text != "" and r.inf1_y.text != "":
            data["inflows"].append((r.inf1.text,r.inf1_x.text,r.inf1_y.text))
        elif r.inf1.text != "" or r.inf1_x.text != "" or r.inf1_y.text != "":
            missingEntry = True
            r.inf1.highlight()
            r.inf1_x.highlight()
            r.inf1_y.highlight()
        if r.inf2.text != "" and r.inf2_x.text != "" and r.inf2_y.text != "":
            data["inflows"].append((r.inf2.text,r.inf2_x.text,r.inf2_y.text))
        elif r.inf2.text != "" or r.inf2_x.text != "" or r.inf2_y.text != "":
            missingEntry = True
            r.inf2.highlight()
            r.inf2_x.highlight()
            r.inf2_y.highlight()
        if r.inf3.text != "" and r.inf3_x.text != "" and r.inf3_y.text != "":
            data["inflows"].append((r.inf2.text,r.inf2_x.text,r.inf2_y.text))
        elif r.inf3.text != "" or r.inf3_x.text != "" or r.inf3_y.text != "":
            missingEntry = True
            r.inf3.highlight()
            r.inf3_x.highlight()
            r.inf3_y.highlight()
        if r.inf4.text != "" and r.inf4_x.text != "" and r.inf4_y.text != "":
            data["inflows"].append((r.inf4.text,r.inf4_x.text,r.inf4_y.text))
        elif r.inf4.text != "" or r.inf4_x.text != "" or r.inf4_y.text != "":
            missingEntry = True
            r.inf4.highlight()
            r.inf4_x.highlight()
            r.inf4_y.highlight()       

        data["outflows"] = []

        if r.out1.text != "":
            data["outflows"].append(r.out1.text)
        if r.out2.text != "":
            data["outflows"].append(r.out2.text)
        if r.out3.text != "":
            data["outflows"].append(r.out3.text)
        if r.out4.text != "":
            data["outflows"].append(r.out4.text)
        
        # don't solve unless we have all necessary entries
        if not(missingEntry):
            # Clear all inflows that have potentially have been highlighted
            if r.inf1.text == "":
                r.inf1.clear()
                r.inf1_x.clear()
                r.inf1_y.clear()
            if r.inf2.text == "":
                r.inf2.clear()
                r.inf2_x.clear()
                r.inf2_y.clear()
            if r.inf3.text == "":
                r.inf3.clear()
                r.inf3_x.clear()
                r.inf3_y.clear()
            if r.inf4.text == "":
                r.inf4.clear()
                r.inf4_x.clear()
                r.inf4_y.clear()
            if r.out1.text == "":
                r.out1.clear()
            if r.out2.text == "":
                r.out2.clear()
            if r.out3.text == "":
                r.out3.clear()
            if r.out4.text == "":
                r.out4.clear()

            self.root.ids.save.disabled=False
            self.root.ids.plot.disabled=False
            self.root.ids.refine.disabled=False
            results = self.controller.pressSolve(data)
            if isinstance(results,dict): # if it's a dict of errors
                self.setErrors(results)
            else:
                print(type(results))
                
                if(data["stokes"]):
                    self.root.energyError = str(results.solution().energyErrorTotal())
                else:
                    self.root.energyError = str(results.solutionIncrement().energyErrorTotal())
            self.root.status = "Solved."
            return
        else:
            self.root.status = "Missing entries."

    def getFilename(self):
        filename = self.root.ids.filename.text
        if filename == '':
            self.root.ids.filename.highlight()
        return filename
    def load(self):
        filename = self.getFilename()
        data = self.controller.pressLoad(filename)
    def save(self):
        filename = self.getFilename()
        #self.controller.pressSave(filename)

    """
    Set the input errors on the GUI
    errors: A map from field to boolean, True if error, False if no error
    """
    def setErrors(self, errors):
        r = self.root.ids
        if errors["reynolds"]:
            r.reynolds.highlight()
        if errors["polyOrder"]:
            r.polyOrder.highlight()
        if errors["numElements"]:
            r.meshElems.highlight()
        if errors["meshDimensions"]:
            r.meshDim.highlight()
        for i in range(0, len(errors["inflows"])):
            if (i == 0) and errors["inflows"][i]:
                r.inf1.highlight()
                r.inf1_x.highlight()
                r.inf1_y.highlight()
            elif (i == 1) and errors["inflows"][i]:
                r.inf2.highlight()
                r.inf2_x.highlight()
                r.inf2_y.highlight()
            elif (i == 2) and errors["inflows"][i]:
                r.inf3.highlight()
                r.inf3_x.highlight()
                r.inf3_y.highlight()
            elif (i == 3) and errors["inflows"][i]:
                r.inf4.highlight()
                r.inf4_x.highlight()
                r.inf4_y.highlight()
        for i in range(0, len(errors["outflows"])):
            if (i == 0) and errors["outflows"][i]:
                r.out1.highlight()
            elif (i == 1) and errors["outflows"][i]:
                r.out2.highlight()
            elif (i == 2) and errors["outflows"][i]:
                r.out3.highlight()
            elif (i == 3) and errors["outflows"][i]:
                r.out4.highlight()
        
        
"""
"""
class PyTextInput(TextInput):
    reset_text = StringProperty("")
    def highlight(self):
        self.background_color=(1,0,0,1)
    def clear(self):
        self.background_color=(1,1,1,1)
        self.text=self.reset_text

"""
"""
class PyButton(Button):
    reset_text = StringProperty("")
    def highlight(self):
        self.background_color=(1,0,0,1)
    def clear(self):
        self.background_color=(1,1,1,1)
        self.text=self.reset_text

class PyDropButton(PyButton):
    def clear(self):
        super(PyDropButton, self).clear()
        self.italic=True

if __name__ == '__main__':
    ViewApp().run()

