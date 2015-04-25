from PyCamellia import *
from FormUtils import *
from InputData import *
from DataUtils import *
import unittest

"""
A whole bunch of variable so that the tests are not as cluttered
"""

data = getDataList()

re = data["reynolds"]
spaceDim = data["spaceDim"]
useConformingTraces = data["useConformingTraces"]
mu = data["mu"]
dims = data["meshDimensions"]
numElements = data["numElements"]
x0 = data["x0"]
polyOrder = data["polyOrder"]
delta_k = data["delta_k"]
dt = data["dt"]
transient = True

meshTopo = MeshFactory.rectilinearMeshTopology(data["meshDimensions"], data["numElements"], data["x0"])

threshold = .05
totalTime = 2.0
numTimeSteps = int(totalTime / dt)

topBoundary = SpatialFilter.matchingY(1.0)
notTopBoundary = SpatialFilter.negatedFilter(topBoundary)
x = Function.xn(1)
rampWidth = 1./64
H_left = Function.heaviside(rampWidth)
H_right = Function.heaviside(1.0-rampWidth);
ramp = (1-H_right) * H_left + (1./rampWidth) * (1-H_left) * x + (1./rampWidth) * H_right * (1-x)
zero = Function.constant(0)
topVelocity = Function.vectorize(ramp,zero)

"""
Test each function in SolutionFns.
form is the formulation being operated on by SolutionFns functions.
foo is the formulation being operated on by PyCamellia functions.
Note: Always recreate the mesh otherwise the mesh will be affected when more than
one refinement test is run.
"""
class TestFormUtils(unittest.TestCase):

    """Test energyPerCell"""
    def test_energyPerCell(self):
        testForm = steadyLinearInit(data["meshDimensions"], data["numElements"], data["polyOrder"])
        
        meshTopo = MeshFactory.rectilinearMeshTopology(data["meshDimensions"], data["numElements"], data["x0"])
        expectedForm = StokesVGPFormulation(data["spaceDim"], data["useConformingTraces"], data["mu"])
        expectedForm.initializeSolution(meshTopo, data["polyOrder"], data["delta_k"])
        expectedForm.addZeroMeanPressureCondition()

        testForm.addWallCondition(notTopBoundary)
        testForm.addInflowCondition(topBoundary, topVelocity)
        testForm.solve()

        testPerCellError = energyPerCell(testForm)
        
        expectedForm.addWallCondition(notTopBoundary)
        expectedForm.addInflowCondition(topBoundary,topVelocity)
        expectedForm.solve()

        expectedPerCellError = expectedForm.solution().energyErrorPerCell()
        
        for cellID in expectedPerCellError:
            if expectedPerCellError[cellID] > .01:
                self.assertAlmostEqual(testPerCellError[cellID], expectedPerCellError[cellID])


