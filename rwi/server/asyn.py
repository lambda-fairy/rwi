import asyncore
import asynchat
from cStringIO import StringIO
import socket

import rwi.defaults as D
import rwi.messages as M
from rwi.server.model import Client, Server, DeservesKick

class AsynServer(Server, asyncore.dispatcher):
    def __init__(self, host=D.HOST, port=D.PORT):
        Server.__init__(self)
        asyncore.dispatcher.__init__(self)

        # Dictionary mapping client addresses to sockets
        self.connected = {}

        # Listen for connections
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            self.connected[addr] = AsynClient(self, addr, sock)

class AsynClient(Client, asynchat.async_chat):
    def __init__(self, server, addr, sock):
        Client.__init__(self, server)
        asynchat.async_chat.__init__(self, sock=sock)
        self.set_terminator(D.MESSAGE_SEPARATOR)
        self.addr = addr
        self.ibuffer = StringIO()

    def send_message(self, msg):
        self.push(M.context.unparse_json(msg) + D.MESSAGE_SEPARATOR)

    def collect_incoming_data(self, data):
        self.ibuffer.write(data)

    def found_terminator(self):
        try:
            self.server.receive_message(self, self.ibuffer.getvalue())
        except DeservesKick as ex:
            self.kick(str(ex))
        finally:
            # Clear the buffer
            self.ibuffer = StringIO()

    def disconnect(self):
        self.close()

    def handle_close(self):
        del self.server.connected[self.addr]
