from __future__ import division
from node import Node
from link import Link
import sys

def printNodes(nodes):
    """Print nodes information

    :param nodes: array of nodes to be printed
    """   
    for node in nodes:
        node.printNode()

def printLinks(links):
    """Print links information

    :param links: array of links to be printed
    """
    for link in links:
        print "" + link.getDesc() + ", locked: " + str(link.lock)

def allLocked(links):
    """Verify if all links are locked
    This function verifies if all links are locked and return true or false.
    Lock is a boolean property of Link

    :param links: array of links
    :returns: true of false
    """
    locked = True
    for link in links:
        if not link.lock:
            locked = False
    return locked

def splitDownload(nodes, changed):
    """Split and distribute the download flow among the incoming connections

    :params nodes: array of nodes
    :params changed: boolean to control whether a link was changed
    :returns: true if a link was changed of the actual change value
    """
    for node in nodes:
        if not (node.inlen > 0):
            continue
        d = node.download / node.inlen
        #print node.label + ", in: " + str(d)
        for link in node.inflow:
            if not link.lock:
                changed = changed if link.value == d else True 
                link.value = d
    return changed

def splitUpload(nodes, changed):
    """Split and distribute the upload flow among the outcome connections
    This functions distribute the upload flow but respecting the current
    TCP value of the link, if any. It considers the current value was set
    before by the splitDownload function, hence one can not surpasse this
    threshold. If the current value is lower, the surpassed amount is
    accumulate to be divided by the remaining outcome connections.
    The list of outcome connections is sorted by their values (ascending order)
    so the surpasse amount can be safely divided because the remaining connections.

    :params nodes: array of nodes
    :params changed: boolean to control whether a link was changed
    :returns: true if a link was changed of the actual change value
    """
    for node in nodes:
        node.outflow.sort(key=lambda x: x.value, reverse=False)
        if (not node.outlen > 0):
            continue
        u = node.upload / node.outlen
        i = 0
        over = 0 
        for link in node.outflow:
            if not link.lock:
                if link.value < u:
                    over = over + (u - link.value)
                else:
                    newu = u + over/(node.outlen - i + 1)
                    changed = changed if link.value == newu else True 
                    link.value = newu
                    link.lock = True
            i = i + 1
    return changed

def downloadLeftOver(nodes):
    """Calculates the remaining download bandwith of the nodes
    This remaining donwload bandwith can be used in the next round.

    :params nodes: array of nodes
    """

    for node in nodes:
        for link in node.inflow:
            if link.lock:
                node.download = max(0, node.download - link.value)
                node.inlen = node.inlen - 1


def main():
    """Main function
    This function finds the distribution of TCP flows among the node links of a network
    based on their upload and donwload capabilities.
    It performs this by executing one or more rounds. Each round has 3 steps:
    1. Distributed the donwload bandwith among the inflow
    2. Distributed the upload bandwith among the outflow taking the value set by step1 as maximum
    3. Calculate the download leftover for the nodes to use in the next round 
    """

    if(len(sys.argv) != 2):
        print "Wrong number of arguments"
        print "Usage: 'python main.py <file>' where file is the network description"
        quit()

    with open(sys.argv[1]) as f:
        content = f.readlines()

    content = [x.strip() for x in content] 

    linksmap = {}
    nodesmap = {}

    for i in range(0, len(content)):
        if not content[i].startswith('#'):
            if content[i].startswith('link'):
                lab = content[i].split(" ")[1]
                linksmap[lab] = Link(lab)
            elif content[i].startswith('node'):
                n,lab,up,dw,ifw,ofw = content[i].split(" ")
                ifw = ifw.replace("[", "").replace("]", "").split(",")
                ofw = ofw.replace("[", "").replace("]", "").split(",")
                inflow = []
                outflow = []
                for lk in ifw:
                    if(lk != ""):
                        inflow.append(linksmap[lk])
                for lk in ofw:
                    if(lk != ""):
                        outflow.append(linksmap[lk])
                nodesmap[lab] = Node(lab, int(up), int(dw), inflow, outflow)
            elif content[i] != "":
                print "Input parse error at line " + str(i) + ": " + content[i]
                quit()
    nodes = nodesmap.values()
    links = linksmap.values()

    # Start the algoritm to find the TCP flux equilibrium...

    changed = True

    while changed:
        changed = False
        # First step: distributed the donwload bandwith among the inflow
        changed = splitDownload(nodes, changed)
        # Second step: distributed the upload bandwith among the outflow taking the value set by step1 as maximum
        changed = splitUpload(nodes, changed)
        # Third step: calculate the download leftover for the nodes to use in the next round 
        downloadLeftOver(nodes)
        print "Actual state:"
        printNodes(nodes)

    print "TCP Max Flow (final state):"
    printLinks(links)

if __name__ == "__main__":
    main()
