from rwi.serial.error import MessageError
from rwi.serial.field import Field

class Message(object):
    """A message type. You create a message type by inheriting from
    ``Message`` and populating it with ``Field``s."""

    def __init__(self, **attrs):
        """Create a message."""
        for key, value in attrs.items():
            setattr(self, key, value)

    def __getattribute__(self, key):
        # If an attribute hasn't been set, raise an error rather than
        # failing silently
        value = object.__getattribute__(self, key)
        if isinstance(value, Field):
            raise AttributeError("attribute '%s' has not been set"
                                 % key)
        else:
            return value

    def __setattr__(self, key, value):
        # Only allow setting an attribute if it's been declared in the class
        if hasattr(self.__class__, key):
            object.__setattr__(self, key, value)
        else:
            raise AttributeError("'%s' object has no attribute named '%s'"
                                 % (self.__class__.__name__, key))

    @classmethod
    def _get_fields(cls):
        """Return a dictionary mapping field names to fields."""
        fields = {}
        for name, entry in cls.__dict__.items():
            if isinstance(entry, Field):
                fields[name] = entry
        return fields

    @classmethod
    def _from_dict(cls, data):
        """Parse a message back from its serialized attributes."""

        data = data.copy()
        result = cls()

        # Check the message type name is correct
        if '__name__' not in data or data.pop('__name__') != cls.__name__:
            raise MessageError("__name__ field is missing or doesn't match")

        # Take each field out of the dictionary, adding it to the result
        for field_name, field in cls._get_fields().items():
            try:
                value = field.parse_dict(data.pop(field_name))
            except KeyError:
                raise MessageError('missing field: %s' % field_name)
            else:
                setattr(result, field_name, value)

        # Since we remove each attribute as we process it, if there are
        # any left in the dictionary it means they are invalid
        if data:
            raise MessageError('unknown attributes: %s' % data.keys())

        return result

    def _to_dict(self):
        """Convert this message to a dictionary that can then be
        serialized to JSON."""

        # Initialize the result with the class name
        result = {'__name__': self.__class__.__name__}

        # Add each field to the dictionary
        for field_name, field in self._get_fields().items():
            result[field_name] = field.unparse_dict(getattr(self, field_name))

        return result

    def __eq__(self, other):
        return self._to_dict() == other._to_dict()

    def __repr__(self):
        return '%s._from_dict(%s)' % (self.__class__.__name__, repr(self._to_dict()))
