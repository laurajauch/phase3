from PyCamellia import *
from time import *

spaceDim = 2 # always two because we aren't handling anything 3D

"""
A class of functions to be used for creating formulations
more conveniently. This also allows testing and adjustments to be made 
to the creation and solving of formulations without breaking the user interface.
"""

def steadyLinearInit(dims, numElements, polyOrder):
    x0 = [0.,0.]
    meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
    delta_k = 1
    mu = 1.0
    useConformingTraces = True
    
    form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
    form.initializeSolution(meshTopo,polyOrder,delta_k)
    form.addZeroMeanPressureCondition()

    return form

def transientLinearInit(spaceDim, dims, numElements, polyOrder, dt):
    transient = True
    x0 = [0.,0.]
    meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
    delta_k = 1
    mu = 1.0
    useConformingTraces = True

    form = StokesVGPFormulation(spaceDim, useConformingTraces, mu, transient, dt)    
    form.initializeSolution(meshTopo, polyOrder, delta_k)
    form.addZeroMeanPressureCondition()

    return form

def steadyNonlinearInit(spaceDim, re, dims, numElements, polyOrder):
    x0 = [0.,0.]
    meshTopo = MeshFactory.rectilinearMeshTopology(dims, numElements, x0)
    delta_k = 1

    form = NavierStokesVGPFormulation(meshTopo, re, polyOrder, delta_k)
    form.addZeroMeanPressureCondition()
    return form
