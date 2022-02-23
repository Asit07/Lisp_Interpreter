from curses.ascii import SP, isalnum, isalpha
import re

def dropFloat(val):
    if (val % 1) == 0:
        return int(val)
    else:
        return val

def Expression(line, expr):
    expr = expr.lower()

    if expr == '+':
        arg1 = float(Parse(line))
        arg2 = float(Parse(line))
        print (arg1, " + ", arg2)
        return dropFloat(arg1 + arg2)
    if expr == '-':
        arg1 = float(Parse(line))
        arg2 = float(Parse(line))
        return dropFloat(arg1 - arg2)
    if expr == '*':
        arg1 = float(Parse(line))
        arg2 = float(Parse(line))
        print(arg1, " * ", arg2)
        return dropFloat(arg1 * arg2)
    if expr == '/':
        arg1 = float(Parse(line))
        arg2 = float(Parse(line))
        return dropFloat(arg1 / arg2)
    if expr == '=':
        return
    if expr == '<':
        return
    if expr == '>':
        return
    if expr == 'cons':
        return
    if expr == 'car':
        return
    if expr == 'cdr':
        return
    if expr == 'number?':
        return
    if expr == 'symbol?':
        return
    if expr == 'list?':
        return 
    if expr == 'null?':
        return
    if expr == 'print':
        print(Parse(line))
        return 
    if expr == 't':
        return
    if expr == 'define':
        return
    if expr == 'call':
        return

def SplitTokens(line):
    pattern = re.compile('''((?:[^ "']|"[^"]*"|'[^']*')+)''')
    line = line.replace('(', ' ( ')
    line = line.replace(')', ' ) ')
    line = line.replace(']', ' ] ')
    line = line.replace('[', ' [ ')
    tokenList = pattern.split(line)[1::2]
    return tokenList 

def Parse(line):
    for expr in line:
        line.pop(0)
        if expr == '(':
            expr = line.pop(0)
            return Expression(line, expr)
        if expr == ')':
            return Parse(line)
        if expr == '[':
            return
        if expr == ']':
            return
        return expr
    return

a = "(print \"hello everyone\")"
b = "(print (- (/ (* (+ 7 4) 3)) 11) 2)"
print(SplitTokens(b))
Parse(SplitTokens(a))
Parse(SplitTokens(b))