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
    my_id = None
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
                self.my_id = client_id
                username = command_body[1]
                print("client_dict: {}".format(client_dict))
                print("self: {}".format(self))
                self.conn = rev_client_dict[client_id]
                print("self.conn: {}".format(self.conn))                
                print("self.conn: {}".format(self.conn))
                client_dict[rev_client_dict[client_id]][1] = username
                print("registered username")
            elif command_type == "start_game":
                # @TODO connect to database
                client = int(command_body[0])
                game_id = int(command_body[1])
                print("client {} requesting to start game {}".format(client, game_id))
                if game_id not in rooms:
                # if command_body.isdigit() and int(command_body) not in rooms:
                    # make sure belongs to that user
                    print("game {} started".format(command_body))
                    game = Game()
                    game.uniqueID = game_id
                    rooms[game_id] = [self, Game(), [client]]
                    print("rooms is now {}".format(rooms))
                    client_dict[rev_client_dict[client]][2] = game_id
                else:
                    print("failed to start game")
            elif command_type == "join_game":
                print("forwarding join request")
                room = command_body[0]
                if room.isdigit() and int(room) in rooms and self != rooms[int(room)][0]:
                    request = ['join_request', [client_dict[self.conn], int(room)]]
                    # @TODO try except
                    # build target/message then do at end?
                    print("sending the forwarded request")
                    rooms[int(room)][0].send(pickle.dumps(request))
                    print("sent the forwarded request")
                else:
                    print("join request was invalid")
                    self.send(pickle.dumps(['join_invalid']))
            elif command_type == 'accept_join':
                print("join request was accepted")
                # do something with the room
                room = command_body[1]
                client = command_body[0][0]
                print("{} ({})".format(client, type(client)))
                print("command body is {}".format(command_body))
                print("appending client {} to room {}".format(client, room))
                print("rooms: {}".format(rooms))
                print("rooms[{}]: {}".format(room, rooms[room]))
                rooms[room][2].append(client_dict[rev_client_dict[client]][0])
                client_dict[rev_client_dict[client]][2] = room
                print("rooms[{}]: {}".format(room, rooms[room]))               
                rev_client_dict[client].send(pickle.dumps(['join_accept', rooms[room][1]]))
            elif command_type == 'reject_join':
                print("join request was rejected")
                rev_client_dict[command_body[0][0]].send(pickle.dumps(['join_reject', command_body]))
            elif command_type == 'leave_game':
                print("player trying to leave game @TODO append to transcript")
                client_id = int(command_body)
                if client_id = self.my_id:
                    print("client_id is {}".format(client_id))
                    client = client_dict[rev_client_dict[client_id]]
                    print("client is {}".format(client))
                    room = client[2]
                    print("room is {}".format(room))
                    self.remove_player(client_id, rooms[room])
                else:
                    print("received leave command for wrong id")
            elif command_type == 'remove_player':
                client_id = int(command_body)
                client = client_dict[rev_client_dict[client_id]]        
                room = client[2]
                self.remove_player(client_id, room)
                # print("removing client_id from game @TODO append to transcript")
                # print("finding client from command_body {}".format(client_id))
                # print("client_dict: {}".format(client_dict))
                # print("rev_client_dict: {}".format(rev_client_dict))
                # client = client_dict[rev_client_dict[client_id]]
                # print("client is {}, finding room".format(client))
                # room = client[2]
                # print("room is {}".format(room))
                # client[2] = None
                # print("removing client from room")
                # # @TODO try/check if exists
                # rooms[room][2].remove(client_id)
                # print("done leaving game")
                # rev_client_dict[client_id].send(pickle.dumps(['removed', '']))
            elif command_type == 'end_game':
                print("@TODO end game, remove players")
                # requester = command_body[0]
                client_id = command_body[0]
                room = command_body[1]
                if rooms[room][0] == self:
                    room_member_copy = rooms[room][2]
                    for player in room_member_copy:
                        self.remove_player(player, rooms[room])
                    self.remove_player(client_id, rooms[room])

            elif command_type == 'chat':
                # for client in room
                print("@TODO append to transcript then send out")
                client_id = command_body[0]
                print("{} ({})".format(client_id, type(client_id)))
                message = command_body[1]
                print("message: {}".format(message))
                room = client_dict[rev_client_dict[client_id]][2]
                print("room {}".format(room))
                self.broadcast(message, room)

            # chat, start_game, join_game, accept_join_request, reject_join_request, action, voice
            # send_to_GM, broadcast
            #logic for i in outgoing:
            #logic     update = ['from server', client_dict[i], reconstructed[1]]

        
            #logic     try:
            #logic         i.send(pickle.dumps(update))
            #logic     except Exception:
            #logic         remove.append(i)
            #logic         continue
        
            #logic print ('sent update data')

            #logic for r in remove:
            #logic     outgoing.remove(r)

        #     i.send(pickle.dumps(update))
        #     updateWorld(recievedData)
        else: self.close()
    def remove_player(self, client_id, room):
        print("removing player from game @TODO append to transcript")
        client = client_dict[rev_client_dict[client_id]]
        room[2].remove(client_id)
        client[2] = None
        # room = client[2]
        # print("room is {}".format(room))
        # client[2] = None
        # print("removing client from room")
        # # @TODO try/check if exists
        # rooms[room][2].remove(player)
        # print("done leaving game")
        rev_client_dict[client_id].send(pickle.dumps(['removed', '']))
    def send_to_GM(self, message, room):
        pass
    def broadcast(self, message, room):
        print("broadcasting")
        for client in rooms[room][2]:
            print("trying to send to client_id: {}".format(client))            
            connection = rev_client_dict[client]
            if connection != self.conn:
                print("sending to someone else")
                connection.send(pickle.dumps(['chat', message]))
            else:
                print("not sending back to self")


def main():
    ConnectionBuilderServer(5000)
    # ConnectionBuilderServer(4322, protocol_type=socket.SOCK_DGRAM)


    asyncore.loop()