# Create ----------------------------------------------------------------------

    """Test formInit"""
    def test_formInit(self):
        return # does not pass, TypeError: in method 'Function_vectorize', argument 1 of type 'FunctionPtr'

        # transient linear, 0
        inputData = InputData()
        populateInputData(inputData)
        inputData.addVariable("stokes", True)
        inputData.addVariable("transient", True)
        (testForm, fType) = formInit(inputData)

        expectedForm = transientLinearInit(data["spaceDim"], data["meshDimensions"], data["numElements"], data["polyOrder"], data["dt"])

        testForm.solve()
        testMesh = testForm.solution().mesh()
        testEnergyError = testForm.solution().energyErrorTotal()
        testElementCount = testMesh.numActiveElements()
        testGlobalDofCount = testMesh.numGlobalDofs()
        
        expectedForm.solve()
        expectedMesh = expectedForm.solution().mesh()
        expectedEnergyError = expectedForm.solution().energyErrorTotal()
        expectedElementCount = expectedMesh.numActiveElements()
        expectedGlobalDofCount = expectedMesh.numGlobalDofs()
        
        self.assertIsNotNone(testForm)
        self.assertEqual(0, fType)
        self.assertAlmostEqual(15, expectedElementCount, testElementCount)
        self.assertEqual(2260, expectedGlobalDofCount, testGlobalDofCount)
        self.assertEqual(0.000, expectedEnergyError, testEnergyError)

        # steady linear, 1
        inputData = InputData()
        populateInputData(inputData)
        inputData.addVariable("stokes", True)
        inputData.addVariable("transient", False)
        (testForm, fType) = formInit(inputData)

        expectedForm = steadyLinearInit(data["spaceDim"], data["meshDimensions"], data["numElements"], data["polyOrder"], data["dt"])

        testForm.solve()
        testMesh = testForm.solution().mesh()
        testEnergyError = testForm.solution().energyErrorTotal()
        testElementCount = testMesh.numActiveElements()
        testGlobalDofCount = testMesh.numGlobalDofs()
        
        expectedForm.solve()
        expectedMesh = expectedForm.solution().mesh()
        expectedEnergyError = expectedForm.solution().energyErrorTotal()
        expectedElementCount = expectedMesh.numActiveElements()
        expectedGlobalDofCount = expectedMesh.numGlobalDofs()
        
        self.assertIsNotNone(testForm)
        self.assertEqual(1, fType)
        self.assertAlmostEqual(15, expectedElementCount, testElementCount)
        self.assertEqual(2260, expectedGlobalDofCount, testGlobalDofCount)
        self.assertEqual(0.000, expectedEnergyError, testEnergyError)

        # steady nonlinear, 2
        inputData = InputData()
        populateInputData(inputData)
        inputData.addVariable("stokes", False)
        inputData.addVariable("transient", False)
        (testForm, fType) = formInit(inputData)

        expectedForm = steadyNonlinearInit(data["spaceDim"], data["reynolds"], data["meshDimensions"], data["numElements"], data["polyOrder"])

        steadyNonlinearSolve(testForm)
        testMesh = testForm.solution().mesh()
        testEnergyError = testForm.solution().energyErrorTotal()
        testElementCount = testMesh.numActiveElements()
        testGlobalDofCount = testMesh.numGlobalDofs()
        
        steadyNonlinearSolve(expectedForm)
        expectedMesh = expectedForm.solution().mesh()
        expectedEnergyError = expectedForm.solution().energyErrorTotal()
        expectedElementCount = expectedMesh.numActiveElements()
        expectedGlobalDofCount = expectedMesh.numGlobalDofs()
        
        self.assertIsNotNone(testForm)
        self.assertEqual(2, fType)
        self.assertAlmostEqual(15, expectedElementCount, testElementCount)
        self.assertEqual(2260, expectedGlobalDofCount, testGlobalDofCount)
        self.assertEqual(0.000, expectedEnergyError, testEnergyError)

    """Test steadyLinearInit"""
    def test_steadyLinearInit(self):
        testForm = steadyLinearInit(data["meshDimensions"], data["numElements"], data["polyOrder"])
        
        meshTopo = MeshFactory.rectilinearMeshTopology(data["meshDimensions"], data["numElements"], data["x0"])
        expectedForm = StokesVGPFormulation(data["spaceDim"], data["useConformingTraces"], data["mu"])
        expectedForm.initializeSolution(meshTopo, data["polyOrder"], data["delta_k"])
        expectedForm.addZeroMeanPressureCondition()
        
        testForm.solve()
        testMesh = testForm.solution().mesh()
        testEnergyError = testForm.solution().energyErrorTotal()
        testElementCount = testMesh.numActiveElements()
        testGlobalDofCount = testMesh.numGlobalDofs()
        
        expectedForm.solve()
        expectedMesh = expectedForm.solution().mesh()
        expectedEnergyError = expectedForm.solution().energyErrorTotal()
        expectedElementCount = expectedMesh.numActiveElements()
        expectedGlobalDofCount = expectedMesh.numGlobalDofs()
        
        self.assertIsNotNone(testForm)
        self.assertAlmostEqual(15, expectedElementCount, testElementCount)
        self.assertEqual(2260, expectedGlobalDofCount, testGlobalDofCount)
        self.assertEqual(0.000, expectedEnergyError, testEnergyError)

    """Test transientLinearInit"""
    def test_transientLinearInit(self):
        testForm = transientLinearInit(data["spaceDim"], data["meshDimensions"], data["numElements"], data["polyOrder"], data["dt"])
     
        meshTopo = MeshFactory.rectilinearMeshTopology(data["meshDimensions"], data["numElements"], data["x0"])
        expectedForm = StokesVGPFormulation(data["spaceDim"], data["useConformingTraces"], data["mu"])
        expectedForm.initializeSolution(meshTopo, data["polyOrder"], data["delta_k"])
        expectedForm.addZeroMeanPressureCondition()
                
        testForm.solve()
        mesh = testForm.solution().mesh()
        energyError = testForm.solution().energyErrorTotal()
        elementCount = mesh.numActiveElements()
        globalDofCount = mesh.numGlobalDofs()
        
        expectedForm.solve()
        expectedMesh = expectedForm.solution().mesh()
        expectedEnergyError = expectedForm.solution().energyErrorTotal()
        expectedElementCount = expectedMesh.numActiveElements()
        expectedGlobalDofCount = expectedMesh.numGlobalDofs()
        
        self.assertIsNotNone(testForm)
        self.assertAlmostEqual(15, expectedElementCount, elementCount)
        self.assertEqual(2260, expectedGlobalDofCount, globalDofCount)
        self.assertEqual(0.000, expectedEnergyError, energyError)

    """Test steadyNonlinearInit"""
    def test_steadyNonlinearInit(self):        
        testForm = steadyNonlinearInit(data["spaceDim"], data["reynolds"], data["meshDimensions"], data["numElements"], data["polyOrder"])
        testForm.addWallCondition(notTopBoundary)
        testForm.addInflowCondition(topBoundary, topVelocity)
       
        meshTopo = MeshFactory.rectilinearMeshTopology(data["meshDimensions"], data["numElements"], data["x0"])
        expectedForm = NavierStokesVGPFormulation(meshTopo, data["reynolds"], data["polyOrder"], data["delta_k"])
        expectedForm.addZeroMeanPressureCondition()
        expectedForm.addWallCondition(notTopBoundary)
        expectedForm.addInflowCondition(topBoundary,topVelocity)
        
        maxSteps = 10
        nonlinearThreshold = 1e-3
        normOfIncrement = 1
        stepNumber = 0
        while normOfIncrement > nonlinearThreshold and stepNumber < maxSteps:
            testForm.solveAndAccumulate()
            expectedForm.solveAndAccumulate()
            normOfIncrement = testForm.L2NormSolutionIncrement()
            expectedNormOfIncrement = expectedForm.L2NormSolutionIncrement()
            self.assertAlmostEqual(normOfIncrement, expectedNormOfIncrement)
            stepNumber += 1


