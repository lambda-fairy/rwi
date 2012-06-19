import legume
import shared
import threading
from time import sleep

class ClientRobot(shared.Robot):
	def __init__(self, host, name="", colour=(255, 255, 255)):
		super(ClientRobot, self).__init__()
		self._name = name
		self._colour = colour
		def messageHandler(sender, args):
			if legume.messages.message_factory.is_a(args, 'StateMessage'):
				self._energy = args.energy.value
				self._speed = args.speed.value
				self._health = args.health.value
				self._angle = args.angle.value
		self.client = legume.Client()
		self.client.OnMessage += messageHandler
		self.lock = threading.Lock()
		self.running = True
		self.client.connect((host, shared.PORT))
		def connect():
			while self.running:
				self.lock.acquire()
				self.client.update()
				self.lock.release()
				sleep(0.05)
			self.lock.acquire()
			self.client.disconnect()
			sleep(0.5)
			self.client.update()
			self.lock.release()
		self.net_thread = threading.Thread(target=connect)
		self.net_thread.start()
		sleep(1)
		msg = shared.RegisterMessage()
		msg.name.value = self._name
		msg.red.value = self._colour[0]
		msg.blue.value = self._colour[1]
		msg.green.value = self._colour[2]
		self.client.send_reliable_message(msg)
	
	def _getEnergy(self):
		return self._energy
	energy = property(_getEnergy)

	def _getSpeed(self):
		return self._speed
	def _setSpeed(self, value):
		msg = shared.ChangeSpeedMessage()
		msg.speed.value = value
		self.lock.acquire()
		self.client.send_reliable_message(msg)
		self.client.update()
		self.lock.release()
	speed = property(_getSpeed, _setSpeed)

	def _getHealth(self):
		return self._health
	def _setHealth(self, value):
		msg = shared.ChangeHealthMessage()
		msg.value.value = value
		self.lock.acquire()
		self.client.send_reliable_message(msg)
		self.client.update()
		self.lock.release()
	health = property(_getHealth, _setHealth)

	def _getAngle(self):
		return self._angle
	def _setAngle(self, value):
		msg = shared.ChangeAngleMessage()
		msg.angle.value = value
		self.lock.acquire()
		self.client.send_reliable_message(msg)		
		self.client.update()
		self.lock.release()
	angle = property(_getAngle, _setAngle)

	def _getRadarAngle(self):
		return self._radarAngle
	def _setRadarAngle(self, value):
		msg = shared.ChangeRadarAngleMessage()
		msg.angle.value = value
		self.lock.acquire()
		self.client.send_reliable_message(msg)
		self.client.update()
		self.lock.release()
	radarAngle = property(_getRadarAngle, _setRadarAngle)

robot = ClientRobot('localhost', 'Bruce', (255, 0, 0))
while True:
	sleep(0.5)
	print "Energy:", robot.energy
	print "Health:", robot.health
	robot.angle = robot.angle + 10
	print "Angle:", robot.angle
	robot.speed += 0.1
	print "Speed:", robot.speed
