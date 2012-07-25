"""Abstract server classes.

This module provides the platform independent part of the server -- in
other words, the "M" in MVC.
"""

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
        # Let clients join the game
        self.handler = JoinHandler()

    def receive_message(self, client, s):
        """Handle a receive message. This simply delegates to the
        current message handler."""
        self.handler.receive_message(self, client, s)

class MessageHandler:
    """A ``MessageHandler`` receives messages and acts on them."""

    def receive_message(self, server, client, s):
        """Parse the message, handing it over to the appropriate
        ``handle_XYZ`` method. If the message cannot be handled, throw a
        ``DeservesKick`` exception.
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
                getattr(self, 'handle_' + msg.__class__.__name__)(server, client, msg)
            except AttributeError:
                raise DeservesKick('invalid message')

class JoinHandler(MessageHandler):
    """Lets clients join the server with a ``Hello`` message."""

    def handle_Hello(self, server, client, msg):
        if client in server.clients.values():
            # Client has already joined the game
            raise DeservesKick('invalid message')
        elif msg.name in server.clients:
            raise DeservesKick('name already taken')
        else:
            # Add the client to the game
            server.clients[msg.name] = client
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
