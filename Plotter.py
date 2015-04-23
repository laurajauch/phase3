from PyCamellia import *
from Plotter  import *
import matplotlib.pyplot as plt
import StringIO
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import sys
import numpy as np



def plot(form, plotType):

    if plotType == "Mesh":
        mesh = form.solution().mesh()
        return plotMesh(mesh)



    elif plotType == "Error":
        mesh = form.solution().mesh();
        error = form.solution().energyErrorPerCell()
        return plotError(error, mesh)


    elif plotType == "Stream Function":
        streamSolution = form.streamSolution()
        streamSolution.solve
        streamFunction = Function.solution(form.streamPhi(), streamSolution)
        return plotFunction(streamFunction, streamSolution.mesh())


    elif plotType == "u1":

        u1_soln = Function.solution(form.u(1),form.solution())
        return plotFunction(u1_soln, form.solution().mesh())

    elif plotType == "u2":
        u2_soln = Function.solution(form.u(2),form.solution())
        return plotFunction(u2_soln, form.solution().mesh())

    elif plotType == "p":
        p_soln = Function.solution(form.p(), form.solution())
        return plotFunction(p_soln, form.solution().mesh())




def plotMesh(mesh):
    num_x = 10
    num_y = 10
    plt.figure(1)
    plt.subplot(111)
    zList = [] # should have tuples (zVals, (x_min,x_max), (y_min,y_max)) -- one for each cell
    activeCellIDs = mesh.getActiveCellIDs()
    xMin = sys.float_info.max
    xMax = sys.float_info.min
    yMin = sys.float_info.max
    yMax = sys.float_info.min
    zMin = sys.float_info.max
    zMax = sys.float_info.min
    for cellID in activeCellIDs:
        vertices = mesh.verticesForCell(cellID)
        xMinLocal = vertices[0][0]
        xMaxLocal = vertices[1][0]
        yMinLocal = vertices[0][1]
        yMaxLocal = vertices[2][1]
        values = []
        for x in range(0,100):
            values.append(0)
        zValues = np.array(values) 
        zValues = zValues.reshape((num_x,num_y)) # 2D array
        zMin = min(zValues.min(),zMin)
        zMax = max(zValues.max(),zMax)
        zList.append((zValues,(xMinLocal,xMaxLocal),(yMinLocal,yMaxLocal)))
        xMin = min(xMinLocal,xMin)
        xMax = max(xMaxLocal,xMax)
        yMin = min(yMinLocal,yMin)
        yMax = max(yMaxLocal,yMax)


    for zTuple in zList:
        zValues,(xMinLocal,xMaxLocal),(yMinLocal,yMaxLocal) = zTuple
        plt.imshow(zValues, cmap='coolwarm', vmin=zMin, vmax=zMax,
                   extent=[xMinLocal, xMaxLocal, yMinLocal, yMaxLocal],
                   interpolation='bicubic', origin='lower')
    plt.title('cavity flow error')
    plt.colorbar()
    plt.axis([xMin, xMax, yMin, yMax])
    return plt.gcf()



def plotError(error, mesh):
    num_x = 10
    num_y = 10
    plt.figure(1)
    plt.subplot(111)
    zList = [] # should have tuples (zVals, (x_min,x_max), (y_min,y_max)) -- one for each cell
    activeCellIDs = mesh.getActiveCellIDs()
    xMin = sys.float_info.max
    xMax = sys.float_info.min
    yMin = sys.float_info.max
    yMax = sys.float_info.min
    zMin = sys.float_info.max
    zMax = sys.float_info.min
    for cellID in activeCellIDs:
        vertices = mesh.verticesForCell(cellID)
        xMinLocal = vertices[0][0]
        xMaxLocal = vertices[1][0]
        yMinLocal = vertices[0][1]
        yMaxLocal = vertices[2][1]
        values = []
        for x in range(0,100):
            values.append(error[cellID])
        zValues = np.array(values) 
        zValues = zValues.reshape((num_x,num_y)) # 2D array
        zMin = min(zValues.min(),zMin)
        zMax = max(zValues.max(),zMax)
        zList.append((zValues,(xMinLocal,xMaxLocal),(yMinLocal,yMaxLocal)))
        xMin = min(xMinLocal,xMin)
        xMax = max(xMaxLocal,xMax)
        yMin = min(yMinLocal,yMin)
        yMax = max(yMaxLocal,yMax)


    for zTuple in zList:
        zValues,(xMinLocal,xMaxLocal),(yMinLocal,yMaxLocal) = zTuple
        plt.imshow(zValues, cmap='coolwarm', vmin=zMin, vmax=zMax,
                   extent=[xMinLocal, xMaxLocal, yMinLocal, yMaxLocal],
                   interpolation='bicubic', origin='lower')
    plt.title('cavity flow error')
    plt.colorbar()
    plt.axis([xMin, xMax, yMin, yMax])
    return plt.gcf()




def plotFunction(f,mesh):
    plt.figure(1)
    plt.subplot(111)
    num_x = 10
    num_y = 10
    refCellVertexPoints = []

    for j in range(num_y):
        y = -1 + 2. * float(j) / float(num_y - 1) # go from -1 to 1
        for i in range(num_x):
            x = -1 + 2. * float(i) / float(num_x - 1) # go from -1 to 1
            refCellVertexPoints.append([x,y])

    zList = [] # should have tuples (zVals, (x_min,x_max), (y_min,y_max)) -- one for each cell
    activeCellIDs = mesh.getActiveCellIDs()
    xMin = sys.float_info.max
    xMax = sys.float_info.min
    yMin = sys.float_info.max
    yMax = sys.float_info.min
    zMin = sys.float_info.max
    zMax = sys.float_info.min
    for cellID in activeCellIDs:
        vertices = mesh.verticesForCell(cellID)
        xMinLocal = vertices[0][0]
        xMaxLocal = vertices[1][0]
        yMinLocal = vertices[0][1]
        yMaxLocal = vertices[2][1]
        (values,points) = f.getCellValues(mesh,cellID,refCellVertexPoints)
        zValues = np.array(values) 
        zValues = zValues.reshape((num_x,num_y)) # 2D array
        zMin = min(zValues.min(),zMin)
        zMax = max(zValues.max(),zMax)
        zList.append((zValues,(xMinLocal,xMaxLocal),(yMinLocal,yMaxLocal)))
        xMin = min(xMinLocal,xMin)
        xMax = max(xMaxLocal,xMax)
        yMin = min(yMinLocal,yMin)
        yMax = max(yMaxLocal,yMax)


    for zTuple in zList:
        zValues,(xMinLocal,xMaxLocal),(yMinLocal,yMaxLocal) = zTuple
        plt.imshow(zValues, cmap='coolwarm', vmin=zMin, vmax=zMax,
                   extent=[xMinLocal, xMaxLocal, yMinLocal, yMaxLocal],
                   interpolation='bicubic', origin='lower')

    plt.title(title)
    plt.colorbar()
    plt.axis([xMin, xMax, yMin, yMax])
    return plt.gcf()

     

    


