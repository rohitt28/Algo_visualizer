from flask import Flask, render_template, request
from igraph import *
from traversals import*
from graphs import*
from PIL import Image
from flask_socketio import SocketIO
from collections import defaultdict
from sortedcontainers import SortedSet
import io, os, json, random, base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app,transports= ['websocket'])
socketio.init_app(app, cors_allowed_origins="*")
def plotgraph(g, visual_style, res, session_id, event, text=None):
    plot(g, **visual_style, target='static/img/myfile.png')
    im = Image.open("static/img/myfile.png")
    data = io.BytesIO()
    im.save(data, "PNG")
    img_data = data.getvalue()
    res=json.dumps(res)
    socketio.emit(event, {'image_data': img_data, 'result':res ,'text':text}
                ,room=session_id)

def initplot(g, session_id, event, weights=None):
    nv = g.vcount()
    g.vs["name"] = [vi for vi in range(nv)]
    g.vs["color"]="white"
    layout = g.layout("kk")
    visual_style = {}
    visual_style["vertex_size"] = 36
    visual_style["vertex_label"] = g.vs["name"]
    if weights:
        visual_style["edge_label"]=weights
    visual_style["layout"] = layout
    visual_style["bbox"] = (380, 380)
    visual_style["margin"] = 20
    plot(g, **visual_style, target='static/img/myfile.png')
    im = Image.open("static/img/myfile.png")
    data = io.BytesIO()
    im.save(data, "PNG")
    img_data = data.getvalue()
    allvs=[]
    for v in g.vs:
        allvs.append(v['name'])
    allvs=json.dumps(allvs)
    socketio.emit(event, {'image_data': img_data, 'allvs':allvs}, 
        room=session_id)
    return visual_style

def allplots(weighted):
    fdata=[]
    for i in allgraphs:
        g = Graph(i[0], directed= True, edge_attrs=dict(weight=i[1]))
        visual_style = {}
        layout = g.layout("kk")
        visual_style["layout"] = layout
        visual_style["bbox"] = (380, 380)
        visual_style["margin"] = 20
        visual_style["vertex_size"] = 38
        nv = g.vcount()
        g.vs["name"] = [vi for vi in range(nv)]
        g.vs["color"]="white"
        visual_style["vertex_label"] = g.vs["name"]
        if weighted:
            visual_style["edge_label"]=i[1]
        plot(g, **visual_style, target='static/img/myfile1.png')
        im = Image.open("static/img/myfile1.png")
        data = io.BytesIO()
        im.save(data, "PNG")
        img_data = data.getvalue()
        i_data = base64.b64encode(img_data).decode()
        fdata.append(i_data)
    return fdata

@app.route('/')
def home():
    return render_template("home.html",)

@app.route('/dfs',methods=['GET', 'POST'])
def dfs():
    data=allplots(False)
    return render_template("dfs.html", data=data)

@socketio.on('dfs')
def handle_my_custom_event(data):

    event ='my-image-event'
    session_id=request.sid
    if(data['flag']==0):
        n=random.randint(0, 3)
        d=data['d']
    else:
        n=data['n']
        d=data['d']
    vids=SortedSet()
    g=Graph(allgraphs[n][0], directed= d)

    visual_style =initplot(g, session_id,event)
    if(data['flag']==1):
        d=DFS(g,int(data['src']),mode=OUT)
        text=[0]
        f=1
        for i in range(len(d[2])-1):
            vid=-1
            if d[2][i] != d[2][i+1]:
                g.vs[d[2][i][1]]["color"] = d[2][i][0]
                tmpsize=len(vids)
                vids.add(d[2][i][1])
                if tmpsize!=len(vids):
                    vid=d[2][i][1]
                if d[2][i][0]=="blue":
                    text=[2,d[2][i][1]]
                elif d[2][i][0]=="cyan":
                    if text[0]!=2:
                        text=[1,d[2][i][1]]
                else:
                    text=[0]
                if f==1:
                    f=0
                    text=[-1,d[2][i][1]]
                if d[2][i][2]:
                    plotgraph(g, visual_style, vid, session_id, event, text)
        text=[2,d[2][len(d[2])-1][1]]
        g.vs[d[2][len(d[2])-1][1]]["color"] = "Blue"
        plotgraph(g, visual_style,-1, session_id, event, text)
    socketio.emit('submit1',{'n':n,'d':d,'flag':data['flag']}, room=session_id)

