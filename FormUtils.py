from PyCamellia import *
from time import *

DEBUG = True # IMPORTANT, needs to be True in order to run tests
spaceDim = 2 # always two because we aren't handling anything 3D

"""
A class of utility functions to make creating and solving formulations
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

# unused
def addWall(form, newWall):
    form.addWallCondition(newWall)

# unused
def addInflow(form, newInflow, newVelocity):
    form.addInflowCondition(newInflow, newVelocity)

# unused
def addOutflow(form, newOutflow):
    form.addOutflowCondition(newOutflow)

def energyPerCell(form):
    perCellError = form.solution().energyErrorPerCell()
    for cellID in perCellError:
        if perCellError[cellID] > .01:
            print("Energy error for cell %i: %0.3f" % (cellID, perCellError[cellID]))
    return perCellError

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

# -------------------------------------------------------------

def steadyLinearHAutoRefine(form):
    print("Automatically refining in h...")
    form.hRefine()
    mesh = form.solution().mesh();
    elementCount = mesh.numActiveElements()
    globalDofCount = mesh.numGlobalDofs()
    print("New mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
    steadyLinearSolve(form)
    return form

def steadyLinearPAutoRefine(form):
    print("Automatically refining in p...")
    form.pRefine()
    mesh = form.solution().mesh();
    elementCount = mesh.numActiveElements()
    globalDofCount = mesh.numGlobalDofs()
    print("New mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
    steadyLinearSolve(form)
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

# ---------------------------------------------------------------

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

# ---------------------------------------------------------------

def steadyNonlinearInit(spaceDim, re, dims, numElements, polyOrder):
    x0 = [0.,0.]
    meshTopo = MeshFactory.rectilinearMeshTopology(dims, numElements, x0)
    delta_k = 1
    form = NavierStokesVGPFormulation(meshTopo, re, polyOrder, delta_k)
    form.addZeroMeanPressureCondition()
    return form

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

def steadyNonlinearSolve(form):
    print("Solving...")
    start = time()

    nonlinearSolve(form)

    mesh = form.solution().mesh()
    energyError = form.solutionIncrement().energyErrorTotal()
    end = time()
    mins = (end - start) / 60
    secs = (end - start) % 60
    print("Solve completed in %i minute, %i seconds." % (mins, secs))
    print("Energy error is %0.3f" % (energyError))

# -------------------------------------------------------------

def nonlinearHAutoRefine(form):
    print("Automatically refining in h..."),
    form.hRefine()
    mesh = form.solution().mesh()
    elementCount = mesh.numActiveElements()
    globalDofCount = mesh.numGlobalDofs() 
    print("New mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
    steadyNonlinearSolve(form)
    return form

def nonlinearPAutoRefine(form):
    print("Automatically refining in p..."),
    form.pRefine()
    mesh = form.solution().mesh()
    elementCount = mesh.numActiveElements()
    globalDofCount = mesh.numGlobalDofs()
    print("New mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
    steadyNonlinearSolve(form)
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

# -------------------------------------------------------------

def solve(data):
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
	numInflows = data.getVariable("numInflows")
	inflowRegions = data.getVariable("inflowRegions")
	inflowX = data.getVariable("inflowX")
	inflowY = data.getVariable("inflowY")
	numOutflows = data.getVariable("numOutflows")
	outflowRegions = data.getVariable("outflowRegions")
	numWalls = data.getVariable("numWalls")
	wallRegions = data.getVariable("wallRegions")
	meshTopo = MeshFactory.rectilinearMeshTopology(dims, numElements, x0)


	transientLinear = False
	steadyLinear = False
	steadyNonlinear = False

	if stokes:
	    if transient:
	        transientLinear = True
		form = transientLinearInit(spaceDim, dims, numElements, polyOrder, dt)
	        timeRamp = TimeRamp.timeRamp(form.getTimeFunction(),1.0)
	    else:
		steadyLinear = True
		form = steadyLinearInit(dims, numElements, polyOrder)
	else:
	    steadyNonlinear = True
	    form = steadyNonlinearInit(spaceDim, Re, dims, numElements, polyOrder)
	
	i = 0
	while i < numInflows:
	    inflowFunction = Function.vectorize(inflowX[i], inflowY[i])
	    if transient:
	        form.addInflowCondition(inflowRegions[i], timeRamp*inflowFunction)
	    else:
	        form.addInflowCondition(inflowRegions[i], inflowFunction)
	    i += 1
	    
	i = 0
	while i < numOutflows:
	    form.addOutflowCondition(outflowRegions[i])
	    i += 1  
	i = 1
	for i in wallRegions:
	    form.addWallCondition(i)
	

	if transientLinear:
		transientLinearSolve(form)
	elif steadyLinear:
		steadyLinearSolve(form)
	elif steadyNonlinear:
		steadyNonlinearSolve(form)

		
	return form 
