import FormUtils
import InputData

"""
Model


"""
class Model(object):

    def __init___(self):
        self.form = None
        self.inputData = InputData.Instance()
           

    #precondition
    #data contains the following: Navier/Stokes, Transient/Steady, Renolds (Navier only), mesh dimensions, initial number of elements, polynomial order, inflow regions list, inflow x velocity list, inflow y velocity list, outflow regions list
    #coming soon: determining wall regions
    def enterData(self, data):
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
        SolveFormulation.solve(self.form)

    def plot(self):
        #Plotter.plot()
        pass
        
    def refine(self):
        pass

    










    if __name__ == '__main__':
        pass
