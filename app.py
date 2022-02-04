from flask import Flask, render_template, request
from igraph import *
from traversals import*
from graphs import*
from component import*
from PIL import Image
import base64
import io
import os
from flask_socketio import SocketIO
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app,transports= ['websocket'])
socketio.init_app(app, cors_allowed_origins="*")
def plotgraph(g, visual_style, session_id, event):
    plot(g, **visual_style, target='myfile.png')
    im = Image.open("myfile.png")
    data = io.BytesIO()
    im.save(data, "PNG")
    img_data = data.getvalue()
    socketio.sleep(1)
    socketio.emit(event, {'image_data': img_data},room=session_id)

def initplot(edges, k, session_id, event):
    g = Graph(edges, directed= k)
    nv = g.vcount()
    g.vs["name"] = [vi for vi in range(nv)]
    g.vs["color"]="white"
    layout = g.layout("kk")
    visual_style = {}
    visual_style["vertex_size"] = 20
    visual_style["vertex_label"] = g.vs["name"]
    visual_style["layout"] = layout
    visual_style["bbox"] = (300, 300)
    visual_style["margin"] = 20
    plot(g, **visual_style, target='myfile.png')
    im = Image.open("myfile.png")
    data = io.BytesIO()
    im.save(data, "PNG")
    img_data = data.getvalue()
    socketio.emit(event, {'image_data': img_data}, room=session_id)
    return (g,visual_style)

@app.route('/')
def home():
    return render_template("home.html",)

@app.route('/dfs',methods=['GET', 'POST'])
def dfs():
    return render_template("dfs.html")

@socketio.on('dfs')
def handle_my_custom_event(data):

    event ='my-image-event'
    session_id=request.sid
    if(data['flag']==0):
        n=random.randint(0, 2)
        d=random.randint(0, 1)
    else:
        n=data['n']
        d=data['d']

    g,visual_style =initplot(allgraphs[n],d,session_id,event)
    if(data['flag']):
        d=DFS(g,0,mode=OUT)
        for i in range(len(d[2])-1):
            if d[2][i] != d[2][i+1]:
                g.vs[d[2][i][1]]["color"] = d[2][i][0]
                if d[2][i][2]:
                    plotgraph(g, visual_style, session_id, event)
        g.vs[d[2][len(d[2])-1][1]]["color"] = "Blue"
        plotgraph(g, visual_style, session_id, event)
    socketio.emit('submit1',{'n':n,'d':d}, room=session_id)

@app.route('/bfs',methods=['GET', 'POST'])
def bfs():
    return render_template("bfs.html")

@socketio.on('bfs')
def handle_my_custom_event(data):
    
    event ='my-image-event2'
    session_id=request.sid
    if(data['flag']==0):
        n=random.randint(0, 2)
        d=random.randint(0, 1)
    else:
        n=data['n']
        d=data['d']
    g,visual_style =initplot(allgraphs[n],d,session_id,event)
    if(data['flag']):
        d=BFS(g,0,mode=OUT)
        for i in d[1]:
            g.vs[i[1]]["color"] = i[0]
            plotgraph(g, visual_style, session_id, event)
    socketio.emit('submit2',{'n':n,'d':d}, room=session_id)

@app.route('/wcc',methods=['GET', 'POST'])
def wcc():
    return render_template("wcc.html")


@socketio.on('wcc')
def handle_my_custom_event(data):

    event ='my-image-event3'
    session_id=request.sid
    if(data['flag']==0):
        n=random.randint(0, 2)
        d=random.randint(0, 1)
    else:
        n=data['n']
        d=data['d']
    g,visual_style =initplot(allgraphs[n],d,session_id,event)
    if(data['flag']):
        d=WCC(g)
        k=0
        for i in d[1]:
            for j in range(len(i)-1):
                if i[j]!=i[j+1]:
                    g.vs[i[j][1]]["color"] = i[j][0]
                    if i[j][2]:
                        plotgraph(g, visual_style, session_id, event)
            g.vs[i[len(i)-1][1]]["color"] = "Blue"
            plotgraph(g, visual_style, session_id, event)
            for j in i:
                g.vs[j[1]]["color"] = "white"
            plotgraph(g, visual_style, session_id, event)
            socketio.emit('text',{'component': d[0][k]},room=session_id)
            k+=1
    socketio.emit('submit3',{'n':n,'d':d}, room=session_id)


if __name__ == '__main__':
    socketio.run(app,debug=True)
