import networkx as nx
class Stack():
	"""Summary of class here.

    Attributes:
        size: Stack size.
        top: Stack top number.
        stack: Strorage of elements
    """

	def __init__(self,size = 100):
		self.size = size
		self.top = -1
		self.stack = []
	def pop(self):
		if self.IsNull():
			raise 'Stack is Null'
		else:
			self.top -= 1
			del self.stack[-1]
	def push(self,element):
		if self.top < self.size:			
			self.top += 1
			self.stack.append(element)
		else:
			print 'Wrong'
	def Last(self):
		return self.stack[self.top]
	def Empty(self):
		self.top = -1
		self.stack = []
	def IsNull(self):
		if self.top == -1:
			return True
		else:
			return False
	def IsFull(self):
		if self.top == self.size:
			print 'Overflow of Stack'
			return True
		else:
			return False
	def InStack(self,element):
		if element in self.stack:
			return True
		else:
			return False
	def Reverse_Stack(self):
		if self.IsNull() != True:
			for i in range(self.top + 1):
				print '[element]',self.stack[i]
		else:
			print 'Wrong size'

def Simpath_Spread(S,eta,U,G,b):
	"""Compute the spread of S.

    Inputs:
        S: The Seed Set
        eta: A pruning threshold
        U: The empty set temporarily and will use in optimization
       	G: The Graph
       	b: The influence weight of node, e.p b[u][v] is the influence u on v
    Returns:
        Sigma(S): The expected number of nodes reachable from S

    Raises:
        IOError: An error occurred accessing the S object.
    """
	Sigma = 0	# Initilize the Sigma
	V = G.nodes()	# V is all nodes set
	for u in S:
		temp = list(set(V) - set(S))	# V minus S
		temp.append(u)	# V minus S append u
		Sigma += BackTrack(u,eta,temp,U,G,b)	# Each node in S calls BackTrack
	return Sigma
def BackTrack(u,eta,W,U,G,b):
	"""Enumerates all simple paths starting from u.

    Inputs:
        u: A start node the simple path
        eta: A pruning threshold
        W: A given set of nodes
        U: The empty set temporarily and will use in optimization
        G: The Graph
        b: The influence weight of node, e.p b[u][v] is the influence u on v
    Returns:
        spd: Track the spread of node u in the subgraph induced by W

    Raises:
        IOError: ?2
    """
	Q  = Stack()	# Stack that maintain the current nodes on the path
    # Initilize the Q,spd,pp and D
	Q.push(u)
	spd = 1 	 
 	pp = 1 	# Maintain the weight of the current path
 	# Produce D
 	D = {}	# D[x] maintains the out-neighbors of x
 	for i in G.nodes():
		D[i] = []
 	while Q.IsNull() != True:
 		[Q,D,spd,pp] = Forward(Q,D,spd,pp,eta,W,U,G,b)
 		u = Q.Last()
 		Q.pop()
 		print '^^^^^',D,u,spd,pp
 		if Q.IsNull() != True:	# When the Q is Null,stop the process
 			v = Q.Last()
 			pp = float(pp)/ b[v][u]
 		print b[v][u],pp
 	return spd
def Forward(Q,D,spd,pp,eta,W,U,G,b):
	"""Extends the last element x in a depth-first fashion

    Inputs:
    	Q: Stack that maintain the current nodes on the path
    	D: D[x] maintains the out-neighbors of x
    	spd: Track the spread of node in the subgraph induced by W
    	pp: Maintain the weight of the current path
    	eta: A pruning threshold
    	W: A given set of nodes
    	U: The empty set temporarily and will use in optimization
    	G: The Graph
    	b: The influence weight of node, e.p b[u][v] is the influence u on v
    Returns:
        [Q,D,spd,pp]: The update of Q,D,spd,pp

    Raises:
        IOError: ?2
    """
	x = Q.Last()
	flag = 0
	i = 0
	sss = True
	#print '???',G.number_of_nodes()
	while i < len(G.successors(x)):	# Main loop,limit cond is the path cover all nodes 
		for y in G.successors(x):
			if Q.InStack(y) != True and y not in D[x] and y in W:	# y is not included in Q and Dx 
				if pp * b[x][y] < eta:
					D[x].append(y)
				else:
					Q.push(y)
					pp *= b[x][y]
					spd += pp
					D[x].append(y)	# Add y to x
					x = Q.Last()
					flag = 0
		print 'value',spd,pp
		i += 1
	return Q,D,spd,pp
def Read_Graph(filename):
	"""Read graph from file.

    Inputs:
        filename: A filename
    Returns:
        G: The formed graph
        b: The influence weight of node, e.p b[u][v] is the influence u on v 

    Raises:
        IOError: An error occurred reading the file.
    """
	G = nx.DiGraph()
	G.add_edge('x','y',influence = .3)
	G.add_edge('x','z',influence = .4)
	G.add_edge('y','x',influence = .1)
	G.add_edge('y','z',influence = .2)
	G.add_edge('z','y',influence = .5)
	G.add_edge('x','x',influence = 1.)
	G.add_edge('y','y',influence = 1.)
	G.add_edge('z','z',influence = 1.)
	G.add_edge('a','a',influence = 1.)
	G.add_edge('a','x',influence = .5)
	b = {}
	for i in G.nodes():
		b[i] = {}
	for line in G.edges(data = True):
		b[line[0]][line[1]] = line[2]['influence']	#Initilize the Edge Weight Value
	return G,b
def main():
	[G,b] = Read_Graph('')
	# Initilize the value
	S = ['x']	# Start seed
	eta = 0
	U = []
	print Simpath_Spread(S,eta,U,G,b)

if __name__ == '__main__':
	main()