"""Abstract server classes."""

from rwi.serial import *
import rwi.messages as M

class DeservesKick(Exception):
    """Raised when the client should be kicked."""
    pass

class Server:
    """Abstract server.

    To implement a real server, inherit from this class and call
    ``receive_message()`` whenever a message is received.
    """

    def __init__(self):
        # Dictionary mapping client name -> client object
        self.clients = {}
        # Whether the game has started or not
        self.game_started = False

    def receive_message(self, client, s):
        """Parse the message, handing it over to the appropriate
        ``handle_XYZ`` method.
        """
        try:
            # Parse the message
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

class Client:
    """Abstract client.

    To create a real client, inherit from this class and override the
    following methods:

    * ``send_message(msg)``
    * ``disconnect()``
    """

    def __init__(self, server):
        self.server = server

    def send_message(self, msg):
        """Send a message to the client."""
        raise NotImplementedError('send_message')

    def kick(self, reason):
        """Kick this client from the game."""
        self.send_message(M.Kick(reason=reason))
        self.disconnect()

    def disconnect(self):
        """Close the connection with the client."""
        raise NotImplementedError('disconnect')
