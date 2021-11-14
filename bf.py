from os import close
from sys import argv

def printCell(cell, pointer):
    print(chr(cell), end='')
    return (cell, pointer)

def getCell(cell, pointer):
    return (ord(input()[0]), pointer)

COMMANDS = {
    '+' : lambda cell, pointer: (cell + 1, pointer),
    '-' : lambda cell, pointer: (cell - 1, pointer),
    '>' : lambda cell, pointer: (cell, pointer + 1),
    '<' : lambda cell, pointer: (cell, pointer - 1),
    '.' : lambda cell, pointer: printCell(cell, pointer),
    ',' : lambda cell, pointer: getCell(cell, pointer)
}

def dumpState(memory, pointer):
    print("memory  : {mem}".format(mem=memory))
    print("pointer : {pointer}".format(pointer=pointer))

def exec(code: str, memory: list=None, debug=False):
    memory  = [0]*32
    pointer = 0

    tokens   = list(code)
    i        = 0

    while i < len(tokens) and i >= 0:
        if tokens[i] == '[' and memory[pointer] == 0:
            closesUntilMatch = 1
            while closesUntilMatch != 0:
                i += 1

                if   tokens[i] == ']': closesUntilMatch -= 1
                elif tokens[i] == '[': closesUntilMatch += 1

        if tokens[i] == ']' and memory[pointer] != 0:
            opensUntilMatch = 1

            while opensUntilMatch != 0:
                i -= 1
                
                if   tokens[i] == '[': opensUntilMatch -= 1
                elif tokens[i] == ']': opensUntilMatch += 1

        if tokens[i] in COMMANDS:
            (memory[pointer], pointer) = COMMANDS[tokens[i]](memory[pointer], pointer)
        
        if debug:
            print('op      : {op}'.format(op=tokens[i]))
            print("char    : {i}".format(i=i))
            dumpState(memory, pointer)
            input()
            print('===')
            print('\033c')
        
        i += 1

    return (memory, pointer)

def run(code=None):
    if code is None:
        if len(argv) < 2:
            print("No input file specified")
            quit()

        fileName     = argv[1]
        with open(fileName, 'r') as file:
            code = file.read()

    debugMode    = '--debug' in argv 
    dumpAtEnd    = '--dump'  in argv
    currentState = exec(code, debug=debugMode)

    if dumpAtEnd:
        dumpState(currentState[0], currentState[1])

if __name__ == '__main__':
    run()