import FormUtils
import InputData

"""
Model

The model in the MVC pattern. This class holds the state of 
the PyCamellia solver at all times.
"""
class Model(object):

    def __init___(self):
        self.form = None
        
    """
    Precondition: data contains the following - Navier/Stokes, Transient/Steady, Renolds 
    (Navier only), mesh dimensions, initial number of elements, polynomial order, 
    inflow regions list, inflow x velocity list, inflow y velocity list, outflow regions list
    Param: data The data...

    Coming Soon: determining wall regions
    """
    def enterData(self, data):
        self.inputData = InputData.Instance()
        errorMsg = {} #True for stored data, false for errors
        errorMsg["stokes"] = inputData.storeStokes(data["stokes"])
        errorMsg["transient"] = inputData.storeState(data["transient"])
        if not inputData.getVariable("stokes"):
            errorMsg["reynolds"] = inputData.storeReynolds(data["reynolds"])
        errorMsg["meshDimensions"] = inputData.storeMeshDims(data["meshDimensions"])
        errorMsg["polyOrder"] = inputData.storePolyOrder(data["polyOrder"])
        inflowError = inputData.storeInflows(data["inflowRegions"],data["inflowX"],data["inflowY"])
        errorMsg["inflowRegions"] = inflowError[0]
        errorMsg["inflowX"] = inflowError[1]
        errorMsg["inflowY"] = inflowError[2]
        errorMsg["outflowRegions"] = inputData.storeOutflows(data["outflowRegions"])
        errorMsg["wallRegions"] = False #need to figure out what to store
        return errorMsg
            

    def solve(self):
        FormUtils.solve(self.form)

    def plot(self):
        #Plotter.plot()
        pass
        
    def refine(self):
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
                
        except (OSError, IOError):
            print("No solution was found with the name \"%s\"" % command)
            

    if __name__ == '__main__':
        pass
