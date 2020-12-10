class Link:
    def __init__(self, label, value = 0, lock = False):
        self.label = label
        self.value = value
        self.lock = lock
    
    def printLink(self):
        """
        Print link info (current TCP flow)
        """
        print "- Link " + self.label + ": " + str(self.value) + " Kbits/s"

    def getDesc(self):
        """
        Print link description
        """
        return "- Link " + self.label + ": " + str(self.value) + " Kbits/s"