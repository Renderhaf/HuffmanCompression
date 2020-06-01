class TreeNode():
    def __init__(self, value, frequency, left=None, right=None):
        self.value = value
        self.frequency = frequency
        self.left: TreeNode = left
        self.right: TreeNode = right

    def setRight(self, value):
        self.right = right

    def setLeft(self, value):
        self.left = left

    def getValuesString(self)->str:
        if self.value != None:
            return 'Frequency: {}, Value: {} ({})'.format(self.frequency, self.value, chr(self.value))
        else:
            return 'Frequency: {}'.format(self.frequency)

    def __str__(self):
        if self.value != None:
            return '''ValueNode[\n  Value:{}({})\n   Frequency:{}\n  Left:{}\n  Right:{}]\n'''\
                .format(self.value, chr(self.value), self.frequency, self.left.__str__(), self.right.__str__())
        else:
            return '''FrequencyNode[\n  Frequency:{}\n  Left:{}\n  Right:{}]\n'''\
                .format(self.frequency, self.left.__str__(), self.right.__str__())

    def __repr__(self):
        return self.__str__()
