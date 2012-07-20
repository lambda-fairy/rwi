"""Packet definitions.

For information on what these messages mean, see ``protocol.rst``.
"""

from rwi.serial import *

PROTOCOL_VERSION = 0

context = MessageContext()

@context.add
class Hello(Message):
    """The client introduces itself to the server."""
    version = field.Int()
    name = field.String()

@context.add
class Olleh(Message):
    """The server accepts the client."""
    server_name = field.String()
    motd = field.String()

@context.add
class Kick(Message):
    """The server is disconnecting the client."""
    reason = field.String()

@context.add
class Tick(Message):
    """One tick has elapsed.

    If `n = 0`, a game has just begun. Clients should clear their
    internal state and prepare for a new game.
    """

    class Player(Message):
        """The status of an adversary."""
        name = field.String()
        health = field.Int()
        energy = field.Int()

        @property
        def is_alive(self):
            return self.health > 0

    class Status(Player):
        """The player's own status."""
        gun_dir = field.Float()
        radar_dir = field.Float()
        direction = field.Float()
        speed = field.Float()

    n = field.Int()
    status = field.Object(Status)
    players = field.List(field.Object(Player))
