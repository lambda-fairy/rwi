import pytest

from rwi.serial import *

context = MessageContext()

@context.add
class Tick(Message):
    n = field.Int()

@context.add
class PlayerInfo(Message):
    id = field.Int()
    name = field.String()
    health = field.Float()

@context.add
class NoOp(Message):
    pass

@context.add
class EpicNestedList(Message):
    what = field.List(field.List(field.List(field.List(field.Int()))))

def test_roundtrip():
    t = Tick(n=1)
    p = PlayerInfo(id=999999999999999,
                   name=u'\0hello\uffff\uabcd\u1234"\ufffe',
                   health=42.42)
    n = NoOp()
    e = EpicNestedList(what=[[[[1,2,3],[4,5,6]]*2]*5]*3)
    for message in [t, p, n, e]: # Timpani! Boom boom boom!
        assert context.parse_json(context.unparse_json(message)) == message

def test_invalid_type():
    with pytest.raises(MessageError):
        context.parse_json('{"__name__": "InvalidSomething"}')

def test_crappy_input():
    for crap in ['{}', '[]', '42', '"a"']:
        with pytest.raises(MessageError):
            context.parse_json(crap)

def test_extra_attrs():
    with pytest.raises(AttributeError):
        Tick(n=1, blah="this shouldn't work")

def test_missing_attrs():
    t = Tick()
    with pytest.raises(AttributeError):
        context.unparse_json(t)
