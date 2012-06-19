import legume
import shared
from math import *
import pygame
import sys
from time import sleep

def stateMessage(robot):
	msg = shared.StateMessage()
	msg.energy.value = robot._energy
	msg.speed.value = robot._speed
	msg.health.value = robot._health
	msg.angle.value = robot._angle
	msg.radarAngle.value = robot._radarAngle
	msg.radarResult.value = robot._radarResult
	return msg

class Arena(object):
	def __init__(self):
		pygame.init()
		self.window = pygame.display.set_mode((shared.WIDTH, shared.HEIGHT))
		self.server = legume.Server()
		self.server.OnConnectRequest += self.connectRequestHandler
		self.server.OnMessage += self.messageHandler
		self.server.OnDisconnect += self.disconnectHandler
		self.tick = 0
		self.clients = {}
	
	def connectRequestHandler(self, sender, args):
		print 'Connection!'
		self.clients[sender]=shared.Robot()
	
	def messageHandler(self, sender, args):
		robot = self.clients[sender]
		if legume.messages.message_factory.is_a(args, 'RegisterMessage'):
			robot._name = args.name.value
			robot._colour = (args.red.value, args.blue.value, args.green.value)
		elif legume.messages.message_factory.is_a(args, 'ChangeAngleMessage'):
			robot._angle = args.angle.value % 360
		elif legume.messages.message_factory.is_a(args, 'ChangeRadarAngleMessage'):
			robot._radarAngle = args.angle.value % 360
		elif legume.messages.message_factory.is_a(args, 'ChangeSpeedMessage'):
			if 0<=args.speed.value<=1:
				robot._speed = args.speed.value
		elif legume.messages.message_factory.is_a(args, 'ChangeHealthMessage'):
			robot._health += min(max(args.value.value, 0)-robot._health, robot._energy, 100-robot._health)
			robot._energy -= min(max(args.value.value, 0)-robot._health, robot._energy, 100-robot._health)
			
	
	def disconnectHandler(self, sender, args):
		del(self.clients[sender])
		print "Disconnect Occurred!"

	def go(self):
		self.server.listen(('', shared.PORT))
		while True:
			self.tick+=1
			self.window.fill((0, 0, 0))
			self.server.update()
			for client, robot in self.clients.items():
				client.send_reliable_message(stateMessage(robot))
				robot._energy += 1
				robot._energy -= robot._speed
				robot._x += robot._speed * sin(radians(robot._angle))
				if robot._x>shared.WIDTH-10:
					robot._x = shared.WIDTH-10
				elif robot._x<10:
					robot._x = 10
				robot._y += robot._speed * cos(radians(robot._angle))
				if robot._y>shared.HEIGHT-10:
					robot._y = shared.HEIGHT-10
				elif robot._y<10:
					robot._y = 10
				for otherRobot in self.clients.values():
					
				pygame.draw.circle(self.window, robot._colour, (int(robot._x), int(robot._y)), 10)
				pygame.draw.line(
					self.window,
					(0, 0, 0),
					(int(robot._x), int(robot._y)),
					(int(robot._x+10*sin(radians(robot._angle))), int(robot._y+10*cos(radians(robot._angle)))))
				pygame.draw.line(
					self.window,
					(0, 0, 0),
					(int(robot._x), int(robot._y)),
					(int(robot._x+8*sin(radians(robot._radarAngle))), int(robot._y+8*cos(radians(robot._radarAngle)))))
			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit(0)
			sleep(0.05)

arena = Arena()
arena.go()
