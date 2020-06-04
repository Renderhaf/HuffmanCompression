from TreeNode import *
from FileIO import *
from TreeBuilder import *

DATA_FILE_EXTENSION = "zap"
TREE_FILE_EXTENSION = "zaptree"

VALUE = 0
FREQUENCY = 1
DEAD_LEAF = 2

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
        '''
        Makes a data file (.zap) in this format:
        extension length - 1 byte
        extension - extension length bytes
        reminder size - 1 byte
        data + reminder - datalen bytes
        '''
        assert self.mode == WRITE

        fileReader = FileIO(self.filename)
        newfilename = self.filename.split(".")[0] + "." + DATA_FILE_EXTENSION
        fileWriter = FileIO(newfilename, WRITE)

        dotloc = self.filename.find('.')
        if dotloc == -1:
            extension = ''
            extlen = 0
        else:
            extension = self.filename[dotloc:]
            extlen = len(extension)

        fileWriter.writeByte(extlen)

        for char in extension:
            fileWriter.writeByte(ord(char))

        bitstream = ""
        for byte in range(len(fileReader._contents)):
            bitstream += self.pathdict.get(fileReader.getNextByte())

        rem = 8 - len(bitstream) % 8

        fileWriter.writeByte(rem)
        fileWriter.writeBits(bitstream)

        fileWriter.close()

    def makeTreeFile(self):
        assert self.mode == WRITE
        newfilename = self.filename.split(".")[0] + "." + TREE_FILE_EXTENSION
        self.treeFileIO = FileIO(newfilename, WRITE)

        treeheight = self.__getTreeHeight(self.tree)
        self.__makeTreeFileHelper(self.tree)

        del self.treeFileIO
        print(treeheight)

    def __makeTreeFileHelper(self, node: TreeNode):
        '''
        For every node:
        if the node has a value, it will be written, and the flag bit will be on (eg: 1-10101010)
        if the node does not have a value (frequency node), the flag bit will be off, and the value will be 1 (eg: 0-00000001)
        if the node is empty (a non-existant leaf to make the tree complete), the value will be zero and the flag will be zero (eg: 0-00000000)
        '''
        if node.value != None:
            # Flag bit is on and repr the bit as a byte
            self.treeFileIO.writeBits('1'+'{:08b}'.format(node.value))
        else:
            # Frequency node - flag is 0 and data is 1
            self.treeFileIO.writeBits('0'+'{:08b}'.format(1))

        if node.left != None:
            self.__makeTreeFileHelper(node.left)
        else:
            # Empty leaf - flag is 0 and data is 0
            self.treeFileIO.writeBits('0'+'{:08b}'.format(0))

        if node.right != None:
            self.__makeTreeFileHelper(node.right)
        else:
            # Empty leaf - flag is 0 and data is 0
            self.treeFileIO.writeBits('0'+'{:08b}'.format(0))

    def __getTreeHeight(self, node:TreeNode)-> int:
        leftHeight = self.__getTreeHeight(node.left)+1 if node.left != None else 0
        rightHeight = self.__getTreeHeight(node.right)+1 if node.right != None else 0

        return leftHeight if leftHeight > rightHeight else rightHeight

    def getTreeFromFile(self)->TreeNode:
        assert self.mode == READ

        treefilename = self.filename.split(".")[0] + "." + TREE_FILE_EXTENSION
        self.treeFileIO = FileIO(treefilename)

        tree = self.__treeFromFileHelper()

        del self.treeFileIO

        return tree
    
    def __getNodeFromFile(self)->tuple:
        assert self.mode == READ

        # Get 9 bits from file
        data = ''
        for i in range(9):
            try:
                data += str(self.treeFileIO.getNextBit())
            except IndexError:
                return DEAD_LEAF, 0

        typebit = int(data[0])
        databyte = int(data[1:],2)

        if typebit == 1:
            return VALUE, databyte
        elif databyte == 1:
            return FREQUENCY, databyte
        else:
            return DEAD_LEAF, databyte 

    def __treeFromFileHelper(self)->TreeNode:
        assert self.mode == READ

        t, val = self.__getNodeFromFile()
        if t == FREQUENCY:
            val = None
        elif t == DEAD_LEAF:
            return None

        left = self.__treeFromFileHelper()
        right = self.__treeFromFileHelper()

        tree = TreeNode(val, None, left, right)
        return tree


