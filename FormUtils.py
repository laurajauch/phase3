from PyCamellia import *
from time import *
from ParsingUtils import *

DEBUG = True # IMPORTANT, needs to be True in order to run tests
spaceDim = 2 # always two because we aren't handling anything 3D

#MANUAL ENUM#
TRANSIENTLINEAR = 0
STEADYLINEAR = 1
STEADYNONLINEAR = 2

H = 0
P = 1


"""
A class of utility functions to make creating and solving formulations
more conveniently. This also allows testing and adjustments to be made 
to the creation and solving of formulations without breaking the user interface.
"""
def energyPerCell(form):
    perCellError = form.solution().energyErrorPerCell()
    for cellID in perCellError:
        if perCellError[cellID] > .01:
            print("Energy error for cell %i: %0.3f" % (cellID, perCellError[cellID]))
    return perCellError


# Create ----------------------------------------------------------------------
"""
Using other the below helper init methods, create the 
appropriate form from the given data.

data: the data to be used in creating a new form
return:
     form The created form 
     fType 0 is transient linear, 1 is steady linear, 2 is steady nonlinear
"""
def formInit(data): 
    print "in init"
    spaceDim = 2
    useConformingTraces = True
    mu = 1.0
    x0 = [0.,0.]
    delta_k = 1
    dt = 0.1

    stokes = data.getVariable("stokes")
    if not stokes:
        Re = data.getVariable("reynolds")
    transient = data.getVariable("transient")
    dims = data.getVariable("meshDimensions")
    numElements = data.getVariable("numElements")
    x0 = [0.,0.]
    polyOrder = data.getVariable("polyOrder")

    inflowRegions = data.getVariable("inflowRegions")
    inflowX = data.getVariable("inflowX")
    inflowY = data.getVariable("inflowY")
    outflowRegions = data.getVariable("outflowRegions")

    meshTopo = MeshFactory.rectilinearMeshTopology(dims, numElements, x0)
    
    #initialize type to 0
    fType = 0

    if stokes:
        if transient:
            fType = TRANSIENTLINEAR
            form = transientLinearInit(spaceDim, dims, numElements, polyOrder, dt)
            timeRamp = TimeRamp.timeRamp(form.getTimeFunction(),1.0)
        else:
            fType = STEADYLINEAR
            form = steadyLinearInit(dims, numElements, polyOrder)
    else:
        fType = STEADYNONLINEAR
        form = steadyNonlinearInit(spaceDim, Re, dims, numElements, polyOrder)

    allInflows = None         #Used for adding walls
    i = 0
    while i < len(inflowRegions):
        inflowFunction = Function.vectorize(inflowX[i], inflowY[i])
        if allInflows == None:
            allInflows = inflowRegions[i]
        else:
            allInflows = SpatialFilter.intersectionFilter(allInflows,inflowRegions[i])
               
        if transient:
            form.addInflowCondition(inflowRegions[i], timeRamp*inflowFunction) 
        else:
            form.addInflowCondition(inflowRegions[i], inflowFunction)
        i += 1
    
    allOutflows = None         #Used for adding walls
    i = 0
    while i < len(outflowRegions):
        if allOutflows == None:
            allOutflows = outflowRegions[i]
        else:
            allOutflows = SpatialFilter.intersectionFilter(allOutflows,outflowRegions[i])
        form.addOutflowCondition(outflowRegions[i])
        i += 1  
    
    #add wall conditions
    if(allInflows != None and allOutflows != None):
        form.addWallCondition(SpatialFilter.negatedFilter(allInflows | allOutflows))
    elif(allInflows != None and allOutflows == None):
        form.addWallCondition(SpatialFilter.negatedFilter(allInflows))

    elif(allInflows == None and allOutflows != None):
        form.addWallCondition(SpatialFilter.negatedFilter(allOutflows))

    return (form,fType)

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

# Refine----------------------------------------------------------------------
def autoRefine(data,refType): # refType: 0 is h, 1 is p      why pass data not form?

    form = data.getVariable("form")

    if refType == H:
        if data.getVariable("stokes"):
            form = linearHAutoRefine(form)
        else:
            form = nonlinearHAutoRefine(form)
    elif refType == P:
        if data.getVariable("stokes"):
            form = linearPAutoRefine(form)
        else:
            form = nonlinearPAutoRefine(form)

    return form 

def linearHAutoRefine(form):
    form.hRefine()
    form = steadyLinearSolve(form)
    return form
   
