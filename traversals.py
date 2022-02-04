from igraph import *

def DFS(g, vid, mode=OUT):
        nv = g.vcount()
        added = [False for v in range(nv)]
        stack = []

        # prepare output
        vids = []
        parents = []
        plott=[]
        curr=[]

        # ok start from vid
        stack.append((vid, g.neighbors(vid, mode=mode)))
        vids.append(vid)
        parents.append(vid)
        added[vid] = True

        while stack:
            vid, neighbors = stack[-1]
            curr.append(vid)
            plott.append(("cyan",vid,1))
            if neighbors:
                # Get next neighbor to visit
                neighbor = neighbors.pop(0)
                if not added[neighbor]:
                    # Add hanging subtree neighbor
                    stack.append((neighbor, g.neighbors(neighbor, mode=mode)))
                    vids.append(neighbor)
                    parents.append(vid)
                    added[neighbor] = True
                    plott.append(("grey",vid,0))
                    plott.append(("cyan",neighbor,1))
            else:
                # No neighbor found, end of subtree
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
    plott.append(("cyan",vid))
    while queue:
        vid = queue.pop(0)
        plott.append(("grey",vid))
        neighbors=g.neighbors(vid, mode=mode)
        for neighbor in neighbors:
            if not added[neighbor]:
                queue.append(neighbor)
                added[neighbor]=True
                vids.append(neighbor)
                plott.append(("cyan",neighbor))       
        plott.append(("blue",vid))
    return (vids,plott)
