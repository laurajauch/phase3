import FormUtils
import InputData

"""
Model


"""
class Model(object):

    def __init___(self):
        self.form = None
           

    #precondition
    #data contains the following: Navier/Stokes, Transient/Steady, Renolds (Navier only), mesh dimensions, initial number of elements, polynomial order, inflow regions list, inflow x velocity list, inflow y velocity list, outflow regions list
    #coming soon: determining wall regions
    def enterData(self, data):
        errorMsg = {} #True for stored data, false for errors
        
            

    def solve(self):
        FormUtils.solve(self.form)

    def plot(self):
        #Plotter.plot()
        pass
        
    def refine(self:
        pass

    










    if __name)) == '__main__':
        pass
