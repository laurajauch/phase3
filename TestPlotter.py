from PyCamellia import *
import Plotter  as Plotter
import unittest
from itertools import chain, combinations
import matplotlib.pyplot as plt
import StringIO
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

spaceDim = 2
useConformingTraces = True
mu = 1.0
dims = [1.0,1.0]
numElements = [2,2]
x0 = [0.,0.]
polyOrder = 3
delta_k = 1
topBoundary = SpatialFilter.matchingY(1.0)
notTopBoundary = SpatialFilter.negatedFilter(topBoundary)
x = Function.xn(1)
rampWidth = 1./64
H_left = Function.heaviside(rampWidth)
H_right = Function.heaviside(1.0-rampWidth);
ramp = (1-H_right) * H_left + (1./rampWidth) * (1-H_left) * x + (1./rampWidth) * H_right * (1-x)
zero = Function.constant(0)
topVelocity = Function.vectorize(ramp,zero)
refinementNumber = 0

class TestPlotter(unittest.TestCase):

    """Test plotMesh"""
    def test_plotMesh(self):
        print "Plot_Mesh"
        form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
        form.initializeSolution(meshTopo,polyOrder,delta_k)
        form.addZeroMeanPressureCondition()
        form.addWallCondition(notTopBoundary)
        form.addInflowCondition(topBoundary,topVelocity)
        form.solve()
        
        Plotter.plot(form, "Mesh")
   

        





    """Test plot Mesh Refine"""
    def test_plotRefineMesh(self):
        print "Plot_RefineMesh"
        form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
        form.initializeSolution(meshTopo,polyOrder,delta_k)
        form.addZeroMeanPressureCondition()
        form.addWallCondition(notTopBoundary)
        form.addInflowCondition(topBoundary,topVelocity)
        form.solve()
        mesh = form.solution().mesh();

        mesh.hRefine([0])

        Plotter.plot(form, "Mesh")

        form = None

    """ Test Plot"""
    def test_plot_u1(self):
        print "Plot_u1"
        form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
        form.initializeSolution(meshTopo,polyOrder,delta_k)
        form.addZeroMeanPressureCondition()
        form.addWallCondition(notTopBoundary)
        form.addInflowCondition(topBoundary,topVelocity)
        form.solve()

        Plotter.plot(form, "u1")

        form = None
    
    """ Test Plot with p auto refine"""
    def test_plotpAutoRefine_u1(self): 
        print "pAutoRefine_u1"
        form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
        form.initializeSolution(meshTopo,polyOrder,delta_k)
        form.addZeroMeanPressureCondition()
        form.addWallCondition(notTopBoundary)
        form.addInflowCondition(topBoundary,topVelocity)
        form.solve()

        form.pRefine()
        Plotter.plot(form, "u1")

        form = None

    """ Test Plot with h auto refine"""
    def test_plothAutoRefine_u1(self):    
        print "hAutoRefine_u1"
        form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
        form.initializeSolution(meshTopo,polyOrder,delta_k)
        form.addZeroMeanPressureCondition()
        form.addWallCondition(notTopBoundary)
        form.addInflowCondition(topBoundary,topVelocity)
        form.solve()
        mesh = form.solution().mesh();

        form.hRefine()
        Plotter.plot(form, "u1")

        form = None

    """ Test Plot with p manual refine"""
    def test_plotpManualRefine_u1(self): 
        print "pManualRefine_u1"
        form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
        form.initializeSolution(meshTopo,polyOrder,delta_k)
        form.addZeroMeanPressureCondition()
        form.addWallCondition(notTopBoundary)
        form.addInflowCondition(topBoundary,topVelocity)
        form.solve()
        mesh = form.solution().mesh();

        mesh.pRefine([3,1])
        Plotter.plot(form, "u1")

        form = None

    """ Test Plot with h manual refine"""
    def test_plothManualRefine_u1(self): 
        #return
        print "hManualRefine_u1"
        form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
        form.initializeSolution(meshTopo,polyOrder,delta_k)
        form.addZeroMeanPressureCondition()
        form.addWallCondition(notTopBoundary)
        form.addInflowCondition(topBoundary,topVelocity)
        form.solve()
        mesh = form.solution().mesh();
        mesh.hRefine([0,1])

        plot(form, "u1")

        form = None

    """ Test Plot"""
    def test_plot_u2(self):
        print "Plot_u2"
        form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
        form.initializeSolution(meshTopo,polyOrder,delta_k)
        form.addZeroMeanPressureCondition()
        form.addWallCondition(notTopBoundary)
        form.addInflowCondition(topBoundary,topVelocity)
        form.solve()

        Plotter.plot(form, "u2")

        form = None
    
    """ Test Plot with p auto refine"""
    def test_plotPAutoRefine_u2(self): 
        print "pAutoRefine_u2"
        form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
        form.initializeSolution(meshTopo,polyOrder,delta_k)
        form.addZeroMeanPressureCondition()
        form.addWallCondition(notTopBoundary)
        form.addInflowCondition(topBoundary,topVelocity)
        form.solve()
        mesh = form.solution().mesh();

        form.pRefine()

        plot(form, "u2")

        form = None

    """ Test Plot with h auto refine"""
    def test_plothAutoRefine_u2(self):    
        print "hAutoRefine_u2"
        form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
        form.initializeSolution(meshTopo,polyOrder,delta_k)
        form.addZeroMeanPressureCondition()
        form.addWallCondition(notTopBoundary)
        form.addInflowCondition(topBoundary,topVelocity)
        form.solve()
        mesh = form.solution().mesh();

        form.hRefine()

        Plotter.plot(form, "u2")

        form = None

    """ Test Plot with p manual refine"""
    def test_plotpManualRefine_u2(self): 
        print "pManualRefine_u2"
        form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
        form.initializeSolution(meshTopo,polyOrder,delta_k)
        form.addZeroMeanPressureCondition()
        form.addWallCondition(notTopBoundary)
        form.addInflowCondition(topBoundary,topVelocity)
        form.solve()
        mesh = form.solution().mesh();

        mesh.pRefine([3,1])

        Plotter.plot(form, "u2")

        form = None

    """ Test Plot with h manual refine"""
    def test_plothManualRefine_u2(self): 
        #return
        print "hManualRefine_u2"
        form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
        form.initializeSolution(meshTopo,polyOrder,delta_k)
        form.addZeroMeanPressureCondition()
        form.addWallCondition(notTopBoundary)
        form.addInflowCondition(topBoundary,topVelocity)
        form.solve()
        mesh = form.solution().mesh();

        mesh.hRefine([0,1])

        Plotter.plot(form, "u2")

        form = None


    if __name__ == '__main__':
        unittest.main()
