import unittest
from node import Node
from link import Link
from main import allLocked
from main import splitDownload 
from main import splitUpload
from main import downloadLeftOver

class TestMainMethods(unittest.TestCase):

    def reset(self):
        self.linkAB = Link("A->B")
        self.linkAC = Link("A->C")
        self.linkBC = Link("B->C")
    
        self.nodeA = Node("A", 100, 1000, [], [self.linkAC, self.linkAB])
        self.nodeB = Node("B", 100, 10000, [self.linkAB], [self.linkBC])
        #self.nodeC = Node("C", 1000, 100000, [linkAC, linkBC], [])
        self.nodeC = Node("C", 1000, 150, [self.linkAC, self.linkBC], [])

        self.noNodes = []
        self.noLinks = []    
        self.nodes = [self.nodeA, self.nodeB, self.nodeC]
        self.links = [self.linkAB, self.linkAC, self.linkBC]


    def testAllLocked(self):
        self.reset()
        self.assertTrue(allLocked(self.noLinks))
        self.assertFalse(allLocked(self.links))

    def testSplitDownload(self):
        self.reset()
        self.assertFalse(splitDownload(self.noNodes, False))
        self.assertTrue(splitDownload(self.noNodes, True))
        self.assertEqual(self.linkAB.value, 0)       
        self.assertEqual(self.linkAC.value, 0)       
        self.assertEqual(self.linkBC.value, 0)       
        self.assertTrue(splitDownload(self.nodes, False))
        self.assertEqual(self.linkAB.value, 10000)       
        self.assertEqual(self.linkAC.value, 75)       
        self.assertEqual(self.linkBC.value, 75)       
        self.assertFalse(splitDownload(self.nodes, False))

    def testSplitUpload(self):
        self.reset()
        self.assertFalse(splitUpload(self.noNodes, False))
        self.assertTrue(splitUpload(self.noNodes, True))
        self.assertEqual(self.linkAB.value, 0)       
        self.assertEqual(self.linkAC.value, 0)       
        self.assertEqual(self.linkBC.value, 0)
        self.assertTrue(splitDownload(self.nodes, False))
        self.assertTrue(splitUpload(self.nodes, True))
        self.assertEqual(self.linkAB.value, 50)       
        self.assertEqual(self.linkAC.value, 50)       
        self.assertEqual(self.linkBC.value, 75) 

    def testDownloadLeftOver(self):
        self.testSplitUpload()
        downloadLeftOver(self.noNodes)
        self.assertEqual(self.linkAB.value, 50)       
        self.assertEqual(self.linkAC.value, 50)       
        self.assertEqual(self.linkBC.value, 75)
        downloadLeftOver(self.nodes)
        self.assertEqual(self.nodeA.download, 1000)
        self.assertEqual(self.nodeB.download, 9950)
        self.assertEqual(self.nodeC.download, 100)
        self.assertEqual(self.nodeA.inlen, 0)
        self.assertEqual(self.nodeB.inlen, 0)
        self.assertEqual(self.nodeC.inlen, 1)

    def testCompletion(self):
        self.testDownloadLeftOver()
        splitDownload(self.nodes, False)
        splitUpload(self.nodes, False)
        downloadLeftOver(self.nodes)
        self.assertEqual(self.linkAB.value, 50)       
        self.assertEqual(self.linkAC.value, 50)       
        self.assertEqual(self.linkBC.value, 100)


if __name__ == '__main__':
    unittest.main()