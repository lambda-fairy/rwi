import legume
from time import sleep

def on_connected(sender, event_args):
	print "Connected to server"
	print sender, event_args

client = legume.Client()
client.OnConnectRequestAccepted += on_connected
client.connect(('127.0.0.1', 4000))
i=0
while i<100:
	i+=1
	client.update()
	sleep(0.005)

client.disconnect()
sleep(0.5)
client.update()
