from rwi.serial import *
import rwi.messages as M

class DeservesKick(Exception):
    """Raised when the client should be kicked."""
    pass

class Server:
    def __init__(self):
        # Dictionary of participating clients
        self.clients = {}
        # Whether the game has started or not
        self.game_started = False

    def handle_Hello(self, client, msg):
        if self.game_started:
            raise DeservesKick('game has already started')
        elif msg.name in self.clients:
            raise DeservesKick('name already taken')
        else:
            # Add the client to the game
            self.clients[msg.name] = client
            # TODO: add customizable server name and motd
            client.send_message(M.Olleh(server_name='', motd=''))

    def receive_message(self, client, s):
        try:
            msg = M.context.parse_json(s)
        except MessageError:
            raise DeservesKick('invalid message')
        else:
            try:
                # Choose which handler to use based on the message type
                # For example, a Hello message will be passed to handle_Hello()
                getattr(self, 'handle_' + msg.__class__.__name__)(client, msg)
            except AttributeError:
                raise DeservesKick('invalid message')

class Client:
    def __init__(self, server):
        self.server = server

    def send_message(self, msg):
        raise NotImplementedError('send_message')

    def kick(self, reason):
        self.send_message(M.Kick(reason=reason))
        self.disconnect()
