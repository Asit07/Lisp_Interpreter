#Joe Hudson
#Structure/Math Operators/Query/define/call
#Asit
#While/If/Cons/Car/Cdr/Begin/Set/print

from ast import parse
from asyncore import loop
from curses.ascii import SP, VT, isalnum, isalpha, isdigit
from fcntl import F_SEAL_SEAL
from lib2to3.pgen2 import token
import re
from tkinter.messagebox import NO
import os

from numpy import empty

class var:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class function:
    def __init__(self):
        self.name = None
        self.args = []
        self.expres = []

variableTable = []
functionTable = []

def dropFloat(val):
    if (val % 1) == 0:
        return int(val)
    else:
        return val

def numerizeTokens(list):
    i = 0
    for x in list:
        if x.isnumeric():
            list[i] = float(list[i])
            list[i] = dropFloat(list[i])
        i += 1
    return list


def findArg(args, argName):
    i = 0
    while(argName != args[i]):
        i += 1
    return i

def call(fun, line):
    expr = fun.expres.pop(0)
    i = 0
    for x in fun.args:
        if(len(line) == 0):
            break
        fun.args[i].value = line.pop(0)
        i += 1
    return Expression(fun.expres, expr, fun.args)

def Expression(line, expr, vT = variableTable):
    if type(expr) != int:
        expr = expr.lower()
    if expr == 'if':
        cond = []
        ifT = []
        ifF = []
        i = 0
        if line[i] == '(':
            cond.append(line[i])
            i += 1
            while line[i] != ')':
                cond.append(line[i])
                i += 1
            while(line[i+1] == ')'):
                cond.append(line[i])
                i += 1
            cond.append(line[i])
            i += 1

        if line[i] == '(':
            ifT.append(line[i])
            i += 1
            while line[i] != ')':
                ifT.append(line[i])
                i += 1
            while(line[i+1] == ')'):
                ifT.append(line[i])
                i += 1
            ifT.append(line[i])
            i += 1

        if line[i] == '(':
            ifF.append(line[i])
            i += 1
            while line[i] != ')':
                ifF.append(line[i])
                i += 1
            while((i+1) < len(line) and line[i+1] == ')'):
                ifF.append(line[i])
                i += 1
            ifF.append(line[i])
            i += 1

        if Parse(cond, vT):
            Parse(ifT, vT) 
        else:
            Parse(ifF, vT)

        j=0
        while j < i:
            line.pop(0)
            j += 1
        
        return

    if expr == 'while':
        cond = []
        loop = []

        i = 0
        if line[i] == '(':
            cond.append(line[i])
            i += 1
            while line[i] != ')':
                cond.append(line[i])
                i += 1
            while(line[i+1] == ')'):
                cond.append(line[i])
                i += 1
            cond.append(line[i])
            i += 1
        if line[i] == '(':
            loop = line[i:len(line)]
        
        tempCond = cond[:]
        tempLoop = loop[:]

        while Parse(cond, vT):
            Parse(loop, vT) 
            cond = tempCond[:]
            loop = tempLoop[:]
        return

    if expr == 'set':
        a = line.pop(0)
        b = Parse(line, vT)
        newVar = var(a, b)
        
        i = 0
        for variable in variableTable:
            if variableTable[i].name == newVar.name:
                variableTable[i].value = newVar.value
                return
            i += 1
        variableTable.append(newVar)
        return

    if expr == 'begin':
        Parse(line, vT)
        if(len(line) == 0):
            return
        while line[1] == ')' and len(line) > 2:
            line.pop(0)
        if(line[0] == ')'):
            line.pop(0)

        while line[0] != ')':
            Parse(line, vT)
            if(len(line) == 0):
                return
            while line[1] == ')' and len(line) > 2:
                line.pop(0)
            if(line[0] == ')'):
                line.pop(0)
        return 

    if expr == '+':
        arg1 = float(Parse(line, vT))
        arg2 = float(Parse(line, vT))
        return dropFloat(arg1 + arg2)

    if expr == '-':
        arg1 = float(Parse(line, vT))
        arg2 = float(Parse(line, vT))
        return dropFloat(arg1 - arg2)

    if expr == '*':
        arg1 = float(Parse(line, vT))
        arg2 = float(Parse(line, vT))
        return dropFloat(arg1 * arg2)

    if expr == '/':
        arg1 = float(Parse(line, vT))
        arg2 = float(Parse(line, vT))
        return dropFloat(arg1 / arg2)

    if expr == '=':
        arg1 = Parse(line, vT)
        arg2 = Parse(line, vT)
        
        arg1 = str(arg1)
        arg2 = str(arg2)

        if type(arg1) == list or type(arg2) == list:
            return False
        if arg1 == arg2:
            return True
        else:
            return False

    if expr == '<':
        arg1 = Parse(line, vT)
        arg2 = Parse(line, vT)
        if(arg1 < arg2):
            return True
        else: 
            return False

    if expr == '>':
        arg1 = Parse(line, vT)
        arg2 = Parse(line, vT)
        if(arg1 > arg2):
            return True
        else: 
            return False

    if expr == 'cons':
        consList = []
        arg1 = []
        arg2 = []
        x = ''
        y = ''

        while len(line) != 0:
            x = line[0]
            line.pop(0)

            if(x == ')'):
                break
            if(x == '('):
                x = line[0]
                line.pop(0)
                arg1.append(Parse(line, vT))
            else:
                arg1.append(Expression(line, x, vT))
            if(len(line) != 0 and line[0] == '('):
                break
            if(len(line) != 0):
                x = line[0]
            
        while len(line) != 0:
            y = line[0]
            if(y == ')'):
                break
            line.pop(0)
            if(y == '('):
                y = line[0]
                line.pop(0)
                arg2.append(Parse(line, vT))
            else:
                arg2.append(Expression(line, y, vT))
            if(len(line) != 0):
                y = line[0]
        if not any(arg2):
            return arg1

        if(len(arg1) == 1):
            consList.append(arg1[0])
        if(len(arg1) != 0 and len(arg1) != 1):
            consList.append(arg1)

        if(len(arg2) == 1):
            consList.append(arg2[0])
        if(len(arg2) != 0 and len(arg2) != 1):
            consList.append(arg2)

        return consList

    if expr == 'car':
        consList = []
        arg1 = []
        arg2 = []
        x = ''
        y = ''

        while len(line) != 0:
            x = line[0]
            line.pop(0)

            if(x == ')'):
                break
            if(x == '('):
                x = line[0]
                line.pop(0)
                arg1.append(Parse(line, vT))
            else:
                arg1.append(Expression(line, x, vT))
            if(len(line) != 0 and line[0] == '('):
                break
            if(len(line) != 0):
                x = line[0]

        while len(line) != 0:
            y = line[0]
            line.pop(0)
            if(y == ')'):
                break
            if(y == '('):
                y = line[0]
                line.pop(0)
                arg2.append(Parse(line, vT))
            else:
                arg2.append(Expression(line, y, vT))
            y = line[0]

        if not any(arg2):
            return arg1[0]

        if(len(arg1) == 1):
            consList.append(arg1[0])
        if(len(arg1) != 0 and len(arg1) != 1):
            consList.append(arg1[0])
        if(len(arg2) == 1):
            consList.append(arg2[0])
        if(len(arg2) != 0 and len(arg2) != 1):
            consList.append(arg2[0])

        return consList[0]

    if expr == 'cdr':
        cdrList = []
        arg1 = []
        arg2 = []
        x = ''
        y = ''

        while len(line) != 0:
            x = line[0]
            line.pop(0)

            if(x == ')'):
                break
            if(x == '('):
                x = line[0]
                line.pop(0)
                arg1.append(Parse(line, vT))
            else:
                arg1.append(Expression(line, x, vT))
            if(len(line) and line[0] == '('):
                break
            if(len(line) != 0):
                x = line[0]

        while len(line) != 0:
            y = line[0]
            line.pop(0)
            if(y == ')'):
                break
            if(y == '('):
                y = line[0]
                line.pop(0)
                arg2.append(Parse(line, vT))
            else:
                arg2.append(Expression(line, y, vT))
            y = line[0]

        if not any(arg2):
            arg1.pop(0)
            return arg1[0]

        if(len(arg1) == 1):
            cdrList.append(arg1[0])
        else:
            cdrList.append(arg1)
        if(len(arg2) == 1):
            cdrList.append(arg2[0])
        else:
            cdrList.append(arg2)

        cdrList.pop(0)

        return cdrList[0]

    if expr == 'number?':
        statement = Parse(line, vT)
        expr = statement
        if type(expr) == int or type(expr) == float:
            return True
        return False

    if expr == 'symbol?':
        statement = line[0]
        expr = statement
        i = 0
        while(i != len(vT) and len(vT) != 0):
            if(vT[i].name == expr):
                break
            i += 1
        if(i != len(vT)):
            return True
        else:
            return False

    if expr == 'list?':
        statement = Parse(line, vT)
        expr = statement
        if type(expr) == list:
            return True
        return False

    if expr == 'null?':
        statement = Parse(line, vT)
        expr = statement
        if expr == False:
            return True
        return False

    if expr == 'print':
        statement = Parse(line, vT)
        if(type(statement) == bool and statement == True):
            statement = 'T'
        if(type(statement) == bool and statement == False):
            statement = '()'
        print(statement)
        return 

    if expr == 't':
        return True

    if expr == 'define':
        newFunction = function()
        newFunction.name = Parse(line, vT)
        
        while True:
            line.pop(0)
            if(line[0] == ')'):
                break
            newFunction.args.append(var(line[0], None))
        while True:
            line.pop(0)
            if len(line) == 0:
                break
            newFunction.expres.append(line[0])
        functionTable.append(newFunction)
        return

    if expr == ')':
        return

    i = 0
    while(i != len(functionTable) and len(functionTable) != 0):
        if(functionTable[i].name.lower() == expr):
            break
        i += 1
    if(i != len(functionTable)):
        return call(functionTable[i], line)

    i = 0
    while(i != len(vT) and len(vT) != 0):
        if(vT[i].name == expr):
            break
        i += 1
    if(i != len(vT)):
        return vT[i].value
    return expr

