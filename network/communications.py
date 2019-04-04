#    https://github.com/PlainSight/pythongame.git

import socket
import asyncore
import select
import random
import pickle, jsonpickle
import time
import sys
sys.path.append('../')
from game_engine.game import Game

BUFFERSIZE = 4096

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


def receive_bundle(connection, buffersize):
    data = []
    while True:
        packet = connection.recv(buffersize)
        if len(packet) < buffersize: break
        data.append(packet)
    # data_arr = pickle.loads(b"".join(data))
    # print (data_arr)
    return b"".join(data)

def double_pickle(data):
    print("jsonpickling")
    jsonpickled = jsonpickle.encode(data)
    print("pickling")
    pickled = pickle.dumps(jsonpickled)
    return pickled

def double_unpickle(data):
    print("unpickling")
    unpickled = pickle.loads(data)
    print("jsonunpickling")
    restored = jsonpickle.decode(unpickled)
    return restored

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
        print("trying to (json)pickle {}".format(['assign_id', client_id]))
        pickled = double_pickle(['assign_id', client_id])
        print("pickled, going to send")
        conn.send(pickled)
        print("sent the assign_id message")
        # playerminion = Minion(playerid)
        # minionmap[playerid] = playerminion
        # conn.send(double_pickle(['id update', playerid]))
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
        # data = []
        # while True:
        #     packet = self.recv(BUFFERSIZE)
        #     if not packet: break
        #     data.append(packet)
        # data_arr = pickle.loads(b"".join(data))
        # print (data_arr)

        recievedData = self.recv(BUFFERSIZE)
        # if recievedData:
        # data = receive_bundle(self, BUFFERSIZE)
        if recievedData:
        # if data:
            print("got some data")
            # reconstructed = double_unpickle(data)
            reconstructed = double_unpickle(recievedData)
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
                # client = int(command_body[0])
                # game_id = int(command_body[1])
                # game = command_body[0]
                game_id = command_body[0]
                client_id = self.my_id
                print("client {} requesting to start game {}".format(client_dict[self.conn][0], game_id))
                if game_id not in rooms:
                # if command_body.isdigit() and int(command_body) not in rooms:
                    # make sure belongs to that user
                    print("game {} started".format(command_body))
                    rooms[game_id] = [self.conn, None, [client_id]]
                    print("rooms is now {}".format(rooms))
                    client_dict[self.conn][2] = game_id
                else:
                    print("failed to start game")
            elif command_type == "join_game":
                print("forwarding join request")
                print("command body is {}".format(command_body))
                room = command_body[0]
                print("checking for room {}".format(room))
                if room.isdigit() and int(room) in rooms and self.conn != rooms[int(room)][0]:
                    request = ['join_request', [client_dict[self.conn], int(room)]]
                    # @TODO try except
                    # build target/message then do at end?
                    print("sending the forwarded request")
                    pickled = double_pickle(request)
                    print("rooms[{}][0] -> {}.send(({} bytes): {})".format(int(room), rooms[int(room)][0], sys.getsizeof(pickled), pickled))
                    rooms[int(room)][0].send(pickled)
                    print("sent the forwarded request")
                else:
                    print("join request was invalid")
                    print("the active rooms are {}".format(rooms.keys()))
                    self.send(double_pickle(['join_invalid', '']))
            elif command_type == 'accept_join':
                print("join request was accepted")
                # do something with the room
                room = command_body[1]
                client = command_body[0][0]
                game_id = room
                print("{} ({})".format(client, type(client)))
                print("command body is {}".format(command_body))
                print("appending client {} to room {}".format(client, room))
                print("rooms: {}".format(rooms))
                print("rooms[{}]: {}".format(room, rooms[room]))
                rooms[room][2].append(client_dict[rev_client_dict[client]][0])
                client_dict[rev_client_dict[client]][2] = room
                print("rooms[{}]: {}".format(room, rooms[room]))         
                rev_client_dict[client].send(double_pickle(['join_accept', game_id]))
            elif command_type == 'reject_join':
                print("join request was rejected")
                rev_client_dict[command_body[0][0]].send(double_pickle(['join_reject', command_body]))
            elif command_type == 'leave_game':
                print("player trying to leave game @TODO append to transcript")
                client_id = int(command_body[0])
                connection = self.get_conn_from_client_id(client_id)
                room_id = self.get_room_id_from_client_id(client_id)
                username = client_dict[connection][1]
                room = rooms[room_id]
                if room[0] == connection:
                    # print("client_id is {}".format(client_id))
                    # client = client_dict[rev_client_dict[client_id]]
                    # print("client is {}".format(client))
                    # room = client[2]
                    # print("room is {}".format(room))
                    print("player {} is leaving in communications.py".format(username))
                    self.remove_player(client_id, room)
                else:
                    print("received leave command for wrong id")
            elif command_type == 'remove_player':
                username = command_body
                print(username)
                client_id = -1
                for client in client_dict:
                    print(client_dict[client][1])
                    if client_dict[client][1] == username:
                        print("found client {} {}".format(client_dict[client][1], client_dict[client][0]))
                        client_id = client_dict[client][0]
                        break
                if client_id != -1:
                    client = self.get_conn_from_client_id(client_id)
                    print("client {}".format(client))
                    room = client[2]
                    print("room {}".format(room))
                    self.remove_player(client_id, room)
                else:
                    print("failed to find client_id from username {}".format(username))
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
                # rev_client_dict[client_id].send(double_pickle(['removed', '']))
            elif command_type == 'end_game':
                print("@TODO end game, remove players")
                # requester = command_body[0]
                client_id = command_body[0]
                room = command_body[1] # game_id
                connection = rev_client_dict[client_id]
                if rooms[room][0] == connection:
                    room_member_copy = rooms[room][2]
                    for player in room_member_copy:
                        if player != client_id:
                            username = client_dict[rev_client_dict[player]][1]
                            print("calling to remove other player {} on connection {}".format(username, player))
                            self.remove_player(player, rooms[room], is_GM=False)
                        else:
                            print("not removing self yet")
                    print("removing self")
                    self.remove_player(client_id, rooms[room], is_GM=True)
                    del rooms[room]
                    print("rooms after end_game are {}".format(rooms))

            elif command_type == 'chat':
                # for client in room
                print("@TODO append to transcript then send out")
                client_id = command_body[0]
                print("{} ({})".format(client_id, type(client_id)))
                message = command_body[1]
                print("message: {}".format(message))
                room_id = self.get_room_id_from_client_id(client_id)
                print("room {}".format(room_id))
                pickled_message = double_pickle(['chat', message])
                self.broadcast(pickled_message, room_id, client_id)
            elif command_type == 'request_action':
                client_id = command_body[0]
                # requested_action = command_body[2]
                # connection = self.get_conn_from_client_id(client_id)
                # username = client_dict[connection][1]
                room_id = self.get_room_id_from_client_id(client_id)
                # print("player {} ({}) has requested action {}\nforwarding to GM for room {}".format(username, client_id, requested_action, room_id))
                rooms[room_id][0].send(recievedData)
            elif command_type == 'update_game':
                # room = command_body[1].get_uniqueID()
                client_id = command_body[0]
                room = command_body[1]
                connection = rev_client_dict[client_id]      
                if rooms[room][0] == connection:
                    print("GM has updated the game")
                    # pickled_message = double_pickle(['update_game', message])
                    self.broadcast(recievedData, room, client_id)
                else:
                    print("a non-GM player tried to update the game")
            elif command_type == 'asset_added':
                client_id = command_body[0]
                room_id = self.get_room_id_from_client_id(client_id)
                connection = rev_client_dict[client_id]
                if rooms[room_id][0] == connection:
                    print("GM added an asset, broadcasting notice to others")                          
                    self.broadcast(recievedData, room_id, client_id)
                else:
                    print("a non-GM player said they added an asset")

            # elif command_type == 'action_approved':
            #     print("@TODO action_approved, broadcast game object")
            # elif command_type == 'action_rejected':
            #     print("@TODO action_rejected")
            # chat, start_game, join_game, accept_join_request, reject_join_request, action, voice
            # send_to_GM, broadcast
            #logic for i in outgoing:
            #logic     update = ['from server', client_dict[i], reconstructed[1]]

        
            #logic     try:
            #logic         i.send(double_pickle(update))
            #logic     except Exception:
            #logic         remove.append(i)
            #logic         continue
        
            #logic print ('sent update data')

            #logic for r in remove:
            #logic     outgoing.remove(r)

        #     i.send(double_pickle(update))
        #     updateWorld(recievedData)
        else: self.close()
    def remove_player(self, client_id, room, is_GM=False):
        username = client_dict[rev_client_dict[client_id]][1]
        print("removing player {} on connection {}".format(username, client_id))
        if is_GM:
            print("not sending remove message to GM")      
        else:
            print("sending the remove message to another player")
            rev_client_dict[client_id].send(double_pickle(['removed', '']))
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
    def get_conn_from_client_id(self, client_id):
            connection = rev_client_dict[client_id]
            return connection
    
    def get_room_id_from_client_id(self, client_id):
        connection = self.get_conn_from_client_id(client_id)
        room_id = client_dict[connection][2]
        return room_id
        
    def send_to_GM(self, message, room):
        pass
    def broadcast(self, pickled_message, room, client_id):
        print("broadcasting")
        for client in rooms[room][2]:
            print("trying to send to client_id: {}".format(client))
            connection = rev_client_dict[client]
            if client != client_id:
                print("sending to someone else")
                connection.send(pickled_message)
            else:
                print("not sending back to self")

            # if chatting:
            #     if client != client_num:
            #         print("sending to someone else")
            #         connection.send(pickled_message)
            #     else:
            #         print("not sending back to self")
            # else:
            #     if rooms[room][0] != connection:
            #         print("sending to someone else")
            #         connection.send(pickled_message)
            #     else:
            #         print("not sending back to self")



def main():
    ConnectionBuilderServer(5000)
    # ConnectionBuilderServer(4322, protocol_type=socket.SOCK_DGRAM)


    asyncore.loop()
