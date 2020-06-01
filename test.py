from TreeFileTranslator import *
from TreeBuilder import *

def test():
  treetranslator = TreeFileTranslator('testfile', WRITE)
  treetranslator.init()
  testingdict = {chr(k):v for (k,v) in treetranslator.pathdict.items()}
  print(testingdict)
  treetranslator.makeDataFile()


if __name__ == "__main__":
  test()