import sys
import os
import socket
import json

filename = sys.argv[1]
linenumber = 0
numVertex = 0
routingTables = []
MAX = 1000000
graph = []
with open(filename) as f:
    for line in f:
        x = line.split()
        linenumber = linenumber + 1
        oneTable = {}
        if linenumber == 1:
            numVertex = int(x[0])
        else:
            for j in range(1, numVertex+1):
                oneTable[str(j)] = str(MAX)
            oneTable[str(linenumber-1)] = str(0)
            for j in range(0, int(x[0])):
                oneTable[x[2*j+1]] = x[2*j+2]
                edge = [linenumber-1, int(x[2*j+1])]
                graph.append(edge)
        routingTables.append(oneTable)

for i in range(0, numVertex-1):
    for edge in graph:
        #send routingTables[edge[0]] to edge[1]
        #received dictionary of edge[0]
        #in my edge[1] dictionary distance to edge[0]
        host = ''
        port = 32000
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((host, port))
        pid = os.fork()
        if pid == 0:
            message, client = s.recvfrom(1024)
            data = json.dumps(routingTables[edge[0]])
            s.sendto(data, client)
            s.close()
            os._exit(0)
        else:
            r = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            r.sendto("handshake message", (host, port))
            data, server = r.recvfrom(1024)
            tableReceived = json.loads(data)
            r.close()
        weight = int(routingTables[edge[1]][str(edge[0])])
        for i in range(1, numVertex+1):
            if int(routingTables[edge[1]][str(i)]) > (weight + int(tableReceived[str(i)])):
                routingTables[edge[1]][str(i)] = str(weight + int(tableReceived[str(i)]))
for j in range(1, numVertex+1):
    routingTables[j] = sorted(routingTables[j].items())
with open('output', 'w') as f:
    for i in range(1, numVertex+1):
        f.write('%s ' %str(numVertex-1))
        for (x, y) in routingTables[i]:
            if int(x) != i:
                f.write('%s %s ' %(x, y))
        f.write('\n')
