from PyCamellia import *
from Plotter import *
import unittest
from itertools import chain, combinations 

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
    


class TestPlotterP(unittest.TestCase):
    """ Test Plot"""
    def test_plot_p(self):
        print "Plot_p"
        form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
        form.initializeSolution(meshTopo,polyOrder,delta_k)
        form.addZeroMeanPressureCondition()
        form.addWallCondition(notTopBoundary)
        form.addInflowCondition(topBoundary,topVelocity)
        form.solve()

        plot(form, "p")

        form = None
    
    """ Test Plot with p auto refine"""
    def test_plotPAutoRefine_p(self): 
        print "pAutoRefine_p"
        form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
        form.initializeSolution(meshTopo,polyOrder,delta_k)
        form.addZeroMeanPressureCondition()
        form.addWallCondition(notTopBoundary)
        form.addInflowCondition(topBoundary,topVelocity)
        form.solve()
        form.pRefine()

        plot(form, "p")

        form = None

    """ Test Plot with h auto refine"""
    def test_plothAutoRefine_p(self):    
        print "hAutoRefine_p"
        form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
        form.initializeSolution(meshTopo,polyOrder,delta_k)
        form.addZeroMeanPressureCondition()
        form.addWallCondition(notTopBoundary)
        form.addInflowCondition(topBoundary,topVelocity)
        form.solve()
        form.hRefine()

        plot(form, "p")

        form = None  

    """ Test Plot with p manual refine"""
    def test_plotpManualRefine_p(self): 
        print "pManualRefine_p"
        form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
        form.initializeSolution(meshTopo,polyOrder,delta_k)
        form.addZeroMeanPressureCondition()
        form.addWallCondition(notTopBoundary)
        form.addInflowCondition(topBoundary,topVelocity)
        form.solve()
        mesh = form.solution().mesh();
        mesh.pRefine([3,1])

        plot(form, "p")

        form = None

    """ Test Plot with h manual refine"""
    def test_plothManualRefine_p(self): 
        #return
        print "hManualRefine_p"
        form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
        meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
        form.initializeSolution(meshTopo,polyOrder,delta_k)
        form.addZeroMeanPressureCondition()
        form.addWallCondition(notTopBoundary)
        form.addInflowCondition(topBoundary,topVelocity)
        form.solve()
        mesh = form.solution().mesh();
        mesh.hRefine([0,1])

        plot(form, "p")

        form = None
