from sys       import argv
from config    import getConfig
import bf

class ChunkTypes:
    # TODO implement factoring system to reduce size
    def literal(chunk):
        return '+'*int(chunk)

    def keyword(chunk):
        return chunk

def tokenize(codeString, config):
    chunks = codeString.replace('\n', ' ').split(' ')
    tokens = []

    for chunk in chunks:
        if chunk == '':
            continue

        if chunk.isdigit():
            tokens.append(ChunkTypes.literal(chunk))
            continue

        if chunk in config:
            tokens.append(ChunkTypes.keyword(config[chunk]))
            continue

    return tokens

def reduce(tokens):
    reduced = []
    while len(tokens) != 0:
        token   = tokens.pop(0)
        argsNum = token.count('{arg')

        for i in range(argsNum):
            arg   = tokens.pop(0)
            token = token.replace('{arg'+str(i)+'}', arg)

        reduced.append(token)
    return reduced

if __name__ == '__main__':
    if len(argv) < 2:
        print("No input file specified")
        quit()

    fileName     = argv[1]
    config       = getConfig('.config')
    run          = '--run' in argv

    with open(fileName, 'r') as inFile:
        lines = reduce(tokenize(inFile.read(), config))
        code  = '\n'.join(lines)
        
        if not run:
            print(code)
        else:
            bf.run(code)