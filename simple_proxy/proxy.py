#!/usr/bin/python

# This is a simple port-forward / proxy, written using only the default python
# library. If you want to make a suggestion or fix something you can contact-me
# at voorloop_at_gmail.com
# Distributed over IDC(I Don't Care) license

import socket
import select
import time
import sys

# Changing the buffer_size and delay, you can improve the speed and bandwidth.
buffer_size = 4096  # Keep reasonably low
delay = 0.0001 # Keep reasonaly high
#delay = 0.0

class Forward:
    def __init__(self):
        self.forward = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, host, port):
        try:
            self.forward.connect((host, port))
            return self.forward
        except Exception, e:
            print e
            return False

class ProxyServer:

    def __init__(self, host, port, forward_port):
        self.channel = {}
        self.forward_port = forward_port

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(200)
        self.server = server
        self.input_list = [self.server]
        

    def main_loop_step(self):
        ss = select.select
        inputready, outputready, exceptready = ss(self.input_list, [], [])
        for self.s in inputready:
            if self.s == self.server:
                self.on_accept()
                break
            self.data = self.s.recv(buffer_size)
            if len(self.data) == 0:
                self.on_close()
            else:
                self.on_recv()

    def on_accept(self):
        clientsock, clientaddr = self.server.accept()
        forward = Forward().start(clientaddr[0], self.forward_port)
        if forward:
            print clientaddr, "has connected"
            self.input_list.append(clientsock)
            self.input_list.append(forward)
            self.channel[clientsock] = forward
            self.channel[forward] = clientsock
        else:
            print "Can't establish connection with remote server.",
            print "Closing connection with client side", clientaddr
            clientsock.close()

    def on_close(self):
        print self.s.getpeername(), "has disconnected"
        #remove objects from input_list
        self.input_list.remove(self.s)
        self.input_list.remove(self.channel[self.s])
        out = self.channel[self.s]
        # close the connection with client
        self.channel[out].close()  # equivalent to do self.s.close()
        # close the connection with remote server
        self.channel[self.s].close()
        # delete both objects from channel dict
        del self.channel[out]
        del self.channel[self.s]

    def on_recv(self):
        data = self.data
        # here we can parse and/or modify the data before send forward
        #print data
        self.channel[self.s].send(data)

import sys
if __name__ == '__main__':
        port = int(sys.argv[1])
        forward_port = int(sys.argv[2])
        server = ProxyServer('', port, forward_port)
        try:
          while 1:
            time.sleep(delay)
            server.main_loop_step()
        except KeyboardInterrupt:
            print "Ctrl C - Stopping server"
            sys.exit(1)
