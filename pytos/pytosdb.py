import sqlite3
import constants
import os
import uuid


class Task:
	id = ''
	methodDeclaration =''
	methodWeight = 0
	argsSize = 0
	timeLocally = 0
	timeRemotelly=0 #may be updated later
	returnWeight='' #optional field :S
	functionBody= ''

	def __init__(self,methodDeclaration,methodWeight,argsSize,timeLocally,functionBody):
		u = uuid.uuid1()
		self.id=u.int
		self.methodDeclaration= methodDeclaration
		self.methodWeight = methodWeight
		self.timeLocally=timeLocally
		self.argsSize = argSize
		self.functionBody = functionBody
	def initialize(self,row):
		self.id,self.methodDeclaration,self.methodWeight, self.argsSize, self.timeLocally,self.timeRemotelly, self.returnWeight, self.functionBody= row


class TaskDAO:
	def __init__(self,task):
		print "Inserting task"
		with sqlite3.connect(constants.ROOT_DIR+constants.DB_FILENAME) as conn:
			cursor = conn.cursor()
			query = "insert into task (method_declaration, method_weight, time_locally, args_size) values (':method_declaration,:method_weight,:time_locally,:args_size')"
			cursor.execute(query, {'method_declaration':task.methodDeclaration, 'method_weight':task.methodWeight, 'time_locally':task.timeLocally, 'args_size':task.argsSize})
	def updateTask(self,task):
		print "Updating Task"
		with sqlite3.connect(constants.ROOT_DIR+constants.DB_FILENAME) as conn:
			cursor = conn.cursor()
			query = "update task set method_declaration =:method_declaration, method_weight =: method_weight, argsSize =:argsSize, time_locally = :time_locally, time_remotelly =:time_remotelly, return_weight =:return_weight, function_body =:function_body where id = :id"
			cursor.execute(query, {'method_declaration':task.methodDeclaration,'method_weight':task.methodWeight, 'argsSize':task.argsSize, 'time_locally':task.timeLocally,'time_remotelly':task.timeRemotelly,'return_weight':task.returnWeight,'function_body':task.functionBody, 'id':task.id})

	def getTask(self,id):
		print "getting a task"
		with sqlite3.connect(constants.ROOT_DIR+constants.DB_FILENAME) as conn:
			cursor = conn.cursor()
			query = "select * from task where id =: task_id "
			cursor.execute(query,{'task_id':id})
			task = None
			for row in cursor.fetchall():
				task = Task(row)
		
		return task
	
	def getTasksByProperties(self,methodDeclaration,methodWeight):
		print "getting a task by properties "
		with sqlite3.connect(constants.ROOT_DIR+constants.DB_FILENAME) as conn:
			cursor = conn.cursor()
			query = "select * from task where method_declaration =:method_declaration, method_weight =: method_weight"
			cursor.execute(query, {'method_declaration':methodDeclaration,'method_weight':methodWeight})
			answers = cursor.fetchall()
			return answers
	
	def getRemoteCalls(self,nTasksRows):
		print "getting n remote calls"
		nRemoteCalls = 0
		for task in nTasksRows:
			if task['time_remotelly'] is not None:
				nRemoteCalls =+1
		#return constants.N_MIN_REMOTE_CALLS-nRemoteCalls
		return nRemoteCalls

	def getLocalCalls(self,nTaskRows):
		print "getting n local calls"
		nLocalCalls = 0
		for task in nTasksRows:
			if task['time_locally'] is not None:
				nLocalCalls =+1
		return nLocalCalls


class PytosDB:
	conn = None
	def __init__(self):
		#self.db_filename = 'pytos/stats.db'
		db_is_new = not os.path.exists(constants.ROOT_DIR+constants.DB_FILENAME)
		with sqlite3.connect(constants.ROOT_DIR+constants.DB_FILENAME) as conn:
			if db_is_new:
				print 'Creating schema'
				conn.execute('''create table task (id integer primary key, method_declaration text not null, method_weight not null, args_size integer,  time_locally real not null, time_remotelly real, return_weight integer, function_body text not null);''')
				print "Table Created!"
				#conn.close() #can not operate on a closed db
			else:
				print 'Db already exists, assume scheme does, too.'
	def xxx(self):
		pass



