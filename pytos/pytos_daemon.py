import multiprocessing
import time
import pdb


class PytosDaemon(multiprocessing.Process):

	def __init__(self, task_queue, result_queue):
		multiprocessing.Process.__init__(self)
		self.daemon=True
		self.task_queue = task_queue
		self.result_queue = result_queue
	
	def run(self):
		proc_name = self.name
		while True:
			next_task = self.task_queue.get()
			if next_task is None:
				#a poisson flag means shutdown
				print ':s: Exiting' % proc_name
				self.task_queue.task_done()
				break
			print '%s: %s' %(proc_name,next_task)
			answer = next_task()
			self.task_queue.task_done()
			self.result_queue.put(answer)
		return

class Solver(object):
	def __init__(self, a, b):
		self.a=a
		self.b=b
	def __call__(self):
		return False

if __name__=='__main__'
	solver = multiprocessing.JoinableQueue()
	result = multiprocessing.Queue()
	d = multiprocessing.Process(name='daemon', target=daemon)
	d.daemon = True
	d.start()



