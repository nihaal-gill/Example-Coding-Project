# Class to represent nodes (vertices) of a graph
#
class Node(object):
    # name must be a string
    def __init__(self, name):
        self.name = name
        self.status = 'unseen'
        self.parent = None
        self.distance = None
        
    def getName(self):
        return self.name

    def getStatus(self):
        return self.status

    # should be one of 'unseen', 'seen', 'processed'
    def setStatus(self, status):
        self.status = status

    def setDistance(self, distance):
        self.distance = distance
        
    def getDistance(self):
        return self.distance

    def setParent(self, parentNode):
        self.parent = parentNode

    def getParent(self):
        return self.parent
        
    def __repr__(self):
        return "<{}>".format(self.name)


# Class for representing undirected graphs, i.e. graphs in which edges
# have no direction - if there is an edge between a and b,
# you can "move" from a to b and/or from b to a
#
class Graph():
    
    #nodes is a list of the nodes in the graph
    #
    # adjacencyLists is a dictionary with the set of nodes as the set of keys.  For each node, n1,
    # adjacencyLists[n1] is a list of the nodes n2 such that (n1,n2) is an edge.
    # i.e. it is a list of all nodes to which n1 is connected directly by an edge.
    #
    def __init__(self):
        self.nodes = []
        self.adjacencyLists = {}
        
    def addNode(self, node):
        if node in self.nodes:
            raise ValueError("node is already in graph. You can't add it again.")
        else:
            self.nodes.append(node)
            self.adjacencyLists[node] = []

    # To add an edge between node1 and node2, node1 and node2 must already be in the graph
    def addEdge(self, node1, node2):
        if node1 == node2:
            raise ValueError("edges to self are not allowed in undirected graphs")
        if not((node1 in self.nodes) and (node2 in self.nodes)):
            raise ValueError("at least one node of given edge is not in the graph")
        if node2 in self.adjacencyLists[node1]:
            raise ValueError("edge is already in graph. You can't add it again.")

        self.adjacencyLists[node1].append(node2)
        self.adjacencyLists[node2].append(node1)
        
    def neighborsOf(self, node):
        return self.adjacencyLists[node]

    def getNode(self, name):
        for node in self.nodes:
            if node.getName() == name:
                return node
        return None
    
    def hasNode(self, node):
        return node in self.nodes

    def hasEdge(self, node1, node2):
        return node2 in self.adjacencyLists[node1]
    
    def __repr__(self):
        result = "[Graph with:\n Nodes:"
        edgesString = "\n Edges: "
        for node in self.nodes:
            result = result + " " + str(node)
            for node2 in self.neighborsOf(node):
                if node.getName() < node2.getName():
                    edgesString += ' {}-{},'.format(node.getName(), node2.getName())
        result = result + edgesString[:-1]
        return result
                                   
def genGraph():
    n1 = Node("NYC")
    n2 = Node("Miami")
    g = Graph()
    print(g)
    g.addNode(n1)
    g.addNode(n2)
    print(g)
    g.addEdge(n1, n2)
    print(g)
    return g

def genCompleteGraph(n):
    nodes = []
    g = Graph()
    for i in range(n):
        g.addNode(Node(str(i)))

    nodes = g.nodes
    for n1 in nodes:
        for n2 in nodes:
            if (n1 != n2) and (not g.hasEdge(n1, n2)):
                g.addEdge(n1,n2)
    return g

import random
# return a new list with the same elements as input L but randomly rearranged
def mixup(L):
    newL = L[:]
    length = len(L)
    for i in range(length):
        newIndex = random.randint(i,length-1)
        newL[newIndex], newL[i] = newL[i], newL[newIndex]
    return(newL)

def genRandomGraph(numNodes, numEdges):
   
    g = Graph()
    
    for i in range(numNodes):
        g.addNode(Node(str(i)))

    allPairs = []
    for i in range(numNodes):
        for j in range(i+1, numNodes):
                allPairs.append((str(i),str(j)))
                    
    allPairs = mixup(allPairs)
    
    edgesAdded = 0
    while edgesAdded < min(numEdges, len(allPairs)):
        g.addEdge(g.getNode(allPairs[edgesAdded][0]), g.getNode(allPairs[edgesAdded][1]))
        edgesAdded = edgesAdded + 1

    return g

# graph used for bfs demo in class 
#
def genDemoGraph():
    nodes = [Node("A"), Node("B"), Node("C"), Node("D"), Node("E"), Node("F"), Node("G"), Node("H")]
    # used to save typing :)
    edgeIndexTuples = [(0,1), # A-B
             (0,2), # A-C
             (0,4), # A-E
             (0,7), # A-H
             (1,2), # B-C
             (1,3), # B-D
             (1,5), # B-F
             (2,5), # C-F
             (4,6), # E-G
             (6,7) # G-H
             ]
    g = Graph()
    for n in nodes:
        g.addNode(n)
    for e in edgeIndexTuples:
        g.addEdge(nodes[e[0]], nodes[e[1]])
    return g

            












