from basicgraph import *

#####
#
# classic Breadth First Search
#
# See, e.g., http://en.wikipedia.org/wiki/Breadth-first_search
#

def bfs(graph, startNode):
    for n in graph.nodes:
        n.setStatus('unseen')
    startNode.setStatus('seen')
    startNode.setDistance(0)

    #print("Initializing queue with: ", startNode.name)
    queue = Queue()
    queue.enqueue(startNode)
    while queue.size() != 0:
        #print(queue)
        currentNode = queue.dequeue()
        #print("removed {} from queue. Processing neighbors".format(currentNode.name))
        for node in graph.neighborsOf(currentNode):
            if node.getStatus() == 'unseen':
                node.setStatus('seen')
                node.setParent(currentNode)
                node.setDistance(currentNode.getDistance() + 1)
                queue.enqueue(node)
        currentNode.setStatus('processed')

#####

class Queue:
    # We represent an empty queue using an empty list                                                      
    def __init__(self):                                                                                    
        self.q = []                                                                                        
                                                                                                           
    # Return True if there are no items in the queue.  Return False otherwise.                             
    def isEmpty(self):                                                                                     
        return (len(self.q) == 0)                                                                                                 
                                                                                                                                                                                                                     
    # Add an item to the rear of the queue.                                                                
    def enqueue (self, item):                                                                              
        self.q.append(item)                                                                                                  
                                                                                                                                                                                                                     
    # If the queue is not empty, remove and return the queue's front item                                  
    # If the queue is empty, generate an error or print(a message and return None.                         
    def dequeue (self):
        if self.isEmpty():
            raise ValueError("dequeue invoked on empty Queue")
        else:
            result = self.q[0]
            # Note that this is O(n). Okay for use in CS1210 BUT use
            # a better implementation if you will do many dequeues on
            # very big queue! (Python's collections.deque provides a good
            # implementation)
            self.q = self.q[1:]
            return result
                                                                                                           
    # Return the number of items currently in the queue                                                    
    def size(self):                                                                                        
        return(len(self.q))

    def __repr__(self):
        return "queue{front: " + str(self.q)[1:-1] + " :end}" 

def testQueue():
    q = Queue()
    print("Created an empty Queue")
    print("Size is now: {}".format(q.size()))
    print("Enqueue-ing: 3, then 'hi', then 99")
    q.enqueue(3)
    q.enqueue("hi")
    q.enqueue(99)
    print("Size is now: {}".format(q.size()))
    print("Dequeue-ing ...")
    print(q.dequeue())
    print("Size is now: {}".format(q.size()))
    print("Dequeue-ing ...")
    print(q.dequeue())
    print("Size is now: {}".format(q.size()))
    print("Enqueue-ing: [1,2]")
    q.enqueue([1,2])
    print("Size is now: {}".format(q.size()))
    print("Dequeue-ing ...")
    print(q.dequeue())
    print("Size is now: {}".format(q.size()))
    print("Dequeue-ing ...")
    print(q.dequeue())
    print("Size is now: {}".format(q.size()))



