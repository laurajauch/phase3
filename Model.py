import FormUtils
import Plotter
import ParsingUtils
from PyCamellia import * #only used for random plot test
from InputData import *


"""
Model

The model in the MVC pattern. This class holds the state of 
the PyCamellia solver at all times.
"""
class Model(object):

    def __init__(self):
        self.inputData = InputData()
        self.errors = {}
       
    """
    Called when refine is pressed
    """
    def refine(self, rtype): # type: 0 is h, 1 is p
        self.inputData.addVariable("form", FormUtils.autoRefine(self.inputData, rtype))
        print "done refine"
            
    """
    Called when plot is pressed
    plotType: a string, etiher Mesh, Error, Stream Function, u1, u2, or p
    """
    def plot(self, plotType):       
        # to test, run TestModel
        Plotter.plot(self.inputData.getVariable("form"), plotType)
        
    """
    Called when reset is pressed
    """
    def reset(self):
        self.inputData = InputData()

    """
    Called when solve is pressed
    data: the raw data as it was taken from the GUI
    return: the solved form if data is valid, else the dict of errors
    """
    def solve(self, rawData):
        (valid, errors) = self.testData(rawData)
        print "In Model.py solve, data validity is: "+str(valid)
        try:
            assert valid
            self.storeData(rawData)
            print "solving"
            self.inputData.addVariable("form", FormUtils.solve(self.inputData))
            print("finish solve")
            return self.inputData.getVariable(["form"])
        except Exception, e:
            print "Model.py Solve exception is: "+str(e)
            for key,value in errors.iteritems():
                print key + " " + str(value)
            self.errors = errors
            return self.errors
            
    """
    Test the given data to see if it is valid
    valid: True if data is valid, else False if data is invalid
    errors: A map from field to boolean, True if error, False if no error
    """
    def testData(self, rawData):
        errors = ParsingUtils.checkValidInput(rawData)
        valid = True
        for key, value in errors.iteritems():
            if value is True:
                valid = False
                break #only need find one error

        return (valid, errors)

    """
    Store the given data in the InputData instance
    """
    def storeData(self, rawData):
        print "in storeData"
        data = ParsingUtils.formatRawData(rawData)              
        self.inputData.setVariables(data)

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
            # don't need to delete anything else since strings
            
            saveFile = open(filename, 'wb')
            pickle.dump(memento, saveFile)
            saveFile.close()

    """
    Load from the specified file
    Param: filename The name fo the file to load from
    """
    def load(self, filename):
        valid = checkValidFile(filename)
        try:           
            assert valid

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
            # do something to tell the GUI that it was an invalid filename
            print("No solution was found with the name \"%s\"" % command) 
 
    if __name__ == '__main__':
        pass
