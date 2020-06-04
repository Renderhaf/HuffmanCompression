from TreeNode import *
from FileIO import *
from TreeFileTranslator import *

def decompress(filename: str):
    filename = filename.split('.')[0]

    treetranslator = TreeFileTranslator(filename,READ)
    tree = treetranslator.getTreeFromFile()
    
    readCompressedIO = FileIO(filename + '.' + DATA_FILE_EXTENSION, READ)

    extlen = readCompressedIO.getNextByte()
    extension = ''
    for i in range(extlen):
        extension += chr(readCompressedIO.getNextByte())

    writeDecompressedIO = FileIO(filename+extension, WRITE)

    rem = readCompressedIO.getNextByte()

    current_node = tree

    #Datalen consists of the actual bit length of the file, minus the reminder, the size of remlen, and the extension
    datalen = len(readCompressedIO._contents)*8 - (rem + 8) - (8 + extlen*8)

    for i in range(datalen):
        current_bit = readCompressedIO.getNextBit()

        if current_bit == 0: #left
            current_node = current_node.left
        elif current_bit == 1: #Right
            current_node = current_node.right

        if current_node.value != None:
            writeDecompressedIO.writeByte(current_node.value)
            current_node = tree
    
    writeDecompressedIO.close()



    
