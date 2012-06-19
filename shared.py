import legume

PORT = 4000
WIDTH = 600
HEIGHT = 600

class Robot(object):
	def __init__(self):
		self._x = 0
		self._y = 0
		self._energy = 0
		self._speed = 0
		self._health = 100
		self._angle = 0
		self._name = ""
		self._colour = (255, 255, 255)
		self._radarAngle = 0
		self._radarResult = ""

class StateMessage(legume.messages.BaseMessage):
	MessageTypeID = 101
	MessageValues = {
		'energy'	: 'float',
		'speed'	: 'float',
		'health'	: 'float',
		'angle'	: 'float',
		'radarAngle'	: 'float',
		'radarResult'	: 'varstring',
	}

class ChangeAngleMessage(legume.messages.BaseMessage):
	MessageTypeID = 102
	MessageValues = {
		'angle'	: 'float',
	}

class ChangeSpeedMessage(legume.messages.BaseMessage):
	MessageTypeID = 103
	MessageValues = {
		'speed'	: 'float',
	}

class ChangeHealthMessage(legume.messages.BaseMessage):
	MessageTypeID = 104
	MessageValues = {
		'value'	: 'float',
	}

class RegisterMessage(legume.messages.BaseMessage):
	MessageTypeID = 105
	MessageValues = {
		'name'	: 'varstring',
		'red'	: 'int',
		'green'	: 'int',
		'blue'	: 'int',
	}

class ChangeRadarAngleMessage(legume.messages.BaseMessage):
	MessageTypeID = 106
	MessageValues = {
		'angle'	: 'float',
	}

class UseRadar(legume.messages.BaseMessage):
	MessageTypeID = 107
	MessageValues = {
	}

legume.messages.message_factory.add(StateMessage, ChangeAngleMessage, ChangeSpeedMessage, ChangeHealthMessage, RegisterMessage, ChangeRadarAngleMessage, UseRadar)
