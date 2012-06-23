"""
JSON (de)serialization library, using reflection to reduce repetitive code.

Examples are in the file ``tests/test_serial.py`` in the source distribution.
"""


__all__ = ['field', 'Message', 'MessageContext']

from rwi.serial import field
from rwi.serial.message import Message
from rwi.serial.context import MessageContext
