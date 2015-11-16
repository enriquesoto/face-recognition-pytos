import sqlite3
import constants
import os
import uuid
import pdb

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
		self.id=u.hex
		self.methodDeclaration= methodDeclaration
		self.methodWeight = methodWeight
		self.timeLocally=timeLocally
		self.argsSize = argsSize
		self.functionBody = functionBody
	def initialize(self,row):
		self.id,self.methodDeclaration,self.methodWeight, self.argsSize, self.timeLocally,self.timeRemotelly, self.returnWeight, self.functionBody= row


class TaskDAO:
	def __init__(self,task):
		print "Inserting task"
		with sqlite3.connect(constants.ROOT_DIR+constants.DB_FILENAME) as conn:
			cursor = conn.cursor()
			query = "insert into task (id, method_declaration, method_weight, args_size, time_locally, function_body) values (:id,:method_declaration,:method_weight,:args_size, :time_locally, :function_body)"
			cursor.execute(query, {'id':task.id,'method_declaration':task.methodDeclaration, 'method_weight':task.methodWeight, 'args_size':task.argsSize, 'time_locally':task.timeLocally, 'function_body':task.functionBody})
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
	
	@staticmethod
	def getTasksByProperties(methodDeclaration,methodWeight):
		print "getting a task by properties "
		with sqlite3.connect(constants.ROOT_DIR+constants.DB_FILENAME) as conn:
			cursor = conn.cursor()
			query = "select * from task where method_declaration =:method_declaration AND method_weight =:method_weight"
			cursor.execute(query, {'method_declaration':methodDeclaration,'method_weight':methodWeight})
			answers = cursor.fetchall()
			return answers
	
	@staticmethod
	def getRemoteCalls(nTasksRows):
		print "getting n remote calls"
		nRemoteCalls = 0
		for task in nTasksRows:
			if task[constants.TIME_REMOTELLY_FIELD] is not None:
				nRemoteCalls =+1
		#return constants.N_MIN_REMOTE_CALLS-nRemoteCalls
		return nRemoteCalls
	
	@staticmethod
	def getLocalCalls(nTasksRows):
			print "getting n local calls"
			nLocalCalls = 0
			for task in nTasksRows:
					if task[constants.TIME_LOCALLY_FIELD] is not None:
							nLocalCalls +=1
			return nLocalCalls
        
class PytosDB:
	conn = None
	def __init__(self):
		#self.db_filename = 'pytos/stats.db'
		db_is_new = not os.path.exists(constants.ROOT_DIR+constants.DB_FILENAME)
		with sqlite3.connect(constants.ROOT_DIR+constants.DB_FILENAME) as conn:
			if db_is_new:
				print 'Creating schema'
				conn.execute('''create table task (id text primary key, method_declaration text not null, method_weight not null, args_size integer,  time_locally real not null, time_remotelly real, return_weight integer, function_body text not null);''')
				print "Table Created!"
				#conn.close() #can not operate on a closed db
			else:
				print 'Db already exists, assume scheme does, too.'
	def xxx(self):
		pass