def linearPAutoRefine(form):
    form.pRefine()
    form = steadyLinearSolve(form)
    return form
    
def linearHManualRefine(form,cellList):
    print("Manually refining in h..."),
    if not DEBUG:
        cellList = cellList.split()
        cellList = map(int, cellList)
    mesh = form.solution().mesh();
    mesh.hRefine(cellList)
    elementCount = mesh.numActiveElements()
    globalDofCount = mesh.numGlobalDofs()
    print("New mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
    steadyLinearSolve(form)
    return form

def linearPManualRefine(form, cellList):
    print("Manually refining in p...")
    if not DEBUG:
        cellList = cellList.split()
        cellList = map(int, cellList)
    mesh = form.solution().mesh();
    mesh.pRefine(cellList)
    elementCount = mesh.numActiveElements()
    globalDofCount = mesh.numGlobalDofs()
    print("New mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
    steadyLinearSolve(form)
    return form

def nonlinearHAutoRefine(form):
    form.hRefine()
    form = steadyNonlinearSolve(form)
    return form
    
def nonlinearPAutoRefine(form):
    form.pRefine()
    form = steadyNonlinearSolve(form)
    return form
    
def nonlinearHManualRefine(form, cellList):
    print("Manually refining in h..."),
    if not DEBUG:
        cellList = cellList.split()
        cellList = map(int, cellList)
    mesh = form.solution().mesh()
    mesh.hRefine(cellList)
    elementCount = mesh.numActiveElements()
    globalDofCount = mesh.numGlobalDofs()
    print("New mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
    steadyNonlinearSolve(form)
    return form

def nonlinearPManualRefine(form, cellList):
    print("Manually refining in p..."),
    if not DEBUG:
        cellList = cellList.split()
        cellList = map(int, cellList)
    mesh = form.solution().mesh()
    mesh.pRefine(cellList)
    elementCount = mesh.numActiveElements()
    globalDofCount = mesh.numGlobalDofs()
    print("New mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
    steadyNonlinearSolve(form)
    return form

# Solve -----------------------------------------------------------------
def solve(data):
	ret = formInit(data)	
        form = ret[0] 
        fType = ret[1]

	if fType == TRANSIENTLINEAR:
		transientLinearSolve(form)
	elif fType == STEADYLINEAR:
		steadyLinearSolve(form)
	elif fType == STEADYNONLINEAR:
		steadyNonlinearSolve(form)
		
	return form 

def steadyLinearSolve(form):
    print("Solving..."),
    start = time()
    form.solve()
    mesh = form.solution().mesh();    
    energyError = form.solution().energyErrorTotal()
    end = time()
    mins = (end - start) / 60
    secs = (end - start) % 60
    print("Solve completed in %i minute, %i seconds." % (mins, secs))
    print("Energy error is %0.3f" % (energyError))
    
    return form

def transientLinearSolve(form):
    print("Solving...")
    start = time()

    dt = 0.1
    totalTime = 2.0
    numTimeSteps = int(totalTime / dt)    
    for timeStepNumber in range(numTimeSteps):
        form.solve()
        form.takeTimeStep()
        print("Time step %i completed" % timeStepNumber)

    mesh = form.solution().mesh()
    energyError = form.solution().energyErrorTotal()
    end = time()
    mins = (end - start) / 60
    secs = (end - start) % 60
    print("Solve completed in %i minute, %i seconds." % (mins, secs))
    print("Energy error is %0.3f" % (energyError))

# helper method
def nonlinearSolve(form):
    maxSteps = 10
    normOfIncrement = 1
    stepNumber = 0
    nonlinearThreshold = 1e-3
    while normOfIncrement > nonlinearThreshold and stepNumber < maxSteps:
        form.solveAndAccumulate()
        normOfIncrement = form.L2NormSolutionIncrement()
        print("L^2 norm of increment: %0.3f" % normOfIncrement)
        stepNumber += 1

    return form

def steadyNonlinearSolve(form):
    print("Solving...")
    start = time()

    form = nonlinearSolve(form)

    mesh = form.solution().mesh()
    energyError = form.solutionIncrement().energyErrorTotal()
    end = time()
    mins = (end - start) / 60
    secs = (end - start) % 60
    print("Solve completed in %i minute, %i seconds." % (mins, secs))
    print("Energy error is %0.3f" % (energyError))
    return form
