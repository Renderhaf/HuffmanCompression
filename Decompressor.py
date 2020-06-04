from TreeNode import *
from FileIO import *
from TreeFileTranslator import *
from LoadingBar import LoadingBar as LB

def decompress(filename: str, LoadingBar=True):
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

    if LoadingBar:
        max_value = datalen
        loading = LB()

    for i in range(datalen):
        current_bit = readCompressedIO.getNextBit()

        if current_bit == 0: #left
            current_node = current_node.left
        elif current_bit == 1: #Right
            current_node = current_node.right

        if current_node.value != None:
            writeDecompressedIO.writeByte(current_node.value)
            current_node = tree
    
        precent = (i/max_value) * 100
        loading.update(precent)

    writeDecompressedIO.close()



    
