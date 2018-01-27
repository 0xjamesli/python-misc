#!/usr/local/bin/python2.7

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
upload             = False
execute            = ""
target             = ""
upload_destination = ""
port               = ""


'''
TODO:
Formatting problems

TODO:
Solve the sudo issue

TODO:
Finish the client part

TODO:
Finish upload part

TODO:
Finish piping part

TODO:
Debugging
'''

def usage():
 print("nc-alt Tool")
 print("Usage: {} -t target_host -p port\n".format(sys.argv[0]))
 print("\t-l --listen - listen on [host]:[port] for incoming connections")
 print("\t-e --execute=file_to_run - execute the given file upon receiving a connection")
 print("\t-c --command - initialize a command shell")
 print("\t-u --upload=destination - upon receiving connection upload a file [destination]")
 print("\n\n\n")
 print("Examples: *")
 print("\t{} -t 192.168.0.1 -p 5555 -l -c".format(sys.argv[0]))
 print("\t{} -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe".format(sys.argv[0]))
 print("\t{} -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"".format(sys.argv[0]))
 print("\techo 'ABCDEF' | ./{} -t 192.168.0.12 -p 135".format(sys.argv[0]))


def main():
 global listen
 global port
 global execute
 global command
 global upload_destination
 global target

 if not len(sys.argv[1:]):
  usage()

 # read the command line options
 try:
  opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:", ["help", "listen", "execute", "target", "port", "command", "upload"])
 except getopt.GetoptError as err:
  print(str(err))
  usage()

 for o, a in opts:
  if o in ("-h", "--help"):
   usage()
  elif o in ("-l", "--listen"):
   listen = True
  elif o in ("-e", "--execute"):
   execute = a
  elif o in ("-c", "--command"):
   command = True
  elif o in ("-u", "--upload"):
   upload_destination = a
  elif o in ("-t", "--target"):
   target = a
  elif o in ("-p", "--port"):
   port = int(a)
  else:
   assert False, "Unhandled Option"

 if not listen and len(target) and port > 0:
  buffer = sys.stdin.read()
  client_sender(buffer)

 if listen:
  server_loop()


def server_loop():
 global target
 global port

 # if no target is defiend we listen on localhost
 if not len(target):
  target = "localhost"

 server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 server.bind((target, port))

 # 5 connections max
 server.listen(5)

 while True:
  client_socket, addr = server.accept()
  # The return value is a pair (conn, address)
  # conn is a new socket object usable to send and receive data
  # on the connection, and address is the address bound to the
  # socket on the other end of the connection.

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
