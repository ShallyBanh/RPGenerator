#    https://github.com/PlainSight/pythongame.git

import socket
import asyncore
import select
import random
import pickle
import time
import sys
sys.path.append('../')
from game_engine.game import Game

BUFFERSIZE = 512

outgoing = []
remove = []
overall_clients = []
client_dict = {}
rev_client_dict = {}
rooms = {}

class Minion:
    def __init__(self, ownerid):
        self.x = 50
        self.y = 50
        self.ownerid = ownerid

minionmap = {}

def updateWorld(message):
    arr = pickle.loads(message)
    print(str(arr))
    playerid = arr[1]
    x = arr[2]
    y = arr[3]

    if playerid == 0: return

    minionmap[playerid].x = x
    minionmap[playerid].y = y

    remove = []

    for i in outgoing:
        update = ['player locations']

        for key, value in minionmap.items():
            update.append([value.ownerid, value.x, value.y])
        
        try:
            i.send(pickle.dumps(update))
        except Exception:
            remove.append(i)
            continue
        
        print ('sent update data')

        for r in remove:
            outgoing.remove(r)

class ConnectionBuilderServer(asyncore.dispatcher):
    def __init__(self, port, protocol_family=socket.AF_INET, protocol_type=socket.SOCK_STREAM):
        asyncore.dispatcher.__init__(self)
        self.port = port
        self.protocol_family = protocol_family
        self.protocol_type = protocol_type
        self.create_socket(protocol_family, protocol_type)
        self.bind(('', port))
        if self.protocol_type != socket.SOCK_DGRAM:
            self.listen(10)
        else:
            DataReadServer()
    def handle_accept(self):
        conn, addr = self.accept()
        print ('Connection address:' + addr[0] + " " + str(addr[1]))
        outgoing.append(conn)
        overall_clients.append(conn)
        client_id = len(overall_clients)
        client_dict[conn] = [client_id, "", None]
        rev_client_dict[client_id] = conn
        # playerid = random.randint(1000, 1000000)
        print("there is a new connection, setting client id to {}".format(client_id))
        conn.send(pickle.dumps(['assign_id', client_id]))
        # playerminion = Minion(playerid)
        # minionmap[playerid] = playerminion
        # conn.send(pickle.dumps(['id update', playerid]))
        DataReadServer(conn)

class DataReadServer(asyncore.dispatcher_with_send):
    # def __init__(self, conn):
    #     asyncore.dispatcher_with_send.__init__(self)
    #     self.conn = conn
    #     self.client_id = None
    conn = None
    # use self.client_id to clean it up a bunch
    def handle_read(self):
        recievedData = self.recv(BUFFERSIZE)
        if recievedData:
            reconstructed = pickle.loads(recievedData)
            print("received data: {}".format(reconstructed))
            print("splitting reconstructed")
            command_type = reconstructed[0]
            command_body = reconstructed[1]
            print("split reconstructed")
            # if reconstructed[0] == 'register_client':
                # client
            print("parsing command type")
            if command_type == 'register_username':
                print("registering username")
                client_id = command_body[0]
                username = command_body[1]
                print("client_dict: {}".format(client_dict))
                print("self: {}".format(self))
                print("self.conn: {}".format(self.conn))
                self.conn = rev_client_dict[client_id]
                print("self.conn: {}".format(self.conn))
                client_dict[rev_client_dict[client_id]][1] = username
                print("registered username")
            
        else: self.close()
    def send_to_GM(self, message, room):
        pass
    def broadcast(self, message, room):
        print("broadcasting")
        for client in rooms[room][2]:
            rev_client_dict[client].send(pickle.dumps(['chat', message]))


ConnectionBuilderServer(4321)
# ConnectionBuilderServer(4322, protocol_type=socket.SOCK_DGRAM)


asyncore.loop()
