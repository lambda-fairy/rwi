from rwi.serial.error import MessageError

class Field(object):
    """The base class of a message field.

    All children of this class should implement two methods:

    1. ``parse_dict(data)`` which parses the raw data and returns the
       result;

    2. ``unparse_dict(data)`` which does the opposite.
    """

    def parse_dict(self, data):
        raise NotImplementedError('parse_dict')

    def unparse_dict(self, value):
        raise NotImplementedError('unparse_dict')

class PrimitiveField(Field):
    """A field that wraps a primitive type, e.g. ``int`` or ``str``."""

    def parse_dict(self, data):
        if not isinstance(data, self.inner_type):
            raise MessageError("expected type '%s', got '%s'"
                % (self.inner_type.__name__, data.__class__.__name__))
        else:
            return data

    def unparse_dict(self, value):
        return value

class Int(PrimitiveField):
    inner_type = int

class Float(PrimitiveField):
    inner_type = float

class String(PrimitiveField):
    inner_type = basestring

class List(Field):
    def __init__(self, subtype):
        self.subtype = subtype

    def parse_dict(self, data):
        return [self.subtype.parse_dict(datum)
                for datum in data]

    def unparse_dict(self, value):
        return [self.subtype.unparse_dict(subvalue)
                for subvalue in value]
