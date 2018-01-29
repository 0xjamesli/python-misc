#!/usr/local/bin/env python

'''
ncat alternative
'''

import sys
import socket
import getopt
import threading
import subprocess


listen             = False
command            = False
target             = ""
port               = ""


def usage():
 print("nc-alt Tool")
 print("Usage: {} -t target_host -p port\n".format(sys.argv[0]))
 print("\t-l --listen - listen on [host]:[port] for incoming connections")
 print("\t-c --command - initialize a command shell")


def main():
 global listen
 global port
 global command
 global target

 if not len(sys.argv[1:]):
  usage()
  exit(0)

 # read the command line options
 try:
  opts, args = getopt.getopt(sys.argv[1:], "hlt:p:c", ["help", "listen", "target", "port", "command"])
 except getopt.GetoptError as err:
  print(str(err))
  exit(1)

 for o, a in opts:
  if o in ("-h", "--help"):
   usage()
  elif o in ("-l", "--listen"):
   listen = True
  elif o in ("-c", "--command"):
   command = True
  elif o in ("-t", "--target"):
   target = a
  elif o in ("-p", "--port"):
   port = int(a)
  else:
   assert False, "Unhandled Option"

 # client mode
 if not listen and len(target) and port > 0:

     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     s.settimeout(20)
     s.connect((target, port))
     s.sendall(b'whoami')
     whoami = s.recv(100)

     try:
        while 1:
         data = input(">>>" + whoami.decode("utf-8").strip() + ":")
         print(a)
     except Exception as e:
        print(str(e))
        s.close()
        print("Exiting...")

 # server mode
 if listen:
  server_loop()


'''
Client propmt: read from stdin
'''
def client_sender(buffer):
    print(buffer)

'''
Listen for incomming TCP connections
'''
def server_loop():

 global target
 global port

 server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 server.bind((target, port))

 # 3 connections max
 server.listen(3)

 '''
 TODO: Add error handle and more verbose message
 '''
 while True:
  client_socket, addr = server.accept()
  # The return value is a pair (conn, address)
  # conn is a new socket object usable to send and receive data
  # on the connection, and address is the address bound to the
  # socket on the other end of the connection.
  print("New client connected.")

  # spin off a thread to handle our new client
  client_thread = threading.Thread(target=client_handler, args=(client_socket, addr))
  client_thread.setDaemon(True)
  client_thread.start()

 server.shutdown()
 server.close()


def client_handler(conn, client_addr):
 while conn:
  cmd = conn.recv(1024).strip()
  if cmd:
   data = run_command(cmd)
   conn.send(data)
  else:
   break
 conn.close()


'''
Execute command
'''
def run_command(command):
 command = command.rstrip()

 try:
  # To also capture standard error in the result, use stderr=subprocess.STDOUT
  output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
 except subprocess.CalledProcessError as err:
  output = err.output

 return output


if __name__ == "__main__":
 main()
