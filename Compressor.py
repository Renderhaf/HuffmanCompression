from TreeNode import * 
from FileIO import *
from TreeFileTranslator import *

def compress(filename:str):
    treetranslator = TreeFileTranslator(filename, WRITE)
    treetranslator.init()
    treetranslator.isLoadingBar = True
    print("Writing to data file...")
    treetranslator.makeDataFile()
    print("Closed Data File")
    print("Writing to Tree File...")
    treetranslator.makeTreeFile()
    print("Closed Tree file!")
