import FormUtils
import Plotter
from ParsingUtils import *
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
    def plot(self, plotType, numPlots): 
        spaceDim = 2
        useConformingTraces = True
        mu = 1.0
        polyOrder = 3
        delta_k = 1
        dims = [1.0, 1.0]
        numElements = [8,8]
        x0 = [0.,0.]
        meshTopo = MeshFactory.rectilinearMeshTopology(dims, numElements, x0)
        
        topBoundary = SpatialFilter.matchingY(1.0)
        notTopBoundary = SpatialFilter.negatedFilter(topBoundary)
        x = Function.xn(1)
        rampWidth = 1./64
        H_left = Function.heaviside(rampWidth)
        H_right = Function.heaviside(1.0-rampWidth);
        ramp = (1-H_right) * H_left + (1./rampWidth) * (1-H_left) * x + (1./rampWidth) * H_right * (1-x)
        zero = Function.constant(0)
        topVelocity = Function.vectorize(ramp,zero)
        
        form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        form.initializeSolution(meshTopo,polyOrder,delta_k)
        form.addZeroMeanPressureCondition()
        form.addInflowCondition(topBoundary,topVelocity)
        form.solve()


      
        # to test, run TestModel
        Plotter.plot(form, plotType,numPlots)
        
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
                if key == "outflows" or key == "inflows":
                    for i in value:
                        print key + " "+str(i)
                else:
                    print key + " " + str(value)
            self.errors = errors
            return self.errors
            
    """
    Test the given data to see if it is valid
    valid: True if data is valid, else False if data is invalid
    errors: A map from field to boolean, True if error, False if no error
    """
    def testData(self, rawData):
        errors = checkValidInput(rawData)
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
        data = formatRawData(rawData)              
        self.inputData.setVariables(data)

    """
    Save to the specified file
    Param: filename The name of the file to save to
    """
    def save(self, filename):
        form = self.inputData.getVariable("form")
        form.save(filename)
        
        memento = self.inputData.createMemento()
        output = memento.get()
        if len(output) >= 10:
            del output["form"]
            del output["inflowRegions"]
            del output["inflowX"]
            del output["inflowY"]
            del output["outflowRegions"]
            
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
            print("No solution was found with the name \"%s\"" % filename) 
 
    if __name__ == '__main__':
        pass
