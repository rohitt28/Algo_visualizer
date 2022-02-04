from igraph import *
from traversals import DFS

def WCC(g):
    nv = g.vcount()
    added = [False for v in range(nv)]
    components=[]
    plott=[]
    for i in range(nv):
        if not added[i]:
            d = DFS(g,i,mode=ALL)
            components.append(d[0])
            plott.append(d[2])
            for j in d[0]:
                added[j]=True

    return (components,plott)            

