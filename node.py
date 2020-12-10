class Node:
    """
    Class Node
    """
    def __init__(self, label, upload, download, inflow, outflow):
        self.label = label
        self.upload = upload
        self.download = download
        self.inflow = inflow
        self.outflow = outflow
        self.inlen = len(inflow)
        self.outlen = len(outflow)
        self.upstr = str(self.upload) + " Kbits/s"
        self.downstr = str(self.download) + " Kbits/s"
        self.desc = "   ::Node " + self.label
    
    def printNode(self):
        """
        Print node info (tpc output and input flow)
        """
        print self.desc
        print "     - Outflow (" + self.upstr + " max):"
        for link in self.outflow:
            print "         " + link.getDesc()
        print "     - Inflow (" + self.downstr + " max):"
        for link in self.inflow:
            print "         " + link.getDesc()
        print
