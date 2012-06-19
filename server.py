import legume
from time import sleep

def disconnectHandler(sender, args):
	print "Disconnected"

server = legume.Server()
server.listen(('', 4000))
server.OnDisconnect += disconnectHandler

while True:
	server.update()
	sleep(0.001)
