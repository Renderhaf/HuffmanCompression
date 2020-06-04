import os

READ = "rb"
WRITE = "wb"
APPEND = "a"

class FileIO():
    def __init__(self, filename:str, opentype:str=READ):
        self.filename = filename
        self.type = opentype

        if opentype == READ:
            self._contents:bytes = None
            self.len = self.loadFile()
            self.current_byte_position = 0
            self.current_bits = []
        elif opentype == WRITE:
            self.file = self.loadFile()
            self.current_bits = ""

    def loadFile(self):
        if self.type == READ:
            with open(self.filename, READ) as file:
                self._contents = file.read()

            return len(self._contents)

        elif self.type == WRITE:
            return open(self.filename, WRITE)

    def getNextByte(self)->int:
        assert self.type == READ
        b = self._contents[self.current_byte_position]
        self.current_byte_position += 1
        return b

    @staticmethod
    def _extractBits(byte_number: int):
        nbyte = []
        for i in range(8):
            nbyte.insert(0, byte_number & 1)
            byte_number = byte_number >> 1
        return nbyte

    def getNextBit(self)->int:
        assert self.type == READ
        if len(self.current_bits) == 0:
            self.current_bits = self._extractBits(self.getNextByte())
        
        return self.current_bits.pop(0)

    def reset(self):
        if self.type == READ:
            self.current_byte_position = 0
            self.current_bits = []

    def getLength(self):
        assert self.type == READ
        return len(self._contents)

    def close(self):
        '''
        This function closes the writing proccess
        '''
        #Make sure you dont have some leftoverss
        if self.current_bits != "":
            rem = 8 - len(self.current_bits)
            self.current_bits += "0"*rem
            self.writeByte(int(self.current_bits, 2))


        self.file.close()

    def writeByte(self, byte:int):
        self.file.write(bytes([byte]))

    def writeBits(self, bits:str):
        self.current_bits += bits
        while len(self.current_bits) >= 8:
            curbyte = self.current_bits[:8]
            self.current_bits = self.current_bits[8:]
            self.writeByte(int(curbyte, 2))


if __name__ == "__main__":
    io = FileIO("testfile")
    print(io._contents)
    for j in range(io.getLength()):
        for i in range(8):
            print(io.getNextBit())
        print("\n")

