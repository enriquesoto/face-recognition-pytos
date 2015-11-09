import sqlite3
import constants
import os
import uuid

class Task:
	id = 0
	methodName =''
	timeLocally = 0
	timeRemotelly=0
	argsSize = 0
	def __init__(self,methodName,timeLocally,argsSize):
		u = uuid.uuid1()
		self.id = u.int
		self.methodName = methodName
		self.timeLocally=timeLocally
		self.argsSize = argSize
	def initialize(self,row):
		self.id,self.methodName,self.timeLocally,self.argsSize,self.timeRemotelly = row


class TaskDAO:
	def __init__(self,task):
		print "Inserting task"
		with sqlite3.connect(constants.ROOT_DIR+constants.DB_FILENAME) as conn:
			cursor = conn.cursor()
			query = "insert into task ( name, time_locally, args_size) values (':task_id,:time_locally,:args_size')"
			cursor.execute(query, {'task_id':task.id, 'time_locally':task.timeLocally, 'args_size':task.argsSize})
	def updateTask(self,task):
		print "Updating Task"
		with sqlite3.connect(constants.ROOT_DIR+constants.DB_FILENAME) as conn:
			cursor = conn.cursor()
			query = "update task set method_name =:method_name, time_locally = :time_locally, time_remotelly =:time_remotelly, argsSize =:argsSize where id = :id"
			cursor.execute(query, {'method_name':task.methodName,'time_locally':task.timeLocally,'time_remotelly':task.timeRemotelly,'argsSize':task.argsSize, 'id':task.id})

	def getTask(self,id):
		print "getting a task"
		query = "select id,method_name, time_locally, args_size, time_remotelly from task where id =: task_id "
		cursor.execute(query,{'task_id':id})
		task = None
		for row in cursor.fetchall():
			task = Task(row)
		return task


class PytosDB:
	conn = None
	def __init__(self):
		#self.db_filename = 'pytos/stats.db'
		db_is_new = not os.path.exists(constants.ROOT_DIR+constants.DB_FILENAME)
		with sqlite3.connect(constants.ROOT_DIR+constants.DB_FILENAME) as conn:
			if db_is_new:
				print 'Creating schema'
				conn.execute('''create table task (id integer primary key not null, method_name not null, time_locally real, args_size    real, time_remotelly real);''')
				print "Table Created!"
				#conn.close() #can not operate on a closed db
			else:
				print 'Db already exists, assume scheme does, too.'
	def xxx(self):
		pass



