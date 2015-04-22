import FormUtils
#import Plotter
import ParsingUtils
from InputData import *


"""
Model

The model in the MVC pattern. This class holds the state of 
the PyCamellia solver at all times.
"""
class Model(object):

    def __init__(self):
        self.inputData = InputData()
        self.errorMsg = {} #True indicates stored data, false indicates an error

    """
    Called when refine is pressed
    """
    def refine(self, rtype, isAuto): # type: 0 is h, 1 is p
        if(isAuto):
            FormUtils.autoRefine(data, rtype)
        elif( not isAuto):
            FormUtils.manualRefine(data, rtype)
            
    """
    Called when plot is pressed
    """
    def plot(self, plotType):
        Plotter.plot(form, plotType)
        
    """
    Called when reset is pressed
    """
    def reset(self):
        pass

    """
    Called when solve is pressed
    """
    def solve(self, data):
        (valid, errors) = testData(data)
        if not valid:
            # need way to say controller.setErrors(errors)
            pass
        else:
            # do more stuff first then...
            # storeData(inputData)
            FormUtils.solve(self.form)
            
    """
    Test the given data to see if it is valid
    valid: True if data is valid, else False if data is invalid
    errors: A map from field to boolean, True if error, False if no error
    """
    def testData(self, data):
        errors = ParsingUtils.checkValidInput(data)
        valid = True
        for key, value in errors.iteritems():
            if value is False:
                valid = False

        return (valid, errors)

    """
    Store the given data in the InputData instance
    """
    def storeData(self, data):
        pass

    """
    Save to the specified file
    Param: filename The name of the file to save to
    """
    def save(self, filename):
        form = context.inputData.getForm()
        form.save(filename)
        
        memento = context.inputData.createMemento()
        output = memento.get()
        if len(output) >= 9:
            del output["form"]
            del output["inflowRegions"]
            del output["inflowX"]
            del output["inflowY"]
            del output["outflowRegions"]
            del output["wallRegions"]
            
            saveFile = open(filename, 'wb')
            pickle.dump(memento, saveFile)
            saveFile.close()
    """
    Load from the specified file
    Param: filename The name fo the file to load from
    """
    def load(self, filename):
        try:           
            loadFile = open(filename)
            memento = pickle.load(loadFile)
            loadFile.close()
            context.inputData = InputData(True)
            context.inputData.setMemento(memento)
            
            polyOrder = context.inputData.getVariable("polyOrder")
            spaceDim = 2
            if not context.inputData.getVariable("stokes"):
                reynolds = context.inputData.getVariable("reynolds")
                form = NavierStokesVGPForumlation(filename, spaceDim, reynolds, polyOrder)
            else:
                useConformingTraces = False
                mu = 1.0
                form = StokesVGPFormulation(spaceDim, useConformingTraces, mu)
                form.initializeSolution(filename, polyOrder)
                
                context.inputData.setForm(form)
                
                mesh = form.solution().mesh()
                elementCount = mesh.numActiveElements()
                globalDofCount = mesh.numGlobalDofs()
                
        except:
            print("No solution was found with the name \"%s\"" % command)
    
  


 # not used anymore but havent updated input data---------------------------------------     
    """
    Precondition: data contains the following in a dictionary - 
    Navier/Stokes, Transient/Steady, Renolds (Navier only), 
    mesh dimensions, initial number of elements, polynomial order, 
    inflow regions list, inflow x velocity list, inflow y velocity list, outflow regions list
    Param: data The data...

    Coming Soon: determining wall regions
    """
    def enterData(self, data):
        self.errorMsg["stokes"] = self.inputData.storeStokes(data["stokes"])
        self.errorMsg["transient"] = self.inputData.storeState(data["transient"])
        if not self.inputData.getVariable("stokes"):
            errorMsg["reynolds"] = self.inputData.storeReynolds(data["reynolds"])
        self.errorMsg["meshDimensions"] = self.inputData.storeMeshDims(data["meshDimensions"])
        self.errorMsg["polyOrder"] = self.inputData.storePolyOrder(data["polyOrder"])
        inflowError = self.inputData.storeInflows(data["inflowRegions"],data["inflowX"],data["inflowY"])
        self.errorMsg["inflowRegions"] = inflowError[0]
        self.errorMsg["inflowX"] = inflowError[1]
        self.errorMsg["inflowY"] = inflowError[2]
        self.errorMsg["outflowRegions"] = self.inputData.storeOutflows(data["outflowRegions"])
        self.errorMsg["wallRegions"] = False #need to figure out what to store
        return self.errorMsg




    if __name__ == '__main__':
        pass
