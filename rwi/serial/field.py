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
    @staticmethod
    def unparse_dict(value):
        return value

class Int(PrimitiveField):
    parse_dict = staticmethod(int)

class Float(PrimitiveField):
    parse_dict = staticmethod(float)

class String(PrimitiveField):
    @staticmethod
    def parse_dict(data):
        if not isinstance(data, basestring):
            raise TypeError("expected 'basestring', got %s" % type(data))
        else:
            return data

class List(Field):
    def __init__(self, subtype, *args, **kwds):
        self.subtype = subtype
        Field.__init__(self, *args, **kwds)

    def parse_dict(self, data):
        return [self.subtype.parse_dict(datum)
                for datum in data]

    def unparse_dict(self, value):
        return [self.subtype.unparse_dict(subvalue)
                for subvalue in value]
