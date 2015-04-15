from PyCamellia import *
from time import *

spaceDim = 2 # always two because we aren't handling anything 3D

"""
A class of functions to be used for solving formulations
more conveniently. This also allows testing and adjustments to be made 
to the solving of formulations without breaking the user interface.
"""

def steadyLinearSolve(form):
    print("Solving..."),
    start = time()
    form.solve()
    #mesh = form.solution().mesh();    
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

    #mesh = form.solution().mesh()
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

def steadyNonlinearSolve(form):
    print("Solving...")
    start = time()

    nonlinearSolve(form)

    #mesh = form.solution().mesh()
    energyError = form.solutionIncrement().energyErrorTotal()
    end = time()
    mins = (end - start) / 60
    secs = (end - start) % 60
    print("Solve completed in %i minute, %i seconds." % (mins, secs))
    print("Energy error is %0.3f" % (energyError))
