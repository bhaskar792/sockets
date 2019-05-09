import socket
import sys

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

def socket_accept():
    # first is object of connection second is list of ip addresses
    conn,address = s.accept()
    print('connection established'+ 'ip' +address[0]+ 'port' + str(address[1]))
    send_commands(conn)
    conn.close()

# send commands to clients
def send_commands(conn):
    while True:
        cmd= input()
        if cmd== 'quit':
            conn.close()
            s.close()
            sys.exit()
        if len(str.encode(cmd))>0:
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(1024),'utf-8')
            print(client_response,end="")

def main():
    create_socket()
    bind_socket()
    socket_accept()

main()