def SplitTokens(line):
    pattern = re.compile('''((?:[^ "']|"[^"]*"|'[^']*')+)''')
    line = line.replace('(', ' ( ')
    line = line.replace(')', ' ) ')
    tokenList = pattern.split(line)[1::2]
    tokenList = numerizeTokens(tokenList)
    if(tokenList[len(tokenList)-1]) == '\n':
        tokenList.pop(len(tokenList)-1)
    return tokenList 

def Parse(line, vT = variableTable):
    for expr in line:
        line.pop(0)
        if expr == 't':
            return Expression(line, expr, vT)
        if expr == '(':
            expr = line.pop(0)
            var = Expression(line, expr, vT)
            return var
        if expr == ')':
            var2 = Parse(line, vT)
            return var2
        i = 0
        while(i != len(vT) and len(vT) != 0):
            if(vT[i].name == expr):
                break
            i += 1
        if(i != len(vT)):
            return vT[i].value
        return expr
    return

entries = os.listdir('lisp_tests/')

for x in entries:
    file = open("lisp_tests/" + x, "r")
    code = file.readlines()
    print("Testing", x, "///////////////////")
    print("")
    for z in code:
        print(z)
    print("")
    print("Answers******************")
    print("")
    for y in code:
        Parse(SplitTokens(y))
    print("")