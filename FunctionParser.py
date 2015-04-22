from PyCamellia import *

class FunctionParser(object):

    def parseFunction(self, input):
        checked = self.cleanUp(input)
        return checked
        #return self.parse(checked)

    def cleanUp(self, input): #not sure if other stuff needs to be done here 
        input = "".join(input.split())
        for i in range(len(input)):
            if(input[i] == ")" and i < len(input)-1):
                if(input[i+1] == "("): # adds a * between parens ex. )( becomes )*(
                    input = input[:i+1]+"*"+input[i+1:]
                #elif (input[i+1] == "^"):
                    #throw some kind of error
            elif(input[i] == "*" and i < len(input)-1 and input[i+1] == "*"):
                input = input[:i]+"^"+input[i+2:]
            elif(self.isNum(input[i]) and i < len(input)-1 and input[i+1].isalpha()):
                input = input[:i+1]+"*"+input[i+1:]
            elif(input[i].isalpha() and i < len(input)-1 and input[i+1].isalpha()):
                input = input[:i+1]+"*"+input[i+1:]

        return input

    def parse(self, input):
        i = 0
        ops = [] #list of operators
        stuff = [] #list of numbers/variables
        while(i < len(input)):
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
                stuff.insert(0, parse(inside))
            elif(i > 0 and input[i] == "-" and self.isOp(i-1)):
                num = "-"
                i+=1
                while(i<len(input) and self.isNum(input[i])):
                    num+=input[i]
                    i+=1
                i = i-1
                stuff.insert(0, num)
            elif(self.isOp(i)):
                ops.insert(0, input[i])
            elif input[i].isalpha():
                stuff.insert(0, input[i])
            elif self.isNum(input[i]):
                toInsert = ""
                while( i< len(input) and (self.isNum(input[i]) or input[i] == ".")):
                    temp+=input[i] #there is no check for two decimals, like 2.0.4 (as in a typo)
                    i+=1
                i = i-1
                stuff.insert(0, input[i])
            i = i+1
        
        if(len(stuff)==1): #no check for empty string
            if self.isNum(comp[0]):
                return Function.constant(float(stuff.pop()))
            else:
                return stuff.pop()

        opComp = {0:["^"], 1:["*","/"], 2:["+","-"]} 
        j = 0
        

        i = 0
        while(i<(len(stuff)-1)):
            if ops[i] == opComp[j][0]:
                if(stuff[i].isalpha):
                    if (stuff[i] == "x"):
                        stuff[i] = Function.xn(stuff[i+1])
                    elif(stuff[i] == "y"):
                        stuff[i] = Function.yn(stuff[i+1])
                elif(self.isNum(stuff[i])):
                    stuff[i] = stuff[i] ** stuff[i]+1
                stuff.pop(i+1)
                ops.pop(i)
                i -=1
            i+=1
        
        j+=1

            
                    


    def isOp(self, toCheck):
        return toCheck == "*" or toCheck == "/" or toCheck == "-" or toCheck == "+" or toCheck == "^"

    def isNum(self, toCheck):
        try:
            int(toCheck)
            return True
        except ValueError:
            return False
            
        
