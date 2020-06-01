from TreeNode import *
from FileIO import *
from TreeBuilder import *

FILE_EXTENSION = "zap"

class TreeFileTranslator():
    def __init__(self, filename, mode):
        '''
        WRITE - generate a compressed bytestream and write it
        READ - read from a compressed stream and decompress it
        '''
        self.filename:str = filename
        self.mode = mode

    def init(self):
        if self.mode == WRITE:
            #Get tree for compressing
            treebuilder = TreeBuilder(self.filename)
            self.tree = treebuilder.generateHuffmanTree()
            self.pathdict = dict()
            #Populates the pathdict
            self.generatePathsDict(self.tree)

    def generatePathsDict(self, current_node:TreeNode, current_path=''):
        if current_node.value != None:
            self.pathdict[current_node.value] = current_path

        if current_node.left != None:
            self.generatePathsDict(current_node.left, current_path+"0")

        if current_node.right != None:
            self.generatePathsDict(current_node.right, current_path+"1")
        
    def makeDataFile(self):
        fileReader = FileIO(self.filename)
        newfilename = self.filename.split(".")[0] + "." + FILE_EXTENSION
        fileWriter = FileIO(newfilename, WRITE)

        bitstream = ""
        for byte in range(len(fileReader._contents)):
            bitstream += self.pathdict.get(fileReader.getNextByte())

        rem = 8 - len(bitstream) % 8

        fileWriter.writeByte(rem)
        fileWriter.writeBits(bitstream)

        fileWriter.close()
        