# Refine----------------------------------------------------------------------

    """Test autoRefine"""
    def test_autoRefine(self):
        pass

    """Test linearHAutoRefine"""
    def test_linearHAutoRefine(self):
        testForm = steadyLinearInit(data["meshDimensions"], data["numElements"], data["polyOrder"])
        testForm.addWallCondition(notTopBoundary)
        testForm.addInflowCondition(topBoundary, topVelocity)
        steadyLinearSolve(testForm)

        meshTopo = MeshFactory.rectilinearMeshTopology(data["meshDimensions"], data["numElements"], data["x0"])
        expectedForm = StokesVGPFormulation(data["spaceDim"], data["useConformingTraces"], data["mu"])
        expectedForm.initializeSolution(meshTopo, data["polyOrder"], data["delta_k"])
        expectedForm.addZeroMeanPressureCondition()    
        expectedForm.addWallCondition(notTopBoundary)
        expectedForm.addInflowCondition(topBoundary,topVelocity)
        expectedForm.solve()
        
        linearHAutoRefine(testForm)
        expectedForm.hRefine()
        expectedForm.solve()

        testMesh = testForm.solution().mesh()
        testEnergyError = testForm.solution().energyErrorTotal()
        testElementCount = testMesh.numActiveElements()
        testGlobalDofCount = testMesh.numGlobalDofs()
        
        expectedMesh = expectedForm.solution().mesh()
        expectedEnergyError = expectedForm.solution().energyErrorTotal()   
        expectedElementCount = expectedMesh.numActiveElements()
        expectedGlobalDofCount = expectedMesh.numGlobalDofs()
        
        self.assertEqual(21, expectedElementCount, testElementCount)
        self.assertEqual(3112, expectedGlobalDofCount, testGlobalDofCount)
        self.assertAlmostEqual(expectedEnergyError, testEnergyError)
        self.assertAlmostEqual(113.18, testEnergyError, 3)

    """Test linearPAutoRefine"""
    def test_linearPAutoRefine(self):
        return # test does not pass, throws error in Camellia/src/CellTools/CamelliaCellTools.cpp:1035:
        testForm = steadyLinearInit(data["meshDimensions"], data["numElements"], data["polyOrder"])
        testForm.addWallCondition(notTopBoundary)
        testForm.addInflowCondition(topBoundary, topVelocity)
        steadyLinearSolve(testForm)

        meshTopo = MeshFactory.rectilinearMeshTopology(data["meshDimensions"], data["numElements"], data["x0"])
        expectedForm = StokesVGPFormulation(data["spaceDim"], data["useConformingTraces"], data["mu"])
        expectedForm.initializeSolution(meshTopo, data["polyOrder"], data["delta_k"])
        expectedForm.addZeroMeanPressureCondition()    
        expectedForm.addWallCondition(notTopBoundary)
        expectedForm.addInflowCondition(topBoundary,topVelocity)
        expectedForm.solve()
        
        linearPAutoRefine(testForm)
        expectedForm.pRefine()
        expectedForm.solve()

        testMesh = testForm.solution().mesh()
        testEnergyError = testForm.solution().energyErrorTotal()
        testElementCount = testMesh.numActiveElements()
        testGlobalDofCount = testMesh.numGlobalDofs()
        
        expectedMesh = expectedForm.solution().mesh()
        expectedEnergyError = expectedForm.solution().energyErrorTotal()   
        expectedElementCount = expectedMesh.numActiveElements()
        expectedGlobalDofCount = expectedMesh.numGlobalDofs()
        
        self.assertEqual(21, expectedElementCount, testElementCount)
        self.assertEqual(3112, expectedGlobalDofCount, testGlobalDofCount)
        self.assertAlmostEqual(expectedEnergyError, testEnergyError)
        self.assertAlmostEqual(113.18, testEnergyError, 3)

    """Test linearHManualRefine"""
    def test_linearHManualRefine(self):
        testForm = steadyLinearInit(data["meshDimensions"], data["numElements"], data["polyOrder"])
        testForm.addWallCondition(notTopBoundary)
        testForm.addInflowCondition(topBoundary, topVelocity)
        steadyLinearSolve(testForm)

        meshTopo = MeshFactory.rectilinearMeshTopology(data["meshDimensions"], data["numElements"], data["x0"])
        expectedForm = StokesVGPFormulation(data["spaceDim"], data["useConformingTraces"], data["mu"])
        expectedForm.initializeSolution(meshTopo, data["polyOrder"], data["delta_k"])
        expectedForm.addZeroMeanPressureCondition()    
        expectedForm.addWallCondition(notTopBoundary)
        expectedForm.addInflowCondition(topBoundary,topVelocity)
        expectedForm.solve()
 
        testMesh = testForm.solution().mesh()
        expectedMesh = expectedForm.solution().mesh()
        testCellIDs = testMesh.getActiveCellIDs()
        expectedCellIDs = expectedMesh.getActiveCellIDs()

        linearHManualRefine(testForm, testCellIDs)
        expectedMesh.hRefine(expectedCellIDs)
        expectedForm.solve()

        testMesh = testForm.solution().mesh()
        testEnergyError = testForm.solution().energyErrorTotal()
        testElementCount = testMesh.numActiveElements()
        testGlobalDofCount = testMesh.numGlobalDofs()
        
        expectedMesh = expectedForm.solution().mesh()
        expectedEnergyError = expectedForm.solution().energyErrorTotal()   
        expectedElementCount = expectedMesh.numActiveElements()
        expectedGlobalDofCount = expectedMesh.numGlobalDofs()
        
        self.assertEqual(60, expectedElementCount, testElementCount)
        self.assertEqual(8778, expectedGlobalDofCount, testGlobalDofCount)
        self.assertAlmostEqual(expectedEnergyError, testEnergyError)
        self.assertAlmostEqual(113.18, testEnergyError, 3)

    """Test linearPManualRefine"""
    def test_linearPManualRefine(self):
        testForm = steadyLinearInit(data["meshDimensions"], data["numElements"], data["polyOrder"])
        testForm.addWallCondition(notTopBoundary)
        testForm.addInflowCondition(topBoundary, topVelocity)
        steadyLinearSolve(testForm)

        meshTopo = MeshFactory.rectilinearMeshTopology(data["meshDimensions"], data["numElements"], data["x0"])
        expectedForm = StokesVGPFormulation(data["spaceDim"], data["useConformingTraces"], data["mu"])
        expectedForm.initializeSolution(meshTopo, data["polyOrder"], data["delta_k"])
        expectedForm.addZeroMeanPressureCondition()    
        expectedForm.addWallCondition(notTopBoundary)
        expectedForm.addInflowCondition(topBoundary,topVelocity)
        expectedForm.solve()
 
        testMesh = testForm.solution().mesh()
        expectedMesh = expectedForm.solution().mesh()
        testCellIDs = testMesh.getActiveCellIDs()
        expectedCellIDs = expectedMesh.getActiveCellIDs()

        linearPManualRefine(testForm, testCellIDs)
        expectedMesh.pRefine(expectedCellIDs)
        expectedForm.solve()

        testMesh = testForm.solution().mesh()
        testEnergyError = testForm.solution().energyErrorTotal()
        testElementCount = testMesh.numActiveElements()
        testGlobalDofCount = testMesh.numGlobalDofs()
        
        expectedMesh = expectedForm.solution().mesh()
        expectedEnergyError = expectedForm.solution().energyErrorTotal()   
        expectedElementCount = expectedMesh.numActiveElements()
        expectedGlobalDofCount = expectedMesh.numGlobalDofs()
        
        self.assertEqual(15, expectedElementCount, testElementCount)
        self.assertEqual(3357, expectedGlobalDofCount, testGlobalDofCount)
        self.assertAlmostEqual(expectedEnergyError, testEnergyError)
        self.assertAlmostEqual(107.4038432214537, testEnergyError, 15)

    """Test steadyNonlinearHAutoRefine"""
    def test_steadyNonlinearHAutoRefine(self):
        testForm = steadyNonlinearInit(data["spaceDim"], data["reynolds"], data["meshDimensions"], data["numElements"], data["polyOrder"])
        testForm.addWallCondition(notTopBoundary)
        testForm.addInflowCondition(topBoundary, topVelocity)
        steadyNonlinearSolve(testForm)

        meshTopo = MeshFactory.rectilinearMeshTopology(data["meshDimensions"], data["numElements"], data["x0"])
        expectedForm = NavierStokesVGPFormulation(meshTopo, data["reynolds"], data["polyOrder"], data["delta_k"])
        expectedForm.addZeroMeanPressureCondition()
        expectedForm.addWallCondition(notTopBoundary)
        expectedForm.addInflowCondition(topBoundary,topVelocity)
        steadyNonlinearSolve(expectedForm)
               
        nonlinearHAutoRefine(testForm)
        expectedForm.hRefine()
        steadyNonlinearSolve(expectedForm)

        testMesh = testForm.solution().mesh()
        testEnergyError = testForm.solutionIncrement().energyErrorTotal()
        testElementCount = testMesh.numActiveElements()
        testGlobalDofCount = testMesh.numGlobalDofs()
        
        expectedMesh = expectedForm.solution().mesh()
        expectedEnergyError = expectedForm.solutionIncrement().energyErrorTotal()
        expectedElementCount = expectedMesh.numActiveElements()
        expectedGlobalDofCount = expectedMesh.numGlobalDofs()
        
        self.assertEqual(60, expectedElementCount, testElementCount)
        self.assertEqual(8896, expectedGlobalDofCount, testGlobalDofCount)
        self.assertAlmostEqual(expectedEnergyError, testEnergyError)
        self.assertAlmostEqual(0.000, testEnergyError, 3)


    """Test steadyNonlinearPAutoRefine"""
    def test_steadyNonlinearPAutoRefine(self):
        testForm = steadyNonlinearInit(data["spaceDim"], data["reynolds"], data["meshDimensions"], data["numElements"], data["polyOrder"])
        testForm.addWallCondition(notTopBoundary)
        testForm.addInflowCondition(topBoundary, topVelocity)
        steadyNonlinearSolve(testForm)

        meshTopo = MeshFactory.rectilinearMeshTopology(data["meshDimensions"], data["numElements"], data["x0"])
        expectedForm = NavierStokesVGPFormulation(meshTopo, data["reynolds"], data["polyOrder"], data["delta_k"])
        expectedForm.addZeroMeanPressureCondition()
        expectedForm.addWallCondition(notTopBoundary)
        expectedForm.addInflowCondition(topBoundary,topVelocity)
        steadyNonlinearSolve(expectedForm)
               
        nonlinearPAutoRefine(testForm)
        expectedForm.pRefine()
        steadyNonlinearSolve(expectedForm)

        testMesh = testForm.solution().mesh()
        testEnergyError = testForm.solutionIncrement().energyErrorTotal()
        testElementCount = testMesh.numActiveElements()
        testGlobalDofCount = testMesh.numGlobalDofs()
        
        expectedMesh = expectedForm.solution().mesh()
        expectedEnergyError = expectedForm.solutionIncrement().energyErrorTotal()
        expectedElementCount = expectedMesh.numActiveElements()
        expectedGlobalDofCount = expectedMesh.numGlobalDofs()
        
        self.assertEqual(15, expectedElementCount, testElementCount)
        self.assertEqual(3385, expectedGlobalDofCount, testGlobalDofCount)
        self.assertAlmostEqual(expectedEnergyError, testEnergyError)
        self.assertAlmostEqual(0.000, testEnergyError, 3)

    """Test steadyNonlinearHManualRefine"""
    def test_steadyNonlinearHManualRefine(self):
        return # test does not pass, seg fault, but not used in this PyCamellia version
        testForm = steadyNonlinearInit(data["spaceDim"], data["reynolds"], data["meshDimensions"], data["numElements"], data["polyOrder"])
        testForm.addWallCondition(notTopBoundary)
        testForm.addInflowCondition(topBoundary, topVelocity)
        steadyNonlinearSolve(testForm)

        meshTopo = MeshFactory.rectilinearMeshTopology(data["meshDimensions"], data["numElements"], data["x0"])
        expectedForm = NavierStokesVGPFormulation(meshTopo, data["reynolds"], data["polyOrder"], data["delta_k"])
        expectedForm.addZeroMeanPressureCondition()
        expectedForm.addWallCondition(notTopBoundary)
        expectedForm.addInflowCondition(topBoundary,topVelocity)
        steadyNonlinearSolve(expectedForm)

        testMesh = testForm.solution().mesh()
        expectedMesh = expectedForm.solution().mesh()
        testCellIDs = testMesh.getActiveCellIDs()
        expectedCellIDs = expectedMesh.getActiveCellIDs()

        nonlinearPManualRefine(testForm, testCellIDs)
        expectedMesh.pRefine(expectedCellIDs)
        steadyNonlinearSolve(expectedForm)

        testMesh = testForm.solution().mesh()
        testEnergyError = testForm.solution().energyErrorTotal()
        testElementCount = testMesh.numActiveElements()
        testGlobalDofCount = testMesh.numGlobalDofs()
        
        expectedMesh = expectedForm.solution().mesh()
        expectedEnergyError = expectedForm.solution().energyErrorTotal()   
        expectedElementCount = expectedMesh.numActiveElements()
        expectedGlobalDofCount = expectedMesh.numGlobalDofs()
        
        self.assertEqual(15, expectedElementCount, testElementCount)
        self.assertEqual(3357, expectedGlobalDofCount, testGlobalDofCount)
        self.assertAlmostEqual(expectedEnergyError, testEnergyError)
        self.assertAlmostEqual(107.4038432214537, testEnergyError, 15)
       
    """Test steadyNonlinearPManualRefine"""
    def test_steadyNonlinearPManualRefine(self):
        return # test does not pass, seg fault, but not used in this PyCamellia version
        testForm = steadyNonlinearInit(data["spaceDim"], data["reynolds"], data["meshDimensions"], data["numElements"], data["polyOrder"])
        testForm.addWallCondition(notTopBoundary)
        testForm.addInflowCondition(topBoundary, topVelocity)
        steadyNonlinearSolve(testForm)

        meshTopo = MeshFactory.rectilinearMeshTopology(data["meshDimensions"], data["numElements"], data["x0"])
        expectedForm = NavierStokesVGPFormulation(meshTopo, data["reynolds"], data["polyOrder"], data["delta_k"])
        expectedForm.addZeroMeanPressureCondition()
        expectedForm.addWallCondition(notTopBoundary)
        expectedForm.addInflowCondition(topBoundary,topVelocity)
        steadyNonlinearSolve(expectedForm)
        
        testMesh = testForm.solution().mesh()
        expectedMesh = expectedForm.solution().mesh()
        testCellIDs = testMesh.getActiveCellIDs()
        expectedCellIDs = expectedMesh.getActiveCellIDs()

        nonlinearHManualRefine(testForm, testCellIDs)
        expectedMesh.hRefine(expectedCellIDs)
        steadyNonlinearSolve(expectedForm)

        testMesh = testForm.solution().mesh()
        testEnergyError = testForm.solution().energyErrorTotal()
        testElementCount = testMesh.numActiveElements()
        testGlobalDofCount = testMesh.numGlobalDofs()
        
        expectedMesh = expectedForm.solution().mesh()
        expectedEnergyError = expectedForm.solution().energyErrorTotal()   
        expectedElementCount = expectedMesh.numActiveElements()
        expectedGlobalDofCount = expectedMesh.numGlobalDofs()
        
        self.assertEqual(15, expectedElementCount, testElementCount)
        self.assertEqual(3357, expectedGlobalDofCount, testGlobalDofCount)
        self.assertAlmostEqual(expectedEnergyError, testEnergyError)
        self.assertAlmostEqual(107.4038432214537, testEnergyError, 15)


