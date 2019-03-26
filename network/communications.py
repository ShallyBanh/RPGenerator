#  https://github.com/PlainSight/pythongame.git

import socket
import asyncore
import select
import random
import pickle
import time

BUFFERSIZE = 512

outgoing = []
remove = []
overall_clients = []
client_dict = {}

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

class MainServer(asyncore.dispatcher):
  def __init__(self, port):
    asyncore.dispatcher.__init__(self)
    self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
    self.bind(('', port))
    self.listen(10)
  def handle_accept(self):
    conn, addr = self.accept()
    print ('Connection address:' + addr[0] + " " + str(addr[1]))
    outgoing.append(conn)
    overall_clients.append(conn)
    client_dict[conn] = len(overall_clients)
    client_id = len(overall_clients)
    # playerid = random.randint(1000, 1000000)
    conn.send(pickle.dumps(['register', client_id]))
    # playerminion = Minion(playerid)
    # minionmap[playerid] = playerminion
    # conn.send(pickle.dumps(['id update', playerid]))
    SecondaryServer(conn)

class SecondaryServer(asyncore.dispatcher_with_send):
  def handle_read(self):
    recievedData = self.recv(BUFFERSIZE)
    if recievedData:
      print("received data: {}".format(pickle.loads(recievedData)))
      reconstructed = pickle.loads(recievedData)
      for i in outgoing:
        update = ['from server', client_dict[i], reconstructed[1]]

    
        try:
          i.send(pickle.dumps(update))
        except Exception:
          remove.append(i)
          continue
    
      print ('sent update data')

      for r in remove:
        outgoing.remove(r)

    #   i.send(pickle.dumps(update))
    #   updateWorld(recievedData)
    else: self.close()

MainServer(4321)
asyncore.loop()