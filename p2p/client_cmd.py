from xmlrpclib import ServerProxy, Fault
from cmd import Cmd
from random import choice
from string import lowercase
from node import Node, UNHANDLED
from threading import Thread
from time import sleep
import sys

HEAD_START = 0.1 # Seconds
SECRET_LENGTH = 100

def randomString(length):
    """
    Returns a random string of letters with the given length.
    """
    chars = []
    letters = lowercase[:26]
    while length > 0:
        length -= 1
        chars.append(choice(letters))
    return ''.join(chars)



class Client(Cmd):
    """
    A simple text-based interface to the Node class.
    """

    """
    You subclass Cmd to create a comnmand-line interface, and implement a method called
    do_foo for each command foo you want it to be able to handle. This method will receive
    the rest of the command line as its only arguments (as a string).

    For example, if you type in the command-line interface:

    say hello

    the method do_say is called with the string 'hello' as its only argument.
    """

    #The prompt of the Cmd subclass is determined by the prompt attribute
    prompt = '> '


    def __init__(self, url, dirname, urlfile):
        """
        Sets the url, dirname, and urlfile, and starts the Node
        Server in a separate thread.
        """
        Cmd.__init__(self)
        self.secret = randomString(SECRET_LENGTH)
        n = Node(url, dirname, self.secret)

        #Normally using thread involves a lot of safeguarding and synchronization with
        #locks and the like. However, because a Client interacts with its Node only
	    #through XML-RPC, you don't any of this.
        t = Thread(target=n._start)
    	#set Node to a daemon thread
    	#Any daemon threads are killed automatically when the program exits
        t.setDaemon(1)
        t.start()
        # Give the server a head start:
        #Make sure the server is fully started before connecting to it with XML-RPC
        sleep(HEAD_START)
        self.server = ServerProxy(url)
        for line in open(urlfile):
            line = line.strip()
            self.server.hello(line)


    def do_fetch(self, arg):
        "Call the fetch method of the Server."
        try:
            self.server.fetch(arg, self.secret)
        except Fault, f:
            if f.faultCode != UNHANDLED: raise
            print "Couldn't find the file", arg

    def do_exit(self, arg):
        "Exit the program."
        print
        sys.exit()

    do_EOF = do_exit #The EOF command occurs when the user press Ctrl+D in UNIX

def main():
    urlfile, directory, url = sys.argv[1:]
    client = Client(url, directory, urlfile)
    client.cmdloop()

if __name__ == '__main__': main()
