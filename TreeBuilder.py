from FileIO import *
from TreeNode import *

from typing import List

class TreeBuilder():
    def __init__(self, filename:str):
        self.fileName = filename
        self.fileIO = FileIO(filename, READ)
        self.frequencyQueue:List[TreeNode] = []

    def generateFrequencyQueue(self)->List[TreeNode]:
        '''
        generates a frequency tree
        the stages for that are:
            - Build a dict with all the values and their frequencies
            - Make an unordered list from that
            - Sort it
        '''
        frequencies = dict()
        
        for i in range(self.fileIO.getLength()):
            current_byte = self.fileIO.getNextByte()
            if frequencies.get(current_byte) == None:
                frequencies[current_byte] = 1
            else:
                frequencies[current_byte] += 1

        self.fileIO.reset()
        self.frequencyQueue = [TreeNode(key, frequencies[key]) for key in frequencies.keys()]
        
        self.sortQueue()
        return self.frequencyQueue

    def sortQueue(self):
        self.frequencyQueue = sorted(
            self.frequencyQueue, key=lambda x: x.frequency)
            
    def insertNode(self, node:TreeNode):
        '''
        This inserts a node into the frequency queue
        Could later use a Binary-Search like inserting to improve the O notation from O(n) to O(nlogn)
        '''
        for i in range(len(self.frequencyQueue)-1):
            elem = self.frequencyQueue[i]
            nextelem = self.frequencyQueue[i+1]
            if node.frequency >= elem.frequency and node.frequency <= nextelem.frequency:
                self.frequencyQueue.insert(i, node)
                return
        
        self.frequencyQueue.append(node)
        return


    def generateHuffmanTree(self)->TreeNode:
        self.generateFrequencyQueue()
        
        current_location = 0
        while current_location < len(self.frequencyQueue)-1:
            current_node:TreeNode = self.frequencyQueue.pop(current_location)
            next_node:TreeNode = self.frequencyQueue.pop(current_location)

            newnode = TreeNode(None, current_node.frequency + next_node.frequency, current_node, next_node)
            self.insertNode(newnode)

        return self.frequencyQueue[0]

    def visualizeBFS(self):
        printQueue = []
        printQueue.append(self.frequencyQueue[0])

        while len(printQueue) != 0:
            current_node:TreeNode = printQueue.pop(0)
            print("Current Node: " + current_node.getValuesString())

            if current_node.left != None:
                printQueue.append(current_node.left)
            
            if current_node.right != None:
                printQueue.append(current_node.right)

    def reset(self):
        self.frequencyQueue = []

if __name__ == "__main__":
    treebuilder = TreeBuilder('testfile')
    treebuilder.generateHuffmanTree()
    treebuilder.visualizeBFS()
    