@app.route('/bfs',methods=['GET', 'POST'])
def bfs():
    data=allplots(False)
    return render_template("bfs.html", data=data)

@socketio.on('bfs')
def handle_my_custom_event(data):
    
    event ='my-image-event2'
    session_id=request.sid
    if(data['flag']==0):
        n=random.randint(0, 3)
        d=data['d']
    else:
        n=data['n']
        d=data['d']
    vids=SortedSet()
    g=Graph(allgraphs[n][0], directed= d)
    
    visual_style =initplot(g, session_id, event)
    if(data['flag']==1):
        f=1
        d=BFS(g,int(data['src']),mode=OUT)
        for i in d[1]:
            vid=-1
            text=[]
            tmpsize=len(vids)
            vids.add(i[1])
            if tmpsize!=len(vids):
                vid=i[1]
            g.vs[i[1]]["color"] = i[0]
            if i[0]=="cyan":
                text=[1,i[1]]
            elif i[0]=="blue":
                text=[2,i[1]]
            else:
                text=[0]
            if f==1:
                f=0
                text=[-1,i[1]]
            plotgraph(g, visual_style, vid, session_id, event, text)
    socketio.emit('submit2',{'n':n,'d':d,'flag':data['flag']}, room=session_id)

@app.route('/dijkstra',methods=['GET', 'POST'])
def dijkstra():
    data=allplots(True)
    return render_template("dijkstra.html", data=data)

@socketio.on('dijkstra')
def handle_my_custom_event(data):

    event ='my-image-event4'
    session_id=request.sid
    if(data['flag']==0):
        n=random.randint(0, 3)
        d=data['d']
    else:
        n=data['n']
        d=data['d']
    g=Graph(allgraphs[n][0], directed= d, edge_attrs=dict(weight=allgraphs[n][1]))
    res=[]
    text=[]

    for i in range(g.vcount()):
        res.append('inf')
    visual_style =initplot(g, session_id, event, allgraphs[n][1])
    if(data['flag']==1):
        wt = defaultdict(dict)
        for e in g.es():
            wt[e.source][e.target]=e["weight"]
            if not g.is_directed():
                wt[e.target][e.source]=e["weight"]
        dists=[math.inf for i in range(g.vcount())]
        d1=dijkstra_sp(g,int(data['src']),dists,wt)
        
        flag=0
        for i in d1[1]:
            if i[0]==0:
                for j in range(len(i[1])):
                    g.vs[j]["name"]=i[1][j]
                    if(i[1][j]==math.inf):
                        i[1][j]='inf'
                    res[j]=i[1][j]
                    text=[0]
                visual_style["vertex_label"] = g.vs["name"]
                plotgraph(g, visual_style, res, session_id, event, text)
            elif i[0]==1:
                if flag==0:
                    flag=1
                    g.vs[i[2]]["name"]=0
                    res[i[2]]=0
                    visual_style["vertex_label"] = g.vs["name"]
                g.vs[i[2]]["color"] = i[1]
                if(i[1]=='cyan'):
                    text=[1,i[2]]
                else:
                    text=[-1]
                plotgraph(g, visual_style, res, session_id, event, text)
            elif i[0]==2:
                g.vs[i[2]]["color"] = i[1]
                g.vs[i[2]]["name"]=i[3]
                if(i[3]==math.inf):
                    i[3]='inf'
                res[i[2]]=i[3]
                if(i[1]=='cyan'):
                    text=[1,i[2]]
                else:
                    text=[-1]
                visual_style["vertex_label"] = g.vs["name"]
                plotgraph(g, visual_style, res, session_id, event, text)
            elif i[0]==-1:
                g.vs[i[1]]["color"] = "blue"
                text=[2,i[1]]
                plotgraph(g, visual_style, res, session_id, event, text)
    socketio.emit('submit4',{'n':n,'d':d,'flag':data['flag']}, 
            room=session_id)

if __name__ == '__main__':
    socketio.run(app, port=int(os.environ.get('PORT', 5000)))
