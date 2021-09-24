import socket
from _thread import *
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = '127.0.0.1'
port = 4556

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(3)
print("Waiting for a connection")

id = "0"
player_state = ["0:,,", "1:,,", "2:,,"]
def thread_client(conn):
    global id, game_state
    conn.send(str.encode(id))
    if id == "1":
        id = "2"
    else:
        id = "1"
    reply = ''

    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')

            if not data:
                conn.send(str.encode("Conexion terminada: No Data"))
                break


            else:
                
                print("Received: " + reply)
                if "Message" not in reply:
                    l = reply.split(":")
                    pid = int(l[0])
                    player_state[pid] = reply

                    if pid == 0: 
                        nid1 = 1
                        nid2 = 2
                    if pid == 1: 
                        nid1 = 2
                        nid2 = 0
                    if pid == 2: 
                        nid1 = 0
                        nid2 = 1

                    reply1 = player_state[nid1][:]
                    reply2 = player_state[nid2][:]
                    print("Sending: " + reply1 + " --- " + reply2)
                
                else:
                    reply1 = "0:,,"
                    reply2 = "0:,,"

            conn.sendall(str.encode(reply1 + "..." + reply2))
            #conn.sendall(str.encode(reply2))


        except:
            break

while True:
    conn, addr = s.accept()

    print("Connected to client: ", addr)

    start_new_thread(thread_client, (conn,))