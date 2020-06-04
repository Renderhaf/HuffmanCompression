from Compressor import *
from Decompressor import *

filename = 'testfile.exe'
def test_write():
  compress(filename)
  

def test_read():
  decompress(filename)


if __name__ == "__main__":
  test_write()
  test_read()
