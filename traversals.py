from igraph import *
from sortedcontainers import SortedSet
import copy

def DFS(g, vid, mode=OUT):
        nv = g.vcount()
        added = [False for v in range(nv)]
        stack = []
        vids = []
        parents = []
        plott=[]
        curr=[]

        stack.append((vid, g.neighbors(vid, mode=mode)))
        vids.append(vid)
        parents.append(vid)
        added[vid] = True

        while stack:
            vid, neighbors = stack[-1]
            curr.append(vid)
            plott.append(("cyan",vid,1))
            if neighbors:
                neighbor = neighbors.pop(0)
                if not added[neighbor]:
                    stack.append((neighbor, g.neighbors(neighbor, mode=mode)))
                    vids.append(neighbor)
                    parents.append(vid)
                    added[neighbor] = True
                    plott.append(("grey",vid,0))
                    plott.append(("cyan",neighbor,1))
            else:
                stack.pop()
                plott.append(("blue",vid,0))

        return (vids, parents, plott)

def BFS(g, vid, mode=OUT):

    queue=[]
    nv = g.vcount()
    added = [False for v in range(nv)]
    vids = []
    added[vid]=True
    queue.append(vid)
    vids.append(vid)
    plott=[]
    while queue:
        vid = queue.pop(0)
        plott.append(("cyan",vid))
        neighbors=g.neighbors(vid, mode=mode)
        for neighbor in neighbors:
            if not added[neighbor]:
                queue.append(neighbor)
                added[neighbor]=True
                vids.append(neighbor)
                plott.append(("grey",neighbor))       
        plott.append(("blue",vid))
    return (vids,plott)

def dijkstra_sp(g, vid,dists, d):
    
    plott=[]
    plott.append([0,copy.deepcopy(dists)])

    vids=SortedSet()
    vids.add((0,vid))
    dists[vid]=0

    while vids:
        vid = vids.pop(0)[1]
        plott.append([1,"cyan",vid])
        neighbors=g.neighbors(vid, mode=OUT)
        for neighbor in neighbors:
            if dists[neighbor]>dists[vid]+d[vid][neighbor]:
                vids.discard((dists[neighbor],neighbor))
                dists[neighbor]=dists[vid]+d[vid][neighbor]
                vids.add((dists[neighbor],neighbor))
                plott.append([2,"grey",neighbor,dists[vid]+d[vid][neighbor]])
        plott.append([-1,vid])
    return (dists,plott)
