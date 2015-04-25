from PyCamellia import *

#class FunctionParser():

def parseFunction(input):
    checked = cleanUp(input)
    return parse(checked)

def cleanUp(input): #not sure if other stuff needs to be done here 
    input = "".join(input.split())
    for i in range(len(input)):
        if(input[i] == ")" and i < len(input)-1):
            if(input[i+1] == "("): # adds a * between parens ex. )( becomes )*(
                input = input[:i+1]+"*"+input[i+1:]
            elif(i+1 < len(input)):
                if(not isOp(input[i+1])):
                    input = input[:i+1]+"*"+input[i+1:]
       # elif(input[i] == "*" and i < len(input)-1 and input[i+1] == "*"):
       #    input = input[:i]+"^"+input[i+2:]
        elif(isNum(input[i]) and i < len(input)-1 and input[i+1].isalpha()):
            input = input[:i+1]+"*"+input[i+1:]
        elif(input[i].isalpha() and i < len(input)-1 and input[i+1].isalpha()):
                input = input[:i+1]+"*"+input[i+1:]
        elif(input[i] == "(" and i > 0):
            if(not isOp(input[i-1])):
                input = input[:i]+"*"+input[i:]
        elif(input[i] == "."):
            if(i==0):
                input = "0"+input[i:]
            elif(not isNum(input[i-1])):
                input = input[:i] +"0"+input[i:]
            elif(i<len(input)-1 and not isNum(input[i+1])):
                input = input[:i+1] +"0"+input[i+1:]


    return input

def parse(input):
    i = 0
    ops = [] #list of operators
    terms = [] #list of numbers/variables
    while(i < len(input)):
        if(i == 0 and input[i] == "-"):
            toInsert = "-"
            i+=1
            while i< len(input) and isNum(input[i]):
                toInsert+=input[i]
                i+=1

            terms.append(float(toInsert))
            if not i<len(input):
                break

        if(input[i] == "("): #if parens, parse the paren recursively.
            inside = ""
            findLast = ["("]
            i+=1
            j = i
            while(len(findLast)>0 and j<len(input)):
                if(input[j]==")"):
                    findLast.pop()
                elif(input[j] == "("):
                    findLast.append("(")
                j+=1

            while(i<j):
                inside+=input[i]
                i+=1
            i = i-1
            terms.append(parse(inside))
        elif(i > 0 and input[i] == "-" and isOp(input[i-1])):
            num = "-"
            i+=1
            while(i<len(input) and isNum(input[i])):
                num+=input[i]
                i+=1
            terms.append(float(num))
        elif(isOp(input[i])):
            ops.append(input[i])
        elif input[i].isalpha():
            terms.append(input[i])
        elif isNum(input[i]):
            toInsert = ""
            while( i< len(input) and (isNum(input[i]) or input[i] == ".")):
                toInsert+=input[i] #there is no check for two decimals, like 2.0.4 (as in a typo)
                i+=1
            i = i-1
            terms.append(float(toInsert))
        i = i+1
        
    if(len(terms)==1): #no check for empty string
        if isNum(terms[0]):
            return Function.constant(float(terms.pop()))
        else:
            return terms.pop()

    opComp = {0:["^"], 1:["*","/"], 2:["+","-"]} 
    j = 0
    """
    for i in range(len(terms)):
        print terms[i]
    """
    i = 0
    while(i<(len(terms)-1)):
        if ops[i] == opComp[j][0]:
            if(isinstance(terms[i],str)):
                if (terms[i] == "x"):
                    terms[i] = Function.xn(int(terms[i+1]))
                elif(terms[i] == "y"):
                    terms[i] = Function.yn(int(terms[i+1]))
            elif(isNum(terms[i])):
                terms[i] = terms[i] ** terms[i+1]
            terms.pop(i+1)
            ops.pop(i)
            i -=1
        else:
            if(isinstance(terms[i],str)):
                if (terms[i] == "x"):
                    terms[i] = Function.xn(1)
                elif(terms[i] == "y"):
                    terms[i] = Function.yn(1)
        i+=1

    if(isinstance(terms[i],str)): #this is for the last entry in terms
                if (terms[i] == "x"):
                    terms[i] = Function.xn(1)
                elif(terms[i] == "y"):
                    terms[i] = Function.yn(1)
        
    j+=1
    i = 0
    while(i< (len(terms)-1)):
        if ops[i] == opComp[j][0]:
            terms [i] = terms[i] * terms[i+1]
            terms.pop(i+1)
            ops.pop(i)
            i-=1
        elif ops[i] == opComp[j][1]:
            terms[i] = terms[i] / terms[i+1]
            terms.pop(i+1)
            ops.pop(i)
            i-=1
        i = i + 1
            
    j+=1
    toReturn = terms[0]
    i = 0
    while(i< (len(terms)-1)):
        if ops[i] == opComp[j][0]:
            toReturn += terms[i+1]
        elif ops[i] == opComp[j][1]:
            toReturn -= terms[i+1]
        i+=1
                
    if isNum(toReturn):
        return Function.constant(toReturn)
    else:
        return toReturn
                 


def isOp(toCheck):
    return toCheck == "*" or toCheck == "/" or toCheck == "-" or toCheck == "+" or toCheck == "^"

def isNum(toCheck):
    try:
        int(toCheck)
        return True
    except:
        return False
            
        
