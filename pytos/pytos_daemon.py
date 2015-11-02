# main definitions
import time
import rpyc
from tendo import singleton
from rpyc.utils.server import ThreadedServer
from threading import Thread

class Global():
    offloading=False

class MyService(rpyc.Service):
    def exposed_getOffloadingDesicion(self):
        return main.offloading

if __name__ == '__main__':
	me = singleton.SingleInstance() # will sys.exit(-1) if other instance is running
	server = ThreadedServer(MyService, port = 12345)
	t = Thread(target = server.start)
	t.daemon = True
	t.start()

# the main logic
	main = Global()
	while True:
		main.offloading = True
		time.sleep(3)
