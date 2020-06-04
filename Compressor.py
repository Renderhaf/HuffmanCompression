from TreeNode import * 
from FileIO import *
from TreeFileTranslator import *

def compress(filename:str):
    treetranslator = TreeFileTranslator(filename, WRITE)
    treetranslator.init()
    treetranslator.makeDataFile()
    treetranslator.makeTreeFile()
