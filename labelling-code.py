#
# Functions used in order to find gadgets proving NP-completeness of some L(a,b)-k-edge labeling problems.
#
# Common parameters:
# E: list of 2-tuples, representing the edges.
# a,b,k: we will consider L(a,b)-k-edge coloring (so the labels will be 0,1,...,k-1 )
# removeSymmetry (True by default): If this parameter value is True, the symmetric coloring are not considered.
#    The symmetric cases are removed by choosing one of the edge with the less possible labeling and only considering 
#     the labeling where this edge is labeled with a label in [0,(k-1)/2].
#    The symmetric cases are always considered if the dictCol parameter is non-empty.
# dictCol (optional): dictionary indexed by edges of int list, representing the allowed labels of this edge.
#      The symmetric cases are always considered if this parameter is non-empty.



# L(E, a, b, k, dictCol={}): 
# Return a list of int list, the list of possible L(a,b)-k-edge labeling of the graph with edges E.
# The order of the edge labels is the same than the order of the edges in E.

# possibilities(E, a, b, k, removeSymmetry=True, dictCol={}): 
# Return a list of int list, each element of this result represent the possible label of one edge.
# The order of the label lists is the same than the order of the edges in E.


# plotPoss(E, a, b, k, dictCol={}):
# Show the graph, with each edge labeled with their possible labeling.

# rangeBranch(E, a, b, k, e, interest):
# Indicate what labels a specified edge can have depending of the label of an other specified edge.
# e: an edge, the edge that we want to force the labeling.
# interest: an edge, the edge we want to know the possible labeling.
# Return a map of list indexed by int: the index is the label of the edge e, the list is the possible values of te edge interest.

from igraph import *

# Compute the list of possible coloring.
def L(E, a, b, k, dictCol={}):
    G=EToGEdge(E)
    V = len(G)
    G2 = square(G)
    c = [-1] * len(G)
    return tryColor(G, G2, a, b, k, c, 0, 0, dictCol)

def possibilities(E, a, b, k, removeSymmetry=True, dictCol={}):
    newDictCol = {}
    for e in dictCol:
        newDictCol[E.index(e)] = dictCol[e]
    
    
    p = L(E, a, b, k, newDictCol)
    res = [set([]) for _ in range(len(E))]
    for s in p:
        for i in range(len(E)):
            res[i].add(s[i])
    if removeSymmetry and len(newDictCol) == 0: # We don't remove symmetry if a subset of color is specified for at least one edge.
        iMin = -1
        vmin = k + 1
        for i in range(len(res)):
            if len(res[i]) > 1 and len(res[i]) < vmin:
                iMin = i
                vmin = len(res[i])
        res2 = [set([]) for _ in range(len(E))]
        for s in p:
            if s[iMin] <= (k - 1) // 2:
                for i in range(len(E)):
                    res2[i].add(s[i])
        
        return res2
    
    return res

def plotPoss(E, a, b, k, dictCol={}):
    poss = [str(x) for x in possibilities(E, a, b, k, dictCol=dictCol)]
    g = Graph(edge_attrs={"label": poss}, edges=E, directed=False)
    plot(g, margin=[150, 100, 100, 100]).show()


def rangeBranch(E, a, b, k, e, interest):
    sol = {}
    G = EToGEdge(E)
    h = E.index(interest)
    for i in range(k):
        p = possibilities(E, a, b, k, dictCol={e:[i]})
        if len(p[h]) > 0:
            sol[i]=p[h]
    return sol


# Graph utilitaries


# Convert a list of edges into an adjacency list representation of the line-graph.
def EToGEdge(E): 
    res = [[] for _ in range(len(E))]
    for i in range(len(E)):
        for j in range(i + 1, len(E)):
            a, b = E[i]
            c, d = E[j]
            if a == c or a == d or b == c or b == d:
                res[i].append(j)
                res[j].append(i)
    return res

# Compute the square of the graph.
def square(G):
    r = []
    for l in range(len(G)):
        adj = G[l]
        squareadj = []
        for i in adj:
            for j in G[i]:
                if j not in squareadj and j not in adj and j != l:
                    squareadj.append(j)
        r.append(squareadj)
    return r



# Check that the color of the edge i is k away from all the neighbour colors in G.
def checkColor(G, c, k, i): 
    for j in G[i]:
        if c[i] >= 0 and c[j] >= 0 and abs(c[i]-c[j]) < k:
            return False
    return True



# The recursive function that will do a backtracking in order to find all possible coloring.
def tryColor(G, G2, a, b, k, c, i, q, dictCol):
    if i == len(G):
        return [c]

    r = []
    c[i] = q
    
    if i not in dictCol.keys() or q in dictCol[i]:
        if checkColor(G, c, a, i) and checkColor(G2, c, b, i):
            copy = c.copy()
            r = tryColor(G, G2, a, b, k, copy, i + 1, 0, dictCol)

    if q < k - 1:
        return r + tryColor(G, G2, a, b, k, c, i, q + 1, dictCol)
    
    return r




# EXAMPLES
# To illustrate how thoses functions can be used, we will consider the L(0,1)-2-Edge labeling of the extended 4-star.


# The extended four star: the first four vertices are the inner vertices, the four last the leaves.
extended_four_star=[(0,1),(0,2),(0,3),(0,4),(1,5),(2,6),(3,7),(4,8)]

#print(L(extended_four_star, 0, 1, 2))
# RETURN: [[0, 0, 0, 0, 1, 1, 1, 1], [1, 1, 1, 1, 0, 0, 0, 0]]
# There is only two possible L(0,1)-2-edge labeling of the extended 4-star: 
# all the inner edge labeled 1 or all labeled 0, and the leaves have the other label.

#print(possibilities(extended_four_star, 0, 1, 2))
# RETURN: [{0}, {0}, {0}, {0}, {1}, {1}, {1}, {1}]
# The possible labels of each edge, not considering symmetric cases.

#print(possibilities(extended_four_star, 0, 1, 2, removeSymmetry=False))
# RETURN: [{0, 1}, {0, 1}, {0, 1}, {0, 1}, {0, 1}, {0, 1}, {0, 1}, {0, 1}]
# Same thing, but considering the symmetric cases.

plotPoss(extended_four_star, 0, 1, 2)
# Same thing but with a graphical representation of the result (symmetrics cases removed).

#plotPoss(extended_four_star, 0, 1, 2,  {(0,1):[1]})
# Same thing, but this time we only consider the coloring with the edge (0,1) labeled 1. 
# The symmetric cases are not removed as a labeling subset is specified for an edge.

#print(rangeBranch(extended_four_star, 0, 1, 2, (3,7), (4,8)))
# RETURN {0: {0}, 1: {1}}
# Depending of the labeling of the edge (3,7), we can see the possible label of the edge (4,8): 
# as thoses two edges are leaves, thoses two edges must have the same label.
    