# Solve -----------------------------------------------------------------

    """Test solve"""
    def test_solve(self):
        pass

    """Test steadyLinearSolve"""
    def test_steadyLinearSolve(self):
        testForm = steadyLinearInit(data["meshDimensions"], data["numElements"], data["polyOrder"])
        testForm.addWallCondition(notTopBoundary)
        testForm.addInflowCondition(topBoundary, topVelocity)
        steadyLinearSolve(testForm)

        meshTopo = MeshFactory.rectilinearMeshTopology(data["meshDimensions"], data["numElements"], data["x0"])
        expectedForm = StokesVGPFormulation(data["spaceDim"], data["useConformingTraces"], data["mu"])
        expectedForm.initializeSolution(meshTopo, data["polyOrder"], data["delta_k"])
        expectedForm.addZeroMeanPressureCondition()    
        expectedForm.addWallCondition(notTopBoundary)
        expectedForm.addInflowCondition(topBoundary,topVelocity)
        expectedForm.solve()

        testMesh = testForm.solution().mesh()
        testEnergyError = testForm.solution().energyErrorTotal()
        testElementCount = testMesh.numActiveElements()
        testGlobalDofCount = testMesh.numGlobalDofs()
        
        expectedMesh = expectedForm.solution().mesh()
        expectedEnergyError = expectedForm.solution().energyErrorTotal()
        expectedElementCount = expectedMesh.numActiveElements()
        expectedGlobalDofCount = expectedMesh.numGlobalDofs()
        
        self.assertIsNotNone(testForm)
        self.assertAlmostEqual(15, expectedElementCount, testElementCount)
        self.assertEqual(2260, expectedGlobalDofCount, testGlobalDofCount)
        self.assertEqual(expectedEnergyError, testEnergyError)
        
    """Test transientLinearSolve"""
    def test_transientLinearSolve(self):
        return # does not pass, seg fault
        testForm = transientLinearInit(data["spaceDim"], data["meshDimensions"], data["numElements"], data["polyOrder"], data["dt"])
        testForm.addWallCondition(notTopBoundary)
        testForm.addInflowCondition(topBoundary, topVelocity)
        transientLinearSolve(testForm)

        meshTopo = MeshFactory.rectilinearMeshTopology(data["meshDimensions"], data["numElements"], data["x0"])
        expectedForm = StokesVGPFormulation(data["spaceDim"], data["useConformingTraces"], data["mu"])
        expectedForm.initializeSolution(meshTopo, data["polyOrder"], data["delta_k"])
        expectedForm.addZeroMeanPressureCondition()    
        expectedForm.addWallCondition(notTopBoundary)
        expectedForm.addInflowCondition(topBoundary,topVelocity)
        
        for timeStepNumber in range(numTimeSteps):
            expectedForm.solve()
            expectedForm.takeTimeStep()
                
        mesh = testForm.solution().mesh()
        energyError = testForm.solution().energyErrorTotal()
        elementCount = mesh.numActiveElements()
        globalDofCount = mesh.numGlobalDofs()
        
        expectedMesh = expectedForm.solution().mesh()
        expectedEnergyError = expectedForm.solution().energyErrorTotal()
        expectedElementCount = expectedMesh.numActiveElements()
        expectedGlobalDofCount = expectedMesh.numGlobalDofs()
        
        self.assertIsNotNone(testForm)
        self.assertAlmostEqual(15, expectedElementCount, elementCount)
        self.assertEqual(2260, expectedGlobalDofCount, globalDofCount)
        self.assertEqual(0.000, expectedEnergyError, energyError)

    """Test nonlinearSolve"""
    def test_nonlinearSolve(self):
        return # does not pass, seg fault
        testForm = steadyNonlinearInit(data["spaceDim"], data["reynolds"], data["meshDimensions"], data["numElements"], data["polyOrder"])
        testForm.addWallCondition(notTopBoundary)
        testForm.addInflowCondition(topBoundary, topVelocity)
        
        meshTopo = MeshFactory.rectilinearMeshTopology(data["meshDimensions"], data["numElements"], data["x0"])
        expectedForm = NavierStokesVGPFormulation(meshTopo, data["reynolds"], data["polyOrder"], data["delta_k"])
        expectedForm.addZeroMeanPressureCondition()
        expectedForm.addWallCondition(notTopBoundary)
        expectedForm.addInflowCondition(topBoundary,topVelocity)
        
        nonlinearSolve(testForm)

        maxSteps = 10
        nonlinearThreshold = 1e-3
        expectedNormOfIncrement = 1
        stepNumber = 0
        while expectedNormOfIncrement > nonlinearThreshold and stepNumber < maxSteps:
            expectedForm.solveAndAccumulate()
            expectedNormOfIncrement = expectedForm.L2NormSolutionIncrement()
            stepNumber += 1

        testMesh = testForm.solution().mesh()
        testEnergyError = testForm.solution().energyErrorTotal()
        testElementCount = testMesh.numActiveElements()
        testGlobalDofCount = testMesh.numGlobalDofs()
        
        expectedMesh = expectedForm.solution().mesh()
        expectedEnergyError = expectedForm.solution().energyErrorTotal()
        expectedElementCount = expectedMesh.numActiveElements()
        expectedGlobalDofCount = expectedMesh.numGlobalDofs()
        
        self.assertIsNotNone(testForm)
        self.assertAlmostEqual(15, expectedElementCount, testElementCount)
        self.assertEqual(2260, expectedGlobalDofCount, testGlobalDofCount)
        self.assertEqual(0.000, expectedEnergyError, testEnergyError)
        Steady
    """Test steadyNonlinearSolve"""
    def test_steadyNonlinearSolve(self):
        return # does not pass, seg fault
        testForm = steadyNonlinearInit(data["spaceDim"], data["reynolds"], data["meshDimensions"], data["numElements"], data["polyOrder"])
        testForm.addWallCondition(notTopBoundary)
        testForm.addInflowCondition(topBoundary, topVelocity)
        
        meshTopo = MeshFactory.rectilinearMeshTopology(data["meshDimensions"], data["numElements"], data["x0"])
        expectedForm = NavierStokesVGPFormulation(meshTopo, data["reynolds"], data["polyOrder"], data["delta_k"])
        expectedForm.addZeroMeanPressureCondition()
        expectedForm.addWallCondition(notTopBoundary)
        expectedForm.addInflowCondition(topBoundary,topVelocity)
        
        nonlinearSolve(testForm)

        maxSteps = 10
        nonlinearThreshold = 1e-3
        expectedNormOfIncrement = 1
        stepNumber = 0
        while expectedNormOfIncrement > nonlinearThreshold and stepNumber < maxSteps:
            expectedForm.solveAndAccumulate()
            expectedNormOfIncrement = expectedForm.L2NormSolutionIncrement()
            stepNumber += 1

        testMesh = testForm.solution().mesh()
        testEnergyError = testForm.solution().energyErrorTotal()
        testElementCount = testMesh.numActiveElements()
        testGlobalDofCount = testMesh.numGlobalDofs()
        
        expectedMesh = expectedForm.solution().mesh()
        expectedEnergyError = expectedForm.solution().energyErrorTotal()
        expectedElementCount = expectedMesh.numActiveElements()
        expectedGlobalDofCount = expectedMesh.numGlobalDofs()
        
        self.assertIsNotNone(testForm)
        self.assertAlmostEqual(15, expectedElementCount, testElementCount)
        self.assertEqual(2260, expectedGlobalDofCount, testGlobalDofCount)
        self.assertEqual(0.000, expectedEnergyError, testEnergyError)

    if __name__ == '__main__':
        unittest.main()
